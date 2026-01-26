import discord
from discord.ext import commands
from discord.ui import View, Button
import requests
import os
import json
import random
import asyncio

# ================== CONFIG ==================

DATA_FILE = "user_data.json"

# ⚠️ PUT YOUR NEW DISCORD BOT TOKEN HERE
TOKEN = os.getenv("TOKEN")

# ================== CLASS DATA ==================

MAIN_CLASSES = {
    "Warrior": ["Knight", "Berserker", "Paladin"],
    "Mage": ["Fire Mage", "Ice Mage", "Arcane Mage"],
    "Rogue": ["Assassin", "Thief", "Shadow"],
    "Ranger": ["Archer", "Sniper", "Beastmaster"],
    "Cleric": ["Priest", "Healer", "Monk"],
    "Bard": ["Musician", "Dancer", "Storyteller"],
    "Summoner": ["Necromancer", "Elementalist", "Spirit Caller"]
}

HIDDEN_CLASSES = [
    "Dragon Knight",
    "Shadow Mage",
    "Time Walker",
    "Void Lord",
    "Celestial Guardian"
]

FLAVOR_TEXT = {
    "Warrior": "🏹 Brave Warrior Brute, ready to crush your enemies! ⚔️",
    "Mage": "✨ Wise Mage, master of arcane arts! 🔮",
    "Rogue": "🗡️ Cunning Rogue, quick and deadly! 🕵️",
    "Ranger": "🏹 Sharp-eyed Ranger, master of ranged combat! 🌲",
    "Cleric": "⛪ Devout Cleric, healer and protector! ✨",
    "Bard": "🎶 Charming Bard, inspiring allies with music! 🎵",
    "Summoner": "🌀 Summoner of mystical creatures, chaos incarnate! 🐉"
}

# ================== BOT SETUP ==================

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ================== FILE FUNCTIONS ==================

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ================== HIDDEN CLASS LOGIC ==================

def assign_hidden_class(answers):
    combined = " ".join(answers).lower()
    if "magic" in combined and "strategy" in combined:
        return "Shadow Mage"
    if "strength" in combined and "alone" in combined:
        return "Berserker"
    if random.random() < 0.05:
        return random.choice(HIDDEN_CLASSES)
    return None

# ================== QUESTIONS ==================

QUESTION_LIST = [
    {"question": "In a fight, do you prefer strength, magic, or strategy?", "choices": ["Strength", "Magic", "Strategy"]},
    {"question": "Do you like to fight alone or in a team?", "choices": ["Alone", "Team"]},
    {"question": "Do you prefer fast attacks or powerful attacks?", "choices": ["Fast", "Powerful"]},
    {"question": "Do you like to protect others or deal damage?", "choices": ["Protect", "Deal Damage"]},
    {"question": "Do you prefer planning or acting instantly?", "choices": ["Planning", "Instant Action"]}
]

# ================== QUESTION UI ==================

async def ask_questions(ctx):
    answers = []

    for q in QUESTION_LIST:
        view = View(timeout=60)
        selected = {}

        async def button_callback(interaction, choice_label):
            if interaction.user != ctx.author:
                await interaction.response.send_message("This is not for you!", ephemeral=True)
                return
            selected["answer"] = choice_label
            view.stop()
            await interaction.response.defer()

        for choice in q["choices"]:
            btn = Button(label=choice, style=discord.ButtonStyle.primary)
            btn.callback = lambda interaction, c=choice: asyncio.create_task(button_callback(interaction, c))
            view.add_item(btn)

        await ctx.send(f"❓ {q['question']}", view=view)
        await view.wait()

        if "answer" not in selected:
            await ctx.send("⏱️ Timeout! Please register again.")
            return None

        answers.append(selected["answer"])

    return answers

# ================== AI ==================

def build_prompt(answers):
    return f"""
You are an RPG class assignment AI.

User answers:
{answers}

Choose:
- One main class from: Warrior, Mage, Rogue, Ranger, Cleric, Bard, Summoner
- One subclass that fits

Respond ONLY:
Main: <class>
Sub: <subclass>
"""

def ask_ai(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        return response.json()["response"]
    except:
        main = random.choice(list(MAIN_CLASSES.keys()))
        sub = random.choice(MAIN_CLASSES[main])
        return f"Main: {main}\nSub: {sub}"

# ================== BOT EVENTS ==================

@bot.event
async def on_ready():
    print(f"✅ Bot is online! Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@bot.command()
async def register(ctx):
    users = load_users()
    user_id = str(ctx.author.id)

    if user_id in users:
        await ctx.send("⚠️ You are already registered. Overwriting...")

    await ctx.send("🎮 Welcome adventurer! Let's find your RPG class...")

    answers = await ask_questions(ctx)
    if not answers:
        return

    await ctx.send("🧠 Analyzing your personality...")

    ai_response = ask_ai(build_prompt(answers))
    lines = ai_response.splitlines()

    main_class = lines[0].replace("Main:", "").strip()
    sub_class = lines[1].replace("Sub:", "").strip()

    if main_class not in MAIN_CLASSES:
        main_class = random.choice(list(MAIN_CLASSES.keys()))
        sub_class = random.choice(MAIN_CLASSES[main_class])

    hidden_class = assign_hidden_class(answers)

    users[user_id] = {
        "main": main_class,
        "sub": sub_class,
        "hidden": hidden_class
    }
    save_users(users)

    hidden_text = hidden_class if hidden_class else "None"

    message = f"""
🏹 **Your class has been chosen!**
Main Class: **{main_class}**
Subclass: **{sub_class}**
🎁 Hidden Class: **{hidden_text}**
💬 {FLAVOR_TEXT.get(main_class, "")}
"""
    await ctx.send(message)

# ================== START BOT ==================

if not TOKEN:
    print("ERROR: TOKEN not found!")
else:
    bot.run(TOKEN)
