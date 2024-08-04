from dotenv import load_dotenv
import os

KEY_PATH = "./keys.env"
load_dotenv(dotenv_path=KEY_PATH)
openai_api_key = os.getenv('OPENAI_API_KEY')
twitter_api_key = os.getenv('TWITTER_API_KEY')
twitter_api_secret_key = os.getenv('TWITTER_API_SECRET_KEY')

print(openai_api_key)
print(twitter_api_key)
print(twitter_api_secret_key)