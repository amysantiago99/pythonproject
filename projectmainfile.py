import mysql.connector as con
from datetime import date
import string
mycon=con.connect(host="localhost",user="root",passwd="aastha",database="mydb")
cursor=mycon.cursor()



fine_per_day =1.0

def creating_tables():
    com1='create table admininfo\
        (\
        admid int(3) PRIMARY KEY,\
        admname varchar(50),\
        admsal int(5),\
        admadd varchar(50),\
        phone int,\
        passwd char(6) unique);'
    cursor.execute(com1)

    com2='create table books\
        (\
        bid int (3) primary key,\
        bname varchar(30),\
        bauthor varchar(30),\
        bstatus varchar(20),\
        bgenre varchar(20),\
        date_added date);'
    cursor.execute(com2)

    com3='create table transactions\
        (\
        bid int (3) primary key,\
        memid int (3),\
        dtissue date,\
        dtreturn date,\
        fine int);'
    cursor.execute(com3)

    com4='create table memberinfo\
        (\
        memid int (3),\
        memname varchar(20),\
        memphone int,\
        mememail varchar(20),\
        mem_issue_status varchar(20),\
        passwd char(6) unique);'
    cursor.execute(com4)
    mycon.commit()
    
#creating_tables()#
    
def registeracc():
    print()
    rec=int(input('How many members to be registered?'))
    for i in range(rec):
        memid=input('Enter the MEMBER ID:')
        memname=input('Enter the MEMBER NAME:')
        memphone=input('Enter the MEMBER PHONE NO:')
        mememail=input('Enter the MEMBER EMAIL:')
        passwd=input('Enter a 6 character PASSWORD:')
        sql='insert into memberinfo(memid,memname,memphone,mememail,passwd)\
        values ('+memid+',"'+memname+'",'+memphone+',"'+mememail+'","'+passwd+'");'
        cursor.execute(sql)
    mycon.commit()
    print(rec,'RECORD(S) ENTERED')



def addbook():
    print()
    rec=int(input('How many Books to be entered?'))   
    for i in range(rec):
        bid=input('Enter the BOOK ID:')
        bname=input('Enter the BOOK NAME:')
        bauthor=input('Enter the BOOK AUTHOR:')
        bgenre=input('Enter the BOOK GENRE:')
        date_added=input('Enter the DATE OF ADDING(yyyy-mm-dd):')
        sql='insert into books(bid,bname,bauthor,bstatus,bgenre,date_added)\
        values ('+bid+',"'+bname+'","'+bauthor+'","available","'+bgenre+'","'+date_added+'");'
        cursor.execute(sql)
    mycon.commit()
    print(rec,'BOOK(S) ADDED') 


def createacc():
    print()
    rec=int(input('How many records to be entered?'))
    for i in range(rec):
        aid=int(input("Enter the Admin id"))
        aname=input('Enter the name of admin')
        asal=input('Enter the salary of admin')
        address=input('Enter the address')
        phone=int(input('Enter the phone no'))
        pswd=input('Enter the password')
        sql='insert into admininfo values(%s,%s,%s,%s,%s,%s);'        
        n=(aid,aname,asal,address,phone,pswd)
        cursor.execute(sql,n)
    mycon.commit()
    print(rec,'RECORD(S) ENTERED')

def updateacc():
    print()
    m=input('Which field do you want to update?')
    field =''
    if m.lower()=='id':
        field ='admid'
    elif m.lower()=='name':
        field ='admname'
    elif m.lower()=='salary':
        field ='admsal'
    elif m.lower()=='phone':
        field ='phone'
    elif m.lower()=='password':
        field ='passwd'
    a=input('Enter the admin id:')
    b=input('Enter the new value :')
    if field=='salary' or field=='phone' or field=='id':
        sql='update admininfo set '+field+'='+b+' where admid='+a+';'
    else:
        sql='update admininfo set '+field+'="'+b+'" where admid='+a+';'
    cursor.execute(sql)
    mycon.commit()
    print('Admin details Updated')


def deleteacc():
    print()
    x=input('Enter the ADMIN ID of the account to be deleted')
    sql='delete from admininfo where admid=%s;'
    y=(x,)
    cursor.execute(sql,y)
    mycon.commit()
    print('Account deleted successfully')

def showacc():
    print()
    r=input('Enter the ADMIN ID for account info')
    sql='select * from admininfo where admid=%s;'
    s=(r,)
    cursor.execute(sql,s)
    for i in cursor:
        print('ADMIN ID =',i[0])
        print('ADMIN NAME=',i[1])
        print('ADMIN SALARY=',i[2])
        print('ADMIN ADDRESS=',i[3])
        print('ADMIN PHONE NO=',i[4])
        print('ADMIN PASSWORD=',i[5])
    mycon.commit()



