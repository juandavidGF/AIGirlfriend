import requests
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")



def get_voices():
	url = "https://api.elevenlabs.io/v1/voices"

	headers = {
	"Accept": "application/json",
	"xi-api-key": ELEVEN_LABS_API_KEY
	}

	response = requests.get(url, headers=headers)

	print(response.text)


get_voices()