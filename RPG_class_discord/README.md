AI-Based RPG Class Allocation Discord Bot

Overview : 

          This project is a Discord bot that assigns RPG classes to users based on their personality and decision-making style. The system uses prompt engineering and a language model to analyze user responses to a set of questions and determine the most suitable class for them.

This repository contains the implementation of Module 1: Class Allocation System, which focuses only on registration, questioning, and class assignment.

The main goal of this project is to study and apply:

   1.Prompt engineering

   2.Open-source language models

   3.AI-driven decision systems

   4.Game logic design using AI

Project Objectives

      1.Build a Discord bot that interacts with users

      2.Design a personality-based question system

      3.Use a language model to analyze answers

      4.Assign:

        7 Main Classes

        21 Sub Classes

        7 Hidden (rare) Classes

      5.Store user profiles persistently

      6.Allow users to re-register or keep their old profile

How the System Works

   1.The user types:

   !register

   2.If the user is already registered, the bot asks whether to:

      Overwrite the existing profile

      Keep the old profile

   3.If registration continues, the bot asks a series of questions using buttons.

   4.The answers are converted into a structured prompt.

   5.The prompt is sent to the language model for analysis.

   6.The model returns the suggested:

       Main Class

       Sub Class

   7.The system checks whether the user qualifies for a Hidden Class.

   8.The final result is saved and shown to the user.

RPG Class Structure
   Main Classes (7)

       Warrior

       Mage

       Rogue

       Archer

       Paladin

       Necromancer

       Monk

    Each main class has three subclasses, making a total of 21 subclasses.

Hidden Classes (7)

       Hidden classes are rare classes that are assigned only when certain personality patterns or answer combinations are detected.

Technologies Used

   1.Python

   2.discord.py

   3.Open-source language model (LLaMA, Mistral, DeepSeek, or HuggingFace models)

   4.JSON file for data storage

   5.Prompt engineering techniques

Prerequisites

  > Python 3.10 or higher

  > Git

  > A Discord bot token

  > (Optional) GPU for running local language models

Installation and Setup

    1.Clone the repository:

        git clone <your-repository-link>
         cd <project-folder>

     2.Install dependencies:

           1.pip install -r requirements.txt

     3.Create a file named .env in the project folder and add:

        DISCORD_TOKEN=your_discord_bot_token_here

     4.Run the bot:
         python bot.py
         
Project Structure
discord-rpg-bot/
│── bot.py
│── ai_engine.py
│── classes.py
│── users.json
│── .env
│── .gitignore
│── README.md
