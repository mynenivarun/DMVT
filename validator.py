from cons import *
import pymysql
import hashlib
import random
import datetime

def ext():
    cursor.close()
    cursor1.close()
    conn1.close()
    conn2.close()
    rpt.append('Closing....')

rpt = []

#db1 connection #mysql.connector
conn1 = pymysql.connect(host=db1_host, database=db1_dtbs, user=db1_user, password=db1_pswd)
cursor = conn1.cursor()
dbdq1 = conn1.cursor()
tbdq1 = conn1.cursor()
ccq1 = conn1.cursor()

#db2 connection
conn2 = pymysql.connect(host=db2_host, database=db2_dtbs, user=db2_user, password=db2_pswd)
cursor1 = conn2.cursor()
dbdq2 = conn2.cursor()
tbdq2 = conn2.cursor()
ccq2 = conn2.cursor()

rpt.append(f'Databases : {db1_host}, {db2_host}')


dbdq = 'SELECT table_schema AS "Database", ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)" FROM information_schema.TABLES GROUP BY table_schema;'
tbdq = f'SELECT table_name AS "Table", ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)"FROM information_schema.TABLES WHERE table_schema = "{db1_dtbs}" ORDER BY (data_length + index_length) DESC;'
ccq = f'SELECT Table_Name, count(*) as No_of_Columns FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = "{db1_dtbs}" group by table_name;'

