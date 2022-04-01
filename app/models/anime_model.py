from app.models import DatabaseConnector
from psycopg2 import sql


class Anime(DatabaseConnector):
    def __init__(self, **kwargs):
        self.anime = str(kwargs["anime"]).title()
        self.seasons = kwargs["seasons"]
        self.released_date = kwargs["released_date"]

    @classmethod
    def create_table(cls):

        query = """
            CREATE TABLE IF NOT EXISTS ka_animes(
                id              BIGSERIAL       PRIMARY KEY,
                anime           VARCHAR(100)    NOT NULL    UNIQUE,
                seasons         INTEGER         NOT NULL,
                released_date   DATE            NOT NULL
            );
        """
        cls.cur.execute(query)
        cls.conn.commit()

    @staticmethod
    def check_data(data):
        anime_columns = [
            "anime",
            "seasons",
            "released_date",
        ]

        incorrect_keys = []
        for value in data:
            if value not in anime_columns:
                incorrect_keys.append(value)

        return (
            False
            if not incorrect_keys
            else {
                "available_keys": anime_columns,
                "Incorrect_keys_sent": incorrect_keys,
            }
        )

    @classmethod
    def serialize(cls, data: tuple):
        anime_columns = [
            "id",
            "anime",
            "seasons",
            "released_date",
        ]

        return dict(zip(anime_columns, data))

    @classmethod
    def read_animes(cls):
        cls.start_conn_cur()
        cls.create_table()

        query = "SELECT * FROM ka_animes;"

        cls.cur.execute(query)

        animes = cls.cur.fetchall()

        cls.end_conn_cur()

        return animes

    @classmethod
    def read_anime(cls, anime_id):
        cls.start_conn_cur()
        cls.create_table()

        query = "SELECT * FROM ka_animes WHERE id = %s;"

        query_value = str(anime_id)

        cls.cur.execute(query, (query_value))

        anime = cls.cur.fetchone()

        cls.end_conn_cur()

        return anime

    def create_anime(self):
        self.start_conn_cur()

        query = """
            INSERT INTO ka_animes
                (anime, seasons, released_date)
            VALUES
                (%s,%s,%s)
            RETURNING *
        """

        query_values = tuple(self.__dict__.values())

        self.cur.execute(query, query_values)
        self.conn.commit()

        inserted_anime = self.cur.fetchone()

        self.end_conn_cur()

        return inserted_anime

    @classmethod
    def patch_anime(cls, anime_id, data):
        cls.start_conn_cur()

        columns = [sql.Identifier(key) for key in data.keys()]
        values = [sql.Literal(value) for value in data.values()]

        query = sql.SQL(
            """
        UPDATE
            ka_animes
        SET
            ({columns}) = ROW({values})
        WHERE
            id = {id}
        RETURNING *;
        """
        ).format(
            id=sql.Literal(anime_id),
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
        )

        cls.cur.execute(query)
        cls.conn.commit()

        updated_anime = cls.cur.fetchone()

        cls.end_conn_cur()

        return updated_anime

    @classmethod
    def delete_anime(cls, anime_id):
        cls.start_conn_cur()

        query = "DELETE FROM ka_animes WHERE id = %s RETURNING *;"

        query_value = anime_id

        cls.cur.execute(query, (query_value,))
        cls.conn.commit()

        deleted_serie = cls.cur.fetchone()

        cls.end_conn_cur()

        return deleted_serie
