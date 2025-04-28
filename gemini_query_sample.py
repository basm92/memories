from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv('environ.env')  

prompt_text = """Transcribe the information present in the images in the following .json format: {
  \"Name\": 
  \"Date of Death\":
  \"Baten (Net Assets)\":
  \"Schulden en Lasten (Net Liabilities)\":
  \"Saldo (Net Wealth): 
  \"Overview\": {
    \"Assets\": [
      {
        \"variable name\": ,
        \"value\": 
      }
    ],
    \"Liabilities\": [
      {
        \"variable name\":
        \"value\": 
      }
    ]
  }
}"""

# --- API Key Setup ---
try:
    # Attempt to get the API key from the environment variable
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    client = genai.Client(api_key=GOOGLE_API_KEY)
    print("API Key configured successfully.")
except ValueError as e:
    print(f"Error: {e}")
    print("Please set the GOOGLE_API_KEY environment variable.")
    print("Get your key from: https://aistudio.google.com/app/apikey")
except Exception as e:
    print(f"An unexpected error occurred during configuration: {e}")


# Upload the images
uploaded_files = {}
images = [i for i in os.listdir('./example_memorie') if i.startswith('NL-HlmNHA_178_2789')]
for i in images:
    uploaded_files[i] = client.files.upload(file=i)

# Create the prompt with text and multiple images
# You have to allow billing using the Google Cloud Console or the Google Cloud SDK Online
response = client.models.generate_content(
    model="gemini-2.5-pro-preview-03-25",
    contents=[
        types.Content(
            role="user",
            parts=[types.Part.from_uri(
                    file_uri=uploaded_files[i].uri,
                    mime_type=uploaded_files[i].mime_type,
                ) for i in uploaded_files.keys()
            ] + [types.Part.from_text(text=prompt_text)]
        )
    ]
)

print(response.text, file=open('response.txt', 'w'))
