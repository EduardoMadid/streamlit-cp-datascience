import streamlit as st

st.set_page_config(
    page_title="Home",
    layout="wide"
)

# =====================
# Dicionário de Tecnologias
# =====================
TECNOLOGIAS = {
    "MySQL": "🐬 MySQL",
    "Python": "🐍 Python",
    "SQLite": "💾 SQLite",
    "Chatbot": "🤖 Chatbot",
}

# =====================
# Função: Mostrar Certificados em Cards
# =====================
def mostrar_certificados(certificados):

    # Opções de tecnologias
    todas_tecnologias = list(TECNOLOGIAS.keys())

    # Multiselect com "Todas" como default
    tecnologias_escolhidas = st.multiselect(
        "🔧 Escolha as tecnologias:",
        todas_tecnologias,
    )

    # Lógica do filtro
    if not tecnologias_escolhidas:
        certificados_filtrados = certificados
    else:
        certificados_filtrados = [
            c for c in certificados 
            if any(t in tecnologias_escolhidas for t in c["tecnologias"])
        ]

    # Renderizar em formato de cards
    if certificados_filtrados:
        cols = st.columns(2)  # 2 cards por linha

        for idx, cert in enumerate(certificados_filtrados):
            with cols[idx % 2]:
                with st.container(border=True):
                    st.subheader(cert['titulo'])
                    st.write(f"🏫 **Instituição:** {cert['instituicao']}")
                    st.write(f"📅 **Data:** {cert['data']}")
                    st.write(f"⏱️ **Duração:** {cert['duracao']}")
                    lista_tec = ", ".join([TECNOLOGIAS[t] for t in cert["tecnologias"]])
                    st.write(f"🔧 **Tecnologias:** {lista_tec}")
                    if cert['imagem']:
                        st.image(cert["imagem"], caption=cert["titulo"], use_container_width=True)
                    
    else:
        st.info("Nenhum certificado encontrado para as tecnologias selecionadas.")

st.logo('assets/logo_uber.png', size="large", link='https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard')

home, exp, skills = st.tabs(['Home', 'Formação e Experiência', 'Skills'])

with home:
    st.markdown("<h1>👋 Olá, sou Eduardo Madid!</h1>", unsafe_allow_html=True)

    # Métricas de destaque no topo
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="🎯 Idade",
            value="19 anos",
            delta="Jovem e motivado"
        )
    
    with col2:
        st.metric(
            label="📚 Formação",
            value="Engenharia de Software",
            delta="FIAP"
        )

    st.markdown("---")

    col1, col2 = st.columns([40,60])
    with col1:
        st.header("🌟 Sobre Mim: ")
        st.markdown("""
        Olá! Sou Eduardo Madid, um entusiasta de tecnologia e inovação de 19 anos. Desde muito jovem, minha curiosidade me impulsiona a explorar, aprender e me aprofundar em tudo o que o vasto universo da tecnologia tem a oferecer.
        """)
        
        # Badges de destaque
        st.markdown("### 🏅 Destaques")
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            st.success("🎯 Focado")
        with col_b2:
            st.info("🚀 Inovador")
        with col_b3:
            st.warning("📈 Crescimento")
    
    
    with col2:
        st.header("🎯 Meu Objetivo Profissional")
        st.markdown("""
        Acredito que o aprendizado é uma jornada contínua e sou incansavelmente motivado por novos desafios. Com uma mente sempre aberta a novas soluções, busco oportunidades para aplicar meu entusiasmo e minhas habilidades em projetos que não apenas inovem, mas também gerem um impacto real. Meu objetivo é contribuir para o desenvolvimento de soluções criativas e eficientes, enquanto continuo a expandir meus conhecimentos e a crescer profissionalmente no dinâmico mundo da tecnologia.
        """)

    st.markdown("---")

    st.header("💼 O que você encontrará neste Projeto")
    
    st.markdown("""
    Um dashboard interativo e informativo, desenvolvido para demonstrar minhas habilidades em análise de dados e visualização. Um dataset público do Kaggle pertencente à Uber, que contém informações detalhadas sobre viagens, incluindo horários, localizações e outras métricas relevantes de corridas na Índia:
    
    - **Análise e Exploração de Dados:** Métodos de limpeza, tratamento e exploração para garantir a qualidade e a confiabilidade dos dados.
    - **Visualização Impactante:** Construção de dashboards e relatórios dinâmicos que comunicam descobertas de forma clara e envolvente.
    - **Análise Estatística:** Aplicação de conceitos estatísticos para validar hipóteses e extrair conclusões significativas.
    """)
    
    # Links de contato em cards
    st.markdown("### 📞 Vamos Conectar?")
    col_l1, col_l2, col_l3 = st.columns(3)
    
    with col_l1:
        st.link_button("🔗 LinkedIn", "https://www.linkedin.com/in/eduardo-madid-10aa862b6/", use_container_width=True)
    
    with col_l2:
        st.link_button("📧 Email", "mailto:dumadid2@gmail.com", use_container_width=True)
    
    with col_l3:
        st.link_button("🐙 GitHub", "https://github.com/EduardoMadid", use_container_width=True)

