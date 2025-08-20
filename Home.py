
from matplotlib import pyplot as plt
import streamlit as st

from data_manage import DataManageSingleton
from data_sheets import ManageSheets

# Inicializa el gestor de hojas con los parámetros necesarios
SPREADSHEET_ID = st.secrets.google_sheets.FILE_ID
FILE_NAME = st.secrets.google_sheets.FILE_NAME
CREDENTIALS_DICT = dict(st.secrets.google_service_account)

st.set_page_config(page_title="Control Humberto", page_icon="🟩", layout="centered")

st.markdown("""
<div style='text-align: center;'>
    <h1 style='color: #2c2c2c;'>Bienvenido al Panel de Control <span style='color: #336699;'>Humberto</span></h1>
    <p style='font-size: 1.2em;'>Gestiona y visualiza el consolidado de montos de manera sencilla y rápida.</p>
</div>
""", unsafe_allow_html=True)

st.write("")

for key, default in [
    ("stage", 0),
    ("pivot_consolidado", None),
    ("manager_sheets", None),
    ("pv_consolidado", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

def set_state(i):
    st.session_state.stage = i

if st.session_state.stage == 0:
    # Inicializar el estado de la sesión
    # Obtiene la instancia del gestor de datos
    with st.spinner("Actualizando datos..."):
            st.session_state.manager_sheets = ManageSheets(
                file_sheet_name=FILE_NAME,
                spreadsheet_id=SPREADSHEET_ID,
                credentials_file=CREDENTIALS_DICT,
            )
    data_manager = DataManageSingleton.get_instance(st.session_state.manager_sheets)
    st.session_state.pivot_consolidado = data_manager.get_pivot_consolidado()
    set_state(1)

if st.session_state.stage == 1:
    format_dict = {
        "Productos": "{:,.2f}",
        "Fletes": "{:,.2f}",
        "Saldo": "{:,.2f}",
    }  # ejemplo {'sum':'${0:,.0f}', 'date': '{:%m-%Y}', 'pct_of_total': '{:.2%}'}
    cmap = plt.colormaps["RdYlGn"] 
    st.dataframe(st.session_state.pivot_consolidado.style.format(format_dict).background_gradient(subset=["Saldo"], cmap=cmap,), hide_index=True) # Aplicar formato y color a la columna "Saldo"
    st.button(label="Actualizar", on_click=set_state, args=(0,), icon="🔄")
        