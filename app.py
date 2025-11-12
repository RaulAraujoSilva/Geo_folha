import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import math

# Configuração da página
st.set_page_config(
    page_title="Auditoria de Ponto | BAP",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado - Design moderno e clean
st.markdown("""
<style>
    /* Fonte e espaçamento global */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Header */
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .main-subtitle {
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Cards de métricas */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }

    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
        line-height: 1;
    }

    .metric-subtitle {
        font-size: 0.875rem;
        color: #9ca3af;
        margin-top: 0.25rem;
    }

    /* Cores por status */
    .metric-success { border-left: 4px solid #10b981; }
    .metric-warning { border-left: 4px solid #f59e0b; }
    .metric-danger { border-left: 4px solid #ef4444; }
    .metric-info { border-left: 4px solid #3b82f6; }

    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        width: 100%;
        letter-spacing: 0.02em;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }

    /* Download buttons */
    .stDownloadButton > button {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stDownloadButton > button:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
    }

    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f9fafb 0%, #ffffff 100%);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f9fafb;
        padding: 0.5rem;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #6b7280;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
    }

    .stTabs [aria-selected="true"] {
        background: white;
        color: #667eea;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Progress steps */
    .step {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .step-active {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 3px solid #667eea;
    }

    .step-completed {
        background: #f0fdf4;
        border-left: 3px solid #10b981;
    }

    .step-number {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.875rem;
        margin-right: 0.75rem;
    }

    .step-number-active {
        background: #667eea;
        color: white;
    }

    .step-number-completed {
        background: #10b981;
        color: white;
    }

    .step-number-pending {
        background: #e5e7eb;
        color: #9ca3af;
    }

    /* File uploader */
    .stFileUploader {
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 2rem;
        background: #fafafa;
        transition: all 0.3s ease;
    }

    .stFileUploader:hover {
        border-color: #667eea;
        background: #f5f7ff;
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Section dividers */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Funções auxiliares (mantidas da versão original)
def haversine(lat1, lon1, lat2, lon2):
    """Calcula a distância entre dois pontos usando Haversine"""
    R = 6371.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def processar_arquivo_ponto(df_excel):
    """Processa o arquivo Excel e retorna DataFrame limpo"""
    registros = []
    empresa = None
    departamento = None
    nome = None
    num_folha = None
    funcao = None

    i = 0
    while i < len(df_excel):
        linha = df_excel.iloc[i]

        if pd.notna(linha[0]) and 'EMPRESA:' in str(linha[0]):
            if i > 0:
                linha_anterior = df_excel.iloc[i-1]
                for col_idx in range(len(linha_anterior)):
                    if pd.notna(linha_anterior[col_idx]) and str(linha_anterior[col_idx]).strip():
                        empresa = str(linha_anterior[col_idx]).strip()
                        break

        elif pd.notna(linha[0]) and 'DEPARTAMENTO:' in str(linha[0]):
            for col_idx in range(len(linha)):
                if pd.notna(linha[col_idx]) and str(linha[col_idx]).strip() and 'DEPARTAMENTO:' not in str(linha[col_idx]):
                    departamento = str(linha[col_idx]).strip()
                    break

        elif pd.notna(linha[0]) and 'NOME:' in str(linha[0]):
            for col_idx in range(len(linha)):
                val = str(linha[col_idx]) if pd.notna(linha[col_idx]) else ''
                if 'NOME:' in val or 'FOLHA:' in val or 'FUNÇÃO' in val or 'FUNCAO' in val:
                    continue
                elif val.strip() and nome is None and not val.replace('.', '').replace(',', '').isdigit():
                    nome = val.strip()
                elif val.strip() and val.replace('.', '').replace(',', '').isdigit():
                    num_folha = val.strip().replace('.0', '')
                elif val.strip() and nome is not None and num_folha is not None and funcao is None:
                    funcao = val.strip()

        elif pd.notna(linha[0]) and 'DATA' in str(linha[0]) and pd.notna(linha[3]) and 'HORA' in str(linha[3]):
            i += 1
            while i < len(df_excel):
                linha_dados = df_excel.iloc[i]
                if pd.notna(linha_dados[0]) and ('EMPRESA:' in str(linha_dados[0]) or 'NOME:' in str(linha_dados[0])):
                    i -= 1
                    nome = None
                    num_folha = None
                    funcao = None
                    break

                if pd.notna(linha_dados[0]):
                    data_hora_raw = str(linha_dados[0])
                    if 'secullum' in data_hora_raw.lower() or 'www.' in data_hora_raw.lower():
                        i += 1
                        continue

                    try:
                        import re
                        data_hora = data_hora_raw
                        hora = str(linha_dados[3]) if pd.notna(linha_dados[3]) else None
                        latitude_str = str(linha_dados[5]) if pd.notna(linha_dados[5]) else None
                        longitude_str = str(linha_dados[7]) if pd.notna(linha_dados[7]) else None
                        precisao_str = str(linha_dados[10]) if pd.notna(linha_dados[10]) else None
                        logradouro = str(linha_dados[12]) if pd.notna(linha_dados[12]) else None

                        latitude = float(latitude_str.replace(',', '.')) if latitude_str else None
                        longitude = float(longitude_str.replace(',', '.')) if longitude_str else None
                        precisao = float(precisao_str.replace(',', '.')) if precisao_str else None

                        match_data = re.search(r'(\d{2}/\d{2}/\d{4})', data_hora)
                        data = match_data.group(1) if match_data else data_hora

                        if not re.match(r'^\d{2}/\d{2}/\d{4}$', data):
                            i += 1
                            continue

                        registros.append({
                            'empresa': empresa,
                            'departamento': departamento,
                            'nome': nome,
                            'num_folha': num_folha,
                            'funcao': funcao,
                            'data': data,
                            'hora': hora,
                            'latitude': latitude,
                            'longitude': longitude,
                            'precisao': precisao,
                            'logradouro': logradouro
                        })
                    except (ValueError, IndexError, AttributeError):
                        pass

                i += 1
                if i >= len(df_excel):
                    break
        i += 1

    return pd.DataFrame(registros)

def calcular_distancias(df, lat_sede, lon_sede):
    """Calcula distâncias e adiciona colunas ao DataFrame"""
    distancias = []
    for _, row in df.iterrows():
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):
            dist = haversine(row['latitude'], row['longitude'], lat_sede, lon_sede)
            distancias.append(round(dist, 3))
        else:
            distancias.append(None)

    df['distancia_sede_km'] = distancias
    df['dentro_raio_5km'] = df['distancia_sede_km'].apply(lambda x: 'SIM' if pd.notna(x) and x <= 5.0 else 'NAO')
    return df

def gerar_relatorio_txt(df):
    """Gera relatório em formato texto"""
    fora_raio = df[df['dentro_raio_5km'] == 'NAO']
    relatorio = []
    relatorio.append("="*80)
    relatorio.append("RELATORIO DE AUDITORIA - REGISTROS DE PONTO")
    relatorio.append("="*80)
    relatorio.append(f"\nData de Geracao: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    relatorio.append(f"\n1. RESUMO EXECUTIVO")
    relatorio.append(f"   Total de registros: {len(df)}")
    relatorio.append(f"   Dentro do raio: {len(df[df['dentro_raio_5km'] == 'SIM'])} ({len(df[df['dentro_raio_5km'] == 'SIM'])/len(df)*100:.1f}%)")
    relatorio.append(f"   Fora do raio: {len(fora_raio)} ({len(fora_raio)/len(df)*100:.1f}%)")

    if len(fora_raio) > 0:
        relatorio.append(f"\n2. COLABORADORES COM REGISTROS FORA DO RAIO")
        relatorio.append("="*80)
        colaboradores = fora_raio.groupby('nome').agg({
            'distancia_sede_km': ['count', 'min', 'max', 'mean']
        }).round(2)
        colaboradores.columns = ['Qtd', 'Min_km', 'Max_km', 'Media_km']
        colaboradores = colaboradores.sort_values('Max_km', ascending=False)

        for nome, row in colaboradores.iterrows():
            relatorio.append(f"\n{nome}")
            relatorio.append(f"  Registros fora: {int(row['Qtd'])}")
            relatorio.append(f"  Distancia min: {row['Min_km']:.2f} km")
            relatorio.append(f"  Distancia max: {row['Max_km']:.2f} km")
            relatorio.append(f"  Distancia media: {row['Media_km']:.2f} km")

    relatorio.append(f"\n3. ESTATISTICAS GERAIS")
    relatorio.append("="*80)
    relatorio.append(f"Distancia minima: {df['distancia_sede_km'].min():.3f} km")
    relatorio.append(f"Distancia maxima: {df['distancia_sede_km'].max():.3f} km")
    relatorio.append(f"Distancia media: {df['distancia_sede_km'].mean():.3f} km")
    relatorio.append("\n" + "="*80)
    relatorio.append("FIM DO RELATORIO")
    relatorio.append("="*80)

    return "\n".join(relatorio)

# Inicializar session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'df_processado' not in st.session_state:
    st.session_state.df_processado = None
if 'df_com_distancia' not in st.session_state:
    st.session_state.df_com_distancia = None

# Sidebar
with st.sidebar:
    st.markdown('<div style="padding: 1rem 0; border-bottom: 1px solid #e5e7eb; margin-bottom: 1.5rem;"><h2 style="margin: 0; font-size: 1.25rem; font-weight: 600;">BAP Administração</h2><p style="margin: 0.25rem 0 0 0; color: #6b7280; font-size: 0.875rem;">Sistema de Auditoria de Ponto</p></div>', unsafe_allow_html=True)

    st.markdown("#### Etapas do Processo")

    steps = [
        ("1", "Upload do Arquivo", st.session_state.step >= 1),
        ("2", "Processamento", st.session_state.step >= 2),
        ("3", "Análise e Relatórios", st.session_state.step >= 3)
    ]

    for num, label, active in steps:
        is_completed = (num == "1" and st.session_state.step > 1) or (num == "2" and st.session_state.step > 2)
        is_active = (num == "1" and st.session_state.step == 1) or (num == "2" and st.session_state.step == 2) or (num == "3" and st.session_state.step == 3)

        step_class = "step-completed" if is_completed else ("step-active" if is_active else "")
        number_class = "step-number-completed" if is_completed else ("step-number-active" if is_active else "step-number-pending")

        st.markdown(f'<div class="step {step_class}"><div class="step-number {number_class}">{num}</div><div style="font-size: 0.875rem; font-weight: 500; color: {"#1a1a1a" if (is_active or is_completed) else "#9ca3af"};">{label}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("#### Configurações da Sede")
    st.markdown("""
    <div style="font-size: 0.875rem; color: #6b7280; line-height: 1.6;">
        <strong>Latitude:</strong> -22.905121<br>
        <strong>Longitude:</strong> -43.177320<br>
        <strong>Raio Permitido:</strong> 5 km
    </div>
    """, unsafe_allow_html=True)

# Header principal
st.markdown('<h1 class="main-header">Auditoria de Ponto Geolocalizado</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Sistema de análise e conformidade de registros de ponto</p>', unsafe_allow_html=True)

# ETAPA 1: Upload de Arquivo
if st.session_state.step == 1:
    st.markdown("### Carregar Arquivo")
    st.markdown("Faça upload do arquivo XLSX exportado do sistema de ponto para iniciar a análise.")

    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Selecione o arquivo XLSX",
        type=['xlsx', 'xls'],
        help="Arquivo exportado do sistema de ponto",
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        with st.spinner('Processando arquivo...'):
            try:
                df_excel = pd.read_excel(uploaded_file, header=None)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                    <div class="metric-card metric-info">
                        <div class="metric-label">Total de Linhas</div>
                        <div class="metric-value">{len(df_excel):,}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="metric-card metric-info">
                        <div class="metric-label">Total de Colunas</div>
                        <div class="metric-value">{len(df_excel.columns)}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    <div class="metric-card metric-info">
                        <div class="metric-label">Tamanho do Arquivo</div>
                        <div class="metric-value">{uploaded_file.size / 1024:.1f}</div>
                        <div class="metric-subtitle">KB</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

                if st.button("Processar Arquivo", type="primary", use_container_width=True):
                    with st.spinner('Processando dados...'):
                        df_processado = processar_arquivo_ponto(df_excel)

                        if len(df_processado) > 0:
                            st.session_state.df_processado = df_processado
                            st.session_state.step = 2
                            st.rerun()
                        else:
                            st.error("Nenhum registro foi processado. Verifique o formato do arquivo.")

            except Exception as e:
                st.error(f"Erro ao processar arquivo: {str(e)}")

# ETAPA 2: Visualização dos dados processados
elif st.session_state.step == 2:
    df = st.session_state.df_processado

    st.markdown("### Dados Processados")
    st.markdown("Visualize os dados extraídos e faça o download do CSV processado antes de continuar.")

    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card metric-info">
            <div class="metric-label">Total de Registros</div>
            <div class="metric-value">{len(df):,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card metric-info">
            <div class="metric-label">Colaboradores</div>
            <div class="metric-value">{df['nome'].nunique()}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card metric-info">
            <div class="metric-label">Empresas</div>
            <div class="metric-value">{df['empresa'].nunique()}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card metric-info">
            <div class="metric-label">Dias Analisados</div>
            <div class="metric-value">{df['data'].nunique()}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("#### Prévia dos Dados")
    st.dataframe(df.head(10), use_container_width=True, height=350)

    with st.expander("Informações Detalhadas"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Empresa:** {df['empresa'].unique()[0] if len(df['empresa'].unique()) > 0 else 'N/A'}")
            st.markdown(f"**Departamento:** {df['departamento'].unique()[0] if len(df['departamento'].unique()) > 0 else 'N/A'}")
            st.markdown(f"**Período:** {df['data'].min()} a {df['data'].max()}")

        with col2:
            st.markdown(f"**Colunas:** {len(df.columns)}")
            st.markdown("**Colaboradores:**")
            for i, nome in enumerate(df['nome'].unique()[:5]):
                st.markdown(f"• {nome}")
            if df['nome'].nunique() > 5:
                st.markdown(f"*... e mais {df['nome'].nunique() - 5} colaboradores*")

    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="Baixar CSV Processado",
            data=csv,
            file_name=f"dados_processados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        if st.button("Calcular Distâncias", type="primary", use_container_width=True):
            with st.spinner('Calculando distâncias...'):
                LAT_SEDE = -22.905121000896163
                LON_SEDE = -43.177319803886164
                df_com_dist = calcular_distancias(df.copy(), LAT_SEDE, LON_SEDE)
                st.session_state.df_com_distancia = df_com_dist
                st.session_state.step = 3
                st.rerun()

# ETAPA 3: Análise e Relatórios
elif st.session_state.step == 3:
    df = st.session_state.df_com_distancia

    st.markdown("### Análise de Conformidade")
    st.markdown("Resultados da análise de distância dos registros em relação à sede da empresa.")

    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

    total = len(df)
    dentro = len(df[df['dentro_raio_5km'] == 'SIM'])
    fora = len(df[df['dentro_raio_5km'] == 'NAO'])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card metric-info">
            <div class="metric-label">Total de Registros</div>
            <div class="metric-value">{total:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card metric-success">
            <div class="metric-label">Conformes</div>
            <div class="metric-value">{dentro:,}</div>
            <div class="metric-subtitle">{dentro/total*100:.1f}% do total</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card metric-danger">
            <div class="metric-label">Não Conformes</div>
            <div class="metric-value">{fora:,}</div>
            <div class="metric-subtitle">{fora/total*100:.1f}% do total</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card metric-warning">
            <div class="metric-label">Distância Média</div>
            <div class="metric-value">{df['distancia_sede_km'].mean():.2f}</div>
            <div class="metric-subtitle">km da sede</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Por Colaborador", "Por Data", "Dados Completos"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            fig_pizza = go.Figure(data=[go.Pie(
                labels=['Dentro do Raio (≤5km)', 'Fora do Raio (>5km)'],
                values=[dentro, fora],
                hole=.4,
                marker_colors=['#10b981', '#ef4444'],
                textinfo='label+percent',
                textfont=dict(size=14, family='Inter')
            )])
            fig_pizza.update_layout(
                title="Conformidade dos Registros",
                height=400,
                font=dict(family='Inter')
            )
            st.plotly_chart(fig_pizza, use_container_width=True)

        with col2:
            faixas = pd.cut(df['distancia_sede_km'], bins=[0, 1, 2, 5, 10, 100], labels=['0-1km', '1-2km', '2-5km', '5-10km', '>10km'])
            dist_faixas = faixas.value_counts().sort_index()

            fig_barras = go.Figure(data=[go.Bar(
                x=dist_faixas.index,
                y=dist_faixas.values,
                marker_color=['#10b981', '#6ee7b7', '#fbbf24', '#fb923c', '#ef4444'],
                text=dist_faixas.values,
                textposition='outside',
                textfont=dict(size=14, family='Inter')
            )])
            fig_barras.update_layout(
                title="Distribuição por Faixa de Distância",
                xaxis_title="Faixa de Distância",
                yaxis_title="Quantidade de Registros",
                height=400,
                font=dict(family='Inter')
            )
            st.plotly_chart(fig_barras, use_container_width=True)

    with tab2:
        fora_raio = df[df['dentro_raio_5km'] == 'NAO']

        if len(fora_raio) > 0:
            colaboradores = fora_raio.groupby('nome').agg({
                'distancia_sede_km': ['count', 'max']
            }).round(2)
            colaboradores.columns = ['Qtd_Registros', 'Dist_Max_km']
            colaboradores = colaboradores.sort_values('Dist_Max_km', ascending=False).reset_index()

            fig_colab = px.bar(
                colaboradores,
                x='nome',
                y='Qtd_Registros',
                color='Dist_Max_km',
                title="Colaboradores com Registros Não Conformes",
                labels={'nome': 'Colaborador', 'Qtd_Registros': 'Quantidade', 'Dist_Max_km': 'Dist. Máxima (km)'},
                color_continuous_scale='Reds',
                text='Qtd_Registros'
            )
            fig_colab.update_xaxes(tickangle=-45)
            fig_colab.update_traces(textposition='outside')
            fig_colab.update_layout(font=dict(family='Inter'), height=500)
            st.plotly_chart(fig_colab, use_container_width=True)

            st.markdown("#### Detalhamento por Colaborador")
            st.dataframe(colaboradores, use_container_width=True, height=400)
        else:
            st.success("Todos os colaboradores estão conformes!")

    with tab3:
        por_data = df.groupby(['data', 'dentro_raio_5km']).size().reset_index(name='count')

        fig_data = px.bar(
            por_data,
            x='data',
            y='count',
            color='dentro_raio_5km',
            title="Registros por Data",
            labels={'data': 'Data', 'count': 'Quantidade', 'dentro_raio_5km': 'Status'},
            color_discrete_map={'SIM': '#10b981', 'NAO': '#ef4444'},
            barmode='stack',
            text='count'
        )
        fig_data.update_traces(textposition='inside')
        fig_data.update_layout(font=dict(family='Inter'), height=400)
        st.plotly_chart(fig_data, use_container_width=True)

        st.markdown("#### Estatísticas por Data")
        stats_data = df.groupby('data').agg({
            'distancia_sede_km': ['count', 'mean', 'max']
        }).round(2)
        stats_data.columns = ['Total', 'Média (km)', 'Máxima (km)']
        st.dataframe(stats_data, use_container_width=True)

    with tab4:
        st.markdown("#### Filtros")

        col1, col2, col3 = st.columns(3)

        with col1:
            filtro_status = st.selectbox("Status", ["Todos", "Dentro do Raio", "Fora do Raio"])

        with col2:
            filtro_colab = st.selectbox("Colaborador", ["Todos"] + sorted(df['nome'].unique().tolist()))

        with col3:
            filtro_data = st.selectbox("Data", ["Todas"] + sorted(df['data'].unique().tolist()))

        df_filtrado = df.copy()

        if filtro_status == "Dentro do Raio":
            df_filtrado = df_filtrado[df_filtrado['dentro_raio_5km'] == 'SIM']
        elif filtro_status == "Fora do Raio":
            df_filtrado = df_filtrado[df_filtrado['dentro_raio_5km'] == 'NAO']

        if filtro_colab != "Todos":
            df_filtrado = df_filtrado[df_filtrado['nome'] == filtro_colab]

        if filtro_data != "Todas":
            df_filtrado = df_filtrado[df_filtrado['data'] == filtro_data]

        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        st.dataframe(df_filtrado, use_container_width=True, height=500)
        st.caption(f"Mostrando {len(df_filtrado):,} de {len(df):,} registros")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("### Downloads")

    col1, col2, col3 = st.columns(3)

    with col1:
        csv_completo = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="CSV Completo",
            data=csv_completo,
            file_name=f"dados_distancias_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        fora_raio = df[df['dentro_raio_5km'] == 'NAO']
        csv_nao_conformes = fora_raio.to_csv(index=False, encoding='utf-8-sig') if len(fora_raio) > 0 else ""
        st.download_button(
            label="CSV Não Conformes",
            data=csv_nao_conformes,
            file_name=f"nao_conformes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            disabled=(len(fora_raio) == 0)
        )

    with col3:
        relatorio_txt = gerar_relatorio_txt(df)
        st.download_button(
            label="Relatório TXT",
            data=relatorio_txt,
            file_name=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

    if st.button("Processar Novo Arquivo", use_container_width=True):
        st.session_state.step = 1
        st.session_state.df_processado = None
        st.session_state.df_com_distancia = None
        st.rerun()

# Footer
st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #9ca3af; padding: 2rem; font-size: 0.875rem; border-top: 1px solid #e5e7eb;'>
    <p style='margin: 0;'>Sistema de Auditoria de Ponto Geolocalizado</p>
    <p style='margin: 0.5rem 0 0 0;'>BAP Administração de Bens LTDA • 2025</p>
</div>
""", unsafe_allow_html=True)
