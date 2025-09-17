# app.py
# -------------------------------------------
# Excel → CSV (Single Page • Tema escuro navy)
# - Sidebar: Conversão avançada em cima, Padrões embaixo
# - Download direto em CSV (sem ZIP)
# - Drag & Drop nativo (funciona sem wrappers)
# - Layout idêntico ao light, só que dark
# -------------------------------------------

import io
import re
import csv
from datetime import datetime

import pandas as pd
import streamlit as st


# =========================
# Configuração da página
# =========================
st.set_page_config(
    page_title="Excel → CSV Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta escura navy
PRIMARY = "#1E3A8A"
ACCENT  = "#3B82F6"
BG      = "#0D1321"
BG2     = "#111827"
TEXT    = "#E5E7EB"

# CSS (mantém layout dark navy sem quebrar drag & drop)
st.markdown(
    f"""
    <style>
      .stApp {{
        background-color: {BG};
        color: {TEXT};
      }}
      .block-container {{
        padding-top: 1.5rem;
      }}
      .stButton > button, .stDownloadButton > button {{
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 600 !important;
        background: {PRIMARY} !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
      }}
      div[data-testid="stFileUploaderDropzone"] {{
        border: 2px dashed rgba(59,130,246,0.6) !important;
        background: {BG2} !important;
        border-radius: 16px !important;
        padding: 28px !important;
      }}
      div[data-testid="stFileUploaderDropzone"]:hover {{
        border-color: {ACCENT} !important;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# Helpers
# =========================
def sanitize_filename(name: str) -> str:
    base = re.sub(r"[^\w\-.]+", "_", name).strip("_")
    return base or "arquivo"

def read_excel_bytes(data: bytes, ext: str, sheet_name=None):
    """Lê Excel via pandas com engine apropriado."""
    if ext == ".xlsx":
        return pd.read_excel(io.BytesIO(data), engine="openpyxl", sheet_name=sheet_name)
    elif ext == ".xls":
        return pd.read_excel(io.BytesIO(data), engine="xlrd", sheet_name=sheet_name)
    raise ValueError("Formato não suportado (apenas .xls ou .xlsx).")

def list_sheet_names(file_obj, ext: str) -> list[str]:
    """Lista nomes de abas sem consumir permanentemente o buffer do upload."""
    try:
        if ext == ".xlsx":
            import openpyxl
            file_obj.seek(0)
            wb = openpyxl.load_workbook(file_obj, read_only=True, data_only=True)
            return wb.sheetnames
        else:
            import xlrd
            file_obj.seek(0)
            book = xlrd.open_workbook(file_contents=file_obj.read())
            return book.sheet_names()
    finally:
        file_obj.seek(0)


# =========================
# Padrões do cliente
# =========================
DEFAULT_SEP = ";"
DEFAULT_ENCODING = "utf-8-sig"
DEFAULT_DECIMAL = "."
DEFAULT_INCLUDE_HEADER = True
DEFAULT_QUOTING = csv.QUOTE_MINIMAL


# =========================
# Sidebar (avançado em cima, defaults embaixo)
# =========================
with st.sidebar:
    adv = st.expander("🛠️ Conversão avançada (opcional)", expanded=False)
    with adv:
        sep = st.selectbox(
            "Separador (CSV)",
            options=[(";", "Ponto e vírgula ;"), (",", "Vírgula ,"), ("\t", "Tabulação \\t")],
            index=0,
            format_func=lambda x: x[1],
        )[0]

        encoding = st.selectbox(
            "Codificação",
            options=[("utf-8-sig", "UTF-8 (compatível Excel)"), ("utf-8", "UTF-8"), ("latin-1", "Latin-1")],
            index=0,
            format_func=lambda x: x[1],
        )[0]

        decimal = st.selectbox(
            "Separador decimal",
            options=[(".", "Ponto ."), (",", "Vírgula ,")],
            index=0,
            format_func=lambda x: x[1],
        )[0]

        include_header = st.toggle("Incluir cabeçalho", value=DEFAULT_INCLUDE_HEADER)

        quoting_opt = st.selectbox(
            "Aspas",
            options=[
                (csv.QUOTE_MINIMAL, "Mínimas"),
                (csv.QUOTE_NONNUMERIC, "Não-numéricas"),
                (csv.QUOTE_ALL, "Todas"),
                (csv.QUOTE_NONE, "Nenhuma (não recomendado)"),
            ],
            index=0,
            format_func=lambda x: x[1],
        )[0]

        st.caption("Se você não tocar nessas opções, os **padrões do cliente** serão usados automaticamente.")

    st.header("⚙️ Conversão (padrões do cliente)")
    st.caption("Defaults usados para gerar CSV igual ao modelo do cliente:")
    st.markdown(
        """
        - **Separador**: `;`  
        - **Codificação**: `utf-8-sig`  
        - **Decimal**: `.`  
        - **Cabeçalho**: incluso  
        - **Aspas**: mínimas
        """,
    )


# =========================
# UI principal
# =========================
st.title("📄 Excel → CSV (tema escuro)")
st.caption("Arraste e solte um arquivo **.xls** ou **.xlsx** e baixe o **CSV** imediatamente — sem ZIP.")

# Uploader nativo
uploaded = st.file_uploader(
    "Arraste e solte seu Excel aqui (ou clique para selecionar)",
    type=["xls", "xlsx"],
    accept_multiple_files=False,
    help="Apenas .xls ou .xlsx. O arquivo permanece local; nada é enviado para a nuvem.",
)

if not uploaded:
    st.info("👆 Envie um arquivo Excel para começar.")
    st.stop()

# Valida extensão
name = uploaded.name
ext = "." + name.rsplit(".", 1)[-1].lower() if "." in name else ""
if ext not in [".xls", ".xlsx"]:
    st.error("Formato não suportado. Envie um arquivo .xls ou .xlsx.")
    st.stop()

# Lista abas
try:
    sheets = list_sheet_names(uploaded, ext)
except Exception as e:
    st.error(f"Não foi possível ler o arquivo: {e}")
    st.stop()

colA, colB = st.columns([2, 1])

with colA:
    if sheets:
        sheet_choice = st.selectbox("Selecione a aba a converter", options=sheets, index=0)
    else:
        sheet_choice = None
        st.info("Arquivo sem múltiplas abas detectadas. A leitura será feita da primeira planilha.")

    # Prévia (até 200 linhas)
    try:
        uploaded.seek(0)
        df_preview = read_excel_bytes(uploaded.read(), ext, sheet_name=sheet_choice if sheets else None)
        if isinstance(df_preview, dict):
            df_preview = next(iter(df_preview.values()))
        st.caption("Prévia dos primeiros 200 registros:")
        st.dataframe(df_preview.head(200), use_container_width=True, hide_index=True)
    except Exception as e:
        st.warning(f"Não foi possível gerar a prévia: {e}")

with colB:
    st.markdown("### Exportar CSV")

    # Usa valores avançados ou defaults
    final_sep = sep or DEFAULT_SEP
    final_enc = encoding or DEFAULT_ENCODING
    final_dec = decimal or DEFAULT_DECIMAL
    final_hdr = include_header if include_header is not None else DEFAULT_INCLUDE_HEADER
    final_q   = quoting_opt or DEFAULT_QUOTING

    if st.button("🔄 Converter agora", type="primary", use_container_width=True):
        try:
            uploaded.seek(0)
            df = read_excel_bytes(uploaded.read(), ext, sheet_name=sheet_choice if sheets else None)
            if isinstance(df, dict):
                df = next(iter(df.values()))

            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            base = sanitize_filename(name.rsplit(".", 1)[0])
            sheet_label = sanitize_filename(sheet_choice) if sheet_choice else "Planilha"

            csv_text = df.to_csv(
                index=False,
                sep=final_sep,
                header=final_hdr,
                decimal=final_dec,
                quoting=final_q,
                encoding=final_enc,
            )
            csv_bytes = csv_text.encode(final_enc, errors="replace")

            st.success("Conversão concluída ✅")
            st.download_button(
                "⬇️ Baixar CSV",
                data=csv_bytes,
                file_name=f"{base}__{sheet_label}__{ts}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Ocorreu um erro durante a conversão: {e}")
            st.exception(e)

st.markdown("---")
st.caption("Padrões do cliente ativos por default. Tudo processado localmente.")
