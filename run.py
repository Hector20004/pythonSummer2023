import database as DB

connection = DB.init()
cursor = connection.cursor()
print('Welcome to Cmail')

while True:
    command = input('To login press 1 \nTo create an account press 2 \nTo quit press q\n')
    if command == '2':
        DB.create_account(cursor)
    if command == 'q':
        querie = cursor.execute('select user_name from user_info').fetchall()
        for row in querie:
            print(row)
        break
connection.commit()
connection.close()