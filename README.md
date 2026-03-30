# 💱 Conversor de Moedas com Streamlit

Um conversor de moedas moderno e elegante desenvolvido com Python e Streamlit, apresentando uma interface bonita com design responsivo e taxas de câmbio em tempo real.

## ✨ Características

- **Design Sofisticado**: Interface moderna com gradientes, animações suaves e layout responsivo
- **Múltiplas Moedas**: Suporte para 12 moedas diferentes (USD, EUR, GBP, JPY, AUD, CAD, CHF, CNY, INR, BRL, MXN, SGD)
- **Taxas em Tempo Real**: Integração com API ExchangeRate para taxas de câmbio atualizadas
- **Cache Inteligente**: Otimização com cache de 1 hora para reduzir requisições
- **UX Amigável**: Seleção intuitiva com flags de país e nomes completos das moedas
- **Informações Detalhadas**: Exibição clara da taxa de câmbio e histórico da conversão
- **Tratamento de Erros**: Fallback automático com dados de taxa padrão em caso de conexão perdida

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
streamlit run conversor_moedas.py
```

A aplicação abrirá automaticamente em seu navegador padrão em `http://localhost:8501`

## 📋 Requisitos

- Python 3.8+
- streamlit
- requests
- pandas

## 🎨 Tecnologias Utilizadas

- **Streamlit**: Framework web para aplicações de dados
- **Requests**: Cliente HTTP para integração com API de taxas
- **CSS Customizado**: Styling avançado com gradientes e efeitos visuais

## 💡 Como Usar

1. Selecione a **moeda de origem** (Da qual você quer converter)
2. Selecione a **moeda de destino** (Para qual você quer converter)
3. Digite o **valor** a ser convertido
4. Veja o resultado em tempo real com a taxa de câmbio aplicada

## 🔄 Fluxo de Taxas de Câmbio

- As taxas são obtidas da ExchangeRate-API
- Cache de 1 hora evita requisições desnecessárias
- Em caso de erro de conexão, usa taxas padrão como fallback

## 📊 Moedas Suportadas

| Código | Moeda | País |
|--------|-------|------|
| USD | Dólar Americano | 🇺🇸 |
| EUR | Euro | 🇪🇺 |
| GBP | Libra Esterlina | 🇬🇧 |
| JPY | Iene Japonês | 🇯🇵 |
| AUD | Dólar Australiano | 🇦🇺 |
| CAD | Dólar Canadense | 🇨🇦 |
| CHF | Franco Suíço | 🇨🇭 |
| CNY | Yuan Chinês | 🇨🇳 |
| INR | Rúpia Indiana | 🇮🇳 |
| BRL | Real Brasileiro | 🇧🇷 |
| MXN | Peso Mexicano | 🇲🇽 |
| SGD | Dólar de Singapura | 🇸🇬 |

## 🛠️ Desenvolvimento

### Estrutura do Código

- **`obter_taxas_cambio()`**: Busca taxas da API com cache
- **`converter_moeda()`**: Núcleo da lógica de conversão
- **`main()`**: Interface e fluxo da aplicação

### Customizações Possíveis

- Adicionar mais moedas ao dicionário `MOEDAS`
- Modificar cores do gradiente no CSS
- Integrar banco de dados para histórico de conversões
- Adicionar gerador de gráficos históricos

## 📝 Autor

Desenvolvido como uma atividade integradora em Python com foco em design de interface e boas práticas de programação.

---

**Aproveite o conversor! 💱**