def displayadm():
    print()
    sql='select * from admininfo;'
    cursor.execute(sql)
    print('{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}'.format('ID','NAME','SAL','ADDRESS','PHONE','PASSWORD'))
    for i in cursor:
        aid,name,sal,add,phone,pswd=i
        print('{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}'.format(aid,name,sal,add,phone,pswd))
    mycon.commit()


def acc():
    while True:
        print('PLEASE CHOOSE AN OPTION')
        print('1. Create New Account')
        print('2. Update An Account')
        print('3. Delete An Account')
        print('4. Show An Account')
        print('5. Show All Accounts')
        print('6. Back to Main Menu')
        ch=int(input('Your choice='))
        if ch==1:
            createacc()
        elif ch==2:
            updateacc()
        elif ch==3:
            deleteacc()
        elif ch==4:
            showacc()
        elif ch==5:
            displayadm()
        elif ch==6:
            break

def mem_issue_status(mem_id):
    sql ='select * from transactions where memid ='+mem_id +' and dtreturn is NULL;'
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

def book_status(book_id):
    sql = 'select * from books where bid ='+book_id + ';'
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[3]

def book_issue_status(book_id,mem_id):
    sql = 'select * from transactions where bid ='+book_id + '\
    and memid ='+ mem_id +' and dtreturn is NULL;'
    cursor.execute(sql)
    result = cursor.fetchone()
    return result

def issue():
    print()
    book_id = input('Enter Book  ID : ')
    mem_id  = input('Enter Member ID :')
    result = book_status(book_id)
    result1 = mem_issue_status(mem_id)
    today = date.today()
    if len(result1) == 0:
      if result == 'available':
          sql = 'insert into transactions(bid,memid,dtissue) values('+book_id+','+mem_id+',\
          "'+str(today)+'");'
          sql_book = 'update books set bstatus="issue" where bid ='+book_id + ';'
          cursor.execute(sql)
          cursor.execute(sql_book)
          print('Book issued successfully')
      else:
          print('Book is not available for ISSUE. Current status :',result1)
    else:
      if len(result1)<1:
        sql = 'insert into transactions(bid, memid, dtissue) values(' + \
             book_id+','+mem_id+',"'+str(today)+'");'
        sql_book = 'update books set bstatus="issue" where bid ='+book_id + ';'
        cursor.execute(sql)
        cursor.execute(sql_book)
        print('Book issued successfully')
      else:
        print('Member already have book from the Library')
    mycon.commit()


def return_book():
    print()
    global fine_per_day
    book_id = input('Enter Book  ID : ')
    mem_id = input('Enter Member ID :')
    today =date.today()
    result = book_issue_status(book_id,mem_id)
    if result==None:
       print('Book was not issued, Check Book Id and Member ID again')
    else:
       sql='update books set bstatus ="available" where bid ='+book_id +';'
       din = (today - result[2]).days
       fine = din * fine_per_day    #  fine per data
       sql1 = 'update transactions set dtreturn ="'+str(today)+'" ,\
       fine='+str(fine)+' where bid='+book_id +' and memid='+mem_id+' and dtreturn is NULL;' 
       cursor.execute(sql)
       cursor.execute(sql1)
       print('\nBook returned successfully')
    mycon.commit()


def adminlogin():
    print()
    admid=input('Please enter admin id:')
    passwd=input('Please enter your password:')
    sql1='select * from admininfo where admid='+admid+' and passwd="'+passwd+'";'
    cursor.execute(sql1)
    d=cursor.fetchone()
    if d[5]==passwd:
        print('You Are logged in.')
    else:
        print('Incorrect Admin ID or Password')

def memberlogin():
    print()
    memid=input('Please enter member id:')
    passwd=input('Please enter your password:')
    sql1='select * from memberinfo where memid="'+memid+'" and passwd="'+passwd+'";'
    cursor.execute(sql1)
    d=cursor.fetchone()
    if d[5]==passwd:
        print('You Are logged in.')
    else:
        print('Incorrect Admin ID or Password')
    print('You Are logged in.')
    
    
def deletebook():
    print()
    x=input('Enter the BOOK ID of the book to be deleted')
    sql='delete from books where bid={}'.format(x)
    cursor.execute(sql)
    mycon.commit()
    print('Book deleted successfully')

def searchbook():
    print()
    r=input('Enter the BOOK ID for book info')
    sql='select * from books where bid={}'.format(r)
    cursor.execute(sql)
    for i in cursor:
        print('BOOK ID =',i[0])
        print('BOOK NAME=',i[1])
        print('BOOK AUTHOR=',i[2])
        print('BOOK STATUS=',i[3])
        print('BOOK GENRE=',i[4])
        print('DATE ADDED=',i[5])
    mycon.commit()
    
