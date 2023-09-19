import openai
from gtts import gTTS
import os

# Set your GPT-4 API key
api_key = "YOUT KEY HERE"

# Initialize the GPT-4 API client
openai.api_key = api_key

# Define a base class for places
class Place:
    def __init__(self, name):
        self.name = name

# Define subclasses for attractions, restaurants, and hotels
class Attraction(Place):
    pass

class Restaurant(Place):
    def __init__(self, name, cuisine_type):
        super().__init__(name)
        self.cuisine_type = cuisine_type

class Hotel(Place):
    def __init__(self, name, star_rating):
        super().__init__(name)
        self.star_rating = star_rating

class Transportation:
    def __init__(self, mode):
        self.mode = mode

# Define a class for the travel chatbot
class TravelChatbot:
    def __init__(self):
        self.conversation = []

    # Method to interact with the chatbot using GPT-4
    def chat_with_bot(self, user_input):
        # Append user input to the conversation (Created the dict in inside the list)
        self.conversation.append({"role": "user", "content": user_input})
        # Generate a response from GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4", messages=self.conversation  # Use the GPT-4 model
        )
        # Append chatbot's response to the conversation
        self.conversation.append(
            {"role": "assistant", "content": response.choices[0].message["content"]}
        )
        # Return chatbot's response
        # return response.choices[0].message["content"]

        # Get chatbot's response text
        chatbot_response = response.choices[0].message["content"]

        # Convert text to speech
        # self.text_to_speech(chatbot_response)

        # Return chatbot's response
        return chatbot_response

    # Method to convert text to speech and play it
    def text_to_speech(self, text):
        tts = gTTS(text=text, lang="en")
        tts.save("chatbot_response.mp3")
        os.system("wmplayer chatbot_response.mp3")

    # Method to get recommendations for attractions
    def recommend_attractions(self, destination):
        return f"I recommend visiting the {destination} Museum and the {destination} Park and the {destination} Beautifull places."

    # Method to get recommendations for restaurants
    def recommend_restaurants(self, destination):
        return f"For dining, try the local cuisine at restaurants like 'Taste of {destination}' and 'Flavors of {destination}'."

    # Method to get recommendations for hotels
    def recommend_hotels(self, destination):
        return f"For accommodation, consider staying at the {destination} Grand Hotel or the {destination} Resort."

    # Method to get recommendations for transportation
    def recommend_transportation(self, destination):
        return f"To get to {destination}, you can use various transportation options, including flights, trains, and buses."

if __name__ == "__main__":
    print("Welcome to our Tripadvisor!".casefold())
    # Create an instance of the TravelChatbot class
    chatbot = TravelChatbot()
    # Get user input for the destination
    destination = input("Enter your desired destination: ")
    # Initialize the conversation with a greeting
    initial_input = f"Welcome to our Tour Guide Chat bot! I'd like to help you plan your trip to {destination}."
    print(f"You: {initial_input}")
    print(f"Chatbot: {chatbot.chat_with_bot(initial_input)}")
    # Enter the conversation loop
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        chatbot_response = chatbot.chat_with_bot(user_input)
        print(f"Chatbot: {chatbot_response}")
        # Provide recommendations based on user input
        if "attraction" in user_input.lower():
            print(chatbot.recommend_attractions(destination))
        elif "restaurant" in user_input.lower():
            print(chatbot.recommend_restaurants(destination))
        elif "hotel" in user_input.lower():
            print(chatbot.recommend_hotels(destination))
        elif "transport" in user_input.lower():
            print(chatbot.recommend_transportation(destination))

