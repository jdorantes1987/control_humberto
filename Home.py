from matplotlib import pyplot as plt
import streamlit as st

from data_manage import DataManageSingleton
from data_sheets import ManageSheets

# Inicializa el gestor de hojas con los parámetros necesarios
SPREADSHEET_ID = st.secrets.google_sheets.FILE_ID
FILE_NAME = st.secrets.google_sheets.FILE_NAME
CREDENTIALS_DICT = dict(st.secrets.google_service_account)

st.set_page_config(page_title="Control Humberto", page_icon="🚀", layout="centered")

st.markdown(
    """
    <div style='background: linear-gradient(90deg, #e3f2fd 0%, #fce4ec 100%); padding: 28px 24px; border-radius: 16px; text-align: center; box-shadow: 0 2px 8px rgba(51,102,153,0.08);'>
        <h2 style='color: #336699; margin-bottom: 12px; font-size: 2.1rem; font-weight: 700; letter-spacing: 1px;'>🚀 Bienvenido al Panel de Control</h2>
        <h4 style='color: #444; font-weight: 400; margin-bottom: 0; font-size: 1.15rem;'>
            <span style='color: #336699;'>Gestiona y visualiza el consolidado de operaciones de manera sencilla y rápida</span>
        </h4>
    </div>
    """,
    unsafe_allow_html=True,
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
        "Saldo": "{:,.2f}",
    }  # ejemplo {'sum':'${0:,.0f}', 'date': '{:%m-%Y}', 'pct_of_total': '{:.2%}'}
    cmap = plt.colormaps["RdYlGn"]
    st.dataframe(
        st.session_state.pivot_consolidado.style.format(
            format_dict
        ).background_gradient(
            subset=["Saldo"],
            cmap=cmap,
        ),
        hide_index=True,
    )  # Aplicar formato y color a la columna "Saldo"
    st.button(label="Actualizar", on_click=set_state, args=(0,), icon="🔄")
