import pyodbc


def init():
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:hector.database.windows.net,1433;Database=encryptions;Uid=CloudSA28d7309b;Pwd={Console_encrypt};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    connection = pyodbc.connect(connection_string)
    return connection

def createAccount(cursor):
    while True:
        username = input('Enter username or press b to go back\n')
        if username == 'b':
            return
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
def login(cursor):
    while True:
        username = input('Enter your username or press b to go back\n')
        if username == 'b':
            return
        user = cursor.execute("select user_name,user_password from user_info where user_name = ?",username).fetchone()
        if user is not None:
            password = input('Enter your password\n')
            while password != user[1]:
                print('wrong password try again or press b to go back')
                password = input()
                if password == 'b':
                    return
            return user

def afterLoginMenu(cursor,usuario):
    unreaded_messages = cursor.execute('select count(*) from receive_message where receiver = ? and readed = 0 ;',usuario).fetchone()[0]
    print('Welcome ',usuario,'you have',unreaded_messages,'new messages')
    option = input('To check your messages press 1\nTo send a message press 2\n to go to main menu press3\nTo exit press q')
