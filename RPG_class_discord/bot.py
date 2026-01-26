import discord
from discord.ext import commands
import requests
import os
import json
from class_data import MAIN_CLASSES, HIDDEN_CLASSES


TOKEN = os.getenv("TOKEN")
# ---------- CONFIG ----------
DATA_FILE = "user_data.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

# ---------- LOAD / SAVE ----------
def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- DISCORD SETUP ----------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- QUESTIONS ----------
QUESTIONS = [
    "In a fight, do you prefer strength, magic, or strategy?",
    "Do you like to fight alone or in a team?",
    "Do you prefer fast attacks or powerful attacks?",
    "Do you like to protect others or deal damage?",
    "Do you prefer planning or acting instantly?"
]

# ---------- EVENTS ----------
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# ---------- OLLAMA AI ----------
def ask_ai(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    return response.json()["response"]

# ---------- QUESTION SYSTEM ----------
async def ask_questions(ctx):
    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for q in QUESTIONS:
        await ctx.send(q)
        msg = await bot.wait_for("message", check=check)
        answers.append(msg.content)

    return answers

# ---------- PROMPT ----------
def build_prompt(answers):
    return f"""
You are an RPG class assignment AI.

User answers:
{answers}

Choose:
- One main class from: Warrior, Mage, Rogue, Ranger, Cleric, Bard, Summoner
- One subclass that belongs to that main class

Respond ONLY in this format:

Main: <class>
Sub: <subclass>
"""

# ---------- SAFE PARSER ----------
def parse_ai_response(text):
    main_class = None
    sub_class = None

    for line in text.splitlines():
        if line.lower().startswith("main"):
            main_class = line.split(":", 1)[1].strip()
        if line.lower().startswith("sub"):
            sub_class = line.split(":", 1)[1].strip()

    # Fallback safety
    if main_class not in MAIN_CLASSES:
        main_class = "Warrior"
    if sub_class not in MAIN_CLASSES.get(main_class, []):
        sub_class = MAIN_CLASSES[main_class][0]

    return main_class, sub_class

# ---------- COMMANDS ----------
@bot.command()
async def register(ctx):
    await ctx.send("🧙 Welcome adventurer! Let's find your RPG class...")

    answers = await ask_questions(ctx)

    await ctx.send("🧠 Analyzing your personality...")

    prompt = build_prompt(answers)
    ai_response = ask_ai(prompt)

    main_class, sub_class = parse_ai_response(ai_response)

    users = load_users()
    user_id = str(ctx.author.id)

    users[user_id] = {
        "main": main_class,
        "sub": sub_class
    }

    save_users(users)

    await ctx.send(
        f"🏹 **Your class has been chosen!**\n"
        f"Main Class: **{main_class}**\n"
        f"Subclass: **{sub_class}**"
    )

@bot.command()
async def profile(ctx):
    users = load_users()
    user_id = str(ctx.author.id)

    if user_id not in users:
        await ctx.send("❌ You are not registered yet. Use `!register` first.")
        return

    data = users[user_id]
    await ctx.send(
        f"📜 **Your Profile**\n"
        f"Main Class: **{data['main']}**\n"
        f"Subclass: **{data['sub']}**"
    )

# ---------- START BOT ----------
if not TOKEN:
    print("ERROR: TOKEN not found!")
else:
    bot.run(TOKEN)


