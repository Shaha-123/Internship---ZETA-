import ollama

def ask_ai(prompt):
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": "You are an RPG class master who assigns fantasy classes."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]
