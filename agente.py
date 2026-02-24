from google import genai
from google.genai import types

from pathlib import Path

import time

from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def upload_file(doc_path):
    
    sample_doc = client.files.upload(
        file=doc_path,
        config=types.UploadFileConfig(
            mime_type="application/pdf"
        )
    )
   
    print(f"Verificando processamento de {doc_path}...", end="")

    while sample_doc.state and sample_doc.state.name == "PROCESSING":

        print(".", end="", flush=True)
        time.sleep(2)
        
    print()
    
    if sample_doc.state and sample_doc.state.name == "FAILED":

        raise Exception(f"Falha ao processar arquivo: {sample_doc.name}")
   
    return sample_doc


def response_json(doc1, doc2, prompt):
    
    print("🤖 Gerando resposta...")
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=[doc1, doc2, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    return response.text
