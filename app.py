import streamlit as st
import base64
from datetime import datetime
from config import PRODUCTOS, VENDEDORES
from sheets import get_sheet, ensure_headers, append_lead, check_duplicate

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Essen Soluciones · Registro de Leads",
    layout="centered",
)

# ── Logo base64 ───────────────────────────────────────────────────────────────
def get_logo():
    try:
        with open("logo.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

logo_b64 = get_logo()
logo_html = (
    f'<img src="data:image/png;base64,{logo_b64}" class="hero-logo">'
    if logo_b64 else ""
)

# ── Estilos ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@600;700&display=swap');

:root {
    --negro:     #000000;
    --rojo:      #CC0000;
    --rojo-vivo: #E00000;
    --blanco:    #FFFFFF;
    --gris1:     #111111;
    --gris2:     #1C1C1C;
    --gris3:     #2A2A2A;
    --gris4:     #444444;
    --gris5:     #888888;
}

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Barlow', sans-serif; font-weight: 400; }

/* Ocultar header y footer nativos de Streamlit */
header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }

.stApp { background: var(--negro); color: var(--blanco); }

/* ── Hero ── */
.hero {
    background: var(--gris1);
    border: 1px solid var(--gris3);
    border-top: 3px solid var(--rojo);
    border-radius: 4px;
    padding: 2rem 2rem 1.8rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}
.hero-content { flex: 1; min-width: 0; }
.hero-logo { height: 52px; width: auto; flex-shrink: 0; opacity: 0.92; }
.hero-tag {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: var(--rojo);
    margin-bottom: 0.5rem;
}
.hero-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: var(--blanco);
    margin: 0 0 0.35rem;
    line-height: 1.05;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}
.hero-sub { font-size: 0.82rem; color: var(--gris5); font-weight: 300; margin: 0; }

/* ── Pantalla vendedor ── */
.vendor-screen {
    background: var(--gris1);
    border: 1px solid var(--gris3);
    border-top: 3px solid var(--rojo);
    border-radius: 4px;
    padding: 2.5rem 2rem;
    margin-top: 2rem;
    text-align: center;
}
.vendor-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--blanco);
    margin-bottom: 0.4rem;
}
.vendor-sub { font-size: 0.82rem; color: var(--gris5); margin-bottom: 2rem; }

.vendor-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.6rem;
    max-width: 400px;
    margin: 0 auto;
}
.vendor-btn {
    background: var(--gris2);
    border: 1px solid var(--gris3);
    border-radius: 3px;
    padding: 0.9rem 0.5rem;
    cursor: pointer;
    transition: all 0.15s;
    text-align: center;
}
.vendor-btn:hover { background: var(--rojo); border-color: var(--rojo); }
.vendor-initials {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--blanco);
    display: block;
    letter-spacing: 0.05em;
}
.vendor-name {
    font-size: 0.65rem;
    color: var(--gris5);
    display: block;
    margin-top: 0.2rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ── Badge vendedor activo ── */
.vendor-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--gris2);
    border: 1px solid var(--gris3);
    border-radius: 2px;
    padding: 0.3rem 0.8rem;
    font-size: 0.75rem;
    color: var(--gris5);
    margin-bottom: 1.2rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 500;
}
.vendor-badge span { color: var(--rojo); font-weight: 700; }

/* ── Section labels ── */
.section-label {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--rojo);
    margin: 1.8rem 0 0.7rem;
    padding-bottom: 0.45rem;
    border-bottom: 1px solid var(--gris3);
}

