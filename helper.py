import requests
import streamlit as st
import base64
import locale
from dotenv import load_dotenv
import os

# Set the locale to the user's default locale
locale.setlocale(locale.LC_ALL, '')

load_dotenv()
api_key = "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"


#base_api_url = "http://localhost:7071"

def get_open_ai_response(image, mime):
    
    with st.spinner(text="Analyzing the image..."):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        base64_image = base64.b64encode(image).decode('utf-8')

        prompt = """
            Extract the information related to the petition information from the table of the people that have signed it. There are ten rows on each sheet, with columns "Signature", "Printed Name", "Address", "City/Town/Village", "County", and "State". The bottom of each sheet has the Sheet No., with the handwritten number being the number of the sheet. The row number will be the index of the signature, between 1-10.

            Return a response strictly in this JSON format and don't include any text before or after:

            {
            "signatures: [
            {
            "row": "string"
            "printed_name": "string",
            "address: "string",
            "city": "string",
            "state": "string"
            "sheet_number": "string"
            }
            ]
        """
        
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1200
        }

        response = requests.post("https://api.openai.com/v1/chat/completions",headers=headers, json=payload)

        json_response = response.json()['choices'][0]['message']['content']
        
        return json_response