import streamlit as st
import pandas as pd
import plotly.express as px

# Função para calcular o patrimônio mês a mês
def calcular_patrimonio_mes_a_mes(idade, capital, aporte_mensal, rendimento_anual, idade_alvo, inflacao_anual):
    historico = []
    patrimonio_sem_inflacao = capital
    total_aportes = 0
    meses_total = (idade_alvo - idade) * 12

    # Calculando o fator mensal para rendimento e inflação
    rendimento_mensal = (1 + rendimento_anual) ** (1 / 12) - 1
    inflacao_mensal = (1 + inflacao_anual) ** (1 / 12) - 1

    for mes in range(meses_total):
        # Calcula rendimento mensal
        rendimento_mensal_valor = patrimonio_sem_inflacao * rendimento_mensal

        # Atualiza valores considerando aportes e rendimentos
        total_aportes += aporte_mensal
        patrimonio_sem_inflacao += aporte_mensal + rendimento_mensal_valor

        # Ajusta o capital com a inflação
        capital += aporte_mensal + rendimento_mensal_valor
        capital /= (1 + inflacao_mensal)

        # Salva os resultados mês a mês
        idade_atual = idade + mes // 12
        historico.append({
            "Idade": idade_atual,
            "Valor Sem Inflação": patrimonio_sem_inflacao,
            "Valor Com Inflação": capital,
            "Valor Investido Até o Momento": total_aportes,
            "Valor em Juros": patrimonio_sem_inflacao - total_aportes
        })

    # Calcula inflação acumulada ao longo do período
    anos_total = (idade_alvo - idade)
    inflacao_acumulada = (1 + inflacao_anual) ** anos_total

    # Ajusta valores finais
    valor_total_rendimento = patrimonio_sem_inflacao
    valor_em_juros = patrimonio_sem_inflacao - total_aportes
    valor_descontado_inflacao = patrimonio_sem_inflacao / inflacao_acumulada

    return historico, total_aportes, valor_em_juros, valor_total_rendimento, valor_descontado_inflacao

# Configurações do layout no Streamlit
st.set_page_config(page_title="Simulador de Investimentos", layout="wide")

# Título da página
st.title("Simulador de Evolução do Patrimônio")

# Inputs do usuário
with st.sidebar:
    st.header("Parâmetros de Simulação")
    idade = st.number_input("Idade atual", min_value=0, value=30, step=1)
    capital = st.number_input("Capital inicial (R$)", min_value=0.0, value=0.0, step=100.0)
    aporte_mensal = st.number_input("Aporte mensal (R$)", min_value=0.0, value=1000.0, step=50.0)
    rendimento_anual = st.number_input("Rendimento anual (%)", min_value=0.0, value=12.0, step=0.1) / 100
    idade_alvo = st.number_input("Idade alvo", min_value=idade, value=50, step=1)
    inflacao_anual = st.number_input("Inflação anual (%)", min_value=0.0, value=0.0, step=0.1) / 100

# Calcula o histórico do patrimônio
historico_patrimonio, total_investido, valor_em_juros, valor_total_rendimento, valor_descontado_inflacao = calcular_patrimonio_mes_a_mes(
    idade, capital, aporte_mensal, rendimento_anual, idade_alvo, inflacao_anual
)

# Converte o histórico em DataFrame
df_historico = pd.DataFrame(historico_patrimonio)

# KPIs no topo
st.header("Indicadores")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Investido", f"R$ {total_investido:,.2f}")
col2.metric("Valor em Juros", f"R$ {valor_em_juros:,.2f}")
col3.metric("Valor Total do Rendimento", f"R$ {valor_total_rendimento:,.2f}")
col4.metric("Valor Descontado pela Inflação", f"R$ {valor_descontado_inflacao:,.2f}")

# Gráfico com os valores
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
        "Valor Sem Inflação": "R$ {:,.2f}",
        "Valor Com Inflação": "R$ {:,.2f}",
        "Valor Investido Até o Momento": "R$ {:,.2f}",
        "Valor em Juros": "R$ {:,.2f}"
    }), use_container_width=True)
