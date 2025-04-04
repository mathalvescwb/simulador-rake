import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Configurações do simulador

def simular_rake(mesas, cap_percentual, maos_por_hora):
    resultados = []
    for mesa in mesas:
        cap_rake = 5 * mesa["blind_bb"]
        rake_por_mao = cap_rake * cap_percentual
        rake_hora = rake_por_mao * maos_por_hora
        rake_dia = rake_hora * 24
        rake_mes = rake_dia * 30
        rake_ano = rake_mes * 12

        resultados.append({
            "Mesa": mesa["nome"],
            "Rake/Hora": rake_hora,
            "Rake/Dia": rake_dia,
            "Rake/Mês": rake_mes,
            "Rake/Ano": rake_ano
        })
    return pd.DataFrame(resultados)

# Interface Streamlit
st.title("Simulador de Rake para Mesas de Omaha")

# Entrada do usuário
cap_percentual = st.slider("% de Mãos que Atingem o Cap de Rake", 0.0, 1.0, 0.65, 0.01)
maos_por_hora = st.slider("Mãos por Hora", 50, 120, 90, 1)

mesas_exemplo = [
    {"nome": "Omaha 0.30/0.60", "blind_bb": 0.60},
    {"nome": "Omaha 0.50/1", "blind_bb": 1.00},
    {"nome": "Omaha 1/2", "blind_bb": 2.00},
    {"nome": "Omaha 2/4", "blind_bb": 4.00},
]

# Simulação e exibição da tabela
resultado = simular_rake(mesas_exemplo, cap_percentual, maos_por_hora)
st.subheader("Resultado da Simulação")
st.dataframe(resultado)

# Gráfico
def gerar_grafico(maos_range, mesas, cap_percentual):
    totais = []
    for mph in maos_range:
        df = simular_rake(mesas, cap_percentual, mph)
        total = df["Rake/Ano"].sum()
        totais.append((mph, total))
    df_plot = pd.DataFrame(totais, columns=["Mãos/Hora", "Rake Anual Total"])
    return df_plot

# Geração do gráfico com base em faixa dinâmica
st.subheader("Gráfico do Rake Anual Total")
if st.checkbox("Exibir gráfico para faixa de mãos por hora"):
    faixa_min = st.number_input("Mínimo de Mãos por Hora", 50, 100, 70)
    faixa_max = st.number_input("Máximo de Mãos por Hora", 60, 150, 100)
    if faixa_min < faixa_max:
        df_grafico = gerar_grafico(range(faixa_min, faixa_max + 1, 5), mesas_exemplo, cap_percentual)
        st.line_chart(df_grafico.set_index("Mãos/Hora"))
    else:
        st.warning("O valor mínimo deve ser menor que o máximo.")
