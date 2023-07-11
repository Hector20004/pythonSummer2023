import database
import database as DB

connection = DB.init()
cursor = connection.cursor()
print('Welcome to Cmail')

while True:
    command = input('To login press 1 \nTo create an account press 2 \nTo quit press q\n')
    if command == 'q':
        break
    if command == '2':
        DB.createAccount(cursor)
    if command == '1':
        user = database.login(cursor)
        if user is not None:
            DB.afterLoginMenu(cursor,user[0])


connection.commit()
connection.close()