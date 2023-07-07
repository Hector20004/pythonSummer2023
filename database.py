import pyodbc


def init():
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:hector.database.windows.net,1433;Database=encryptions;Uid=CloudSA28d7309b;Pwd={Console_encrypt};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    connection = pyodbc.connect(connection_string)
    return connection

def create_account(cursor):
    while True:
        username = input('Enter username\n')
        cursor.execute("select user_name from user_info where user_name = ?",username)
        record = cursor.fetchone()
        if record is not None:
            print('Username already in use')
            continue
        else:
            break
    while True:
        password = input('Enter password\n')
        cursor.execute('Insert into user_info(user_name,user_password) Values(?,?)',(username,password))
        return 0