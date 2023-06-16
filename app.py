from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import find_dotenv, load_dotenv
import requests
from playsound import playsound
import os


load_dotenv(find_dotenv())
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

def get_response_from_ai(human_input):
    template= """
    you are as a role of my girlfriend, now lets paly.following these requirement: 
    1/ your name is Shirley, 19 years old, your job is tv model 
    2/ you are my girlfriend, you are a little Two-dimensional and have language addiction,
    you like to say "em..." at the end of the sentence. 3 response with english
    3/ Don't be overly enthusiastic, don't be cringe; dont be overlay negative
    
    {history}
    Boyfriend: {human_input},
    Shirley: 
    """
    prompt = PromptTemplate(
        input_variables=("history", "human_input"),
        template = template
	)
    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0.2),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2)
	)
    output = chatgpt_chain.predict(human_input=human_input)
    return output

def get_voice_message(message):
    payload = {
        "text": message,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
		}
	}
    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json"
	}
    
    voice_id = "21m00Tcm4TlvDq8ikWAM"
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?optimize_streaming_latecy=0"
    
    CHUNK_SIZE = 1024
    # url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
    
    response = requests.post(tts_url, json=payload, headers=headers)
    
    if response.status_code == 200 and response.content:
        with open('audio.mp3', 'wb') as f:
            f.write(response.content)
        playsound('audio.mp3')
        return response.content
    
    
    print('response', response)



from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/send_message', methods=['POST'])
def send_message():
    human_input=request.form["human_input"]
    message = get_response_from_ai(human_input)
    get_voice_message(message)
    return message

if __name__ == "__main__":
    app.run(debug=True)    
