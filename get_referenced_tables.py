import mysql.connector

mysql_connection = mysql.connector.connect(host="localhost", user="root", password="password", database="mrms")

cursor = mysql_connection.cursor()


def get_related_tables(list_of_tables: list, original_table_list: list) -> list:
    related_tables_list = []
    for table in list_of_tables:
        sql_query = f"""SELECT 
            kcu.CONSTRAINT_NAME,
            kcu.TABLE_NAME AS referencing_table,
            kcu.COLUMN_NAME AS referencing_column,
            kcu.REFERENCED_TABLE_NAME AS referenced_table,
            kcu.REFERENCED_COLUMN_NAME AS referenced_column,
            kcu2.TABLE_NAME AS referenced_by_table
        FROM 
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
        JOIN 
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu2 
            ON kcu.REFERENCED_TABLE_NAME = kcu2.TABLE_NAME 
            AND kcu.REFERENCED_COLUMN_NAME = kcu2.COLUMN_NAME
        WHERE 
            kcu.TABLE_NAME = '{table}'
            AND kcu.TABLE_SCHEMA = 'mrms';"""

        cursor.execute(sql_query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # print(f'data: {data}')
        # print(f'columns: {columns}')

        for row in data:
            related_tables_list.extend(
                row[i]
                for i in range(len(data[0]))
                if columns[i] == 'referenced_table' and row[i] not in list_of_tables and row[i] in original_table_list
            )

        # print(f'related_tables_list: {related_tables_list}')

    return list(set(list_of_tables + related_tables_list))

# final_list_of_tables = get_support_tables(list_of_tables=['employee_external_link', 'states'])
