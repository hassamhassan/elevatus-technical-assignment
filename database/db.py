import sys

from configurations.config import settings
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase
)


class Database:
    _instance = None

    def __new__(cls) -> AsyncIOMotorDatabase:
        """
        Singleton implementation for the Database class.

        Returns:
            Database: The Database instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = AsyncIOMotorClient(settings.MONGODB_URL)

            if "pytest" in sys.modules:
                cls._instance.db = cls._instance.client.elevatus_test
            else:
                cls._instance.db = cls._instance.client.elevatus

        return cls._instance

    @classmethod
    async def get_collection(cls, collection_name) -> AsyncIOMotorCollection:
        """
        Get a collection from the database.

        Args:
            collection_name: str - The name of the collection.

        Returns:
            AsyncIOMotorCollection: The specified collection.
        """
        db_instance: AsyncIOMotorDatabase = cls().__new__(cls)
        return db_instance.db[collection_name]

    @classmethod
    def drop_database(cls):
        """
        Drop the entire database.
        """
        cls()._instance.client.drop_database(cls()._instance.db.name)


database: Database = Database()
