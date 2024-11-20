!pip install plotly

import streamlit as st
import pandas as pd
import plotly.express as px

# Função para calcular o patrimônio mês a mês
def calcular_patrimonio_mes_a_mes(idade, capital, aporte_mensal, rendimento_anual, idade_alvo, inflacao_anual):
    historico = []
    patrimonio_sem_inflacao = capital
    meses_total = (idade_alvo - idade) * 12

    # Convertendo as taxas anuais para mensais
    rendimento_mensal = rendimento_anual / 12
    inflacao_mensal = inflacao_anual / 12

    for mes in range(meses_total):
        # Calcula rendimento mensal considerando o rendimento anual dividido por 12
        rendimento_mensal_valor = capital * rendimento_mensal
        rendimento_mensal_valor_sem_inflacao = patrimonio_sem_inflacao * rendimento_mensal

        # Atualiza os valores considerando aportes e rendimentos
        capital += aporte_mensal + rendimento_mensal_valor
        patrimonio_sem_inflacao += aporte_mensal + rendimento_mensal_valor_sem_inflacao

        # Aplica impacto da inflação mensal
        capital *= (1 - inflacao_mensal)

        # Salva os resultados mês a mês
        idade_atual = idade + mes // 12
        historico.append({
            "Idade": idade_atual,
            "Valor Ajustado": capital,
            "Valor Descontado pela Inflação": capital / (1 + inflacao_mensal) ** (mes + 1),
            "Valor Sem Inflação": patrimonio_sem_inflacao
        })

    return historico

# Configurações do layout no Streamlit
st.set_page_config(page_title="Simulador de Investimentos", layout="wide")

# Título da página
st.title("Simulador de Evolução do Patrimônio")

# Inputs do usuário
with st.sidebar:
    st.header("Parâmetros de Simulação")
    idade = st.number_input("Idade atual", min_value=0, value=30, step=1)
    capital = st.number_input("Capital inicial (R$)", min_value=0.0, value=1000.0, step=100.0)
    aporte_mensal = st.number_input("Aporte mensal (R$)", min_value=0.0, value=500.0, step=50.0)
    rendimento_anual = st.number_input("Rendimento anual (%)", min_value=0.0, value=5.0, step=0.1) / 100
    idade_alvo = st.number_input("Idade alvo", min_value=idade, value=65, step=1)
    inflacao_anual = st.number_input("Inflação anual (%)", min_value=0.0, value=3.0, step=0.1) / 100

# Calcula o histórico do patrimônio
historico_patrimonio = calcular_patrimonio_mes_a_mes(
    idade, capital, aporte_mensal, rendimento_anual, idade_alvo, inflacao_anual
)

# Converte o histórico em DataFrame
df_historico = pd.DataFrame(historico_patrimonio)

# Gráfico com o patrimônio ajustado e sem inflação
fig = px.line(
    df_historico.melt(id_vars="Idade", var_name="Tipo", value_name="Valor"),
    x="Idade",
    y="Valor",
    color="Tipo",
    title="Evolução do Patrimônio ao Longo do Tempo",
    labels={"Idade": "Idade (anos)", "Valor": "Valor Acumulado (R$)", "Tipo": "Tipo de Valor"}
)

fig.update_traces(line_width=2)
fig.update_layout(title_font_size=20, xaxis_title="Idade", yaxis_title="Valor (R$)")

# Layout principal com duas colunas
col1, col2 = st.columns([2, 1])

# Exibindo o gráfico
with col1:
    st.plotly_chart(fig, use_container_width=True)

# Exibindo a tabela
with col2:
    st.header("Tabela de Evolução")
    st.dataframe(df_historico.style.format({
        "Valor Ajustado": "R$ {:,.2f}",
        "Valor Descontado pela Inflação": "R$ {:,.2f}",
        "Valor Sem Inflação": "R$ {:,.2f}"
    }), use_container_width=True)
