import requests
import sys

# 1. Configuration Check
# Ensure config.py exists and contains the necessary keys
try:
    from config import GROQ_API_KEY, GROQ_API_URL, MODEL_NAME
except ImportError:
    print("Error: 'config.py' not found or missing required variables!")
    print("Please create a 'config.py' file and add your GROQ_API_KEY.")
    sys.exit() 

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

chat_history = []

def ask_groq(prompt):
    """
    Sends the user's prompt and chat history to the Groq API
    and returns the model's response.
    """
    # Add user message to history
    chat_history.append({"role": "user", "content": prompt})
    
    data = {
        "model": MODEL_NAME,
        "messages": chat_history
    }

    # 2. Network Request with Error Handling
    try:
        # Sending POST request with a 10-second timeout
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=10)
        
        # Check for HTTP errors (4xx or 5xx status codes)
        response.raise_for_status()

        response_json = response.json()
        
        # 3. Validate Response Structure
        if 'choices' in response_json and len(response_json['choices']) > 0:
            message = response_json['choices'][0]['message']['content']
            # Add assistant message to history
            chat_history.append({"role": "assistant", "content": message})
            return message.strip()
        else:
            return "Error: Server returned an empty response (no choices found)."

    except requests.exceptions.ConnectionError:
        return "Connection Error: Please check your internet connection."
    except requests.exceptions.Timeout:
        return "Timeout Error: The server took too long to respond."
    except requests.exceptions.HTTPError as err:
        # Handle specific API errors (e.g., Invalid Key, Rate Limit)
        return f"API Error (Status {response.status_code}): {response.text}"
    except Exception as e:
        # Handle any unexpected errors
        return f"Unexpected Error: {e}"

def main():
    print(f"AI Assistant started (Model: {MODEL_NAME})")
    print("Type 'exit' or 'quit' to close the program.\n")
    
    while True:
        try:
            user_input = input("You: ")
            
            # Skip empty input
            if not user_input.strip():
                continue
                
            # Exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            # Get response
            response = ask_groq(user_input)
            print(f"AI: {response}\n")
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nProgram interrupted. Exiting...")
            break

if __name__ == "__main__":
    main()
