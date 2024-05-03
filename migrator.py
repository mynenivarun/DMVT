from cons import *
import pymysql
import datetime

def ext():
    source_cursor.close()
    target_cursor.close()
    source_conn.close()
    target_conn.close()
    rpt.append('Closing....')

rpt = []

# Source database connection
source_conn = pymysql.connect(host=db1_host, database=db1_dtbs, user=db1_user, password=db1_pswd)
source_cursor = source_conn.cursor()

# Target database connection
target_conn = pymysql.connect(host=db2_host, user=db2_user, password=db2_pswd)
target_cursor = target_conn.cursor()

rpt.append(f'Databases : Source - {db1_host}, Target - {db2_host}')

if source_conn.open and target_conn.open:
    rpt.append('Connections Established')

    # Check if the target database exists, create it if necessary
    target_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db2_dtbs}")
    target_cursor.execute(f"USE {db2_dtbs}")

    source_cursor.execute("SHOW TABLES")
    tables = source_cursor.fetchall()

    for table in tables:
        table_name = table[0]
        rpt.append(f'Migrating Table: {table_name}')

        # Fetch data from the source table
        source_cursor.execute(f"SELECT * FROM {table_name}")
        data = source_cursor.fetchall()

        # Get the column names and data types from the source table
        source_cursor.execute(f"""
            SELECT COLUMN_NAME, COLUMN_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = '{db1_dtbs}' AND TABLE_NAME = '{table_name}'
        """)
        columns = source_cursor.fetchall()

        # Create the table in the target database if it doesn't exist
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for column in columns:
            column_name = column[0]
            column_type = column[1]
            create_table_query += f"{column_name} {column_type}, "
        create_table_query = create_table_query.rstrip(', ') + ")"
        target_cursor.execute(create_table_query)

        # Insert the data into the target table
        column_names = [column[0] for column in columns]
        insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['%s'] * len(column_names))})"
        target_cursor.executemany(insert_query, data)
        target_conn.commit()

        rpt.append(f'Migrated {len(data)} rows from {table_name}')

    rpt.append('Migration Completed')

else:
    rpt.append('Connections Not Established. Kindly Check the Connection Details')
    ext()

dt = datetime.datetime.now()
xt = dt.strftime("%a_%d-%b-%Y_%I-%M_%p")
file = f'559\Project\DMT-Report_{xt}.txt'

with open(file, 'w') as f:
    for item in rpt:
        f.write(str(item) + '\n')