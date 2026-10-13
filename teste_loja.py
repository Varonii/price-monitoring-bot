import requests
from bs4 import BeautifulSoup

URL = "https://www.mercadolivre.com.br/monitor-gamer-lg-ultragear-24ips-full-hd-180hz-1ms-gtg-nvidia-g-sync-amd-freesync-hdr10-srgb-99-hdmi-displayport-preto-24gs60f/p/MLB38947984?pdp_filters=item_id%3AMLB4025119893#polycard_client=search-desktop&be_origin=searchv2&overlay_label=not_apply&search_layout=grid&position=1&type=product&tracking_id=0e1055b1-1343-494a-92d3-ddf5d5795214&wid=MLB4025119893&sid=search"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9",
}

resp = requests.get(URL, headers=HEADERS, timeout=15)
print("Status:", resp.status_code)
print("Tamanho da página:", len(resp.text))

sopa = BeautifulSoup(resp.text, "html.parser")
print("Título da aba:", sopa.title.get_text(strip=True) if sopa.title else None)

html = resp.text.lower()
print("Menciona captcha:", "captcha" in html)
print("Tem 'R$' no HTML:", "R$" in resp.text)