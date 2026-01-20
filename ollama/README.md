AI-Based RPG Class Allocation Discord Bot

Overview



This project is a Discord bot that assigns RPG classes to users based on their personality and decision-making style. The system uses prompt engineering and a language model to analyze user responses to a set of questions and determine the most suitable class for them.



This repository contains the implementation of Module 1: Class Allocation System, which focuses only on registration, questioning, and class assignment.



The main goal of this project is to study and apply:



Prompt engineering



Open-source language models



AI-driven decision systems



Game logic design using AI



Project Objectives



Build a Discord bot that interacts with users



Design a personality-based question system



Use a language model to analyze answers



Assign:



7 Main Classes



21 Sub Classes



7 Hidden (rare) Classes



Store user profiles persistently



Allow users to re-register or keep their old profile



How the System Works



The user types:



!register



If the user is already registered, the bot asks whether to:



Overwrite the existing profile



Keep the old profile



If registration continues, the bot asks a series of questions using buttons.



The answers are converted into a structured prompt.



The prompt is sent to the language model for analysis.



The model returns the suggested:



Main Class



Sub Class



The system checks whether the user qualifies for a Hidden Class.



The final result is saved and shown to the user.



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



Python



discord.py



Open-source language model (LLaMA, Mistral, DeepSeek, or HuggingFace models)



JSON file for data storage



Prompt engineering techniques



Prerequisites



Python 3.10 or higher



Git



A Discord bot token



(Optional) GPU for running local language models



Installation and Setup



Clone the repository:



git clone <your-repository-link>

cd <project-folder>



Install dependencies:



pip install -r requirements.txt



Create a file named .env in the project folder and add:



DISCORD\_TOKEN=your\_discord\_bot\_token\_here



Run the bot:



python bot.py

Project Structure

discord-rpg-bot/

│── bot.py

│── ai\_engine.py

│── classes.py

│── users.json

│── .env

│── .gitignore

│── README.md



