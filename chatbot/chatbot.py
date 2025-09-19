import re
import datetime

# Store context information
context = {
    "name": None,
    "mood": None
}

def chatbot_response(user_input):
    user_input = user_input.lower().strip()

    # Greeting patterns
    if re.search(r"\b(hello|hi|hey)\b", user_input):
        return "Hello! What's your name?"

    # Capture name
    elif re.search(r"my name is (.*)", user_input):
        name = re.findall(r"my name is (.*)", user_input)[0].strip().title()
        context["name"] = name
        return f"Nice to meet you, {name}! How are you feeling today?"

    # Capture mood
    elif re.search(r"i am (.*)", user_input):
        mood = re.findall(r"i am (.*)", user_input)[0].strip()
        context["mood"] = mood
        if context["name"]:
            return f"I'm glad to know that, {context['name']}. Thanks for sharing!"
        else:
            return f"I'm glad to know that. Thanks for sharing!"

    # Ask about bot's name
    elif re.search(r"your name", user_input):
        return "I'm a simple chatbot created to chat with you!"

    # Ask how bot is doing
    elif re.search(r"how are you", user_input):
        return "I'm just a bot, but I'm doing great! How about you?"

    # Time
    elif re.search(r"time", user_input):
        return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}"

    # Weather (mock)
    elif re.search(r"weather", user_input):
        return "I can't check the weather yet, but it's always sunny in my code world!"

    # Exit
    elif re.search(r"bye|goodbye|see you", user_input):
        if context["name"]:
            return f"Goodbye, {context['name']}! Have a wonderful day."
        else:
            return "Goodbye! Take care."

    # Default
    else:
        if context["name"]:
            return f"Nice to hear that, {context['name']}."
        else:
            return "I'm not sure how to respond to that."


# Run chatbot loop
print("Chatbot: Hi! Type 'bye' to exit.")
while True:
    user_text = input("You: ")
    response = chatbot_response(user_text)
    print("Chatbot:", response)
    if re.search(r"bye|goodbye|see you", user_text.lower()):
        break
