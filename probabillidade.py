import streamlit as st
import pandas as pd
import itertools

# Função para calcular a probabilidade de uma sequência
def calcular_probabilidade_sequencia(sequencia, probabilidade_numeros):
    probabilidade_sequencia = 1
    for numero in sequencia:
        probabilidade_sequencia *= probabilidade_numeros.get(numero, 0)
    return probabilidade_sequencia

# Função principal do Streamlit
def main():
    # Cabeçalho
    st.title("Calculadora de Probabilidades de Sequências Lotofácil")

    # Passo 1: Carregar o arquivo Excel
    uploaded_file = st.file_uploader("Escolha o arquivo Excel", type=["xlsx"])

    if uploaded_file:
        # Carregar os dados do Excel
        df = pd.read_excel(uploaded_file)

        # Selecionar as colunas das bolas
        colunas_bolas = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 
                         'Bola7', 'Bola8', 'Bola9', 'Bola10', 'Bola11', 'Bola12', 
                         'Bola13', 'Bola14', 'Bola15']

        # Passo 2: Calcular a contagem de cada número
        numeros_mais_sorteados = df[colunas_bolas].values.flatten()
        contagem_numeros = pd.Series(numeros_mais_sorteados).value_counts()

        # Normalizar as frequências para obter a probabilidade de cada número ser sorteado
        total_sorteios = len(df)
        probabilidade_numeros = contagem_numeros / total_sorteios

        # Passo 3: Gerar todas as combinações possíveis de 15 números (conjunto de 15 números do 1 ao 25)
        numeros_disponiveis = range(1, 26)  # Números de 1 a 25
        combinacoes_possiveis = itertools.combinations(numeros_disponiveis, 15)

        # Passo 4: Calcular a probabilidade de todas as combinações
        sequencias_com_probabilidade = []

        for combinacao in combinacoes_possiveis:
            probabilidade = calcular_probabilidade_sequencia(combinacao, probabilidade_numeros)
            sequencias_com_probabilidade.append((combinacao, probabilidade))

        # Passo 5: Ordenar as sequências por probabilidade e pegar as 5 maiores
        sequencias_com_probabilidade.sort(key=lambda x: x[1], reverse=True)

        # Exibir as 5 sequências com maior probabilidade
        top_5_sequencias = sequencias_com_probabilidade[:5]
        sequencias_df = pd.DataFrame(top_5_sequencias, columns=['Sequência', 'Probabilidade'])

        # Exibir as sequências mais prováveis como tabela
        st.write("Top 5 Sequências com Maior Probabilidade:")
        st.dataframe(sequencias_df)

        # Passo 6: Exportar os dados em CSV
        st.download_button(
            label="Baixar Resultados em CSV",
            data=sequencias_df.to_csv(index=False).encode('utf-8'),
            file_name="sequencias_probabilidade.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()