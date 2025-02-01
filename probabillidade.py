import streamlit as st
import pandas as pd
import itertools
from collections import defaultdict

# Função para calcular a probabilidade de uma sequência
def calcular_probabilidade_sequencia(sequencia, probabilidade_numeros):
    probabilidade_sequencia = 1
    for numero in sequencia:
        probabilidade_sequencia *= probabilidade_numeros.get(numero, 0)
    return probabilidade_sequencia

# Função para calcular a frequência de pares de números
def calcular_frequencia_pares(df, colunas_bolas):
    pares = defaultdict(int)
    for _, row in df.iterrows():
        numeros = row[colunas_bolas].values
        for pair in itertools.combinations(numeros, 2):
            pares[pair] += 1
    return pares

# Função para calcular a frequência de trios de números
def calcular_frequencia_trios(df, colunas_bolas):
    trios = defaultdict(int)
    for _, row in df.iterrows():
        numeros = row[colunas_bolas].values
        for trio in itertools.combinations(numeros, 3):
            trios[trio] += 1
    return trios

# Função principal do Streamlit
def main():
    # Cabeçalho
    st.title("Calculadora de Probabilidades Lotofácil")

    # Upload do arquivo Excel
    uploaded_file = st.file_uploader("Escolha o arquivo Excel", type=["xlsx"])

    if uploaded_file:
        # Carregar os dados do Excel
        df = pd.read_excel(uploaded_file)

        # Selecionar as colunas das bolas
        colunas_bolas = [f'Bola{i}' for i in range(1, 16)]

        # Calcular a contagem e a probabilidade de cada número
        numeros_mais_sorteados = df[colunas_bolas].values.flatten()
        contagem_numeros = pd.Series(numeros_mais_sorteados).value_counts()

        # Normalizar as frequências para obter a probabilidade de cada número ser sorteado
        total_sorteios = len(df)
        probabilidade_numeros = contagem_numeros / total_sorteios

        # Calcular a frequência de pares e trios
        frequencia_pares = calcular_frequencia_pares(df, colunas_bolas)
        frequencia_trios = calcular_frequencia_trios(df, colunas_bolas)

        # Selecionar os 20 números mais frequentes
        numeros_mais_frequentes = probabilidade_numeros.nlargest(20).index

        # Gerar todas as combinações possíveis de 15 números a partir dos 20 mais frequentes
        combinacoes_possiveis = itertools.combinations(numeros_mais_frequentes, 15)

        # Calcular a probabilidade de todas as combinações
        sequencias_com_probabilidade = []

        for combinacao in combinacoes_possiveis:
            probabilidade = calcular_probabilidade_sequencia(combinacao, probabilidade_numeros)
            
            # Adicionar peso para pares de números que costumam aparecer juntos
            peso_pares = sum(frequencia_pares.get(pair, 0) for pair in itertools.combinations(combinacao, 2))
            
            # Adicionar peso para trios de números que costumam aparecer juntos
            peso_trios = sum(frequencia_trios.get(trio, 0) for trio in itertools.combinations(combinacao, 3))
            
            # Ajuste de ponderação
            probabilidade_total = probabilidade * (1 + (peso_pares / total_sorteios)) * (1 + (peso_trios / total_sorteios))
            
            sequencias_com_probabilidade.append((combinacao, probabilidade_total))

        # Ordenar as sequências por probabilidade em ordem decrescente
        sequencias_com_probabilidade.sort(key=lambda x: x[1], reverse=True)  # Agora está em ordem decrescente

        # Exibir as 5 sequências mais prováveis
        top_5_sequencias = sequencias_com_probabilidade[:5]
        sequencias_df = pd.DataFrame(top_5_sequencias, columns=['Sequência', 'Probabilidade'])

        # Exibir as sequências mais prováveis como tabela
        st.write("Top 5 Sequências com Maior Probabilidade:")
        st.dataframe(sequencias_df)

        # Botão para exportar os dados em CSV
        st.download_button(
            label="Baixar Resultados em CSV",
            data=sequencias_df.to_csv(index=False).encode('utf-8'),
            file_name="sequencias_probabilidade.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
