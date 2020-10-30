import mysql.connector
from mysql.connector import errorcode

# try:

con = mysql.connector.connect(host='localhost', user='root',password='12345678')
cursor = con.cursor()

databaseName = "urban_kinetics"


def trainersTableInitialiser():
    global trainersTableName
    global trainersTableFields
    global trainersNameList
    global trainersExperience
    global trainersSpeciality
    global trainersAge
    global trainersId
    trainersId = "NULL"

    trainersTableName = "trainers"
    trainersTableFields = "sr_no int(5) NOT NULL AUTO_INCREMENT, name varchar(20),\
        experience varchar(20), speciality varchar(50), age int(2), PRIMARY KEY(SR_NO)"

    trainersNameList = ['Thomas', 'Stephen','Lewis','Samuel', 'Kane']
    trainersExperience = ['2 Years','5 Years','8 Years','10 Years','6 Years', '3 Years']
    trainersSpeciality = ['Weight Loss', 'Muscle Gain', 'Aesthetics','Calisthenics','Aerobics']
    trainersAge = [26, 28, 32, 35, 30, 29]

    makeOrCheckDatabase = f"create database if not exists {databaseName}"
    cursor.execute(makeOrCheckDatabase)

    useDatabase = f"use {databaseName}"
    cursor.execute(useDatabase)

    makeOrCheckTrainersTable = f"create table if not exists {trainersTableName}({trainersTableFields}) "
    cursor.execute(makeOrCheckTrainersTable)

    makeAutoIncrementAt1001 = f"ALTER TABLE {trainersTableName} AUTO_INCREMENT = 1001"
    cursor.execute(makeAutoIncrementAt1001)


    def query(command):
        cursor.execute(command)
        con.commit()


    for i in range(len(trainersNameList)):
        insertTrainersRecord = f"insert into {trainersTableName} value({trainersId}, '{trainersNameList[i]}','{trainersExperience[i]}', '{trainersSpeciality[i]}', '{trainersAge[i]}')"

        query(insertTrainersRecord)

trainersTableInitialiser()





cursor.close()
con.close()
print("done")
dir(errorcode)
# except mysql.connector.Error as err:
#     if err.errno == 1062:
#         print("""
#         TABLE ALREADY MADE AND,
#         THE DATA YOU WANT TO ENTER IS CLASHING WITH THE EXISTING ONE!!!""")
#     else:
#         print(err.errno,err.msg)


# for i in dir(errorcode):
#     code = "errorcode."+str(i)
#     code = eval(code)
#     if code==1049:
#         print(i)