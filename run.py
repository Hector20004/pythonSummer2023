import database
import database as DB

connection = DB.init()
print('Welcome to Cmail')

while True:
    command = input('To login press 1 \nTo create an account press 2 \nTo quit press q\n')
    if command == 'q':
        break
    if command == '2':
        DB.createAccount(connection)
    if command == '1':
        user = database.login(connection)
        if user is not None:
            DB.afterLoginMenu(connection,user[0])


connection.commit()
connection.close()