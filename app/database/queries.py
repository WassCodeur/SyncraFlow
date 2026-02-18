from app.database.connection import get_conn
from psycopg.sql import SQL, Identifier
from psycopg.types.json import Json, Jsonb
from psycopg.rows import dict_row, namedtuple_row
from app.core.config import setup_logging
from app.database.utils import auto_pars_json, generate_sql_query
from typing import List
from app.core.exceptions import AlreadyExistsError, NotFoundError


# TODO:  handle exceptions properly, also add logging for better debugging and monitoring.

logger = setup_logging()


def insert(table, data):
    """Insert data in the database table.

    Parameters
    ----------
    table : str
        The name of the table to insert into.
    data : dict
        A dictionary of column-value pairs to insert into the table.

    Returns
    -------
    bool
        True if the insertion was successful, False otherwise.
    """
    try:

        data_exist = get_one(table, filter=data)
        if data_exist:
            raise AlreadyExistsError("Resource already exists")

        columns = data.keys()
        values = [Jsonb(v) if isinstance(v, dict)
                  else v for v in data.values()]

        placeholders_list = [SQL('%s') for _ in columns]
        placeholders = SQL(', ').join(placeholders_list)
        query = SQL("INSERT INTO {} ({}) VALUES ({})").format(
            Identifier(table),
            SQL(', ').join(map(Identifier, columns)),
            placeholders
        )

        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query, values)
            conn.commit()
        return True
    except Exception as e:
        logger.error(e)
        raise


def get_all(table, columns: List = None):
    """Retrieve all in a table with the specified columns, if no column is specified, all columns will be retrieved.

    Parameters
    ----------
    table : str
        The name of the table to query.
    columns : List, optional
        A list of column names to retrieve, by default None (retrieves all columns).
    Returns
    -------
    List[dict]
        A list of dictionaries representing the retrieved rows, or an empty list if no matching rows are found.
    """
    try:

        if columns:
            query = SQL("SELECT ({}) FROM {}").format(
                SQL(', ').join(map(Identifier, columns)),
                Identifier(table)
            )
        else:
            query = SQL("SELECT * FROM {}").format(
                Identifier(table)
            )
        with get_conn() as conn:

            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                if not rows:
                    return False

                data = [
                    {k: auto_pars_json(v) for k, v in row.items()} for row in rows
                ]

                return data

    except Exception as e:
        logger.error(e)
        raise


def get_one(table, columns: List = None, filter: dict = None):
    """retrieve one item in the table.

    Parameters
    ----------
    table : str
        The name of the table to query.
    columns : List, optional
        A list of column names to retrieve, by default None (retrieves all columns).
    filter : dict, optional
        A dictionary of column-value pairs to filter the rows to retrieve, by default None (retrieves all rows).

    Returns
    -------
    dict
        A dictionary representing the retrieved row, or an empty dictionary if no matching row is found.
    """
    query, values = generate_sql_query(
        table, columns=columns, comparison_elems=filter)

    try:
        with get_conn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, values)
                row = cur.fetchone()

                if not row:
                    return False

                data = {
                    k: auto_pars_json(v) for k, v in row.items()
                }

                return data

    except Exception as e:
        logger.error(e)
        raise NotFoundError("Resource not found") from e


def update(table,  filter: dict = None, new_data: dict = None):
    """Update a particular item in the table.

    Parameters
    ----------
    table : str
        The name of the table to update.
    filter : dict, optional
        A dictionary of column-value pairs to filter the rows to update, by default None.
        new_data : dict, optional
        A dictionary of column-value pairs to update the filtered rows with, by default None.

    Returns
    -------
    bool
        True if the update was successful, False otherwise.
    """
    try:
        query, values = generate_sql_query(
            table, q_type='UPDATE', comparison_elems=filter, new_data=new_data)
        data_exist = get_one(table=table, filter=filter)
        if not data_exist:
            raise NotFoundError("Resource not found")
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query, values)
                conn.commit()
                return True
    except Exception as e:
        logger.error(e)
        raise e


def delete(table, filter: dict = None):
    """Delete a particular item in the table.

     Parameters
     ----------
    table : str
        The name of the table to delete from.
    filter : dict, optional
        A dictionary of column-value pairs to filter the rows to delete, by default None.

    Returns
    -------
    bool
        True if the deletion was successful, False otherwise.
    """
    try:
        query, values = generate_sql_query(
            table, q_type='DELETE', comparison_elems=filter)

        data_exist = get_one(table, filter=filter)

        if not data_exist:
            raise NotFoundError("Resource not found")

        with get_conn() as conn:
            with conn.cursor() as cur:
                print(cur.execute(query, values))
                return True

    except Exception as e:
        logger.error(e)
        raise e
