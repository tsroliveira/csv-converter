# 📄 Excel → CSV Converter (Tema Escuro Navy)

Aplicação **single-page web** desenvolvida em **Python** utilizando **Streamlit**, para converter planilhas **Excel (.xls / .xlsx)** em arquivos **CSV**.  

O sistema foi feito para ser **simples, rápido e visualmente agradável**, com **tema escuro azul marinho (navy)** e interface intuitiva.  
Suporta **arrastar e soltar (drag & drop)**, preview da planilha antes da conversão e **download direto em CSV**.  

---

## 🚀 Tecnologias utilizadas

- **[Python 3.10+](https://www.python.org/)** → linguagem principal
- **[Streamlit](https://streamlit.io/)** → framework para criar a interface web interativa
- **[Pandas](https://pandas.pydata.org/)** → manipulação de dados e conversão Excel → CSV
- **[OpenPyXL](https://openpyxl.readthedocs.io/)** → leitura de arquivos `.xlsx`
- **[xlrd](https://pypi.org/project/xlrd/)** → leitura de arquivos `.xls`

---

## ⚙️ Funcionalidades

- ✅ Upload de arquivos `.xls` ou `.xlsx` (drag & drop ou seleção manual)  
- ✅ Conversão direta para **CSV** (sem compactação em ZIP)  
- ✅ Preview dos **primeiros 200 registros** antes da exportação  
- ✅ Seleção da **aba (sheet)** a ser convertida  
- ✅ **Sidebar interativa**:
  - Opções **avançadas de conversão** no topo
  - **Padrões do cliente** exibidos abaixo
- ✅ Tema **dark navy** moderno e agradável

---

## 📦 Estrutura do Projeto

```bash
csv-converter/
├── app.py              # Código principal da aplicação Streamlit
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação
```

---

## 🔧 Instalação e execução

### 1. Clonar ou baixar o projeto
Baixe o repositório ou extraia os arquivos em uma pasta local:

```bash
git clone https://github.com/tsroliveira/csv-converter.git
cd csv-converter
```

Ou apenas extraia o `.zip` fornecido.

---

### 2. Criar ambiente virtual (opcional, mas recomendado)

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / Mac**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Instalar dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Rodar o projeto
```bash
streamlit run app.py
```

Após rodar, acesse no navegador:  
👉 [http://localhost:8501](http://localhost:8501)

---

## 🎛️ Padrões do Cliente

Se você não abrir a seção **Conversão avançada**, os seguintes padrões são usados automaticamente:

- **Separador**: `;`  
- **Codificação**: `utf-8-sig` (UTF-8 com BOM, compatível com Excel)  
- **Decimal**: `.`  
- **Cabeçalho**: incluso  
- **Aspas**: mínimas  

Esses parâmetros garantem que o CSV gerado siga exatamente o modelo esperado pelo cliente.

---

## 🛠️ Conversão Avançada

No menu lateral (**sidebar**), é possível personalizar:

- Separador do CSV (`;`, `,`, `\t`)
- Codificação (`utf-8-sig`, `utf-8`, `latin-1`)
- Separador decimal (`.`, `,`)
- Inclusão ou não de cabeçalho
- Nível de aspas (`mínimas`, `não-numéricas`, `todas`, `nenhuma`)

---

## 📷 Demonstração da Interface

### Tela principal
- Upload por **arrastar e soltar**
- Preview da planilha
- Botão para conversão e download direto do CSV

### Sidebar
- Conversão avançada configurável
- Padrões do cliente destacados

![Application Preview](https://github.com/tsroliveira/csv-converter/blob/main/app.png)

---

## 🧑‍💻 Autor

**Thiago Oliveira**  
Solutions Architect & Full-Stack Developer  

---

## 📜 Licença

Este projeto foi desenvolvido para fins de demonstração / uso interno.  
Você pode adaptar livremente para seu contexto.
