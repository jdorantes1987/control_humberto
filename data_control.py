from pandas import DataFrame


class DataControl:
    def __init__(self, manager_sheets) -> None:
        self.oSheets = manager_sheets

    def get_productos(self) -> DataFrame:
        """
        Obtiene los datos de productos de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="productos")

    def get_fletes(self) -> DataFrame:
        """
        Obtiene los datos de fletes de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="fletes")
