import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt

# Parâmetros de configuração
VOLUME_RECEPIENTE = 100  # Volume do recipiente em mL
ESCALA_TENSAO = 1  # Escala para tensão V
ESCALA_CORRENTE = 0.001  # Escala para corrente mA
ESCALA_SAL = 1  # Escala para sal g

# Parâmetros adicionais para cálculo de incerteza
MENOR_ESCALA_TENSAO = 0.001  # Menor escala do voltímetro é 1 mV
MENOR_ESCALA_CORRENTE = 0.001 * 0.001  # Menor escala do amperímetro é 0.001 mA
MENOR_ESCALA_BALANCA = 0.01  # Menor escala da balança é 0.0001 g

# Parâmetros adicionais para cálculo de resistividade
LARGURA = 2.4  # Largura do recipiente em cm
ALTURA = 5.2  # Altura do recipiente em cm
DISTANCIA = 8  # Distância entre os eletrodos em cm
ESCALA_METRO = 0.01  # Escala para metro... CM

# Calcular área da seção transversal
area = LARGURA * ALTURA * ESCALA_METRO**2

def incerteza_amperimetro(corrente):
    """Calcular a incerteza associada ao amperímetro"""
    incerteza_leitura = MENOR_ESCALA_CORRENTE / (2 * sqrt(3))
    incerteza_calibracao = (0.0005 * corrente + 3 * MENOR_ESCALA_CORRENTE) / sqrt(3)
    return sqrt(incerteza_leitura**2 + incerteza_calibracao**2)

def incerteza_voltimetro(tensao):
    """Calcular a incerteza associada ao voltímetro"""
    incerteza_leitura = MENOR_ESCALA_TENSAO / (2 * sqrt(3))
    incerteza_calibracao = (0.005 * tensao + 3 * MENOR_ESCALA_TENSAO) / sqrt(3)
    return sqrt(incerteza_leitura**2 + incerteza_calibracao**2)

def incerteza_resistencia(tensao, corrente):
    """Calcular a incerteza associada à resistência"""
    incerteza_tensao = incerteza_voltimetro(tensao)
    incerteza_corrente = incerteza_amperimetro(corrente)
    
    if corrente == 0:
        return 0.0
    
    dR_dV = 1 / corrente * incerteza_tensao
    dR_dI = -tensao / (corrente**2) * incerteza_corrente
    return sqrt(dR_dV**2 + dR_dI**2)

def calcular_resistencia(tensao, corrente):
    """Calcular a resistência"""
    return tensao / corrente if corrente != 0 else float('inf')

def plotar_grafico_resistencia_concentracao(save = False):
    # Limpar os gráficos anteriores
    axs[0].cla()
    axs[1].cla()

    # Plotar gráfico de Resistência vs Concentração
    axs[0].errorbar(concentracoes, resistencias, yerr=incertezas_resistencias, fmt='o', label='Resistência vs Concentração', color='purple', ecolor='red', capsize=5)
    axs[0].plot(concentracoes, resistencias, color='purple')  # Adicionar linha
    axs[0].set_title('Resistência vs Concentração de Sal')
    axs[0].set_xlabel('Concentração (g/mL)')
    axs[0].set_ylabel('Resistência (Ohms)')
    axs[0].legend()

    # Plotar gráfico de Resistividade vs Concentração
    axs[1].scatter(concentracoes, resistividades, label='Resistividade vs Concentração', color='blue')
    axs[1].plot(concentracoes, resistividades, color='blue')  # Adicionar linha
    axs[1].set_title('Resistividade vs Concentração de Sal')
    axs[1].set_xlabel('Concentração (g/mL)')
    axs[1].set_ylabel('Resistividade (Ohm·m)')
    axs[1].legend()

    plt.tight_layout()
    plt.pause(1)  # Pausar por 1 segundo antes da próxima atualização

    if save:
        plt.savefig('graficos.png')

# Inicializar listas para armazenar os dados
tensoes, correntes, sais, resistencias, concentracoes = [], [], [], [], []

# Ativar modo interativo do Matplotlib
plt.ion()

# Configurar figura e eixos uma vez
fig, axs = plt.subplots(2, 1, figsize=(10, 12))

try:
    while True:
        # Ler o arquivo CSV
        df = pd.read_csv('dados.csv')  # Ajuste o nome do arquivo conforme necessário

        # Limpar listas para armazenar os dados atuais
        tensoes.clear()
        correntes.clear()
        sais.clear()
        resistencias.clear()
        concentracoes.clear()

        total_sal = 0
        for index, row in df.iterrows():
            tensao = row['tensao'] * ESCALA_TENSAO
            corrente = row['corrente'] * ESCALA_CORRENTE
            sal = row['sal'] * ESCALA_SAL

            # Calcular resistência e concentração
            resistencia = calcular_resistencia(tensao, corrente)
            total_sal += sal
            concentracao = total_sal / VOLUME_RECEPIENTE

            # Armazenar os dados
            tensoes.append(tensao)
            correntes.append(corrente)
            sais.append(sal)
            resistencias.append(resistencia)
            concentracoes.append(concentracao)

        # Calcular resistividade
        resistividades = [resistencia * area / DISTANCIA for resistencia in resistencias]
        incertezas_resistencias = [incerteza_resistencia(tensao, corrente) for tensao, corrente in zip(tensoes, correntes)]

        # Plotar gráfico de Resistência vs Concentração
        plotar_grafico_resistencia_concentracao()


except KeyboardInterrupt:
    plotar_grafico_resistencia_concentracao(save=True)
    print("Gráfico salvo como 'graficos.png'.")
    print("Programa interrompido.")
    plt.ioff()

except Exception as e:
    print(f"Erro: {e}")
