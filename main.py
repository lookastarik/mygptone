import os
from concurrent.futures import ThreadPoolExecutor
import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# add your OpenAI API key
openai.api_key = "sk-b9knxcX7XwBL7ymIJfBJT3BlbkFJNQfrqkNQXOTIr6Rgi6"

# add your Telegram bot token here
TELEGRAM_TOKEN = "6175028198:AAGGFfbuPaXGIkpZkWr--Aq4pRgJ1prJKtE"
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# set the path where the text files will be stored
TEXT_FILES_PATH = "./text_files/"

# create the folder if it doesn't exist
if not os.path.exists(TEXT_FILES_PATH):
    os.mkdir(TEXT_FILES_PATH)

# function to handle the /start command
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi there! I am a chatbot powered by OpenAI. Type something to get started!')

# function to handle text messages
def handle_text_message(update, context):
    # get the user's message
    user_message = update.message.text

    # generate a response using OpenAI
    response = generate_response(user_message)

    # send the response to the user
    update.message.reply_text(response)

# function to handle file uploads
def handle_file_upload(update, context):
    # get the file from the message
    file = update.message.document

    # download the file
    file_path = os.path.join(TEXT_FILES_PATH, file.file_name)
    file.download(file_path)

    # read the contents of the file
    with open(file_path, "r") as f:
        text = f.read()

    # generate a response using OpenAI
    response = generate_response(text)

    # send the response to the user
    update.message.reply_text(response)

# function to generate a response using OpenAI
def generate_response(text):
    # create a list of text chunks
    chunks = split_into_chunks(text)

    # generate a response for each chunk in parallel
    with ThreadPoolExecutor() as executor:
        responses = list(executor.map(call_openai_api, chunks))

    # join the responses together and return them
    response = "\n".join(responses)
    return response

# function to call the OpenAI API
def call_openai_api(chunk):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=chunk,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

# function to split text into chunks
def split_into_chunks(text, max_chunk_size=3000):
    chunks = []
    current_chunk = ""

    for line in text.splitlines():
        if len(current_chunk) + len(line) + 1 <= max_chunk_size:
            current_chunk += line + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line + "\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# create the custom keyboard
keyboard = telegram.ReplyKeyboardMarkup(
    keyboard=[
        ["Zagruzit' fajl"]
    ],
    resize_keyboard=True
)