if conn1.open==True and conn2.open==True:
    rpt.append('Connections Established')

    dbdq1.execute(dbdq)
    dbdq2.execute(dbdq)

    dbdq_l1 = dbdq1.fetchall()
    dbdq_l2 = dbdq2.fetchall()
    mdbs_l = []
    udbs_l = []

    for i in range(len(dbdq_l1)):
        if(dbdq_l1[i] in dbdq_l2):
            mdbs_l.append(dbdq_l1[i])
        else:
            udbs_l.append(dbdq_l1[i])

    rpt.append('_________________________________________')
    rpt.append('Available Database and sizes')
    rpt.append(f'DB-1 {db1_host} : {dbdq_l1}')
    rpt.append(f'DB-2 {db2_host} : {dbdq_l2}')
    rpt.append(" ")
    rpt.append(f'Matched DB Sizes : {mdbs_l}')
    rpt.append(f'UN-Matched DB Sizes : {udbs_l}')
    rpt.append(" ")

    tbdq1.execute(tbdq)
    tbdq2.execute(tbdq)

    tbdq_l1 = tbdq1.fetchall()
    tbdq_l2 = tbdq2.fetchall()
    mtbs_l = []
    utbs_l = []

    for i in range(len(tbdq_l1)):
        if(tbdq_l1[i] in tbdq_l2):
            mtbs_l.append(tbdq_l1[i])
        else:
            utbs_l.append(tbdq_l1[i])

    rpt.append('_________________________________________')
    rpt.append('Available Tables and sizes')
    rpt.append(f'DB-1 {db1_host} : {tbdq_l1}')
    rpt.append(f'DB-2 {db2_host} : {tbdq_l2}')
    rpt.append(" ")
    rpt.append(f'Matched Table Sizes : {mtbs_l}')
    rpt.append(f'UN-Matched Table Sizes : {utbs_l}')
    rpt.append(" ")

    ccq1.execute(ccq)
    ccq2.execute(ccq)

    ccq_l1 = ccq1.fetchall()
    ccq_l2 = ccq2.fetchall()
    mccq_l = []
    uccq_l = []

    for i in range(len(ccq_l1)):
        if(ccq_l1[i] in ccq_l2):
            mccq_l.append(ccq_l1[i])
        else:
            uccq_l.append(ccq_l1[i])

    rpt.append('_________________________________________')
    rpt.append('Columns Counts')
    rpt.append(f'DB-1 : {ccq_l1}')
    rpt.append(f'DB-2 : {ccq_l2}')
    rpt.append(" ")
    rpt.append(f'Matched Table columns : {mccq_l}')
    rpt.append(f'UN-Matched Table columns : {uccq_l}')
    rpt.append(" ")

    cursor.execute("SHOW TABLES")
    cursor1.execute("SHOW TABLES")

    #adding-query-result1-to-list
    lst = cursor.fetchall()
    lst1 = cursor1.fetchall()

    tbls = []

    for i in range(len(lst)):
        if(lst[i] in lst1):
            tbls.append(lst[i])
    rpt.append(" ")       
    rpt.append(f'Matched tables : {tbls}')

    for x in range(len(tbls)):
        rpt.append(" ")
        rpt.append(" ")

        tblt = tbls[x]
        tbl = tblt[0]
        rpt.append(f'{x} Dvt Running For Table {tbl}')

        con1 = pymysql.connect(host=db1_host, database=db1_dtbs, user=db1_user, password=db1_pswd)
        con2 = pymysql.connect(host=db2_host, database=db2_dtbs, user=db2_user, password=db2_pswd)

        #geting all values from table 
        crsr = con1.cursor()
        crsr.execute("SELECT * FROM {0}".format(tbl))
        crsr1 = con2.cursor()
        crsr1.execute("SELECT * FROM {0}".format(tbl))
        #listing values from table
        t_lst = crsr.fetchall()
        t_lst1 = crsr1.fetchall() 

        #appending the list to tupple
        t_tup = tuple(t_lst)
        t_tup1 = tuple(t_lst1)

        #hasing the tupple
        t_h = hash(t_tup)
        t_h1 = hash(t_tup1)


        if t_h == t_h1:
            t_H = str(t_h+t_h1)
            t_md = hashlib.md5(t_H.encode()).hexdigest()

            rpt.append(f'THE MD5 Hash : {t_md}')
            rpt.append(f'All Values found in both {db1_dtbs} , {db2_dtbs} Databases')
            rpt.append(f'length of DB1 rows {len(t_lst)}, DB2 rows {len(t_lst1)}')

            if(len(t_lst)==len(t_lst1)):

                rpt.append('Comparing Random Rows')
                r = random.randint(0,len(t_lst1))
                n = r
                rpt.append(f'Random row no :{n}')
                r1 = t_lst1[n]
                r2 = t_lst1[n]
                rpt.append(f'DB-1 Row : {r1}')
                rpt.append(f'DB-2 Row : {r2}')
                rt1 = tuple(r1)
                rt2 = tuple(r2)
                rh1 = hash(rt1)
                rh2 = hash(rt2)
                if rh1 == rh2 or rt1 == rt2:
                    rpt.append('Row Matched')
                else:
                    rpt.append('Row Not Matched')
            else:
                rpt.append(f'Row count Not Matched DB1 rows {len(t_lst)}, DB2 rows {len(t_lst1)}')
    
        else:
            rpt.append('The tables values not matched')
            if len(t_lst)==len(t_lst1):
                rpt.append('maunal DVT runing...')
                for i in range(len(t_lst)):
                    r1 = t_lst[i]
                    r2 = t_lst1[i]
                    rt1 = tuple(r1)
                    rt2 = tuple(r2)
                    rh1 = hash(rt1)
                    rh2 = hash(rt2)
                    if rh1 != rh2 and r1 != r2:
                        rpt.append(f'Row No {i} Not Matched')
                        rpt.append(f'DB-1 Row : {r1}')
                        rpt.append(f'DB-2 Row : {r2}')

            else:
                rpt.append(f'No of Rows not Matched \nDB-1 Rows :{len(t_lst)}\nDB-2 Rows :{len(t_lst1)}')

else :
    rpt.append('Connections Not Established. Kindly Check the Connection Details')
    ext()

dt = datetime.datetime.now()
xt = dt.strftime("%a_%d-%b-%Y_%I-%M_%p")
file = f'559\Project\DVT-Report_{xt}.txt'

with open(file, 'w') as f:
    for item in rpt:
        f.write(str(item) + '\n')