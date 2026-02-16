import json
from psycopg.sql import SQL, Identifier

# TODO:  handle exceptions properly, also add logging for better debugging and monitoring.


def auto_pars_json(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    else:
        return value


def generate_sql_query(table, q_type='SELECT', columns=None, comparison_type='eq', comparison_elems: dict = None, new_data: dict = None):
    if columns:
        sql_columns = SQL(', ').join(map(Identifier, columns))
    else:
        sql_columns = SQL('*')

    conditions = []
    values = []
    query = "wertyj"

    for col, val in comparison_elems.items():
        if comparison_type == 'eq':
            conditions.append(SQL("{} = %s").format(Identifier(col)))

        values.append(val)

    if not conditions:
        raise ValueError()

    conditions_sql = SQL(" AND ").join(conditions)

    if q_type == "SELECT":
        query = SQL("SELECT {} FROM {} WHERE {}").format(
            sql_columns,
            Identifier(table),
            conditions_sql
        )
    elif q_type == "UPDATE" and new_data:
        sets = []
        vals = []
        for col, val in new_data.items():
            sets.append(SQL("{} = %s").format(Identifier(col)))
            vals.append(val)

        values = vals + values
        if not sets:
            raise ValueError()

        sets_sql = SQL(', ').join(sets)

        query = SQL(
            "UPDATE {} SET {} WHERE {}"
        ).format(
            Identifier(table),
            sets_sql,
            conditions_sql
        )
    elif q_type == "DELETE":
        query = SQL("DELETE FROM {} WHERE {}").format(
            Identifier(table),
            conditions_sql
        )
    return query, tuple(values)
