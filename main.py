"""
The program connects to a database using its
configuration file: ./config/mysql_connection.cfg
It will show the name of the tables from the
database.
The content of the selected tables will be written
in csv files.
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
