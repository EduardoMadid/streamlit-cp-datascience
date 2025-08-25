# Dashboard de Corridas na Índia

Este projeto é um **dashboard interativo desenvolvido em Streamlit** para análise de dados de corridas urbanas na Índia.  
O objetivo é explorar padrões de comportamento, avaliar desempenho, métodos de pagamento, horários de pico e fatores que influenciam cancelamentos e valores das viagens.

---

## Funcionalidades

- Visualização de **estatísticas gerais** das corridas (completadas e canceladas).  
- Análise de **preço, duração e distância das viagens**.  
- Avaliação de **motivos de cancelamento** por clientes e motoristas.  
- Identificação de **horários e meses de pico**.  
- Exibição de **métodos de pagamento mais utilizados**.  
- **Gráficos interativos** com Plotly para exploração detalhada dos dados.  
- **Tabs e expanders** para organizar conclusões e respostas às perguntas analíticas.

## Instalação

1. Clone o repositório:  
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_PROJETO>
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o Streamlit:
```bash
streamlit run Home.py
```

## Tecnologias Utilizadas

- **Python 3.10+** – Linguagem principal do projeto  
- **Streamlit** – Framework para dashboards interativos  
- **Pandas** – Manipulação e análise de dados  
- **Plotly Express** – Criação de gráficos interativos  
- **SciPy** – Testes estatísticos e análises avançadas  

---

## Observações

- Estrutura modular com páginas (`/pages`) e funções auxiliares (`/utils`) para facilitar manutenção  
- Sidebar interativo com filtros e navegação para melhor experiência do usuário  
- Uso de **tabs e expanders** para organizar informações sem poluir visualmente  
- Ideal para análises exploratórias, apresentações executivas e suporte à tomada de decisão  
- O dashboard é responsivo e facilmente escalável para futuras funcionalidades
