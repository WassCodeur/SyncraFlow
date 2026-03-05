from psycopg.sql import SQL, Identifier
from psycopg.types.json import Jsonb
from psycopg.rows import dict_row
from psycopg.errors import UndefinedColumn
from psycopg import Connection
from typing import List
from app.core.config import logger
from app.database.utils import auto_pars_json, generate_sql_query
from fastapi import HTTPException, status


def insert(db_conn: Connection, table, data):
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

    data_exist = get_one(db_conn, table, filter=data)
    if data_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This Resource already exists"
        )

    try:
        columns = data.keys()
        values = [Jsonb(v) if isinstance(v, dict)
                  else v for v in data.values()]

        placeholders_list = [SQL('%s') for _ in columns]
        placeholders = SQL(', ').join(placeholders_list)
        query = SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(
            Identifier(table),
            SQL(', ').join(map(Identifier, columns)),
            placeholders
        )
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, values)

            db_conn.commit()
            new_added = cur.fetchone()

            return new_added

    except UndefinedColumn as e:
        logger.error("SQL Error: ", exc_info=True)
        db_conn.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error: Unknown or invalid column.")
    except Exception as e:
        logger.error("SQL Error: ", exc_info=True)
        db_conn.rollback()

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="An error occurred while processing the request.")


def get_all(db_conn: Connection, table, columns: List = None):
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

            with db_conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                if not rows:
                    return []

                data = [
                    {k: auto_pars_json(v) for k, v in row.items()} for row in rows
                ]

                return data
    except UndefinedColumn as e:
        logger.error("SQL error:", exc_info=True)
        db_conn.rollback()
        raise HTTPException(
            status_code=400, detail="Error: Unknown or invalid column.")

    except Exception as e:
        logger.error("SQL Error: ", exc_info=True)
        db_conn.rollback()
        raise HTTPException(
            status_code=400, detail="An error occurred while processing the request.")


def get_one(db_conn: Connection, table, columns: List = None, filter: dict = None):
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

        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, values)
            row = cur.fetchone()

            if not row:
                return {}

            data = {
                k: auto_pars_json(v) for k, v in row.items()
            }

            return data
    except UndefinedColumn as e:
        logger.error("SQL error:", exc_info=True)
        db_conn.rollback()
        print(e)
        raise HTTPException(
            status_code=400, detail="Error: Unknown or invalid column.")

    except Exception as e:
        logger.error("SQL error:", exc_info=True)
        db_conn.rollback()
        print(e)
        raise HTTPException(
            status_code=400, detail="An error occurred while processing the request.")


def get_all_by_filter(db_conn: Connection, table, columns: List = None, filter: dict = None):
    """retrieve all item in the table by filter.

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

        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, values)
            rows = cur.fetchall()

            data = []

            if not rows:
                return {}

            for row in rows:
                data.append({
                    k: auto_pars_json(v) for k, v in row.items()})

            return data
    except UndefinedColumn as e:
        logger.error("SQL error:", exc_info=True)
        db_conn.rollback()
        print(e)
        raise HTTPException(
            status_code=400, detail="Error: Unknown or invalid column.")

    except Exception as e:
        logger.error("SQL error:", exc_info=True)
        db_conn.rollback()
        print(e)
        raise HTTPException(
            status_code=400, detail="An error occurred while processing the request or no matching data found.")


def update(db_conn: Connection, table,  filter: dict = None, new_data: dict = None):
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
    data_exist = get_one(db_conn, table=table, filter=filter)
    if not data_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The ressource your trying to update doesn't exist"
        )

    try:
        query, values = generate_sql_query(
            table, q_type='UPDATE', comparison_elems=filter, new_data=new_data)

        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, values)
            db_conn.commit()
            updated_data = cur.fectchone()

            return updated_data

    except UndefinedColumn:
        logger.error("SQL error:", exc_info=True)
        db_conn.rollback()
        raise HTTPException(
            status_code=400, detail="Error: Unknown or invalid column.")

    except Exception as e:
        logger.error("SQL error:", exc_info=True)
        db_conn.rollback()
        raise HTTPException(
            status_code=400, detail="An error occurred while processing the request.")


def delete(db_conn: Connection, table, filter: dict = None):
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
    data_exist = get_one(db_conn, table, filter=filter)

    if not data_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The ressource your trying to delete doesn't exist"
        )

    try:
        query, values = generate_sql_query(
            table, q_type='DELETE', comparison_elems=filter)

        with db_conn.cursor() as cur:
            cur.execute(query, values)
            deleted_data_id = cur.fetchone()[0]
            return deleted_data_id

    except UndefinedColumn:
        logger.error("SQL error:", exc_info=True)
        db_conn.rollback()
        raise HTTPException(
            status_code=400, detail="Error: Unknown or invalid column.")

    except Exception as e:
        logger.error("SQL error:", exc_info=True)
        db_conn.rollback()
        raise HTTPException(
            status_code=400, detail="An error occurred while processing the request.")