with exp:
    st.header("📚 Formação e Experiência Sobre o Projeto")
    
    # =====================
    # Dados dos Certificados
    # =====================
    certificados = [
        {
            "titulo": "MySQL e JSON",
            "instituicao": "Alura",
            "data": "18 de Agosto de 2025",
            "duracao": "12 horas",
            "tecnologias": ["MySQL"],
            "imagem": "assets/mysql_json.png",
            "link": "https://on.fiap.com.br/pluginfile.php/1/local_nanocourses/certificado_nanocourse/114536/b81b9571057f832a17116778992a703b/certificado.png"
        },
        {
            "titulo": "Python",
            "instituicao": "FIAP", 
            "data": "5 de junho de 2024",
            "duracao": "80 horas",
            "tecnologias": ["Python"],
            "imagem": "assets/python_fiap.png",
            "link": "https://on.fiap.com.br/pluginfile.php/1/local_nanocourses/certificado_nanocourse/114536/b81b9571057f832a17116778992a703b/certificado.png"
        },
        {
            "titulo": "SQLite",
            "instituicao": "Alura",
            "data": "14 de Maio de 2024", 
            "duracao": "8 horas",
            "tecnologias": ["SQLite"],
            "imagem": "assets/sqlite.png",
            "link": "https://on.fiap.com.br/pluginfile.php/1/local_nanocourses/certificado_nanocourse/114536/b81b9571057f832a17116778992a703b/certificado.png"
        },
        {
            "titulo": "Chatbot",
            "instituicao": "FIAP",
            "data": "13 de Março de 2025",
            "duracao": "60 horas", 
            "tecnologias": ["Chatbot"],
            "imagem": "assets/chatbot.png",
            "link": "https://on.fiap.com.br/pluginfile.php/1/local_nanocourses/certificado_nanocourse/114536/b81b9571057f832a17116778992a703b/certificado.png"
        }
    ]
    
    # Mostrar certificados com filtros
    mostrar_certificados(certificados)
    
    st.markdown("---")
    
    # Seção de Formação Acadêmica
    st.subheader("🎓 Formação Acadêmica")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📚 Curso",
            value="Engenharia de Software",
            delta="FIAP"
        )
    
    with col2:
        st.metric(
            label="📅 Período",
            value="2024 - 2028",
            delta="Em andamento"
        )
    
    with col3:
        st.metric(
            label="📊 Progresso",
            value="46%",
            delta="2º Semestre"
        )
    
    with col4:
        st.metric(
            label="🎯 Status",
            value="Ativo",
            delta="Cursando"
        )
    
    # Progress bar fixa em 46%
    st.progress(0.46)
    st.caption("Progresso atual: 46% - 2º Semestre")
    
    st.markdown("---")
    
    # Seção de Experiência Profissional
    st.subheader("💼 Experiência Profissional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="🏢 CANIS",
            value="Administrador Geral",
            delta="01/06/2023 - 01/06/2024"
        )
        st.caption("📍 SP, São Paulo")
        st.info("Administrava todo o fluxo operacional da empresa, cuidando de despesas e gastos, até do próprio sistema utilizado pela empresa.")
    
    with col2:
        st.metric(
            label="🏢 THM",
            value="Estagiário",
            delta="18/04/2025 - Atual"
        )
        st.caption("📍 SP, São Paulo")
        st.info("Aplicações de IA com LangChain, Streamlit, e outros projetos interessantes.")

