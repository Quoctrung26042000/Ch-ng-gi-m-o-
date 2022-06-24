import psycopg2
import sys


con = None
cur = None

def connect_database():
    global con
    global cur
    con = psycopg2.connect(database="test1", user="pi", password="hthuan04", host="huuthuanbk.ddns.net", port="5432")
    # con = psycopg2.connect(database = "test1", user = "pi", password = "hthuan04", host = "huuthuanbk.ddns.net", port = "5432")
    print ("Opened database successfully")
    cur = con.cursor()

def disconnect_database():
    cur.close()
    con.close()
    print("Disconect Database!")

# Upload database


def readImage(name):
    try:
        fin = open(name, "rb")
        img = fin.read()
        return img

    except IOError:
        # print ("Error %d: %s" % (e.args[0],e.args[1]))
        sys.exit(1)

    finally:
        if fin:
            fin.close()

def uploadImg(user_id, pathImg, nameImg):
    try:
        data = readImage(pathImg)
        binary = psycopg2.Binary(data)
        cur.execute("INSERT INTO img(user_id, name, data) VALUES (%s,%s,%s)", (user_id,nameImg,binary) )
        con.commit()
    except psycopg2.DatabaseError:
        if con:
            con.rollback()
        # print 'Error %s' % e
        sys.exit(1)

# get frame from database
def saveImg(path, name, data, id, user_id):
    try:
        fin = open(path + "/Users." + str(user_id) + "." + name.split(".jpg")[0] + "_" + str(id) + ".jpg", "wb")
        fin.write(data)
    except IOError:
        # print ("Error %d: %s" % (e.args[0],e.args[1]))
        sys.exit(1)

def getAllImg(pathSave):
    try:
        cur.execute("select * from img ORDER BY id")
        con.commit()
        print("The number of row: ", cur.rowcount)
        record = cur.fetchone()
        while record is not None:
            print(record)
            record = cur.fetchone()
            if (record is not None and record[3] is not None):
                saveImg(pathSave, record[2], record[3], record[0], record[1])
    except psycopg2.DatabaseError:
        if con:
            con.rollback()
        # print 'Error %s' % e
        sys.exit(1)

def getImg(pathSave, id):
    try:
        # print(id)
        # print(type(id))
        # xxx = str(id)
        # print(xxx)
        cur.execute("select * from img right join usr on img.user_id = usr.id where user_id = {}".format(id))
        #cur.execute("select * from img right join usr on img.user_id = usr.id where user_id = 1; INSERT INTO img (user_id, name, data) SELECT 1, name, data FROM img AS old WHERE old.user_id = 2 ")
        # cur.execute("select * from img right join usr on img.user_id = usr.id where user_id = 1")

        con.commit()
        print("Finall!")
        record = cur.fetchone()
        print(record)
        while record is not None:
            record = cur.fetchone()
            print(record)
            if (record is not None and record[3] is not None):
                saveImg(pathSave, record[2], record[3], record[0], record[1])
                break
    except psycopg2.DatabaseError:
        if con:
            con.rollback()
        # print 'Error %s' % e
        sys.exit(1)
    return 'Users.' + record[2], record[5], record[0], record[1]



# create table usr (
# 	id int not null primary key,
# 	name varchar not null,
# 	unique(id)
# );
#
#
# create table img (
# 	id_1 SERIAL primary key,
# 	user_id int not null references usr (id),
# 	name varchar not null,
# 	data bytea
# );
#
# insert into usr (id, "name") values (0, 'None');
# insert into usr (id, "name") values (1, 'Thuat');
# insert into usr (id, "name") values (2, 'ABC');




