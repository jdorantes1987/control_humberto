from matplotlib import pyplot as plt
import streamlit as st

from data_manage import DataManageSingleton
from data_sheets import ManageSheets

# Inicializa el gestor de hojas con los parámetros necesarios
SPREADSHEET_ID = st.secrets.google_sheets.FILE_ID
FILE_NAME = st.secrets.google_sheets.FILE_NAME
CREDENTIALS_DICT = dict(st.secrets.google_service_account)

st.set_page_config(page_title="Control Humberto", page_icon="🚀")

st.title("Bienvenido! 🚀")
st.write("")
st.write(
    """
Este panel de control permite visualizar y actualizar los datos consolidados de productos y fletes desde **:green[Google Sheets]**.
"""
)

st.info(
    "¿Cómo cambiar el tema de la app?",
    icon="ℹ️",
)
with st.expander("Instrucciones para cambiar el tema de la app"):
    st.write(
        """
    Puedes cambiar entre el tema claro y oscuro usando el menú de configuración de Streamlit:
    1. Haz clic en el ícono de ajustes ⚙️ en la esquina superior derecha de la app.
    2. Selecciona la opción **'Tema'**.
    3. Elige entre **'Claro'**, **'Oscuro'** o **'Automático'** según tu preferencia.

    Esto ajustará automáticamente los colores y el estilo de la interfaz.
    """
    )

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
        "Neto": "{:,.2f}",
        "Saldo": "{:,.2f}",
    }  # ejemplo {'sum':'${0:,.0f}', 'date': '{:%m-%Y}', 'pct_of_total': '{:.2%}'}

    cmap_dict = {"Neto": "RdYlGn", "Saldo": "YlGnBu"}
    styled_df = st.session_state.pivot_consolidado.style.format(format_dict)
    for col, cmap_name in cmap_dict.items():
        styled_df = styled_df.background_gradient(cmap=cmap_name, subset=[col])
    st.dataframe(
        styled_df,
        hide_index=True,
    )
    st.button(label="Actualizar", on_click=set_state, args=(0,), icon="🔄")
