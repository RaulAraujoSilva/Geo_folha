# Sistema de Auditoria de Ponto Geolocalizado

Sistema web para auditoria de registros de ponto de colaboradores, verificando se estão dentro do raio permitido da sede da empresa.

## Funcionalidades

- Upload de arquivos XLSX exportados do sistema de ponto
- Processamento automático de dados com limpeza e validação
- Cálculo de distância geográfica usando fórmula de Haversine
- Análise de conformidade com raio de 5km da sede
- Visualizações interativas com gráficos Plotly
- Relatórios detalhados por colaborador e data
- Múltiplas opções de download (CSV completo, não conformes, relatório TXT)

## Tecnologias

- **Python 3.11+**
- **Streamlit** - Framework web para dados
- **Pandas** - Manipulação de dados
- **Plotly** - Gráficos interativos
- **OpenPyXL** - Leitura de arquivos Excel

## Instalação Local

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/auditoria-ponto-bap.git
cd auditoria-ponto-bap

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run app.py
```

Acesse em: http://localhost:8501

## Deploy na Web

Acesse o arquivo [README_DEPLOY.md](README_DEPLOY.md) para instruções completas de como fazer deploy no Streamlit Cloud.

## Como Usar

### 1. Upload do Arquivo
- Faça upload do arquivo XLSX exportado do sistema de ponto
- O sistema detecta automaticamente a estrutura e processa os dados

### 2. Visualizar Dados Processados
- Veja prévia dos dados limpos e estruturados
- Estatísticas gerais: total de registros, colaboradores, empresas, dias
- Baixe o CSV processado se necessário

### 3. Análise de Conformidade
- Calcule as distâncias automaticamente
- Visualize métricas de conformidade
- Explore gráficos interativos:
  - Visão geral (pizza e barras)
  - Por colaborador (ranking)
  - Por data (série temporal)
  - Dados completos (tabela filtrada)
- Baixe relatórios em diferentes formatos

## Configurações

A sede da empresa está configurada em:
- **Latitude**: -22.905121000896163
- **Longitude**: -43.177319803886164
- **Raio permitido**: 5 km

Para alterar, edite as constantes no arquivo `app.py`:

```python
LAT_SEDE = -22.905121000896163
LON_SEDE = -43.177319803886164
RAIO_KM = 5.0
```

## Estrutura do Arquivo de Entrada

O sistema espera arquivos XLSX com a seguinte estrutura:
- Cabeçalhos com informações de EMPRESA, DEPARTAMENTO, NOME
- Colunas de dados: DATA (col 0), HORA (col 3), LATITUDE (col 5), LONGITUDE (col 7), PRECISÃO (col 10), LOGRADOURO (col 12)
- Células mescladas são tratadas automaticamente

## Desenvolvimento

### Scripts CLI Disponíveis

- `processar_ponto.py` - Processa XLSX para CSV limpo
- `calcular_distancia.py` - Calcula distâncias e gera relatórios

### Estrutura do Projeto

```
.
├── app.py                    # Aplicação Streamlit principal
├── processar_ponto.py        # Script de processamento
├── calcular_distancia.py     # Script de cálculo de distâncias
├── requirements.txt          # Dependências Python
├── .streamlit/
│   └── config.toml          # Configurações do Streamlit
├── .gitignore               # Arquivos ignorados pelo Git
├── README.md                # Este arquivo
├── README_DEPLOY.md         # Guia de deploy
└── DESCRICAO_INTERFACE.md   # Documentação da interface
```

## Segurança

- Arquivos de dados (.xlsx, .xls, .csv) não são commitados no Git
- Use repositório privado no GitHub para código sensível
- Considere adicionar autenticação para deploy em produção
- HTTPS é fornecido automaticamente pelo Streamlit Cloud

## Licença

Uso interno - BAP Administração de Bens LTDA

## Suporte

Para problemas ou dúvidas, consulte:
- [Documentação do Streamlit](https://docs.streamlit.io/)
- [README_DEPLOY.md](README_DEPLOY.md) para questões de deployment

---

**Sistema de Auditoria de Ponto Geolocalizado v1.0**
BAP Administração de Bens LTDA | 2025
