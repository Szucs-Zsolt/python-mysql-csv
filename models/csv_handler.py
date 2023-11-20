import csv

def csv_writer(file_name, rows):
    """
    It will write out the rows in the file, using csv format.
    
    Parameter
        file_name: it will overwrite this file
        rows: it will write out these rows (list of strings)
    """
    try:
        with open(file_name, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for sor in rows:
                writer.writerow(sor)
            return True
    except Exception as e:
        return False