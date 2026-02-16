from app.database.connection import get_conn
from psycopg.sql import SQL, Identifier
from psycopg.types.json import Json, Jsonb
from psycopg.rows import dict_row, namedtuple_row
from app.core.config import setup_logging
from app.database.utils import auto_pars_json, generate_sql_query


# TODO:  handle exceptions properly, also add logging for better debugging and monitoring.

logger = setup_logging()


def insert(table, data):
    try:
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
        return False


def get_all(table, columns=None, eq={}):
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

                data = [
                    {k: auto_pars_json(v) for k, v in row.items()} for row in rows
                ]

                return data

    except Exception as e:
        logger.error(e)
        raise


def get_one(table, columns=None, filter: dict = None):
    query, values = generate_sql_query(
        table, columns=columns, comparison_elems=filter)

    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, values)

            row = cur.fetchone()
            data = {
                k: auto_pars_json(v) for k, v in row.items()
            }

            return data


def update(table,  filter: dict = None, new_data: dict = None):
    query, values = generate_sql_query(
        table, q_type='UPDATE', comparison_elems=filter, new_data=new_data)

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)


def delete(table, filter: dict = None):
    query, values = generate_sql_query(
        table, q_type='DELETE', comparison_elems=filter)

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
