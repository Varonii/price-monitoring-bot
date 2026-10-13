import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9",
}

# seletores do preço, do mais específico ao mais genérico
SELETORES_PRECO = [
    "#corePrice_feature_div span.a-offscreen",
    "span.priceToPay span.a-offscreen",
    "span.a-price span.a-offscreen",
]

def limpar_preco(texto):
    # "R$ 1.299,90" -> 1299.90
    achado = re.search(r"[\d.]+,\d{2}", texto)
    if not achado:
        return None
    return float(achado.group().replace(".", "").replace(",", "."))

def pegar_produto(url):
    resposta = requests.get(url, headers=HEADERS, timeout=15)
    resposta.raise_for_status()
    sopa = BeautifulSoup(resposta.text, "html.parser")

    elemento_titulo = sopa.select_one("#productTitle")
    titulo = elemento_titulo.get_text(strip=True) if elemento_titulo else None

    preco = None
    for seletor in SELETORES_PRECO:
        elemento = sopa.select_one(seletor)
        if elemento:
            preco = limpar_preco(elemento.get_text(strip=True))
            if preco:
                break

    return titulo, preco

if __name__ == "__main__":
    URL = "https://www.amazon.com.br/dp/B0D8DPT7ZY"
    titulo, preco = pegar_produto(URL)
    print("Produto:", titulo)
    print("Preço:", preco)