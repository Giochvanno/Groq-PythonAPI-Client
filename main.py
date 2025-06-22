import requests
from config import GROQ_API_KEY, GROQ_API_URL, MODEL_NAME

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

chat_history = []

def ask_groq(prompt):
    chat_history.append({"role": "user", "content": prompt})
    data = {
        "model": MODEL_NAME,
        "messages": chat_history
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        message = response.json()['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": message})
        return message.strip()
    else:
        return f"Ошибка: {response.text}"

def main():
    print(" ИИ-помощник запущен (via Groq API)")
    while True:
        user_input = input("Ты: ")
        if user_input.lower() in ["выход", "exit", "quit"]:
            break
        response = ask_groq(user_input)
        print(f"ИИ: {response}")

if __name__ == "__main__":
    main()