with skills:
    st.header("💻 Skills e Competências")
    
    # Métricas de skills
    col_metrics = st.columns(4)
    with col_metrics[0]:
        st.metric("🛠️ Hard Skills", "15+", "Tecnologias")
    with col_metrics[1]:
        st.metric("🌟 Soft Skills", "6+", "Competências")
    with col_metrics[2]:
        st.metric("📚 Aprendizado", "∞", "Sempre evoluindo")
    with col_metrics[3]:
        st.metric("🎯 Foco", "Inovação", "Desenvolvimento")
    
    st.markdown("---")
    
    # Hard Skills com tabs
    st.subheader("🛠️ Tecnologias, Ferramentas e Hard Skills")
    
    tab1, tab2, tab3 = st.tabs(["💻 Frontend", "⚙️ Backend/DB", "🛠️ Ferramentas"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - 🌐 HTML
            - 🎨 CSS
            - ⚡ JavaScript
            - 🎨 Tailwind
            - ⚛️ Next.js
            """)
        with col2:
            st.markdown("""
            - 🎨 Blender / 3D Modelling
            - 💡 Design Thinking
            - 📱 UI/UX
            - 🎯 Responsive Design
            """)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - 🐍 Python
            - ☕ Java
            - 🔵 C
            - 🟢 Node.js
            """)
        with col2:
            st.markdown("""
            - 🗄️ SQL e SQLite
            - 🐬 MySQL
            - 🔥 Firebase
            - 🔗 LangChain
            """)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - 📝 Git e GitHub
            - 📊 Agile Methodology
            - 🤖 Chatbots
            - 🔌 IoT
            """)
        with col2:
            st.markdown("""
            - 🔧 Hardware
            - 🧠 Lógica de Programação
            - 📈 Análise de Dados
            - 🎨 Streamlit
            """)
    
    st.markdown("---")
    
    # Soft Skills com progress bars coloridas
    st.subheader("🌟 Soft Skills")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💬 Comunicação e Trabalho em Equipe")
        
        # Progress bars com cores diferentes
        st.markdown("**💬 Comunicação** - Clara e eficaz")
        st.markdown("""
        <div style="background-color: #000000; padding: 8px; border-radius: 6px; margin-bottom: 15px;">
            <div style="background: linear-gradient(90deg, #28a745 0%, #20c997 100%); width: 95%; height: 20px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">
                95% - Excelente
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**👥 Trabalho em Equipe** - Colaborativo")
        st.markdown("""
        <div style="background-color: #000000; padding: 8px; border-radius: 6px; margin-bottom: 15px;">
            <div style="background: linear-gradient(90deg, #17a2b8 0%, #6f42c1 100%); width: 85%; height: 20px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">
                85% - Muito Bom
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**🎯 Liderança** - Em situações desafiadoras")
        st.markdown("""
        <div style="background-color: #000000; padding: 8px; border-radius: 6px; margin-bottom: 15px;">
            <div style="background: linear-gradient(90deg, #ffc107 0%, #fd7e14 100%); width: 75%; height: 20px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">
                75% - Bom
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**🤝 Relacionamento** - Interpessoal")
        st.markdown("""
        <div style="background-color: #000000; padding: 8px; border-radius: 6px; margin-bottom: 15px;">
            <div style="background: linear-gradient(90deg, #28a745 0%, #20c997 100%); width: 90%; height: 20px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">
                90% - Excelente
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🧠 Desenvolvimento Pessoal")
        
        # Progress bars com cores diferentes
        st.markdown("**🧠 Flexibilidade** - Mente aberta")
        st.markdown("""
        <div style="background-color: #000000; padding: 8px; border-radius: 6px; margin-bottom: 15px;">
            <div style="background: linear-gradient(90deg, #28a745 0%, #20c997 100%); width: 95%; height: 20px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">
                95% - Excelente
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**🌍 Inglês** - Avançado")
        st.markdown("""
        <div style="background-color: #000000; padding: 8px; border-radius: 6px; margin-bottom: 15px;">
            <div style="background: linear-gradient(90deg, #28a745 0%, #20c997 100%); width: 88%; height: 20px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">
                88% - Fluente
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**⚡ Resiliência** - Sob pressão")
        st.markdown("""
        <div style="background-color: #000000; padding: 8px; border-radius: 6px; margin-bottom: 15px;">
            <div style="background: linear-gradient(90deg, #17a2b8 0%, #6f42c1 100%); width: 82%; height: 20px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">
                82% - Muito Bom
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**📚 Aprendizado** - Sempre evoluindo")
        st.markdown("""
        <div style="background-color: #000000; padding: 8px; border-radius: 6px; margin-bottom: 15px;">
            <div style="background: linear-gradient(90deg, #6f42c1 0%, #e83e8c 100%); width: 100%; height: 20px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">
                100% - Contínuo
            </div>
        </div>
        """, unsafe_allow_html=True)
    