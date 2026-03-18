# ── Configuración de la app ───────────────────────────────────────────────────

# Nombre de tu Google Spreadsheet (exacto, como aparece en Drive)
SPREADSHEET_NAME = "Leads Feria"

# Nombre de la hoja dentro del spreadsheet
SHEET_NAME = "Leads"

# Productos de tu empresa (editá esta lista)
PRODUCTOS = [
    "Logística",
    "Movimiento (ruedas)",
    "Carros a medida",
    "Cajones",
    "Pallets",
    "Pallets antiderrame",
    "Enfardadoras",
    "Cortadora HSM de embalaje",
]

# Campos obligatorios (mínimo para guardar)
CAMPOS_OBLIGATORIOS = ["nombre", "empresa"]

# Columnas en el orden que van a aparecer en Google Sheets
COLUMNAS = [
    "Fecha",
    "Hora",
    "Nombre",
    "Empresa",
    "Cargo",
    "Teléfono",
    "Email",
    "Productos de interés",
    "Nivel de interés",
    "Notas",
]
