import mysql.connector
con=con=mysql.connector.connect(host="localhost",user="root",password="anand",database="urban_kinetics")
cur=con.cursor()
# try:
# p="use database urban_kinetics12"
# cur.execute(p)
#d="desc users"
#cur.execute(d)
#print(cur.fetchall())

def query(command):
    cur.execute(command)
    con.commit()

def info():
    name=input("Enter the name of the member: ")
    phn=input("Enter the phone number: ")
    while True:
        if len(phn)!=10:
            y=input("Please reenter the number: ")
        else:
            phn=int(phn)
            break

    add=input("Enter the address: ")
    med=input("Is there any medical issue? if yes press Y if no press N: ")
    if med.upper()=="Y":
        issue=input("Please enter the issue: ")
    gender=input("Enter the gender M/F: ")
    pack=("Select the package which you want from the packages given below: ")
    print(pack)
    packages=input('''
                    1. 12 months= ₹24000
                    2. 6 months= ₹15000
                    3. 3 months= ₹8000 
                    4. 1 month= ₹3000
                    5. one day pass= ₹500
                    ''')
    def create_records(eno,enm,age,gend,sal):
        query="insert into users values(%s,'%s',%s,'%s',%s)" % (eno,enm,age,gend,sal)
        cur.execute(query)
        con.commit()
        print("new emp record inserted successfully")
                    