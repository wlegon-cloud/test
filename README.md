# 🎯 App de Registro de Leads

App Streamlit para registrar leads en ferias y eventos, con guardado automático en Google Sheets.

---

## 📁 Archivos

```
lead_app/
├── app.py              # App principal
├── sheets.py           # Conexión con Google Sheets
├── config.py           # Productos, nombre de planilla, etc.
├── requirements.txt    # Dependencias
└── credentials.json    # 🔑 Tu clave de Google (ver paso 2)
```

---

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

---

## 🔑 Configurar Google Sheets (una sola vez)

### Paso 1 — Crear proyecto en Google Cloud
1. Ir a https://console.cloud.google.com
2. Crear un proyecto nuevo (ej: "leads-feria")
3. Ir a **APIs & Services → Library**
4. Habilitar **Google Sheets API**
5. Habilitar **Google Drive API**

### Paso 2 — Crear cuenta de servicio
1. Ir a **APIs & Services → Credentials**
2. Clic en **Create Credentials → Service Account**
3. Darle un nombre (ej: "leads-bot") y crear
4. Entrar a la cuenta de servicio creada → pestaña **Keys**
5. **Add Key → Create new key → JSON**
6. Descargar el archivo y renombrarlo a `credentials.json`
7. Moverlo a la carpeta `lead_app/`

### Paso 3 — Crear la planilla en Google Sheets
1. Crear una planilla nueva en Google Sheets
2. Nombrarla exactamente igual a `SPREADSHEET_NAME` en `config.py` (por defecto: `"Leads Feria"`)
3. Renombrar la hoja a `"Leads"` (o cambiar `SHEET_NAME` en `config.py`)

### Paso 4 — Dar acceso a la cuenta de servicio
1. Abrir el archivo `credentials.json` y copiar el campo `client_email`
   (tiene formato `nombre@proyecto.iam.gserviceaccount.com`)
2. En Google Sheets, clic en **Compartir**
3. Pegar el email y darle permiso de **Editor**

---

## ⚙️ Personalizar

Editá `config.py` para:
- Cambiar el nombre de la planilla (`SPREADSHEET_NAME`)
- Cambiar el nombre de la hoja (`SHEET_NAME`)
- Actualizar la lista de productos (`PRODUCTOS`)

---

## ▶️ Correr la app

```bash
streamlit run app.py
```

La app queda disponible en `http://localhost:8501`

### Para compartir con tu equipo en la feria:
Podés desplegarlo gratis en **Streamlit Community Cloud** (https://streamlit.io/cloud):
1. Subir el proyecto a GitHub (sin el `credentials.json`)
2. En Streamlit Cloud, agregar el contenido del `credentials.json` como **Secret** con la clave `GOOGLE_CREDENTIALS`
3. Modificar `sheets.py` para leer desde `st.secrets` en vez del archivo (ver nota abajo)

---

## 🌐 Deploy en Streamlit Cloud (opcional)

Si desplegás en la nube, reemplazá en `sheets.py` la función `get_sheet()` con:

```python
import json

@st.cache_resource
def get_sheet():
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)
```

Y en Streamlit Cloud, agregá el secret `GOOGLE_CREDENTIALS` con el contenido JSON del archivo de credenciales.
