import mysql.connector as conn
#mycon=conn.connect()
#cur.execute()
def search_username(x,mycon):
    cur = mycon.cursor()
    cur.execute('''SELECT * FROM users WHERE username=%s''',(x,))
    validUserTable = cur.fetchall()
    print(validUserTable)
    mycon.commit()  

    return validUserTable

def insert(name,passwor,mail,mycon):
    cur=mycon.cursor()
    try:
        cur.execute('''INSERT INTO users(username,password,email) VALUES('{}','{}','{}')'''.format(name,passwor,mail))
        mycon.commit()
    except:
        return 0
    return 1
