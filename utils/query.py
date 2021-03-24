import pandas as pd
from utils.preparation_data import remove_spaces


def insert(table, values, cursor, connection):
    query_text = "insert into {0} values {1};".format(table, values)
    cursor.execute(query_text)
    connection.commit()


def update(table, new_values, cursor,  connection, condition=None):
    if condition is None:
        query_text = "update {0} set {1};".format(table, new_values)
    else:
        query_text = "update {0} set {1} where {2};".format(table, new_values, condition)
    print(query_text)
    cursor.execute(query_text)
    connection.commit()


def delete(table,  cursor, connection, condition=None):
    if condition is None:
        query_text = "delete from {0}".format(table)
    else:
        query_text = "delete from {0} where {1}".format(table, condition)
    print(query_text)
    cursor.execute(query_text)
    connection.commit()


def select(table, columns, connection, condition=None):
    if condition is None:
        query_text = "select {0} from {1};".format(columns, table)
    else:
        query_text = "select {0} from {1} where {2};".format(columns, table, condition)
    print(query_text)
    selected_data = pd.read_sql(query_text, connection)
    selected_data.fillna('', inplace=True, axis=0)
    selected_data.drop_duplicates(inplace=True)
    for col in selected_data:
        selected_data[col] = selected_data[col].apply(lambda x: remove_spaces(x) if (type(x) is str) else int(x))
    return selected_data

