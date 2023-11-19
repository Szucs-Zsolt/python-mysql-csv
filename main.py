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

if __name__=="__main__":
    # It uses a config file to get the necessary data for the connection.
    db = Database(config_file=".\\config\\mysql_connection.cfg")

    app = wx.App()
    main_window = MainWindow("MySQL - CSV converter", db)
    app.MainLoop()
