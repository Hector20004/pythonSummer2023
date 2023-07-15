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
        user = cursor.execute('Select user_name from user_info where user_name = ?',recipient).fetchone()[0]
        if user is None:
            recipients.remove(recipient)
            print(user,"Not found")
    if not recipients == []:
        args = (email,public_key_exponent,public_key_module,private_key,sender)
        cursor.execute("""Insert Into sended_messages(message,public_key1,public_key2,private_key,sender,sended_date)
                        Output Inserted.sended_id
                        Values (?,?,?,?,?,GETDATE())""",args )
        id = cursor.fetchone()[0]
        for recipient in recipients:
            args = [id,recipient]
            cursor.execute("""Insert Into receive_message(sended_id,receiver)
                            Values(?,?)""",args)
        print("Message sended successfully")
    else:
        return
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

def check_Messages(connection,user):
    cursor = connection.cursor()
    cursor.execute(""" Select sended_messages.sended_id, sended_messages.message,sended_messages.sender,sended_messages.public_key2,sended_messages.private_key,sended_messages.sended_date,receive_message.readed,receive_message.sended_id,receive_message.received_id
                        From receive_message
                        Inner Join sended_messages On receive_message.sended_id = sended_messages.sended_id
                        Where receive_message.receiver = ?  
                        Order by sended_date DESC""",user)
    emails = cursor.fetchall()
    i = 0
    for i in range(len(emails)):
        emails[i][1] = RSA.decryptMessage(emails[i][1],emails[i][4],emails[i][3])
        font_style = '\033[0m'
        if emails[i][6] == 0:
            font_style = '\033[91m'
        subject = emails[i][1].split('\n')[0]
        print(font_style,i+1,"- From", emails[i][2], subject, "on",emails[i][5],'\n','\033[0m')
        i += 1
    option = int(input('Input email number to read it or press 0 to go back\n'))

    if option == 0:
        return
    else:
        print(emails[option-1][1],'\n')
        cursor.execute("""Update receive_message
                          Set readed = 1
                          where received_id = ?
                        """,emails[option-1][7])