/* ── Inputs ── */
.stTextInput label, .stTextArea label, .stMultiSelect label, .stRadio label span {
    color: #BBBBBB !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}
.stTextInput input {
    background: var(--gris2) !important;
    border: 1px solid var(--gris3) !important;
    border-radius: 3px !important;
    color: var(--blanco) !important;
    -webkit-text-fill-color: var(--blanco) !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 0.95rem !important;
}
.stTextInput input:focus {
    border-color: var(--rojo) !important;
    box-shadow: 0 0 0 2px rgba(204,0,0,0.15) !important;
}
.stTextArea textarea {
    background: var(--gris2) !important;
    border: 1px solid var(--gris3) !important;
    border-radius: 3px !important;
    color: var(--blanco) !important;
    -webkit-text-fill-color: var(--blanco) !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 0.95rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--rojo) !important;
    box-shadow: 0 0 0 2px rgba(204,0,0,0.15) !important;
}
.stMultiSelect > div > div {
    background: var(--gris2) !important;
    border: 1px solid var(--gris3) !important;
    border-radius: 3px !important;
    color: var(--blanco) !important;
}
.stMultiSelect span[data-baseweb="tag"] {
    background: var(--rojo) !important;
    border-radius: 2px !important;
}

/* ── Radio ── */
.stRadio > div { gap: 0.5rem; }
.stRadio label { color: var(--blanco) !important; font-size: 0.88rem !important; }

/* ── Botones ── */
.stButton > button[kind="primary"] {
    background: var(--rojo) !important;
    color: var(--blanco) !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 3px !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
}
.stButton > button[kind="primary"]:hover { background: var(--rojo-vivo) !important; }
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: var(--gris5) !important;
    border: 1px solid var(--gris3) !important;
    border-radius: 3px !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 0.85rem !important;
    width: 100% !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--gris5) !important;
    color: var(--blanco) !important;
}

/* ── Counter ── */
.counter {
    display: inline-block;
    background: var(--gris2);
    border: 1px solid var(--gris3);
    border-radius: 2px;
    padding: 0.3rem 1rem;
    font-size: 0.75rem;
    color: var(--gris5);
    margin-bottom: 1.2rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-weight: 500;
}
.counter span { color: var(--rojo); font-weight: 700; }

