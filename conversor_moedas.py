import streamlit as st
import requests
from datetime import datetime
from typing import Dict, Tuple
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="💱 Conversor de Moedas do GUILHERME",
    page_icon="💱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para design bonito
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
    }
    
    .stContainer {
        max-width: 600px;
        margin: 0 auto;
    }
    
    .header {
        text-align: center;
        color: white;
        margin-bottom: 30px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    .header h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .header p {
        font-size: 1em;
        opacity: 0.9;
    }
    
    .converter-box {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    .input-group {
        margin-bottom: 20px;
    }
    
    .input-label {
        color: #333;
        font-weight: 600;
        margin-bottom: 8px;
        display: block;
        font-size: 0.9em;
    }
    
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .result-value {
        font-size: 2.5em;
        font-weight: bold;
        margin: 15px 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .info-box {
        background: rgba(102, 126, 234, 0.1);
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        color: #333;
        font-size: 0.85em;
    }
    
    .exchange-rate {
        background: #f5f5f5;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
        text-align: center;
        color: #666;
        font-weight: 500;
    }
    
    .stNumberInput input, .stSelectbox select {
        border: 2px solid #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 1em !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.2) !important;
    }
    
    .currency-flag {
        font-size: 2em;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Dados de moedas com símbolos e flags
MOEDAS = {
    "USD": {"nome": "Dólar Americano", "flag": "🇺🇸", "simbolo": "$"},
    "EUR": {"nome": "Euro", "flag": "🇪🇺", "simbolo": "€"},
    "GBP": {"nome": "Libra Esterlina", "flag": "🇬🇧", "simbolo": "£"},
    "JPY": {"nome": "Iene Japonês", "flag": "🇯🇵", "simbolo": "¥"},
    "AUD": {"nome": "Dólar Australiano", "flag": "🇦🇺", "simbolo": "A$"},
    "CAD": {"nome": "Dólar Canadense", "flag": "🇨🇦", "simbolo": "C$"},
    "CHF": {"nome": "Franco Suíço", "flag": "🇨🇭", "simbolo": "CHF"},
    "CNY": {"nome": "Yuan Chinês", "flag": "🇨🇳", "simbolo": "¥"},
    "INR": {"nome": "Rúpia Indiana", "flag": "🇮🇳", "simbolo": "₹"},
    "BRL": {"nome": "Real Brasileiro", "flag": "🇧🇷", "simbolo": "R$"},
    "MXN": {"nome": "Peso Mexicano", "flag": "🇲🇽", "simbolo": "$"},
    "SGD": {"nome": "Dólar de Singapura", "flag": "🇸🇬", "simbolo": "S$"},
}

@st.cache_data(ttl=3600)
def obter_taxas_cambio() -> Dict[str, float]:
    """
    Obtém as taxas de câmbio da API ExchangeRate-API.
    Usa cache de 1 hora para otimizar requisições.
    """
    try:
        # Usando a API de taxa de câmbio gratuita
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("rates", {})
    except requests.exceptions.RequestException:
        # Dados de fallback em caso de erro de conexão
        return {
            "USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 149.50,
            "AUD": 1.53, "CAD": 1.36, "CHF": 0.88, "CNY": 7.24,
            "INR": 83.12, "BRL": 4.97, "MXN": 17.05, "SGD": 1.34
        }

def converter_moeda(valor: float, de: str, para: str, taxas: Dict) -> Tuple[float, float]:
    """
    Converte um valor de uma moeda para outra.
    
    Args:
        valor: Valor a converter
        de: Código da moeda de origem
        para: Código da moeda de destino
        taxas: Dicionário com as taxas de câmbio
    
    Returns:
        Tupla com (valor_convertido, taxa_de_cambio)
    """
    if de not in taxas or para not in taxas:
        return 0, 0
    
    taxa_de_cambio = taxas[para] / taxas[de]
    valor_convertido = valor * taxa_de_cambio
    
    return valor_convertido, taxa_de_cambio

def main():
    # Cabeçalho
    st.markdown("""
    <div class="header">
        <h1>💱 Conversor de Moedas</h1>
        <p>Converta valores entre diferentes moedas com taxas de câmbio em tempo real</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Container principal
    with st.container():
        st.markdown('<div class="converter-box">', unsafe_allow_html=True)
        
        # Obter taxas de câmbio
        taxas = obter_taxas_cambio()
        
        # Layout em colunas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<label class="input-label">De (Moeda de Origem)</label>', unsafe_allow_html=True)
            moeda_origem = st.selectbox(
                "Selecione a moeda de origem",
                options=list(MOEDAS.keys()),
                format_func=lambda x: f"{MOEDAS[x]['flag']} {x} - {MOEDAS[x]['nome']}",
                key="origem",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown('<label class="input-label">Para (Moeda de Destino)</label>', unsafe_allow_html=True)
            moeda_destino = st.selectbox(
                "Selecione a moeda de destino",
                options=list(MOEDAS.keys()),
                format_func=lambda x: f"{MOEDAS[x]['flag']} {x} - {MOEDAS[x]['nome']}",
                index=1,
                key="destino",
                label_visibility="collapsed"
            )
        
        # Input do valor
        st.markdown('<label class="input-label">Valor a Converter</label>', unsafe_allow_html=True)
        valor = st.number_input(
            "Digite o valor",
            value=100.0,
            min_value=0.0,
            step=0.01,
            format="%.2f",
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botão de conversão (implícito pelo estado)
        if valor > 0:
            valor_convertido, taxa = converter_moeda(valor, moeda_origem, moeda_destino, taxas)
            
            # Box de resultado
            st.markdown(f"""
            <div class="result-box">
                <div style="font-size: 0.9em; opacity: 0.9;">Valor Convertido</div>
                <div class="result-value">
                    {MOEDAS[moeda_destino]['simbolo']} {valor_convertido:,.2f}
                </div>
                <div style="font-size: 0.85em; opacity: 0.8;">
                    De {MOEDAS[moeda_origem]['flag']} {moeda_origem} para {MOEDAS[moeda_destino]['flag']} {moeda_destino}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Taxa de câmbio
            st.markdown(f"""
            <div class="exchange-rate">
                1 {moeda_origem} = {taxa:.4f} {moeda_destino}
            </div>
            """, unsafe_allow_html=True)
            
            # Informações adicionais
            st.markdown(f"""
            <div class="info-box">
                <strong>📊 Detalhes da Conversão:</strong><br>
                • Valor Original: {MOEDAS[moeda_origem]['simbolo']} {valor:,.2f} {moeda_origem}<br>
                • Valor Convertido: {MOEDAS[moeda_destino]['simbolo']} {valor_convertido:,.2f} {moeda_destino}<br>
                • Taxa de Câmbio: {taxa:.6f}<br>
                • Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
