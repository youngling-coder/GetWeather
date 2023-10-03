import sqlite3
import os

class Database:
    def __init__(self) -> None:
        self.__dbFile = os.path.join(os.getenv("DATABASE_PATH"), "GetWeather", "users.db")
       
        self.__conn = sqlite3.connect(self.__dbFile)
        self.__cursor = self.__conn.cursor()

    def userExists(self, uID: str) -> bool:

        # Return does user exists
        with self.__conn:
            query = "select id from usersInfo where id = ?"
            res = self.__cursor.execute(query, (uID,)).fetchone()
            return bool(res)

    def updateNotificationStatus(self, uID: str, status: bool):

        # Update notification status
        with self.__conn:
            query = "update usersInfo set notifications = ? where id = ?"
            return self.__cursor.execute(query, (status, uID))
        

    def updateUnitSystem(self, uID: str, unitSystem: str):
                # Update subscription status
        with self.__conn:
            query = "update usersInfo set unitSystem = ? where id = ?"
            return self.__cursor.execute(query, (unitSystem, uID))
        

    def getUnitSystemFromUser(self, uID: str) -> str:
        
        # Obtain unit system from user with specific uID:
        with self.__conn:
            query = "select unitSystem from usersInfo where id = ?"
            res = self.__cursor.execute(query, (uID,)).fetchone()[0]

            return str(res)

    def addNewUser(self, uID: str, unitSystem="metric"):

        # Add user to database
        with self.__conn:
            query = "insert into usersInfo values (?, ?, ?, ?)"
            return self.__cursor.execute(query, (uID, unitSystem, False, ""))


    def close(self):
        
        # Close connection
        self.__conn.close()
