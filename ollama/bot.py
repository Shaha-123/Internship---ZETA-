
import discord
from discord.ext import commands
from discord.ui import View, Button
import requests
import os
import json
import random
from class_data import MAIN_CLASSES, HIDDEN_CLASSES
import asyncio

# ---------- File & Bot Setup ----------
DATA_FILE = "user_data.json"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- Flavor Text ----------
FLAVOR_TEXT = {
    "Warrior": "🏹 Brave Warrior Brute, ready to crush your enemies! ⚔️",
    "Mage": "✨ Wise Mage, master of arcane arts! 🔮",
    "Rogue": "🗡️ Cunning Rogue, quick and deadly! 🕵️",
    "Ranger": "🏹 Sharp-eyed Ranger, master of ranged combat! 🌲",
    "Cleric": "⛪ Devout Cleric, healer and protector! ✨",
    "Bard": "🎶 Charming Bard, inspiring allies with music! 🎵",
    "Summoner": "🌀 Summoner of mystical creatures, chaos incarnate! 🐉"
}

# ---------- Helper Functions ----------
def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def assign_hidden_class(answers):
    combined = " ".join(answers).lower()
    # Patterns for specific hidden classes
    if "magic" in combined and "strategy" in combined:
        return "Shadow Mage"
    if "strength" in combined and "alone" in combined:
        return "Berserker"
    # Rare random chance
    if random.random() < 0.05:
        return random.choice(HIDDEN_CLASSES)
    return None

# ---------- Questions ----------
QUESTION_LIST = [
    {
        "question": "In a fight, do you prefer strength, magic, or strategy?",
        "choices": ["Strength", "Magic", "Strategy"]
    },
    {
        "question": "Do you like to fight alone or in a team?",
        "choices": ["Alone", "Team"]
    },
    {
        "question": "Do you prefer fast attacks or powerful attacks?",
        "choices": ["Fast", "Powerful"]
    },
    {
        "question": "Do you like to protect others or deal damage?",
        "choices": ["Protect", "Deal Damage"]
    },
    {
        "question": "Do you prefer planning or acting instantly?",
        "choices": ["Planning", "Instant Action"]
    }
]

async def ask_questions(ctx):
    answers = []
    for q in QUESTION_LIST:
        question_text = q["question"]
        choices = q["choices"]

        view = View(timeout=60)
        selected = {}

        # Callback function for button clicks
        async def button_callback(interaction, choice_label):
            if interaction.user != ctx.author:
                await interaction.response.send_message("This is not for you!", ephemeral=True)
                return
            selected["answer"] = choice_label
            view.stop()
            await interaction.response.defer()  # stop loading

        # Add buttons
        for choice in choices:
            button = Button(label=choice, style=discord.ButtonStyle.primary)
            button.callback = lambda interaction, c=choice: asyncio.create_task(button_callback(interaction, c))
            view.add_item(button)

        # Send question
        await ctx.send(f"❓ {question_text}", view=view)

        # Wait for answer
        await view.wait()
        if "answer" not in selected:
            await ctx.send("⏱️ Timeout! Please register again.")
            return None
        answers.append(selected["answer"])
    return answers

def build_prompt(answers):
    return f"""
You are an RPG class assignment AI.

User answers:
{answers}

You must choose:
- One main class from: Warrior, Mage, Rogue, Ranger, Cleric, Bard, Summoner
- One subclass that belongs to that main class

Respond ONLY in this format:
Main: <class>
Sub: <subclass>

Do not explain anything.
"""

def ask_ai(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]
    except Exception as e:
        print(f"Error calling AI: {e}")
        return "Main: Adventurer\nSub: Novice"

# ---------- Bot Events ----------
@bot.event
async def on_ready():
    print(f"Bot is online! Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@bot.command()
async def register(ctx):
    users = load_users()
    user_id = str(ctx.author.id)

    # Check if already registered
    if user_id in users:
        selected = {"overwrite": None}
        view = View(timeout=30)

        async def overwrite_callback(interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("This is not for you!", ephemeral=True)
                return
            selected["overwrite"] = True
            view.stop()
            await interaction.response.defer()

        async def keep_callback(interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("This is not for you!", ephemeral=True)
                return
            selected["overwrite"] = False
            view.stop()
            await interaction.response.defer()

        btn_yes = Button(label="✅ Overwrite", style=discord.ButtonStyle.success)
        btn_yes.callback = overwrite_callback
        btn_no = Button(label="❌ Keep old class", style=discord.ButtonStyle.danger)
        btn_no.callback = keep_callback
        view.add_item(btn_yes)
        view.add_item(btn_no)

        await ctx.send("⚠️ You have already registered! What do you want to do?", view=view)
        await view.wait()

        # If user chose to keep old class or timeout
        if selected["overwrite"] is False:
            return await ctx.send("✅ Profile unchanged.")
        elif selected["overwrite"] is None:
            return await ctx.send("⏱️ Timeout! Profile unchanged.")

    # If new user or overwrite
    await ctx.send("🎮 Welcome adventurer! Let's find your RPG class...")

    answers = await ask_questions(ctx)
    if not answers:
        return

    await ctx.send("🧠 Analyzing your personality...")

    prompt = build_prompt(answers)
    ai_response = ask_ai(prompt)

    # Parse AI output
    lines = ai_response.splitlines()
    main_class = lines[0].replace("Main:", "").strip() if len(lines) > 0 else random.choice(MAIN_CLASSES)
    sub_class = lines[1].replace("Sub:", "").strip() if len(lines) > 1 else "Adventurer"

    # Hidden class
    hidden_class = assign_hidden_class(answers)

    # Save user profile
    users[user_id] = {
        "main": main_class,
        "sub": sub_class,
        "hidden": hidden_class
    }
    save_users(users)

    # Send result with flavor text and emojis
    hidden_text = hidden_class if hidden_class else "None"
    message = f"🏹 **Your class has been chosen!**\n" \
              f"Main Class: **{main_class}**\n" \
              f"Subclass: **{sub_class}**\n" \
              f"🎁 Hidden Class: **{hidden_text}**\n" \
              f"💬 {FLAVOR_TEXT.get(main_class, '')}"

    await ctx.send(message)

# -------- START BOT --------


bot.run("TOKEN_HERE")
