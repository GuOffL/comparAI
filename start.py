import agente as ai
from pathlib import Path

docs = [Path(doc) for doc in Path("docs").iterdir() if doc.is_file()]

if len(docs) != 2: print("Erro: Você precisa de pelo menos 2 arquivos na pasta 'docs'.")

else:
    
    doc1 = ai.upload_file(docs[0])
    doc2 = ai.upload_file(docs[1])
    
    try:
    
        resposta = ai.response_json(doc1, doc2)
        
        if resposta is not None:
            
            with open("response.json", "w", encoding="utf-8") as f:

                f.write(resposta)
        
    except Exception as e:
        
        print("Erro ao gerar Conteúdo")