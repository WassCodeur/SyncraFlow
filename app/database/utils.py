import json
from psycopg.sql import SQL, Identifier
from psycopg.types.json import Jsonb
from app.core.config import logger


def auto_pars_json(value):
    """Automatically parse JSON strings to Python objects, if the value is a string and can be parsed as JSON,it will be converted to the corresponding Python object. Otherwise, the original value will be returned.

    Parameters
    ----------
    value : str or any
        The value to be parsed. If it's a string, the function will attempt to parse it as JSON. If it's not a string, it will be returned as is.

    Returns
    -------
    any
        The parsed Python object if the input was a JSON string, or the original value if it was not a string or could not be parsed as JSON.
    """
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    else:
        return value


def generate_sql_query(table, q_type='SELECT', columns=None, comparison_type='eq', comparison_elems: dict = None, new_data: dict = None, order_by: str = None):
    """To generate SQL query accoring to the given type and parameters, it supports SELECT, UPDATE and DELETE queries.

    Parameters
    ----------
    table : str
        The name of the table to query.
    q_type : str, optional
        The type of the query to generate, it can be "SELECT", "UPDATE" or "DELETE". The default is "SELECT".
    columns : List, optional
        A list of column names to retrieve for SELECT queries, by default None (retrieves all columns).
    comparison_type : str, optional
        The type of comparison to use in the WHERE clause, it can be "eq" for equality, "gt" for greater than, "lt" for less than, etc. The default is "eq".
    comparison_elems : dict, optional
        A dictionary of column-value pairs to use in the WHERE clause for filtering the results. The keys are the column names and the values are the corresponding values to compare against. The default is None (no filtering).
    new_data : dict, optional
        A dictionary of column-value pairs to use in the SET clause for UPDATE queries. The keys are the column names and the values are the new values to set. The default is None (no
    new data for UPDATE queries).
    order_by : str, optional
        The column name to order the results by, by default None (no ordering).

    Returns
    -------
    tuple
        A tuple containing the generated SQL query as a psycopg.sql.SQL object and a tuple of values to be used as parameters in the query execution. The SQL query is constructed based on the
    """
    if columns:
        sql_columns = SQL(', ').join(map(Identifier, columns))
    else:
        sql_columns = SQL('*')

    if order_by:
        order_by_sql = SQL(" ORDER BY {}").format(Identifier(order_by))
    else:
        order_by_sql = SQL('')

    conditions = []
    values = []
    query = ""

    for col, val in comparison_elems.items():
        if comparison_type == 'eq':
            conditions.append(SQL("{} = %s").format(Identifier(col)))

        if isinstance(val, dict):
            val = Jsonb(val)

        values.append(val)

    if not conditions:
        raise ValueError()

    conditions_sql = SQL(" AND ").join(conditions)

    if q_type == "SELECT":
        query = SQL("SELECT {} FROM {} WHERE {}").format(
            sql_columns,
            Identifier(table),
            conditions_sql,
            order_by_sql
        )
    elif q_type == "UPDATE" and new_data:
        sets = []
        vals = []
        for col, val in new_data.items():
            sets.append(SQL("{} = %s").format(Identifier(col)))
        if isinstance(val, dict):
            val = Jsonb(val)

        vals.append(val)

        values = vals + values
        if not sets:
            raise ValueError()

        sets_sql = SQL(', ').join(sets)

        query = SQL(
            "UPDATE {} SET {} WHERE {} RETURNING *"
        ).format(
            Identifier(table),
            sets_sql,
            conditions_sql
        )
    elif q_type == "DELETE":
        query = SQL("DELETE FROM {} WHERE {} RETURNING id").format(
            Identifier(table),
            conditions_sql
        )
    return query, tuple(values)
