from utils.functions import get_queimadas_clima, enviar_email, acionar_drone_via_api
import json

# Integrantes do grupo:
# João Victor Oliveira Santos 557948
# Matheus Alcântara Estevão 558193
# Nicolle Pellegrino Jelinski 558610

# Carrega os locais monitorados
with open('D:/Desktop/EstudoQueimadas/json/places.json', 'r', encoding='utf-8') as file:
    dados = json.load(file)

# Checa o primeiro estado (ou todos, se quiser)
for estado, locais in dados.items():
    for ponto in locais:
        lat = ponto['latitude']
        lon = ponto['longitude']
        data_incendio = ponto['data']

        # Pega o clima atual na região
        clima = get_queimadas_clima(lat, lon)

        # Verifica se há risco com base na temperatura e umidade
        if clima['temperatura'] >= 30 and clima['umidade'] <= 50:
            print(f"[🔥 ALERTA] Potencial incêndio em {lat}, {lon} - {estado}")
            corpo_email = (
                f"🔥 Alerta de Incêndio 🔥\n"
                f"Local: Latitude {lat}, Longitude {lon}\n"
                f"Estado: {estado}\n"
                f"Temperatura: {clima['temperatura']}°C\n"
                f"Umidade: {clima['umidade']}%\n"
                f"Vento: {clima.get('vento', 'N/A')} km/h\n"
                f"Condições: {clima.get('descricao', 'Não informado')}\n"
                f"Data do último incêndio: {data_incendio}\n"
                f"Ação: Drone acionado para verificação."
            )
            # Envia o alerta por email
            enviar_email(
                senha='sua_senha_fake_ou_real',
                destinatario='destinatario@example.com',
                assunto='🚨 Alerta de Incêndio',
                corpo=corpo_email
            )
            # Aciona o drone fictício
            acionar_drone_via_api(lat, lon, clima['temperatura'], clima['umidade'], clima.get('vento', 0))
        else:
            print(f"[OK] Sem risco em {lat}, {lon} - {estado} | Temp: {clima['temperatura']}°C, Umidade: {clima['umidade']}%")
    