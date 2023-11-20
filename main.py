"""
A program csatlakozik egy adatbázishoz. Az ehhez szükséges
adatokat a konfigurációs fájljából veszi.
Ezután kiírja a táblák nevét, amik kijelölhetők.
A kijelölt táblák tartalmát csv fájlokba menti.
"""
import wx
from models.database import Database
from models.csv_handler import csv_writer
from views.main_window import MainWindow


def main():
    """
    It initializes the database handler with the necessary 
    data from the config file, then the application starts.
    """
    db = Database(config_file=".\\config\\mysql_connection.cfg")

    app = wx.App()
    main_window = MainWindow("MySQL - CSV converter", db)
    app.MainLoop()


if __name__ == "__main__":
    main()
