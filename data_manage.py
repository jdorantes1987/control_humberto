from pandas import DataFrame, concat, to_numeric, to_datetime
from numpy import where

from data_control import DataControl


class DataManageSingleton:
    _instance = None

    @classmethod
    def get_instance(cls, manager_sheets):
        if cls._instance is None:
            cls._instance = DataManage(manager_sheets)
        return cls._instance


class DataManage:
    """
    Clase para manejar la gestión de datos de las hojas de cálculo.
    """

    def __init__(self, manager_sheets) -> None:
        self.oSheets = manager_sheets
        self.oDataControl = DataControl(manager_sheets=self.oSheets)

    def get_productos(self) -> DataFrame:
        """
        Obtiene los datos de productos.
        """
        return self.oDataControl.get_productos()

    def get_fletes(self) -> DataFrame:
        """
        Obtiene los datos de fletes.
        """
        return self.oDataControl.get_fletes()
    
    def get_consolidado(self) -> DataFrame:
        """
        Obtiene el consolidado de productos y fletes.
        """
        productos = self.get_productos()
        fletes = self.get_fletes()
        consolidado = concat([productos, fletes], axis=0)
        cols_montos = [
            "monto",
        ]  # Lista de columnas que contienen montos
        # Eliminar separadores de miles y reemplazar coma decimal por punto
        for col in cols_montos:
            consolidado[col] = (
                consolidado[col]
                .str.replace(".", "", regex=False)  # Remove thousand separator
                .str.replace(",", ".", regex=False)  # Replace decimal comma with dot
            )
        try:
            # Convertir a float, forzando errores a NaN
            consolidado[cols_montos] = consolidado[cols_montos].apply(
                to_numeric, errors="raise"  # Convertir a float errores a NaN
            )
        except Exception as e:
            print(f"Error al convertir columnas a numéricas: {e}")
            consolidado = DataFrame()  # Si hay un error, devuelve un DataFrame vacío
        consolidado["monto"] = where(
            consolidado["tipo"]=="Fletes", -consolidado["monto"], consolidado["monto"]
        )
        consolidado['fecha'] = to_datetime(consolidado['fecha'], format='%d/%m/%Y')


        return consolidado
    
    def get_pivot_consolidado(self) -> DataFrame:
        """
        Obtiene un pivot consolidado de productos y fletes.
        """
        consolidado = self.get_consolidado()
        if consolidado.empty:
            return DataFrame()

        consolidado["periodo"] = consolidado["fecha"].dt.to_period("M")
        pivot_consolidado = consolidado.pivot_table(
            index=["periodo"],
            columns=["tipo"],
            values="monto",
            aggfunc="sum",
            fill_value=0,
            sort=False,
        ).reset_index()
        pivot_consolidado.sort_values(by="periodo", inplace=True)
        pivot_consolidado = pivot_consolidado.groupby("periodo").sum().reset_index()
        pivot_consolidado["Saldo"] = (pivot_consolidado["Productos"] + pivot_consolidado["Fletes"]).cumsum()
        return pivot_consolidado


if __name__ == "__main__":
    # Ejemplo de uso
    from data_sheets import ManageSheets

    # Inicializa el gestor de hojas con los parámetros necesarios
    manager_sheets = ManageSheets(
        file_sheet_name="Humberto Faria Teles",
        spreadsheet_id="1ysIXTO959YdanNspRXBmkTTpDnUY3YMBornvt4iPXpk",
        credentials_file="key.json",
    )

    # Obtiene la instancia del gestor de datos
    data_manager = DataManageSingleton.get_instance(manager_sheets)

    consolidado = data_manager.get_pivot_consolidado()
    print(consolidado)