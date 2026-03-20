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

# Vendedores: { "INICIALES": "Nombre completo" }
VENDEDORES = {
    "CR": "Carlos Rodríguez",
    "CP": "Claudia Pereira",
    "JP": "Juan Pérez",
    "LM": "Laura Martínez",
    "AG": "Andrés González",
    "FA": "Federico Álvarez",
    "WL": "Walter López",
    "EC": "Elena Castro",
}

# Columnas en el orden que van a aparecer en Google Sheets
COLUMNAS = [
    "Fecha",
    "Hora",
    "Vendedor",
    "Nombre",
    "Empresa",
    "Cargo",
    "Teléfono",
    "Email",
    "Productos de interés",
    "Nivel de interés",
    "Notas",
]
