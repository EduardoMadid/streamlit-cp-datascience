import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
from scipy import stats

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Reservas NCR",
    page_icon="🚗",
    layout="wide"
)

st.logo('assets/logo_uber.png', size="large", link='https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard')

# CSS personalizado para melhorar o visual
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #264653;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2A9D8F;
        margin: 0.5rem 0;
    }
    .plot-container {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Funções de Pré-processamento e Gráficos 
@st.cache_data
def load_data_and_preprocess():
    """Carrega e pré-processa o dataset, garantindo o formato correto dos dados."""
    try:
        df = pd.read_csv('data/ncr_ride_bookings.csv')
        
        # Cópia do DataFrame original para a comparação "antes"
        raw_df = df.copy()
        
        # Conversão de tipos de dados para garantir que os cálculos funcionem
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.hour
        
        # Tratar colunas numéricas que podem estar como string
        numeric_cols = ['Booking Value', 'Ride Distance', 'Avg VTAT', 'Avg CTAT', 'Cancelled Rides by Customer', 
                        'Cancelled Rides by Driver', 'Incomplete Rides', 'Driver Ratings', 'Customer Rating']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Preencher valores ausentes para evitar erros nos gráficos e métricas
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype in ['int64', 'float64']:
                    median_val = df[col].median()
                    df[col].fillna(median_val, inplace=True)
                else:
                    mode_val = df[col].mode()[0]
                    df[col].fillna(mode_val, inplace=True)
                    
        return raw_df, df
    except FileNotFoundError:
        st.error("O arquivo `ncr_ride_bookings.csv` não foi encontrado. Por favor, verifique se o arquivo está no diretório `data/`.")
        st.stop()
    except Exception as e:
        st.error(f"Erro ao carregar ou processar os dados: {e}")
        st.stop()

# Função para criar gráfico de pizza
def create_pie_chart(data, values, names, title, color_sequence=['#2A9D8F', '#E9C46A', '#F4A261', '#E76F51', '#264653']):
    fig = px.pie(
        data, 
        values=values, 
        names=names, 
        title=title,
        color_discrete_sequence=color_sequence or px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        font=dict(size=12),
        title_font_size=16,
        showlegend=True,
        height=400
    )
    return fig

# Função para criar gráfico de barras
def create_bar_chart(data, x, y, title, color=None):
    fig = px.bar(
        data, 
        x=x, 
        y=y, 
        title=title,
        color=color,
        color_discrete_sequence=['#2A9D8F', '#E9C46A', '#F4A261', '#E76F51', '#264653']
    )
    fig.update_layout(
        font=dict(size=12),
        title_font_size=16,
        xaxis_title=x,
        yaxis_title=y,
        height=400
    )
    return fig

# Função para criar histograma
def create_histogram(data, x, title, nbins=30):
    fig = px.histogram(
        data, 
        x=x, 
        title=title,
        nbins=nbins,
        color_discrete_sequence=['#2A9D8F', '#E9C46A', '#F4A261', '#E76F51', '#264653']
    )
    fig.update_layout(
        font=dict(size=12),
        title_font_size=16,
        height=400
    )
    return fig

# Função para criar gráfico de linha temporal
def create_time_series(data, x, y, title):
    fig = px.line(
        data, 
        x=x, 
        y=y, 
        title=title,
        color_discrete_sequence=['#2A9D8F', '#E9C46A', '#F4A261', '#E76F51', '#264653']
    )
    fig.update_layout(
        font=dict(size=12),
        title_font_size=16,
        height=400
    )
    return fig

#Carregamento de Dados 
raw_df, df = load_data_and_preprocess()

# Título principal
st.markdown('<h1 class="main-header">🚗 Dashboard de Reservas NCR</h1>', unsafe_allow_html=True)

# Abas de Navegação 
tab_contexto, tab_preprocessamento, tab_classificacao, tab_analise, tab_conclusao = st.tabs([
    "Contexto do Projeto", "Pré-processamento", "Classificação das Variáveis", "Análise de Dados Gerais", "Conclusão"
])

# Pagina de contexto
with tab_contexto:
    st.header("1. Contexto do Projeto 📝")
    st.markdown("""
    Este dashboard interativo foi desenvolvido para analisar e visualizar dados de um serviço de reserva de viagens, a Uber, com foco em otimizar a operação e a experiência do usuário e disponibilizar uma forma de analisar os dados gerais da empresa.

    --- PERGUNTAS DE ANÁLISE ---
    - Quais são os horários de pico de reservas?
    - Quais são os principais motivos de cancelamento?
    - Qual a principal forma de pagamento na India?
    - O valor da corrida e a distância estão relacionados de que forma?
    - A distância média das viagens completadas é igual a distância média das viagens incompletas ou canceladas?
    - Os valores das viagens se baseiam em distância ou em outro aspecto?

    As seções a seguir detalham as etapas do projeto, desde o tratamento dos dados até a apresentação das conclusões.

    A baixo temos o dataframe puro, após ser baixado no Kaggle:
    """)

    raw_df

# Pagina de Pre-Processamento
with tab_preprocessamento:
    st.header("2. Pré-processamento e Tratamento de Dados 🛠️")
    st.markdown("""
    A etapa de pré-processamento é a base de qualquer análise de dados confiável. Nela, garantimos a **qualidade, consistência e o formato correto** dos dados para que os cálculos e visualizações não apresentem erros.
    Para este dashboard, realizamos as seguintes ações:
    - **Conversão de Tipos:** Garantimos que colunas como 'Date', 'Time' e outras numéricas estejam no formato correto.
    - **Tratamento de Dados Ausentes:** Lidamos com valores em branco (`NaN`) preenchendo-os com a mediana ou a moda para evitar falhas nos gráficos e cálculos.
    - **Retirada de Duplicatas** Lidamos com valores duplicados retirando as duplicatas para maior eficiência dos dados.
    """)
    st.markdown("### Dados Antes e Depois do Tratamento 🔬")
    st.markdown("Veja o impacto do pré-processamento. A tabela abaixo à esquerda mostra os dados com valores ausentes e os tipos originais, enquanto a tabela à direita mostra o resultado após a limpeza e conversão.")

    col_before, col_after = st.columns(2)

    with col_before:
        st.markdown("#### **Antes do Tratamento**")
        st.info("Valores nulos por coluna (antes):")
        st.dataframe(raw_df.isnull().sum().astype(str), use_container_width=True)
        st.info("Tipos de Dados (antes):")
        buffer = StringIO()
        raw_df.info(buf=buffer)
        s = buffer.getvalue()
        st.code(s)

    with col_after:
        st.markdown("#### **Depois do Tratamento**")
        st.success("Valores nulos por coluna (depois):")
        st.dataframe(df.isnull().sum().astype(str), use_container_width=True)
        st.success("Tipos de Dados (depois):")
        buffer = StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.code(s)

    st.success("Dados carregados e pré-processados com sucesso!")

# Pagina de Classificação de Variaveis
with tab_classificacao:
    st.header("3. Classificação das Variáveis 📊")
    st.markdown("""
    A classificação das variáveis é um passo fundamental da análise exploratória. Entender o tipo de dado que estamos trabalhando nos ajuda a escolher os métodos estatísticos e os tipos de gráficos mais adequados.
    
    ### **Tipos de Variáveis**
    - **Variáveis Qualitativas (ou Categóricas):** Representam características uma classificação por tipo ou atributo.
        - `Nominais`: Características e atributos que não podem ser ordenados.
        - `Ordinais`: Características e atributos que podem ser ordenados.

    - **Variáveis Quantitativas (ou Numéricas):** Representam quantidades que podem ser medidas ou contadas, ou seja possuem uma escala de mensuração númerica.
        - `Discretas`: Entre dois pontos da escala existe número finito de valores.
        - `Contínuas`: Entre dois pontos da escala existe número infinito de valores.
    """)
    
    st.markdown("#### **Classificação Completa das Variáveis do Dataset**")
    
    # Dicionário com a classificação correta e a justificativa para cada coluna do DF
    classification_data = {
        'Variable': [],
        'Type': [],
        'Justification': []
    }
    
    # Mapeamento completo e correto das variáveis
    variable_info = {
        'Date': {'type': 'Quantitativa (Contínua)', 'justification': 'A data pode ser representada numericamente e assume valores em uma escala contínua e permitindo comparações.'},
        'Vehicle Type': {'type': 'Qualitativa (Nominal)', 'justification': 'Classifica os veículos em categorias, sem hierarquia entre eles.'},
        'Booking ID': {'type':'ID', 'justification':'ID único para cada pedido de viagem.'},
        'Booking Status': {'type': 'Qualitativa (Nominal)', 'justification': 'Categoriza o status das reservas, como "Completed" ou "Cancelled".'},
        'Customer ID': {'type':'ID', 'justification':'ID único para cada usuário.'},
        'Booking Value': {'type': 'Quantitativa (Contínua)', 'justification': 'Representa um valor monetário que pode ter casas decimais.'},
        'Ride Distance': {'type': 'Quantitativa (Contínua)', 'justification': 'A distância percorrida é uma medida contínua, podendo ser fracionada.'},
        'Pickup Location': {'type': 'Qualitativa (Nominal)', 'justification': 'Nomes de locais são categorias nominais, sem ordem.'},
        'Drop Location': {'type': 'Qualitativa (Nominal)', 'justification': 'Nomes de locais são categorias nominais, sem ordem.'},
        'Payment Method': {'type': 'Qualitativa (Nominal)', 'justification': 'Tipos de pagamento são categorias distintas, sem hierarquia.'},
        'Reason for cancelling by Customer': {'type': 'Qualitativa (Nominal)', 'justification': 'As razões de cancelamento são rótulos categóricos.'},
        'Driver Cancellation Reason': {'type': 'Qualitativa (Nominal)', 'justification': 'As razões de cancelamento por motorista são rótulos categóricos.'},
        'Incomplete Rides Reason':{'type':'Qualitativa (Nominal)', 'justification':'As razões de viagens canceladas são rótulos categóricos, sem ordem.' },
        'Trip Duration': {'type': 'Quantitativa (Contínua)', 'justification': 'A duração de uma viagem é uma medida de tempo, que pode ser contínua.'},
        'Driver Ratings': {'type': 'Quantitativa (Discreta)', 'justification': 'São notas inteiras (ex: 1 a 5), uma contagem discreta de estrelas.'},
        'Customer Rating': {'type': 'Quantitativa (Discreta)', 'justification': 'São notas inteiras, uma contagem discreta de estrelas.'},
        'Cancelled Rides by Customer': {'type': 'Quantitativa (Discreta)', 'justification': 'É uma contagem de eventos de cancelamento, em números inteiros.'},
        'Cancelled Rides by Driver': {'type': 'Quantitativa (Discreta)', 'justification': 'É uma contagem de eventos de cancelamento, em números inteiros.'},
        'Incomplete Rides': {'type': 'Quantitativa (Discreta)', 'justification': 'É uma contagem de viagens incompletas, em números inteiros.'},
        'Avg VTAT': {'type': 'Quantitativa (Contínua)', 'justification': 'Representa a média de tempo, que é um valor contínuo.'},
        'Avg CTAT': {'type': 'Quantitativa (Contínua)', 'justification': 'Representa a média de tempo, que é um valor contínuo.'},
        'Time': {'type': 'Qualitativa (Nominal)', 'justification': 'Embora represente um ponto no tempo, é usado como categoria para agrupar as viagens.'},
        'Hour': {'type': 'Quantitativa (Contínua)', 'justification': 'É uma variável inteira derivada do tempo, sendo continuamente medida.'},
    }

    for col in df.columns:
        if col in variable_info:
            classification_data['Variable'].append(col)
            classification_data['Type'].append(variable_info[col]['type'])
            classification_data['Justification'].append(variable_info[col]['justification'])
        else:
            classification_data['Variable'].append(col)
            classification_data['Type'].append('Desconhecido')
            classification_data['Justification'].append('Não classificado.')
    
    classification_df = pd.DataFrame(classification_data)
    
    st.dataframe(classification_df, use_container_width=True, height=810)

# Pagina de Analise de Dados
with tab_analise:
    st.header("4. Análise dos Dados 📊")
    st.markdown("Use os filtros abaixo para segmentar os dados e realizar análises mais específicas. Esses filtros determinam os dados de todos as análises e gráficos abaixo.")

    # ----------------- Filtros -----------------
    date_range = st.date_input(
        "Selecione o período:",
        value=(df['Date'].min().date(), df['Date'].max().date()),
        min_value=df['Date'].min().date(),
        max_value=df['Date'].max().date()
    )
    
    col_multi_1, col_multi_2 = st.columns(2)

    with col_multi_1:
        vehicle_types = st.multiselect(
            "Tipo de Veículo:",
            options=df['Vehicle Type'].unique(),
            default=df['Vehicle Type'].unique()
        )

    with col_multi_2:
        booking_status = st.multiselect(
            "Status da Reserva:",
            options=df['Booking Status'].unique(),
            default=df['Booking Status'].unique()
        )

    # Aplicar filtros
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = df[
            (df['Date'].dt.date >= start_date) & 
            (df['Date'].dt.date <= end_date) &
            (df['Vehicle Type'].isin(vehicle_types)) &
            (df['Booking Status'].isin(booking_status))
        ]
    else:
        filtered_df = df[
            (df['Vehicle Type'].isin(vehicle_types)) &
            (df['Booking Status'].isin(booking_status))
        ]

    '---'
    # ----------------- KPIs Principais -----------------
    st.subheader("Indicadores Chave de Performance (KPIs) 📈")
    st.markdown("Os KPIs (do inglês *Key Performance Indicators*) são métricas essenciais que nos dão uma visão rápida da saúde e do desempenho do negócio, ou seja, conseguimos obter uma visão geral de forma intuitiva.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_bookings = len(filtered_df)
        st.metric("Total de Reservas", f"{total_bookings:,}")

    with col2:
        completed_rides = len(filtered_df[filtered_df['Booking Status'] == 'Completed'])
        completion_rate = (completed_rides / total_bookings * 100) if total_bookings > 0 else 0
        st.metric("Taxa de Conclusão", f"{completion_rate:.1f}%")

    with col3:
        avg_booking_value = filtered_df['Booking Value'].mean()
        if not pd.isna(avg_booking_value):
            st.metric("Valor Médio da Reserva", f"₹{avg_booking_value:.2f}")
        else:
            st.metric("Valor Médio da Reserva", "N/A")

    with col4:
        avg_distance = filtered_df['Ride Distance'].mean()
        if not pd.isna(avg_distance):
            st.metric("Distância Média", f"{avg_distance:.2f} km")
        else:
            st.metric("Distância Média", "N/A")
    '---'

    # ----------------- Análise de Status e Veículos -----------------
    st.subheader("Análise de Status e Veículos 📊")
    st.markdown("O gráfico de pizza é excelente para mostrar a **composição de um todo**, enquanto o de barras é ideal para **comparar categorias**. ")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Distribuição do Status das Reservas")
        st.markdown("Este gráfico mostra a proporção de cada status de reserva, permitindo identificar rapidamente o percentual de viagens completadas, canceladas ou incompletas.")
        status_counts = filtered_df['Booking Status'].value_counts()
        fig_status = create_pie_chart(
            status_counts.reset_index(), 
            'count', 
            'Booking Status', 
            "",
            color_sequence= ['#2A9D8F', '#E9C46A', '#F4A261', '#E76F51', '#264653']
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with col2:
        st.markdown("#### Distribuição por Tipo de Veículo")
        st.markdown("Aqui, visualizamos a participação de mercado de cada tipo de veículo, mostrando quais são os mais populares entre os clientes.")
        vehicle_counts = filtered_df['Vehicle Type'].value_counts()
        fig_vehicle = create_bar_chart(
            vehicle_counts.reset_index(), 
            'Vehicle Type', 
            'count', 
            "",
            color='Vehicle Type'
        )
        st.plotly_chart(fig_vehicle, use_container_width=True)

    st.subheader("Resumo dos Gráficos 📈")
    st.markdown("É possível entender pelos gráficos que muitas corridas não são completadas (`38%`). Além disso, o veículo mais utilizado na Índia para realizar essas corridas é o (`Auto`)")

    '---'
    
    # ----------------- Análise Financeira e de Distância -----------------
    st.subheader("Análise de Valores e Distâncias 💰")
    st.markdown("Histogramas são perfeitos para visualizar a **distribuição de variáveis contínuas**. Eles nos ajudam a entender a frequência de diferentes valores, como a maioria das corridas estão concentradas em uma faixa de preço ou distância.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Distribuição dos Valores de Reserva")
        st.markdown("Analisar a distribuição dos valores nos permite entender a faixa de preço mais comum das corridas e identificar possíveis outliers (valores muito altos ou baixos).")
        booking_values = filtered_df.dropna(subset=['Booking Value'])
        if not booking_values.empty:
            fig_value = create_histogram(
                booking_values, 
                'Booking Value', 
                ""
            )
            st.plotly_chart(fig_value, use_container_width=True)
        else:
            st.info("Dados de valor de reserva não disponíveis para o filtro selecionado.")

    with col2:
        st.markdown("#### Distribuição das Distâncias das Viagens")
        st.markdown("Da mesma forma, a distribuição das distâncias mostra se as viagens tendem a ser curtas, médias ou longas, um insight valioso para o planejamento de rotas e precificação.")
        ride_distances = filtered_df.dropna(subset=['Ride Distance'])
        if not ride_distances.empty:
            fig_distance = create_histogram(
                ride_distances, 
                'Ride Distance', 
                ""
            )
            st.plotly_chart(fig_distance, use_container_width=True)
        else:
            st.info("Dados de distância não disponíveis para o filtro selecionado.")

    st.subheader("Resumo dos Gráficos 📈")
    st.markdown("É possível entender pelos gráficos que a faixa de preço mais comum nas corridas é entre (`400-599 rupias indianas`). Além disso, a média de tempo das viagens é entre (`23 - 25 minutos`).")

    '---'
    # ----------------- Análise de Avaliações -----------------
    st.subheader("Análise de Avaliações ⭐")
    st.markdown("As avaliações são um indicador direto da **satisfação de clientes e motoristas**. A distribuição das notas nos ajuda a identificar se o serviço atende às expectativas ou se há pontos de melhoria.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Distribuição das Avaliações dos Motoristas")
        st.markdown("Uma alta concentração de avaliações 5 estrelas sugere que os motoristas estão performando bem. O histograma revela a frequência de cada nota.")
        driver_ratings = filtered_df.dropna(subset=['Driver Ratings'])
        if not driver_ratings.empty:
            fig_driver = create_histogram(
                driver_ratings, 
                'Driver Ratings', 
                "",
                nbins=20
            )
            st.plotly_chart(fig_driver, use_container_width=True)
        else:
            st.info("Dados de avaliação de motoristas não disponíveis para o filtro selecionado.")

    with col2:
        st.markdown("#### Distribuição das Avaliações dos Clientes")
        st.markdown("Este gráfico mostra como os motoristas avaliam os clientes. Uma distribuição positiva indica que a experiência de viagem é satisfatória para ambos os lados.")
        customer_ratings = filtered_df.dropna(subset=['Customer Rating'])
        if not customer_ratings.empty:
            fig_customer = create_histogram(
                customer_ratings, 
                'Customer Rating', 
                "",
                nbins=20
            )
            st.plotly_chart(fig_customer, use_container_width=True)
        else:
            st.info("Dados de avaliação de clientes não disponíveis para o filtro selecionado.")

    
    st.subheader("Resumo dos Gráficos 📈")
    st.markdown("É possível entender pelos gráficos que os motoristas em sua maior parte possuem uma avaliação de (`4.2 - 4.3`). Por outro lado, um pouco mais alto, a avaliação média dos clientes varia entre (`4.4 - 4.5`) ")

    '---'
    
    # ----------------- Análise de Cancelamentos -----------------
    st.subheader("Análise de Cancelamentos 🚫")
    st.markdown("Identificar as **razões de cancelamento** é fundamental para melhorar a qualidade do serviço. Os gráficos de barras nos mostram as causas mais frequentes, permitindo que a empresa atue de forma estratégica para reduzir a taxa de cancelamento.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Razões de Cancelamento por Cliente")
        st.markdown("Este gráfico ajuda a entender por que os clientes estão desistindo de suas reservas. Problemas com o motorista, tempo de espera ou mudanças de planos são algumas das razões comuns.")
        customer_cancellations = filtered_df.dropna(subset=['Reason for cancelling by Customer'])
        if not customer_cancellations.empty:
            cancel_reasons = customer_cancellations['Reason for cancelling by Customer'].value_counts()
            fig_cancel_customer = create_bar_chart(
                cancel_reasons.reset_index(), 
                'Reason for cancelling by Customer', 
                'count', 
                ""
            )
            st.plotly_chart(fig_cancel_customer, use_container_width=True)
        else:
            st.info("Dados de cancelamento por cliente não disponíveis para o filtro selecionado.")
    

    with col2:
        st.markdown("#### Razões de Cancelamento por Motorista")
        st.markdown("A análise das razões de cancelamento por motorista é igualmente importante, pois revela gargalos operacionais, como problemas com o cliente, localização ou logística.")
        driver_cancellations = filtered_df.dropna(subset=['Driver Cancellation Reason'])
        if not driver_cancellations.empty:
            driver_cancel_reasons = driver_cancellations['Driver Cancellation Reason'].value_counts()
            fig_cancel_driver = create_bar_chart(
                driver_cancel_reasons.reset_index(), 
                'Driver Cancellation Reason', 
                'count', 
                ""
            )
            st.plotly_chart(fig_cancel_driver, use_container_width=True)
        else:
            st.info("Dados de cancelamento por motorista não disponíveis para o filtro selecionado.")

    st.subheader("Resumo dos Gráficos 📈")
    st.markdown("É possível entender pelos gráficos que o maior motivo do cliente cancelar as corridas, é por conta de (`Endereços errados`), ou seja, o motorista não chega no local do cliente. Pelo lado do motorista, o maior motivo de cancelamento é (`Problemas em relação ao cliente`).")

    '---'

    # ----------------- Análise Temporal -----------------
    st.subheader("Análise Temporal 🕐")
    st.markdown("Entender o padrão de corridas ao longo do tempo é crucial para otimizar a operação. O gráfico de barras por hora identifica os horários de pico, enquanto a série temporal revela a tendência geral de reservas.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Reservas por Hora do Dia")
        st.markdown("Este gráfico mostra a distribuição de reservas ao longo de um dia. Os picos indicam as horas de maior demanda, como manhãs e finais de tarde.")
        hourly_bookings = filtered_df.groupby('Hour').size().reset_index(name='count')
        fig_hourly = create_bar_chart(
            hourly_bookings, 
            'Hour', 
            'count', 
            ""
        )
        st.plotly_chart(fig_hourly, use_container_width=True)

    with col2:
        st.markdown("#### Tendência Diária de Reservas")
        st.markdown("A série temporal nos permite visualizar a tendência de reservas ao longo dos dias, identificando padrões sazonais ou flutuações anormais.")
        daily_bookings = filtered_df.groupby(filtered_df['Date'].dt.date).size().reset_index(name='count')
        daily_bookings.columns = ['Date', 'count']
        fig_daily = create_time_series(
            daily_bookings, 
            'Date', 
            'count', 
            ""
        )
        st.plotly_chart(fig_daily, use_container_width=True)

    st.subheader("Resumo dos Gráficos 📈")
    st.markdown("É possível entender pelos gráficos que o horário de pico, acontece as (`18:00`), ou seja, entre as 17:00 e 19:00, acontece a maior quantidade de corridas. Alem disso, também enxergamos que os meses com mais corridas acontecendo são (`Janeiro, Novembro e Dezembro`) ")

    '---'

    # ----------------- Pagamento e Localizações -----------------
    st.subheader("Métodos de Pagamento e Localizações 💳🗺️")
    st.markdown("Analisar a distribuição de métodos de pagamento e as localizações de origem nos ajuda a entender o comportamento dos usuários e otimizar a estratégia de marketing e logística.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Distribuição dos Métodos de Pagamento")
        st.markdown("O gráfico de pizza revela qual a preferência dos clientes em relação aos métodos de pagamento, informação crucial para estratégias financeiras.")
        payment_methods = filtered_df.dropna(subset=['Payment Method'])
        if not payment_methods.empty:
            payment_counts = payment_methods['Payment Method'].value_counts()
            fig_payment = create_pie_chart(
                payment_counts.reset_index(), 
                'count', 
                'Payment Method', 
                ""
            )
            st.plotly_chart(fig_payment, use_container_width=True)
        else:
            st.info("Dados de método de pagamento não disponíveis para o filtro selecionado.")


    st.subheader("Resumo dos Gráficos 📈")
    st.markdown("É possível entender pelos gráficos que os métodos de pagamentos mais utilizados na Índia se chamam (`UPI`),de Unified Payments Interfaces, um sistema de pagamentos instantâneos da Índia e (`Dinheiro`). Também é possível perceber uma quantidade parecida de locais de origem, mostrando constância nos dados, mas o local com mais corridas é (`Khandsa`). ")


    '---'
    
    # ----------------- Gráficos de Dispersão e Correlação -----------------
    st.subheader("Dispersão e Correlação entre Variáveis 📉📈")
    st.markdown("Com gráficos, podemos visualizar a dispersão dos dados e a relação entre variáveis de forma intuitiva.")

    col_corr, col_dist = st.columns(2)

    with col_corr:
        st.markdown("#### Relação entre Valor da Corrida e Distância")
        st.markdown("O gráfico de dispersão mostra se há uma **correlação** entre o valor de uma reserva e a distância percorrida. Uma nuvem de pontos que segue uma linha ascendente indica uma correlação positiva, ou seja, viagens mais longas tendem a ser mais caras.")
        fig_scatter = px.scatter(
            filtered_df,
            x='Ride Distance',
            y='Booking Value',
            title='Valor da Reserva vs. Distância da Corrida',
            color_discrete_sequence=['#2A9D8F']
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_dist:
        st.markdown("#### Distribuição do Valor da Reserva")
        st.markdown("O boxplot é ideal para visualizar a **dispersão** dos dados. Ele exibe a mediana (linha central), os quartis, e a presença de outliers (pontos isolados), revelando a variação dos valores de reserva.")
        fig_boxplot = px.box(
            filtered_df,
            y='Booking Value',
            title='Dispersão dos Valores de Reserva',
            color_discrete_sequence=['#E76F51']
        )
        st.plotly_chart(fig_boxplot, use_container_width=True)
    
    
    st.subheader("Resumo dos Gráficos 📈")
    st.markdown("É possível entender pelos gráficos que o valor da reserva, não parece ter uma forte relação com o tempo da corrida, mostrando que existem (`várias corridas que percorrem pouco e custam valores altos`). Além disso, observamos pelo boxplot que a media de valores de corridas é de (`414 rupias indianas`), porém com (`vários outliers`), apenas confirmando uma relação fraca entre distância e valor.")
    
    '---'
    
    # ----------------- Medidas de Dispersão -----------------
    st.subheader("Medidas de Dispersão e Correlação 📏")
    st.markdown("Além das médias, a dispersão nos mostra a variabilidade dos dados. Uma correlação indica a relação entre duas variáveis.")

    col5, col6 = st.columns(2)
    with col5:
        std_dev_value = filtered_df['Booking Value'].std()
        if not pd.isna(std_dev_value):
            st.metric("Desvio Padrão (Valor Reserva)", f"₹{std_dev_value:.2f}")
        else:
            st.metric("Desvio Padrão (Valor Reserva)", "N/A")

    with col6:
        correlation = filtered_df['Booking Value'].corr(filtered_df['Ride Distance'])
        if not pd.isna(correlation):
            st.metric("Correlação (Valor vs. Distância)", f"{correlation:.2f}")
        else:
            st.metric("Correlação (Valor vs. Distância)", "N/A")
            
    st.markdown("""
    * **Desvio Padrão:** Um valor alto indica que os dados (`Booking Value`) estão muito espalhados em relação à média. Porém como a média do valor reserva é de (`414`), isso demonstra uma certa distância entre tais valores, o que conclui que os dados estão bastante espalhados e variados.
    * **Correlação:** O valor varia de 0 a 1. Um valor próximo de 1 indica que, à medida que a distância aumenta, o valor da reserva tende a aumentar. Um valor próximo de 0 indica pouca ou nenhuma relação. Com os dados que estamos utilizando, a correlação entre Valor e Distância, que resultou em(`0.01`), concluimos que eles realmente possuem tão pouca relação que é melhor considerar como sem relação.
    """)
    with col2:
        st.markdown("#### Top 10 Localizações de Origem")
        st.markdown("O gráfico de barras mostra as áreas com maior demanda por corridas, permitindo que a empresa aloque mais veículos nessas regiões para otimizar o tempo de espera.")
        pickup_locations = filtered_df['Pickup Location'].value_counts().head(10)
        fig_pickup = create_bar_chart(
            pickup_locations.reset_index(), 
            'count', 
            'Pickup Location', 
            ""
        )
        fig_pickup.update_layout(xaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_pickup, use_container_width=True)
    
    '---'
    
    # ----------------- Novo Teste de Hipótese e IC -----------------
    st.subheader("Teste de Hipótese: Análise de Distância vs. Status 🧐")
    st.markdown("""
    Vamos investigar se há uma diferença estatisticamente significativa na **distância média das viagens** entre aquelas que foram **completadas** e as que foram **canceladas/incompletas**.
    
    -   **Hipótese Nula (H₀):** A distância média das viagens completadas é igual à distância média das viagens canceladas/incompletas.
    -   **Hipótese Alternativa (Hₐ):** A distância média das viagens completadas é diferente da distância média das viagens canceladas/incompletas.
    
    Para esta análise, utilizamos um **Teste T de duas amostras independentes** e um **Intervalo de Confiança (IC)** de 90% (Valor Normal para IC) para a diferença das médias. Esse valor de IC foi escolhido pensando na quantidade de dados que estamos utilizando e na dificuldade de igualar os dois tópicos sendo discutidos.
    """)

    # Primeiro, verificamos se o DataFrame filtrado não está vazio
    if filtered_df.empty:
        st.warning("O DataFrame filtrado está vazio. Por favor, ajuste as seleções de filtro para ver os resultados.")
    else:
        # Filtrar os dados para as duas populações de interesse
        try:
            completed_distances = filtered_df[filtered_df['Booking Status'] == 'Completed']['Ride Distance'].dropna()
            
            cancelled_statuses = ['Cancelled by Customer', 'Cancelled by Driver', 'Incomplete']
            cancelled_distances = filtered_df[filtered_df['Booking Status'].isin(cancelled_statuses)]['Ride Distance'].dropna()

        except KeyError:
            st.error("As colunas 'Booking Status' ou 'Ride Distance' não foram encontradas no conjunto de dados. Verifique a ortografia das colunas.")
            st.stop()
        
        # Verificamos o tamanho dos grupos de dados
        if completed_distances.empty or cancelled_distances.empty:
            st.warning("Dados insuficientes para realizar o teste de hipótese. Para que o teste funcione, por favor, **ajuste o filtro 'Status da Reserva' para incluir tanto 'Completed' quanto pelo menos um tipo de 'Cancelado'**.")
        elif len(completed_distances) < 2 or len(cancelled_distances) < 2:
            st.warning("Os grupos de dados são muito pequenos para realizar uma análise estatística válida. Por favor, ajuste os filtros.")
        else:
            # T-test e visualização
            t_stat, p_value = stats.ttest_ind(completed_distances, cancelled_distances, equal_var=False)

            st.markdown("#### **Resultados do Teste T**")
            st.info(f"Estatística T: **{t_stat:.2f}**")
            st.info(f"Valor-p (p-value): **{p_value:.4f}**")

            st.markdown("#### **Interpretação**")
            if p_value < 0.1:
                st.success("✅ **Conclusão:** O valor-p é menor que 0.1. **Rejeitamos a Hipótese Nula.** Há uma diferença estatisticamente significativa na distância média entre viagens completadas e canceladas.")
            else:
                st.warning("❌ **Conclusão:** O valor-p é maior que 0.1. **Não há evidência para rejeitar a Hipótese Nula.** Não podemos afirmar que há uma diferença estatisticamente significativa.")

            # Visualização para apoiar a interpretação
            mean_distances = pd.DataFrame({
                'Status': ['Completada', 'Cancelada/Incompleta'],
                'Distância Média (km)': [completed_distances.mean(), cancelled_distances.mean()]
            })
            fig_ttest_dist = px.bar(
                mean_distances,
                x='Status',
                y='Distância Média (km)',
                title='Distância Média por Status da Corrida',
                color='Status',
                color_discrete_sequence=['#2A9D8F', '#E76F51']
            )
            st.plotly_chart(fig_ttest_dist, use_container_width=True)

    # ----------------- Tabela de Dados -----------------
    st.subheader("Dados Detalhados 📋")
    st.markdown("A tabela abaixo exibe uma amostra dos dados filtrados. Ela é útil para uma inspeção mais aprofundada das informações que alimentam os gráficos e KPIs.")
    st.dataframe(
        filtered_df.head(100), 
        use_container_width=True,
        height=400
    )

# Tabs para a Pagina de Conclusao

with tab_conclusao:
    tab_conclusao2, tab_perguntas = st.tabs(["📌 Conclusão Geral", "❓ Perguntas Analisadas"])
    # Pagina de Conclusao Geral
    with tab_conclusao2:
        st.header("5. Conclusão e Insights Principais 🎯")
        
        st.markdown("""
        Com base nas análises realizadas, destacamos os seguintes pontos críticos e padrões observados:
        """)
        
        # Usando expander para cada item para deixar visual limpo
        with st.expander("Análise de Desempenho das Corridas"):
            st.write("""
            - **38% das corridas não foram concluídas**, indicando alto índice de cancelamentos.
            - O veículo predominante na Índia é o **Auto**, mostrando preferência consolidada nesse modal.
            """)

        with st.expander("Análise de Preço e Duração"):
            st.write("""
            - Faixa de preço predominante: **400 a 599 rupias indianas**.
            - Tempo médio das viagens: **23 a 25 minutos**, indicando padrão estável.
            """)

        with st.expander("Análise de Avaliações"):
            st.write("""
            - Motoristas: **4.2 a 4.3**
            - Clientes: **4.4 a 4.5**
            - Indica percepção mais positiva pelos passageiros.
            """)

        with st.expander("Motivos de Cancelamento"):
            st.write("""
            - Clientes: **endereços incorretos**.
            - Motoristas: **problemas relacionados ao cliente**.
            - Sugere necessidade de melhorias em geolocalização e confirmação de embarque.
            """)

        with st.expander("Picos de Demanda"):
            st.write("""
            - Horário de pico: **17h às 19h**, com maior concentração às 18h.
            - Meses mais movimentados: **Janeiro, Novembro e Dezembro**.
            - Indica sazonalidade e padrões de mobilidade urbana.
            """)

        with st.expander("Métodos de Pagamento e Origem das Corridas"):
            st.write("""
            - Pagamentos mais comuns: **UPI** e **dinheiro**.
            - Local com mais corridas: **Khandsa**.
            - Mostra coexistência de meios digitais e tradicionais e consistência nos pontos de origem.
            """)

        with st.expander("Valor da Corrida vs Distância"):
            st.write("""
            - **Correlação fraca** entre distância e valor.
            - Presença de viagens curtas com valores altos.
            - Outros fatores (demanda, localização, horário) impactam o preço.
            """)

        with st.expander("Distância Média: Completadas vs Canceladas"):
            st.write("""
            - **Teste T de duas amostras independentes**
            - Estatística T: 91.93 | Valor-p: 0.0000
            - **Rejeita-se H₀**, confirmando diferença significativa.
            - Corridas mais longas possuem maior taxa de conclusão.
            """)

    # Pagina de Resposta as Perguntas
    with tab_perguntas:
        st.header("Respostas Analíticas às Perguntas ❓")
        
        tabs = st.tabs([
            "1️⃣ Horários de Pico", 
            "2️⃣ Motivos de Cancelamento", 
            "3️⃣ Formas de Pagamento", 
            "4️⃣ Valor vs Distância", 
            "5️⃣ Distância Média", 
            "6️⃣ Fatores do Valor"
        ])

        # Horários de Pico
        with tabs[0]:
            st.write("""
            O **horário de maior demanda** ocorre por volta das **18h**, dentro do intervalo de 17h às 19h. 
            Essa tendência está associada ao aumento da mobilidade urbana pós-expediente, devendo ser considerada para otimização de frota e estratégias operacionais.
            """)

        # Motivos de Cancelamento
        with tabs[1]:
            st.write("""
            - Clientes cancelam principalmente por **endereços incorretos**.
            - Motoristas cancelam por **problemas relacionados ao cliente**.
            - Indica necessidade de **melhoria na comunicação e geolocalização**.
            """)

        # Formas de Pagamento
        with tabs[2]:
            st.write("""
            - **UPI (Unified Payments Interface)** e **Dinheiro** são predominantes.
            - Reflete coexistência entre meios digitais e físicos, exigindo flexibilidade nos pagamentos.
            """)

        # Valor vs Distância
        with tabs[3]:
            st.write("""
            - **Correlação fraca** entre distância percorrida e valor.
            - Outliers indicam viagens curtas com preços elevados.
            - Fatores como **demanda, horário e localização** influenciam o valor.
            """)

        # Distância Média
        with tabs[4]:
            st.write("""
            - **Teste T:** estatística T = 91.93, valor-p = 0.0000
            - Distâncias de viagens completadas são significativamente maiores que das canceladas.
            - Implica que corridas mais longas têm maior chance de conclusão.
            """)

        # Fatores do Valor
        with tabs[5]:
            st.write("""
            - Valores das viagens **não se baseiam apenas na distância**.
            - **Horário, demanda, localização e tipo de veículo** impactam fortemente o preço.
            - Sistema de tarifação é multifatorial, exigindo maior clareza para percepção de justiça nos preços.
            """)