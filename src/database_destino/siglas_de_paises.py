import pdfplumber

with pdfplumber.open('tabela-sigla-pais.pdf') as pdf:
    for page in pdf.pages:        
        # Extrair siglas dos paises
        text = page.extract_text().split("\n")
        for line in text:
            print(f"Descrição: {line[:-2]}, Sigla: {line[-2:]}")