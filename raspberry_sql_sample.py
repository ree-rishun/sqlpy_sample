# import
import RPi.GPIO as GPIO
import sqlite3
import datetime
import sys

# define
SWITCH_PIN = 18

# commandline argument
args = sys.argv


# table writer
def table_wrt():

    # switch setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # connect DB
    conn = sqlite3.connect('pushswitch.db')
    c = conn.cursor()

    # count variable
    i = 0

    # create table
    c.execute('select count(*) from sqlite_master where type="table" and name="data"')
    if c.fetchone() == (0,):
        c.execute('create table data(time text)')

    try:
        while True:
            if GPIO.input(SWITCH_PIN) == 1:
                while GPIO.input(SWITCH_PIN) == 1:
                   continue
                # get date and time
                dt_now = datetime.datetime.now()

                sql = 'insert into data values (?)'
                params = (dt_now.strftime('%Y/%m/%d %H:%M:%S'),)

                # insert table
                c.execute(sql, params)
                i += 1
                print("pushed:", i, "time")
    except KeyboardInterrupt:
        # data commit
        conn.commit()

        # fin
        conn.close()
        GPIO.cleanup()
        sys.exit(0)

    # data commit
    conn.commit()

    # fin
    conn.close()
    GPIO.cleanup()


# table printer
def table_prt():
    # connect DB
    conn = sqlite3.connect('pushswitch.db')
    c = conn.cursor()

   # check DB
    c.execute('select count(*) from sqlite_master where type="table" and name="data"')
    if c.fetchone() == (0,):
        print('not found')
        conn.close()
        sys.exit(0)

        # get data
    for row in c.execute('select * from data order by time asc'):
        print(row)

    # close DB
    conn.close()

# table delete
def table_del():

    # connect DB
    conn = sqlite3.connect('pushswitch.db')
    
    c = conn.cursor()

    # confirmation
    print('data table delete OK? [y/n]:')
    answer = input()

    if answer == "y":
        # delete table
        drop_table = 'drop table if exists data'
        c.execute(drop_table)
        print('delete success')
    else :
        print('delete failed')

    # close DB
    conn.close()

# main

# commandline argument
args = sys.argv

# mode
if 2 > len(args):
    print("-w : record the number of presses.")
    print("-p : display the recorded data.")
    print("-d : delete the recorded data.")
elif args[1] == "-w":
    table_wrt()
elif args[1] == "-p":
    table_prt()
elif args[1] == "-d":
    table_del()
else :
    print("-w : record the number of presses.")
    print("-p : display the recorded data.")
    print("-d : delete the recorded data.")