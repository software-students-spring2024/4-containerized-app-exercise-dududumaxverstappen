import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import base64
import json
import os
from urllib.parse import urlparse

_ =load_dotenv(find_dotenv())

OpenAI.api_key = os.environ.get('OPENAI_API_KEY')


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

#TAKE IMAGES
image_local = '../26408-2.png'
image_url = f"data:image/jpeg;base64,{encode_image(image_local)}"
#image_url = 'https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2021/02/19/ML-1955-2.jpg'

client = OpenAI() #Best practice needs OPENAI_API_KEY environment variable
# client = OpenAI('OpenAI API Key here')

response = client.chat.completions.create(
    model='gpt-4-vision-preview', 
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Is this healthy?  Only return JSON not other text."},
                {
                    "type": "image_url",
                    "image_url": {"url": image_url}
                }
            ],
        }
    ],
    max_tokens=500,
)

# Extract JSON data from the response and remove Markdown formatting
json_string = response.choices[0].message.content
json_string = json_string.replace("```json\n", "").replace("\n```", "")

# Parse the string into a JSON object
json_data = json.loads(json_string)

filename_without_extension = os.path.splitext(os.path.basename(urlparse(image_url).path))[0] #for URL image
#filename_without_extension = os.path.splitext(os.path.basename(image_local))[0] #for local image
print(json_string)
# Add .json extension to the filename
"""
json_filename = f"{filename_without_extension}.json"

# Save the JSON data to a file with proper formatting
with open("./Data/" + json_filename, 'w') as file:
    json.dump(json_data, file, indent=4)

print(f"JSON data saved to {json_filename}")
"""