def displayall():
    print()
    sql='select * from books;'
    cursor.execute(sql)
    print('{:<15}{:<15}{:<15}{:<15}{:<15}{:<15}'.format('ID','NAME','AUTHOR','STATUS','GENRE','DATE ADDED'))
    for i in cursor:
        bid,bname,bauthor,bstatus,bgenre,date_added=i
        print('{:<15}{:<15}{:<15}{:<15}{:<15}{:<15}'.format(bid,bname,bauthor,bstatus,bgenre,date_added))
    mycon.commit()
    
def book():
    while True:
        print()
        print('PLEASE CHOOSE AN OPTION')
        print('1. Add Book')
        print('2. Issue Book')
        print('3. Return Book')
        print('4. Delete Book')
        print('5. Search Book')
        print('6. Show All Books')
        print('7. Back To Main Menu')
        ch=int(input('Your choice='))
        if ch==1:
            addbook()
        elif ch==2:
            issue()
        elif ch==3:
            returnbook()
        elif ch==4:
            deletebook()
        elif ch==5:
            searchbook()
        elif ch==6:
            displayall()
        elif ch==7:
            break


def updacc():
    print()
    m=input('Which field do you want to update?')
    field =''
    if m.lower()=='id':
        field ='memmid'
    elif m.lower()=='name':
        field ='memname'
    elif m.lower()=='phone':
        field ='memphone'
    elif m.lower()=='email':
        field ='mememail'
    elif m.lower()=='genre':
        field='genre'
    elif m.lower()=='password':
        field ='passwd'
    a=input('Enter the member id:')
    b=input('Enter the new value:')
    if field=='id' or field=='phone':
        sql='update memberinfo set '+field+'='+b+'where memid='+a+';'
    else:
        sql='update memberinfo set '+field+'="'+b+'"where memid='+a+';'
    cursor.execute(sql)
    print('Member details Updated')
    mycon.commit()

def removeacc():
    print()
    x=input('Enter the MEMBER ID of the account to be deleted')
    sql='delete from memberinfo where memid=%s;'
    y=(x,)
    cursor.execute(sql,y)
    print('MEMBER deleted successfully')
    mycon.commit()

def dispacc():
    print()
    r=input('Enter the MEMBER ID for member info')
    sql='select * from memberinfo where memid=%s;'
    s=(r,)
    cursor.execute(sql,s)
    for i in cursor:
        print('MEMBER ID =',i[0])
        print('MEMBER NAME=',i[1])
        print('MEMBER PHONE=',i[2])
        print('MEMBER EMAIL=',i[3])
        print('GENRE PREFERRED=',i[4])
    mycon.commit()


def viewbooks():
    print()
    sql="select bname from books where bstatus='available';"
    cursor.execute(sql)
    a=cursor.fetchall()
    for row in a:
        for attr in row:
            print(attr,end='\t')
    mycon.commit()

def showtrans():
    memid=input('Enter the member id')
    sql='select * from transactions where memid=(%s);'
    n=(memid,)
    cursor.execute(sql,n)
    a=cursor.fetchall()
    print(a)

def menu():
    while True:
        print(''.center(60,'*'))
        print('WELCOME TO LIBRARY MANAGEMENT SYSTEM'.center(60,'*'))
        print(''.center(60,'*'))
        a=input('Are you an Admin or a Member?')
        if a.lower()=='admin':
            adminlogin()
            while True:
                print('------------------')
                print('1. MANAGE ACCOUNTS')
                print('2. MANAGE BOOKS')
                print('3. EXIT')
                ch=int(input('ENTER YOUR CHOICE'))
                print('------------------')
                if ch==1:
                    acc()
                elif ch==2:
                    book()
                elif ch==3:
                    print('THANK YOU'.center(60))
                    break

        elif a.lower()=='member':
            memberlogin()
            while True:
                print('1. Register Yourself')
                print('2. Update Account')
                print('3. Delete Account')
                print('4. Display Account Info')
                print('5. Show Transactions')
                print('6. View available books')
                print('7. EXIT')
                ch=int(input('Please Enter your Choice:'))
                if ch==1:
                    registeracc()
                elif ch==2:
                    updacc()
                elif ch==3:
                    removeacc()
                elif ch==4:
                    dispacc()
                elif ch==5:
                    showtrans()
                elif ch==6:
                    viewbooks()
                elif ch==7:
                    print('THANK YOU'.center(60))
                    break

menu()
