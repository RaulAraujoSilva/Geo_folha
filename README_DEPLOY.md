# Deploy na Web - Guia Completo

## 🚀 Deploy no Streamlit Cloud (Recomendado)

O Streamlit Cloud é a plataforma oficial e gratuita para hospedar aplicações Streamlit.

### Pré-requisitos
- Conta no [GitHub](https://github.com)
- Conta no [Streamlit Cloud](https://streamlit.io/cloud) (use sua conta do GitHub)

### Passo a Passo

#### 1. Preparar o Repositório no GitHub

1. **Criar novo repositório no GitHub:**
   - Acesse: https://github.com/new
   - Nome: `auditoria-ponto-bap`
   - Descrição: `Sistema de Auditoria de Ponto Geolocalizado`
   - Visibilidade: Privado (recomendado) ou Público
   - Clique em "Create repository"

2. **Fazer upload dos arquivos:**

   **Opção A - Via interface web do GitHub:**
   - Clique em "uploading an existing file"
   - Arraste os seguintes arquivos:
     - `app.py`
     - `requirements.txt`
     - `.streamlit/config.toml`
     - `README.md`
   - Commit: "Initial commit"

   **Opção B - Via Git (linha de comando):**
   ```bash
   cd "C:\Users\raula\OneDrive\Documentos\Codigos e sistemas pessoais\Geo_folha"

   git init
   git add app.py requirements.txt .streamlit/config.toml README.md .gitignore
   git commit -m "Initial commit: Sistema de Auditoria de Ponto"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/auditoria-ponto-bap.git
   git push -u origin main
   ```

#### 2. Deploy no Streamlit Cloud

1. **Acessar Streamlit Cloud:**
   - https://share.streamlit.io/

2. **Fazer login:**
   - Use sua conta do GitHub

3. **Criar nova app:**
   - Clique em "New app"
   - Repository: Selecione `auditoria-ponto-bap`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL (opcional): escolha um nome personalizado
   - Clique em "Deploy!"

4. **Aguardar deploy:**
   - O processo leva 2-5 minutos
   - Você verá os logs em tempo real

5. **Pronto!**
   - Sua app estará disponível em: `https://[seu-app].streamlit.app`
   - Copie e compartilhe o link

### Atualizar a Aplicação

Sempre que fizer alterações:

1. **Commit e push para o GitHub:**
   ```bash
   git add .
   git commit -m "Descrição das alterações"
   git push
   ```

2. **Atualização automática:**
   - O Streamlit Cloud detecta mudanças automaticamente
   - A app será redeployada em ~2 minutos

### Configurações Avançadas

#### Secrets (Variáveis de Ambiente)

Se precisar de configurações secretas:

1. No Streamlit Cloud, acesse sua app
2. Clique em "Settings" > "Secrets"
3. Adicione no formato TOML:
   ```toml
   LAT_SEDE = -22.905121000896163
   LON_SEDE = -43.177319803886164
   RAIO_KM = 5.0
   ```

4. No código, acesse com:
   ```python
   import streamlit as st
   LAT_SEDE = st.secrets["LAT_SEDE"]
   ```

#### Domínio Personalizado

1. No Streamlit Cloud: Settings > Custom domain
2. Configure um CNAME no seu provedor de DNS:
   - Nome: `auditoria` (ou outro)
   - Valor: `[seu-app].streamlit.app`
3. Aguarde propagação (pode levar até 48h)

---

## ⚠️ Limitações do Plano Gratuito

- **1 app privada** (ilimitadas públicas)
- **1 GB de RAM** por app
- **1 CPU compartilhada**
- **50 GB/mês de largura de banda**
- Apps hibernam após 7 dias sem uso

Para uso corporativo, considere:
- **Streamlit Cloud Team** ($250/mês)
- **Streamlit Cloud Enterprise** (preço customizado)

---

## 🐳 Alternativa: Deploy com Docker

Se preferir hospedar em seu próprio servidor:

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./app.py:/app/app.py
    restart: unless-stopped
```

### Comandos

```bash
# Build
docker build -t auditoria-ponto .

# Run
docker run -p 8501:8501 auditoria-ponto

# Ou com Docker Compose
docker-compose up -d
```

---

## 🌐 Outras Alternativas de Deploy

### 1. Heroku
- Gratuito limitado
- Fácil deploy via Git
- App dorme após 30min de inatividade

### 2. AWS Elastic Beanstalk
- Pago (a partir de ~$10/mês)
- Escalável
- Mais complexo

### 3. Google Cloud Run
- Pay-as-you-go
- Serverless
- Gratuito até certos limites

### 4. Azure App Service
- Pago (a partir de ~$13/mês)
- Integração com Microsoft
- Bom para ambientes corporativos

### 5. Seu próprio servidor (VPS)
- DigitalOcean, Linode, Vultr
- A partir de $5/mês
- Controle total

---

## 📱 Testar Antes do Deploy

```bash
# Testar localmente
streamlit run app.py

# Testar como será em produção
streamlit run app.py --server.port=8501 --server.headless=true
```

---

## 🔒 Segurança

### Recomendações

1. **Autenticação:**
   - Streamlit Cloud: integração com Google OAuth
   - Alternativa: adicionar senha simples no código

2. **HTTPS:**
   - Streamlit Cloud: automático
   - Docker: usar Nginx com Let's Encrypt

3. **Dados sensíveis:**
   - Nunca commitar arquivos com dados reais
   - Usar `.gitignore` adequadamente
   - Considerar criptografia dos uploads

4. **Rate Limiting:**
   - Streamlit Cloud: automático
   - Docker: configurar no Nginx

---

## 📊 Monitoramento

### Streamlit Cloud

- Logs disponíveis na interface
- Métricas de uso
- Alertas via email

### Alternativas

- **Grafana + Prometheus** para métricas
- **Sentry** para erros
- **Google Analytics** para uso

---

## 💰 Custos Estimados

| Plataforma | Custo Mensal | Recursos |
|------------|--------------|----------|
| Streamlit Cloud (Free) | $0 | 1 app privada, 1GB RAM |
| Streamlit Cloud (Team) | $250 | 5 apps, 4GB RAM/app |
| Heroku (Basic) | $7 | 512MB RAM, sempre ativo |
| DigitalOcean (Droplet) | $5 | 1GB RAM, 1 CPU |
| AWS (t2.micro) | ~$10 | 1GB RAM, 1 CPU |

---

## 🆘 Troubleshooting

### Erro: "ModuleNotFoundError"
- Verifique `requirements.txt`
- Certifique-se de incluir todas as dependências

### Erro: "Memory Limit Exceeded"
- Otimize o código para usar menos memória
- Use cache (`@st.cache_data`)
- Upgrade para plano pago

### App lenta
- Use `@st.cache_data` para dados
- Use `@st.cache_resource` para modelos
- Reduza tamanho dos arquivos processados

### Deploy falhou
- Verifique logs no Streamlit Cloud
- Teste localmente primeiro
- Verifique sintaxe do Python

---

## ✅ Checklist Pré-Deploy

- [ ] Testar aplicação localmente
- [ ] Verificar `requirements.txt` completo
- [ ] Adicionar `.gitignore`
- [ ] Remover dados sensíveis
- [ ] Criar README.md
- [ ] Configurar `.streamlit/config.toml`
- [ ] Testar com diferentes tamanhos de arquivo
- [ ] Verificar responsividade mobile
- [ ] Documentar uso da aplicação

---

## 📞 Suporte

- **Documentação Streamlit:** https://docs.streamlit.io/
- **Comunidade:** https://discuss.streamlit.io/
- **GitHub Issues:** https://github.com/streamlit/streamlit/issues

---

## 🎉 Pronto!

Após o deploy, sua aplicação estará acessível 24/7 na web!

Compartilhe o link com sua equipe e comece a auditar os registros de ponto de qualquer lugar. 🚀
