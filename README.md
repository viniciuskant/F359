# Análise de Resistência e Resistividade em Soluções Salinas

Este projeto usa Python para ler dados de um arquivo CSV, calcular a resistência e resistividade de uma solução salina, e gerar gráficos da relação entre concentração de sal e resistência/resistividade.

## Funcionalidades

- **Cálculo de Resistência e Resistividade**: Calcula a resistência e resistividade a partir de valores de tensão, corrente e área da seção transversal.
- **Cálculo de Incertezas**: Considera as incertezas do voltímetro, amperímetro e balança para adicionar intervalos de confiança aos valores.
- **Gráficos Atualizados em Tempo Real**: Exibe gráficos de Resistência vs Concentração e Resistividade vs Concentração atualizados a cada leitura do arquivo CSV.
- **Salvar Gráficos**: Ao interromper a execução, os gráficos são salvos como `graficos.png`.

## Estrutura do Código

- `calcular_resistencia(tensao, corrente)`: Calcula a resistência.
- `incerteza_voltimetro(tensao)`: Calcula a incerteza da medição da tensão.
- `incerteza_amperimetro(corrente)`: Calcula a incerteza da medição da corrente.
- `incerteza_resistencia(tensao, corrente)`: Calcula a incerteza associada à resistência.
- `plotar_grafico_resistencia_concentracao(save=False)`: Plota os gráficos de Resistência e Resistividade vs Concentração.

## Notação dos Dados

Os dados coletados nos experimentos seguem a notação `dados-dia-mes-numero_da_coleta.csv`. O arquivo principal de dados que o programa lê é `dados.csv`, que contém as medições de tensão, corrente e área da seção transversal para diferentes concentrações de solução salina. Certifique-se de que o arquivo `dados.csv` esteja no diretório correto para que o programa possa acessá-lo e processar as informações corretamente.

## Requisitos
### Configuração do Ambiente Virtual

Para garantir que todas as dependências do projeto sejam instaladas corretamente, recomenda-se o uso de um ambiente virtual. Abaixo estão as instruções para criar e ativar um ambiente virtual tanto no Windows quanto no Linux.

#### Windows

1. Crie o ambiente virtual:
    ```bash
    python -m venv venv
    ```

2. Ative o ambiente virtual:
    ```bash
    .\venv\Scripts\activate
    ```

#### Linux

1. Crie o ambiente virtual:
    ```bash
    python3 -m venv venv
    ```

2. Ative o ambiente virtual:
    ```bash
    source venv/bin/activate
    ```

### Instalação dos Requisitos

Com o ambiente virtual ativado, instale as dependências do projeto usando o comando abaixo:

```bash
pip install -r requirements.txt
```

Caso o arquivo `requirements.txt` não esteja disponível, você pode instalar as bibliotecas necessárias manualmente:

```bash
pip install pandas matplotlib
```