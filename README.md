# 🔥 Sistema Inteligente de Monitoramento de Queimadas

Este projeto tem como objetivo criar um sistema automatizado capaz de **identificar regiões com alto risco de queimadas**, utilizando dados históricos de incêndios florestais, informações climáticas em tempo real e automação via Python.

---

## 📌 Objetivo

Desenvolver uma aplicação que:
- Detecte automaticamente regiões vulneráveis a incêndios com base em dados reais;
- Use uma **API de clima** (OpenWeather) para coletar temperatura, umidade e vento de cada ponto monitorado;
- Calcule um **índice de risco de incêndio** para cada região;
- Gere alertas e relatórios com base nesse risco.

---

## 🧱 Estrutura do Projeto
queimadas/
├── dados/
│ ├── wildfires.csv # Base histórica com mais de 2 milhões de incêndios
│ ├── pontos_monitoramento.json # Regiões críticas extraídas do histórico
│ └── regioes.csv # (opcional) fonte inicial para JSON
│
├── etl/
│ └── gerar_json_de_monitoramento.py # Extrai os principais focos do CSV e gera JSON
│
├── monitoramento/
│ └── analisar_risco.py # Lê o JSON, consulta clima via API e avalia risco
│
├── config/
│ └── settings.yaml # Contém chave da API e opções de execução
│
└── README.md

## 🔄 Pipeline de Funcionamento

1. **ETL:** Usa a base histórica `wildfires.csv` para extrair os locais com maior frequência de incêndios;
2. **Transformação:** Gera o arquivo `pontos_monitoramento.json`, com nome, latitude e longitude dos locais críticos;
3. **Monitoramento:** Um script consulta a **API climática (OpenWeather)** para cada ponto e calcula um índice de risco baseado em:
   - Temperatura atual
   - Umidade do ar
   - Velocidade do vento
4. **Saída:** O sistema imprime alertas no terminal ou gera um relatório simples, destacando regiões em alerta vermelho.

---

## 🔧 Tecnologias Utilizadas

- Python 3.11+
- Pandas
- Requests
- JSON / YAML
- OpenWeatherMap API
- Jupyter Notebook (opcional para visualizações)
- VSCode / Terminal

---

## ⚠️ Avisos

Alguns ajustes são necessários para rodar o projeto corretamente:

    Arquivo CSV: atualize o caminho da variável path na main para localizar o wildfires.csv.

    Configuração da API: na função get_queimadas_clima, ajuste o caminho do arquivo settings.yaml.

    Envio de e-mails: na função enviar_email, insira seu e-mail, senha e destinatário manualmente.

Todos esses pontos estão comentados no código como # ⚠️ AJUSTE NECESSÁRIO.
