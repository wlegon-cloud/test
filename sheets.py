import json
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from config import SPREADSHEET_NAME, SHEET_NAME, COLUMNAS

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@st.cache_resource
def get_sheet():
    """Conecta con Google Sheets usando Streamlit Secrets. Cachea la conexión."""
    try:
        creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open(SPREADSHEET_NAME)
        sheet = spreadsheet.worksheet(SHEET_NAME)
        return sheet
    except KeyError:
        st.error(
            "❌ No se encontraron las credenciales. "
            "Agregá `GOOGLE_CREDENTIALS` en **Settings → Secrets** de Streamlit Cloud."
        )
        st.stop()
    except json.JSONDecodeError:
        st.error("❌ El formato del secret `GOOGLE_CREDENTIALS` no es JSON válido.")
        st.stop()
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(
            f"❌ No se encontró la planilla **'{SPREADSHEET_NAME}'**. "
            "Verificá el nombre en `config.py` y que la cuenta de servicio tenga acceso."
        )
        st.stop()
    except Exception as e:
        st.error(f"❌ Error al conectar con Google Sheets: {e}")
        st.stop()


def ensure_headers(sheet):
    if sheet.row_count == 0 or sheet.cell(1, 1).value is None:
        sheet.append_row(COLUMNAS)


def get_all_leads(sheet):
    try:
        return sheet.get_all_records()
    except Exception:
        return []


def append_lead(sheet, row: list):
    sheet.append_row(row, value_input_option="USER_ENTERED")


def check_duplicate(sheet, email: str, telefono: str):
    if not email and not telefono:
        return None
    leads = get_all_leads(sheet)
    for lead in leads:
        email_match = (
            email
            and lead.get("Email", "").strip().lower() == email.strip().lower()
        )
        tel_match = (
            telefono
            and str(lead.get("Teléfono", "")).strip() == str(telefono).strip()
        )
        if email_match or tel_match:
            return lead
    return None
