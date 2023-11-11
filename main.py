# Import necessary libraries and modules
from wake_word_detector import WakeWordDetector
from whisper_mic.whisper_mic import WhisperMic
import warnings
import openai
import pyttsx3
import json
import search_module
# Disable warnings
warnings.filterwarnings("ignore")


search_api_key = 'AIzaSyDQNrxzv98qgAHn5HPn4VQ57oPfgZKIXcU'
cx = 'f7b9195485d7a444e'  # Your custom search engine ID

# Configure paths and keys
model_path = 'model.ppn'  # Path to the wake word model
access_key = 'gYAl+VcZDDKcu9PX5VjEjCljWJJeHf6GLkl9s5WBYlp1EHpI+DrHnA=='  # Access key for wake word detector

# Set your OpenAI API key
openai.api_key = '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'

# Define a function that calls the ChatGPT API
def chat_with_gpt(user_message, messages=[]):

    # Create a message that sets the role and content for the assistant (Jarvis)
    assistant_message = {"role": "user", "content": "You are Jarvis, a virtual assistant. If you can't provide any specific information about questions that are out of your scope, you will answer my question with only a parsable search query like this: 'Search this {your provided query}'"}
    messages.append(assistant_message)
    
    
    # Create a message from the user
    user_message = {"role": "user", "content": user_message}
    messages.append(user_message)



    # Call the ChatGPT API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    # Extract and return the assistant's reply
    reply = response['choices'][0]['message']['content']
    return reply

# Initialize the WhisperMic with English language support
mic = WhisperMic(english=True)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) #change index to change voices
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
conversation = []  # Initialize the conversation outside the loop

# Start the detection loop and print a message when the wake word is detected
while True:
    try:
        # Initialize the WakeWordDetector
        wake_word_detector = WakeWordDetector(model_path, access_key)
        
        # Check for the wake word
        if wake_word_detector.start_detection():
            print("Jarvis: Yes master?")  # Modify the print statement
            engine.say("Yes master?")
            engine.runAndWait()
            # Capture audio input
            result = mic.listen()
            print(result)
            user_input = result
            
            # Delete the wake word detector instance to release resources
            del wake_word_detector

            # Check if the user's input contains 'exit' or 'stop' and break the loop if true
            if 'exit' in user_input.lower() or 'stop' in user_input.lower():
                break

            # Get a response from ChatGPT based on user input
            assistant_reply = chat_with_gpt(user_input, conversation)

            # Add assistant's reply to the conversation
            conversation.append({"role": "assistant", "content": assistant_reply})
            
            if "Search this" in assistant_reply:
                parsed_text = assistant_reply[13:]
                # Get the first three search results
                search_results = search_module.get_search_results(search_api_key, cx, parsed_text, num_results=3)
                print("Jarvis:", " I cannot provide an exact answer for you but I can look it up on the internet: ")
                engine.say(" I cannot provide an exact answer for you but I can look it up on the internet")
                engine.runAndWait()
                print(parsed_text)
                engine.say(parsed_text)
                engine.runAndWait()
                if search_results:
                    for result in search_results:
                        title = result['title']
                        link = result['link']
                        print(f"Title: {title}")
                        print(f"Link: {link}")
                        print("=" * 50)
            else:
                print("Jarvis:", assistant_reply)
                engine.say(assistant_reply)
                engine.runAndWait()
    except Exception as e:
        # Handle any exceptions here
        print("An error occurred:", e)
