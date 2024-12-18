import requests
import json

# Estados do Brasil com suas capitais
estados = {
    "SP": "São Paulo",
    "RJ": "Rio de Janeiro",
    "MG": "Belo Horizonte",
    "BA": "Salvador",
    "RS": "Porto Alegre",
    "PR": "Curitiba",
    "PE": "Recife",
    "CE": "Fortaleza",
    "PA": "Belém",
    "SC": "Florianópolis",
    "MA": "São Luís",
    "GO": "Goiânia",
    "AM": "Manaus",
    "ES": "Vitória",
    "PB": "João Pessoa",
    "RN": "Natal",
    "MT": "Cuiabá",
    "AL": "Maceió",
    "PI": "Teresina",
    "DF": "Brasília"
}

# Overpass API URL
url = "http://overpass-api.de/api/interpreter"

# Query base para buscar bairros de uma cidade
query_base = """
                [out:json];
                area["name"="{city}"]->.searchArea;
                nwr["place"="neighbourhood"](area.searchArea);
                out center 20000;
            """

# Lista para armazenar os dados coletados
resultados = []

# Iterar pelos estados e buscar dados
for estado, capital in estados.items():
    print(f"Buscando dados para {capital} ({estado})...")
    query = query_base.format(city=capital)
    response = requests.get(url, params={"data": query})
    
    if response.status_code == 200:
        data = response.json()
        for element in data.get("elements", []):
            bairro = element.get("tags", {}).get("name")
            lat = element.get("center", {}).get("lat")
            lon = element.get("center", {}).get("lon")
            if bairro and lat and lon:
                resultados.append({
                    "estado": estado,
                    "cidade": capital,
                    "bairro": bairro,
                    "latitude": lat,
                    "longitude": lon
                })
    else:
        print(f"Erro ao buscar dados para {capital}: {response.status_code}")

# Salvar os dados em um arquivo JSON
with open("bairros_brasil.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=4)

print("Dados salvos em 'bairros_brasil.json'")
