import pyodbc

serverName = "hector.database.windows.net"
database = "encryptions"
connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:hector.database.windows.net,1433;Database=encryptions;Uid=CloudSA28d7309b;Pwd={Console_encrypt};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'


connection = pyodbc.connect(connection_string)
cursor = connection.cursor()
