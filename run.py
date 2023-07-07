import database as DB

connection = DB.init()
cursor = connection.cursor()
print('Welcome to Cmail')

while True:
    command = input('To login press 1 \nTo create an account press 2 \nTo quit press q\n')
    if command == '2':
        DB.create_account(cursor)
    if command == '1':
        DB.login(cursor)
    if command == 'q':
        break
connection.commit()
connection.close()