::placeholder { color: var(--gris4) !important; opacity: 1 !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--negro); }
::-webkit-scrollbar-thumb { background: var(--gris3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "vendedor" not in st.session_state:
    st.session_state.vendedor = None
if "form_key" not in st.session_state:
    st.session_state.form_key = 0
if "leads_session" not in st.session_state:
    st.session_state.leads_session = 0
if "pending_lead" not in st.session_state:
    st.session_state.pending_lead = None
if "success_msg" not in st.session_state:
    st.session_state.success_msg = False


# ── Header (siempre visible) ──────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-content">
        <div class="hero-tag">Stand &middot; Registro de Contactos</div>
        <div class="hero-title">Registro de Leads</div>
        <p class="hero-sub">Essen Soluciones</p>
    </div>
    {logo_html}
</div>
""", unsafe_allow_html=True)


# ── Pantalla de selección de vendedor ────────────────────────────────────────
if st.session_state.vendedor is None:
    st.markdown("""
    <div class="vendor-screen">
        <div class="vendor-title">Identificate para continuar</div>
        <p class="vendor-sub">Seleccioná tus iniciales</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (iniciales, nombre) in enumerate(VENDEDORES.items()):
        with cols[i % 4]:
            if st.button(f"{iniciales}\n{nombre.split()[0]}", key=f"v_{iniciales}"):
                st.session_state.vendedor = iniciales
                st.rerun()
    st.stop()


# ── Conexión Sheets ───────────────────────────────────────────────────────────
sheet = get_sheet()
ensure_headers(sheet)


# ── Badge vendedor + contador ─────────────────────────────────────────────────
vendedor_nombre = VENDEDORES.get(st.session_state.vendedor, "")
badge_extra = ""
if st.session_state.leads_session > 0:
    badge_extra = f" &nbsp;·&nbsp; Leads esta sesión: <span>{st.session_state.leads_session}</span>"

st.markdown(
    f'<div class="vendor-badge">Vendedor: <span>{st.session_state.vendedor}</span>'
    f' &nbsp;{vendedor_nombre}{badge_extra}'
    f' &nbsp;&nbsp;<a href="?" style="color:var(--gris5);font-size:0.7rem;">cambiar</a></div>',
    unsafe_allow_html=True,
)


# ── Mensaje de éxito ──────────────────────────────────────────────────────────
if st.session_state.success_msg:
    st.success("Lead guardado correctamente en Google Sheets.")
    st.session_state.success_msg = False


# ── Confirmacion de duplicado ─────────────────────────────────────────────────
if st.session_state.pending_lead is not None:
    datos = st.session_state.pending_lead["datos"]
    dup = st.session_state.pending_lead["duplicado"]

    st.warning(
        f"**Posible duplicado detectado**\n\n"
        f"Ya existe un contacto con este email o teléfono:\n\n"
        f"**{dup.get('Nombre', '—')}** · {dup.get('Empresa', '—')} "
        f"· Cargado el {dup.get('Fecha', '—')} a las {dup.get('Hora', '—')} "
        f"por {dup.get('Vendedor', '—')}\n\n"
        f"¿Querés guardarlo igual?"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Guardar igual", type="primary"):
            append_lead(sheet, datos)
            st.session_state.leads_session += 1
            st.session_state.pending_lead = None
            st.session_state.form_key += 1
            st.session_state.success_msg = True
            st.rerun()
    with col2:
        if st.button("Cancelar", type="secondary"):
            st.session_state.pending_lead = None
            st.rerun()

    st.stop()


# ── Formulario ────────────────────────────────────────────────────────────────
fk = st.session_state.form_key

st.markdown('<div class="section-label">Datos del contacto</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    nombre = st.text_input("Nombre *", key=f"nombre_{fk}", placeholder="Juan Pérez")
with col2:
    empresa = st.text_input("Empresa *", key=f"empresa_{fk}", placeholder="Empresa S.A.")

col3, col4 = st.columns(2)
with col3:
    cargo = st.text_input("Cargo", key=f"cargo_{fk}", placeholder="Gerente Comercial")
with col4:
    telefono = st.text_input("Teléfono", key=f"telefono_{fk}", placeholder="+598 99 000 000")

email = st.text_input("Email", key=f"email_{fk}", placeholder="juan@empresa.com")

st.markdown('<div class="section-label">Interes comercial</div>', unsafe_allow_html=True)

productos = st.multiselect(
    "Productos de interés",
    options=PRODUCTOS,
    key=f"productos_{fk}",
)

nivel = st.radio(
    "Nivel de interés",
    options=["Caliente", "Tibio", "Frio"],
    index=1,
    horizontal=True,
    key=f"nivel_{fk}",
)

st.markdown('<div class="section-label">Notas</div>', unsafe_allow_html=True)

notas = st.text_area(
    "Comentarios adicionales",
    key=f"notas_{fk}",
    placeholder="Ej: muy interesado en pricing, vuelve la semana que viene...",
    height=100,
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Guardar ───────────────────────────────────────────────────────────────────
if st.button("Guardar lead", type="primary"):

    errores = []
    if not nombre.strip():
        errores.append("**Nombre** es obligatorio.")
    if not empresa.strip():
        errores.append("**Empresa** es obligatoria.")

    if errores:
        for e in errores:
            st.error(e)
    else:
        now = datetime.now()
        row = [
            now.strftime("%d/%m/%Y"),
            now.strftime("%H:%M"),
            st.session_state.vendedor,
            nombre.strip(),
            empresa.strip(),
            cargo.strip(),
            telefono.strip(),
            email.strip().lower(),
            ", ".join(productos) if productos else "",
            nivel,
            notas.strip(),
        ]

        duplicado = check_duplicate(sheet, email.strip(), telefono.strip())

        if duplicado:
            st.session_state.pending_lead = {"datos": row, "duplicado": duplicado}
            st.rerun()
        else:
            append_lead(sheet, row)
            st.session_state.leads_session += 1
            st.session_state.form_key += 1
            st.session_state.success_msg = True
            st.rerun()
