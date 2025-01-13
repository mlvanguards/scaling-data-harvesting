import os
import pymongo.errors

from pymongo import MongoClient


class DatabaseConnection:

    _client: MongoClient = None

    @classmethod
    def connect(cls):
        if cls._client is None:
            try:
                cls._client = MongoClient(os.getenv('DATABASE_URI', "mongodb+srv://lXFEMtjH:3hfh5QC4wbAztExO@eu-central-1.2dfzz.mongodb.net/genezio-case-study-db"))
            except pymongo.errors.ConnectionFailure as exc:
                print(f"Database failed connection: {exc}")
                raise
            print("Created connection to database")

    @classmethod
    def get_database(cls, name: str):
        if cls._client is None:
            cls.connect()
        return cls._client[name]

    @classmethod
    def close(cls):
        if cls._client is not None:
            cls._client.close()
            cls._client = None

        print("Closed connection to database")


database = DatabaseConnection.get_database(os.getenv('DATABASE_NAME', "genezio-case-study-db"))
