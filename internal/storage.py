from tinydb import TinyDB, Query
from typing import Union


class Storage:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.__con: Union[TinyDB, None] = None

    @property
    def con(self):
        if not self.__con:
            return TinyDB(self.db_name)
        return self.__con

    def get_all_by_fields(self, fields: list[str]) -> list[dict]:
        q = Query()
        query = None

        for field in fields:
            if query is None:
                query = getattr(q, field).exists()

            else:
                query &= getattr(q, field).exists()
        try:
            return self.con.search(query)
        except Exception as e:
            raise Exception(f"failed to query {e}")


storage = Storage(db_name="db.json")
