import pandas as pd


def insert(table, values, cursor, connection):
    query_text = "insert into {0} values {1};".format(table, values)
    cursor.execute(query_text)
    connection.commit()


def update(table, values, conn):
    pass


def delete(table, values, conn):
    pass


def select(table, columns, connection):
    query_text = "select {0} from {1};".format(columns, table)
    selected_data = pd.read_sql(query_text, connection)
    selected_data = selected_data[(selected_data.name_value != '') | (selected_data.surname_value != '') | \
                    (selected_data.middle_name_value != '') | (selected_data.street_value != '')]

    selected_data.drop_duplicates(subset=['telephone'], inplace=True)
    for col in selected_data:
        selected_data[col] = selected_data[col].apply(lambda x: x.replace(' ', '') if (type(x) is str) else x)
    return selected_data
