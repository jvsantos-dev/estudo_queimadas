import yaml
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime
from functools import lru_cache
import random

def read_yaml(path):
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def enviar_email(
    senha: str,
    destinatario: str,
    assunto: str,
    corpo: str,
    remetente: str = 'seuemail@gmail.com'
):
    # ⚠️ Use uma senha de app do Gmail (não a sua senha normal)
    
    # Monta a mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto

    if not corpo:
        corpo = "Nenhum incêndio foi detectado."

    msg.attach(MIMEText(corpo, 'plain'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remetente, senha)  # senha de app
        servidor.send_message(msg)
        print('✅ Email enviado com sucesso!')
    except Exception as e:
        print(f'❌ Erro ao enviar email: {e}')
    finally:
        servidor.quit()
def get_queimadas_clima(lat, lon) -> dict:
    # Pode mudar o caminho do arquivo de configuração
    # Certifique-se de que o arquivo YAML contém a chave 'key' com a sua API Key do OpenWeather
    config = read_yaml("D:\Downloads\EstudoQueimadas\keys\openweather.yaml")
    api_key = config['key']
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    try:
        if response.status_code == 200:
            data = response.json()
            clima = {
            'temperatura': round(data['main']['temp'] - 273.15, 2),  # Convertendo de Kelvin para Celsius
            'umidade': data['main']['humidity'],
            'vento': data['wind']['speed'],
            'descricao': data['weather'][0]['description']
            }
    except Exception as e:
        print(f"Erro ao obter dados do OpenWeather: {e}")
        clima = {}
    return clima


def gerar_mapa_incendio(temperatura, umidade, vento, tamanho=10):
    """
    Gera uma matriz tamanho x tamanho com 0 e 1.
    Probabilidade de ter fogo (1) aumenta com temperatura alta,
    umidade baixa e vento alto.
    """
    mapa = []
    # Calcula chance base de fogo: escala 0 a 1
    chance_fogo = min(max((temperatura - 20) * 0.05 + (50 - umidade) * 0.03 + (vento * 0.02), 0), 1)

    for _ in range(tamanho):
        linha = []
        for _ in range(tamanho):
            # Sorteia 1 com chance_fogo, senão 0
            cell = 1 if random.random() < chance_fogo else 0
            linha.append(cell)
        mapa.append(linha)
    return mapa

def acionar_drone_via_api(lat, lon, temperatura, umidade, vento):
    print(f"[🚁 DRONE] Sobrevoando a área em {lat}, {lon}...")

    incendio_confirmado = random.choice([True, False])  # 50% chance

    if incendio_confirmado:
        mapa_lista = gerar_mapa_incendio(temperatura, umidade, vento)
        # Converte para tupla de tuplas para ser hashable
        mapa = tuple(tuple(linha) for linha in mapa_lista)

        tempo = tempo_propagacao_incendio(mapa, 0, 0)  # Supondo que inicia no topo esquerdo (0,0)
        print(f"🔥 Incêndio confirmado! Tempo estimado de propagação crítica: {tempo} unidades de tempo.")
        print("📷 Imagens térmicas capturadas.")
    else:
        print("✅ Nenhum sinal visível de incêndio detectado.")

@lru_cache(maxsize=None)
def tempo_propagacao_incendio(mapa, i, j, limite=15):
    linhas, colunas = len(mapa), len(mapa[0])
    
    if limite == 0 or not (0 <= i < linhas) or not (0 <= j < colunas) or mapa[i][j] == 0:
        return 0  # Para parar a recursão ou células inválidas

    # Marca a célula como queimada criando um novo mapa imutável
    mapa_lista = [list(linha) for linha in mapa]
    mapa_lista[i][j] = 0
    novo_mapa = tuple(tuple(linha) for linha in mapa_lista)

    norte = tempo_propagacao_incendio(novo_mapa, i-1, j, limite-1)
    sul   = tempo_propagacao_incendio(novo_mapa, i+1, j, limite-1)
    leste = tempo_propagacao_incendio(novo_mapa, i, j+1, limite-1)
    oeste = tempo_propagacao_incendio(novo_mapa, i, j-1, limite-1)

    return 1 + max(norte, sul, leste, oeste)