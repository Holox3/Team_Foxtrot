import sys
import openai
import os
from gtts import gTTS
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QLineEdit,
)


# Set your GPT-4 API key
api_key = "YOUR KEY HERE"
# Initialize the GPT-4 API client
openai.api_key = api_key


# Define a base class for places
class Place:
    def __init__(self, name):
        self.name = name


# Define subclasses for attractions, restaurants, and hotels
class Attraction(Place):
    def __init__(self, name, description):
        super().__init__(name)
        self.description = description


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
        self.places = []  # Store information about places
        self.last_chatbot_response = ""  # Store the last chatbot response

    def chat_with_bot(self, user_input):
        # Append user input to the conversation
        self.conversation.append({"role": "user", "content": user_input})
        # Generate a response from GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4", messages=self.conversation
        )
        # Append chatbot's response to the conversation
        chatbot_response = response.choices[0].message["content"]
        self.last_chatbot_response = chatbot_response  # Store the response

        # Return the response as a dictionary
        return {"type": "bot", "message": chatbot_response}

    def text_to_speech(self, text):
        # Convert text to speech and play it
        tts = gTTS(text=text, lang="en")
        tts.save("chatbot_response.mp3")
        os.system("afplay chatbot_response.mp3")

    def add_place(self, place):
        # Add a place to the list of places
        self.places.append(place)

    def find_place(self, place_name):
        # Find a place by name in the list of places
        for place in self.places:
            if place.name.lower() == place_name.lower():
                return place
        return None


# Define the chatbot application using PyQt5
class ChatBox(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Assistant Intelligence (T.A.I.)")
        self.layout = QVBoxLayout()
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.layout.addWidget(self.chat_history)
        self.input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setStyleSheet("color: white; font-size: 18px; font: bold 12px;")
        self.input_layout.addWidget(self.input_box)
        self.send_button = QPushButton(
            "Send"
        )  # Create the "Send" button and set its size
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet(
            "background-color: grey; color: lightgreen; font-size: 16px; font: bold 12px;"
        )
        self.send_button.setFixedSize(80, 30)  # Adjust the size here
        self.input_layout.addWidget(self.send_button)
        self.tts_button = QPushButton(
            "Text-to-Speech (OFF)"
        )  # Create the "Text-to-Speech" button and set its size
        self.tts_button.clicked.connect(self.toggle_text_to_speech)
        self.tts_enabled = False  # Track the TTS state (initially off)
        self.tts_button.setStyleSheet(
            "background-color: grey; color: lightblue; font-size: 16px; font: bold 12px;"
        )
        self.tts_button.setFixedSize(150, 30)  # Adjust the size here
        self.input_layout.addWidget(self.tts_button)
        self.layout.addLayout(self.input_layout)
        self.setLayout(self.layout)
        self.input_box.returnPressed.connect(self.send_button.click)

        # Create an instance of the TravelChatbot
        self.chatbot = TravelChatbot()

        # Apply styles to the chat window and input elements
        self.setStyleSheet(
            "background-color: #323232;"  # Set the background color to dark gray
        )
        # Set the text color for the QTextEdit widget directly
        self.chat_history.setStyleSheet(
            "color: lightblue; font-size: 18px; font: bold 12px;"
        )

        # Display the welcome message when the chatbot is initialized
        self.chat_history.append(
            """
            Welcome to Team-Foxtrot's <font color="orange">Travel Assistant Intelligence (T.A.I.)</font
        """
        )
        self.chat_history.append(
            """
        <font color="orange">T.A.I.:</font> Hey, I am <font color="orange">T.A.I</font>, the Travel Assistant Intelligence that will help plan your trip for the perfect holidays! <font color="pink">^w^</font>\n
        Please Tell me a Land or Country that u would like to Visit, make sure to give me in the first input a location and in the second further information (Example: How long and which activity) so I can make sure you have the perfect time!
        """
        )

    def send_message(self):
        user_input = self.input_box.text()
        self.input_box.clear()
        self.display_message(
            '<font color="lightgreen">You:</font> ' + user_input, "white", "user"
        )
        initial_input = f"Prepare yourself for an awesome time in {user_input}!."
        chatbot_response = self.chatbot.chat_with_bot(initial_input)
        # Display each line of T.A.I.'s response as a separate message
        bot_responses = chatbot_response["message"].split("\n")
        for response in bot_responses:
            if response:
                self.display_message(
                    '<font color="orange">T.A.I.:</font> ' + response,
                    "lightblue",
                    "bot",
                )

    def display_message(self, message, color, message_type):
        # Display a message with the specified color and message type (user or bot)
        formatted_message = f'<font color="{color}">{message}</font>'
        if message_type == "user":
            self.chat_history.append(formatted_message)
        elif message_type == "bot":
            self.chat_history.append(formatted_message)

    def toggle_text_to_speech(self):
        # Toggle the TTS state and update the button text
        self.tts_enabled = not self.tts_enabled
        if self.tts_enabled:
            self.tts_button.setText("Text-to-Speech (ON)")
            self.convert_text_to_speech(self.chatbot.last_chatbot_response)
        else:
            self.tts_button.setText("Text-to-Speech (OFF)")

    def convert_text_to_speech(self, text):
        # Get the last chatbot response
        chatbot_response = text

        if chatbot_response and self.tts_enabled:
            # Convert text to speech and play it
            tts = gTTS(text=chatbot_response, lang="en")
            tts.save("chatbot_response.mp3")
            os.system("afplay chatbot_response.mp3")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat = ChatBox()
    chat.resize(600, 800)
    chat.show()
    sys.exit(app.exec_())
