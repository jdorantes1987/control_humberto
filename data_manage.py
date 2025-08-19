from pandas import DataFrame, to_datetime, to_numeric

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

    # Obtiene los productos y fletes
    productos = data_manager.get_productos()
    fletes = data_manager.get_fletes()

    print(productos)
    print(fletes)
