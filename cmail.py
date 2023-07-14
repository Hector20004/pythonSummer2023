import RSA
import pyodbc
def getLinesOfText():
    text_list = []
    while True:
        line = input()
        if line:
            text_list.append(line)
        else:
            break
    return text_list

def insertMailIntoDatabase(sender,recipients,email):
    global cnxn
    cursor = cnxn.cursor()

    keys = RSA.generateKeys()
    public_key_exponent = keys[0]
    public_key_module = keys[1]
    private_key = keys[2]

    email = RSA.encodeMessage(email,public_key_exponent,public_key_module)
    for recipient in recipients:
        user = cursor.execute('Select user_name from user_info where user_name = ?',recipient)
        if user is not None:
            args = (email,public_key_exponent,public_key_module,private_key,sender)
            cursor.execute("""Insert Into sended_messages(message,public_key1,public_key2,private_key,sender)
                           Values (?,?,?,?,?)""",args )
def sendMessage(connection,user):
    global cnxn
    cnxn = connection
    print('Write the persons you which to write, press enter two times to finish')
    recipients = getLinesOfText()

    subject = input('Enter email subject:\n')
    print('write email, press enter two times to send')

    text = getLinesOfText()
    text.insert(0, subject)

    email = '\n'.join(text)
    insertMailIntoDatabase(user,recipients,email)