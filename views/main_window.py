import wx
import wx.grid
from models.database import Database
from models.csv_handler import csv_writer


class MainWindow(wx.Frame):
    """
    It creates and display the GUI
    - The window contains a table with the name of the tables
      and a column to select them.
    - Button to start the conversion
    It also acts as a controller:
      - It connects the database (reading the rows of the tables from it)
        and the method that is responsible to write it out as a csv file.
    """

    def __init__(self, title, db):
        """
        It acquires the object to access the database in order to get
        the name of the tables in it.

        Parameter
            title:  name of the window
            db:     object, used to connect to the database
        """
        super().__init__(parent=None, title=title, size=(800, 600))

        # Acquiring the name of the tables from the database.
        self.db = db
        table_names = db.get_table_names()
        if (table_names is None):
            print("Failed to access the name of tha tables.")
            exit()

        # Creation of the GUI
        self.panel = wx.Panel(self)
        font = self.panel.GetFont()
        font.SetPointSize(16)
        self.panel.SetFont(font)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # 1. element - text in the header
        header_text = wx.StaticText(self.panel, label="Database conversion")

        # 2. element - table
        # It creates the grid, the cells in the first column can be
        # marked in order to make sure that these tables will be
        # converted.
        # The name of the tables will be in the second coloumn.
        self.table = wx.grid.Grid(self.panel)
        self.table.CreateGrid(len(table_names), 2)
        self.table.SetColLabelValue(0, "Save")
        self.table.SetColLabelValue(1, "Name of the table")
        self.table.SetSelectionMode(wx.grid.Grid.GridSelectNone)
        self.table.SetColSize(1, 580)

        # Style of the first column: checkbox
        attr = wx.grid.GridCellAttr()
        attr.SetEditor(wx.grid.GridCellBoolEditor())
        attr.SetRenderer(wx.grid.GridCellBoolRenderer())
        self.table.SetColAttr(0, attr)

        for i in range(len(table_names)):
            self.table.SetCellValue(i, 1, table_names[i])
            self.table.SetReadOnly(i, 1, True)

        # 3. element - button
        self.conversion_button = wx.Button(self.panel, label="Save")

        # The grid will use all of the empty space.
        self.sizer.Add(header_text, proportion=0,
                       flag=wx.ALIGN_CENTER | wx.BOTTOM | wx.TOP, border=20)
        self.sizer.Add(self.table, proportion=1, flag=wx.EXPAND |
                       wx.LEFT | wx.RIGHT | wx.BOTTOM, border=20)
        self.sizer.Add(self.conversion_button, proportion=0,
                       flag=wx.EXPAND | wx.RIGHT | wx.BOTTOM, border=20)

        # If the button is clicked the conversion method will be called.
        self.panel.Bind(event=wx.EVT_BUTTON, source=self.conversion_button,
                        handler=self.conversion_button_handler)
        # Simple click on a cell also mark/unmark the checkbox
        self.table.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
                        self.table_clicked_handler)

        self.panel.SetSizer(self.sizer)

        self.Center()
        self.Show()

    def conversion_button_handler(self, event):
        """
        It reads the content all of the marked tables and write 
        it out each of them in a separate csv file.
        """
        success = True
        for i in range(self.table.GetNumberRows()):
            # Conversion based of the marked rows
            if (self.table.GetCellValue(i, 0) == "1"):
                table_name = self.table.GetCellValue(i, 1)
                rows = self.db.get_all_rows(table_name)
                if rows is None:
                    self.message_error(
                        "I wasn't able to read the content of the tables.", "Error")
                    return

                table_written = csv_writer(
                    file_name=table_name+".csv", rows=rows)
                if table_written:
                    self.table.SetCellValue(i, 0, "")

                success = success and table_written
        if success:
            self.message_ok("Marked tables has been written as csv", "OK")
        else:
            self.message_error(
                "I wasn't able to save the table's content as csv.", "Error")

    def table_clicked_handler(self, event):
        """
        It is possible to check/uncheck a line with single click.  
        """
        row = event.GetRow()
        col = event.GetCol()
        if col == 0:
            self.table.SetGridCursor(row, col)
            if self.table.GetCellValue(row, col) == "1":
                self.table.SetCellValue(row, col, "")
            else:
                self.table.SetCellValue(row, col, "1")

    def message_error(self, msg, title):
        """
        Dialog box with error message.
        """
        wx.MessageBox(msg, title, wx.OK | wx.ICON_ERROR)

    def message_ok(self, msg, title):
        """
        Dialog box with info message.
        """
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)
