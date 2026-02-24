from google import genai
from google.genai import types

from pathlib import Path

import time

from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

with open("prompt.txt", "r", encoding="utf-8") as f:
    
    prompt = f.read()


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


def response_json(doc1, doc2):
    
    print("🤖 Gerando resposta...")
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=[doc1, doc2, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    return response.text


if __name__ == "__main__":

    print("--- Modelos disponíveis no seu projeto ---")

    modelos_validos = []

    for m in client.models.list():
        if "generateContent" in m.supported_actions: # type: ignore

            print(f"ID: {m.name}")
            modelos_validos.append(m.name)

    print("------------------------------------------")

    docs = [Path(doc) for doc in Path("docs").iterdir() if doc.is_file()]
    
    if len(docs) < 2:

        print("Erro: Você precisa de pelo menos 2 arquivos na pasta 'docs'.")

    else:

        uploaded_doc1 = upload_file(docs[0])
        uploaded_doc2 = upload_file(docs[1])
        
        try:

            resp = response_json(uploaded_doc1, uploaded_doc2)
            
            if resp is not None:

                with open("response.json", "w", encoding="utf-8") as f:

                    f.write(resp)
                
                print("\nResultado JSON:")
                print(resp)

            else: print("Nenhuma resposta foi gerada.")

        except Exception as e:

            print(f"Erro ao gerar conteúdo: {e}")