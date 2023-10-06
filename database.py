import sqlite3
import os

class Database:
    def __init__(self) -> None:
        self.__dbFile = os.path.join(os.getenv("DATABASE_PATH"), "GetWeather", "users.db")
       
        self.__conn = sqlite3.connect(self.__dbFile)
        self.__cursor = self.__conn.cursor()

    def userExists(self, uID: str) -> bool:

        with self.__conn:
            # Return does user exists
            query = "select id from usersInfo where id = ?"
            res = self.__cursor.execute(query, (uID,)).fetchone()
            return bool(res)

    def updateNotificationStatus(self, uID: str, status: bool):

        with self.__conn:
            # Update notification status
            query = "update usersInfo set notifications = ? where id = ?"
            self.__cursor.execute(query, (status, uID))
        
    def updateUnitSystem(self, uID: str, unitSystem: str):
        
        with self.__conn:
            # Update subscription status
            query = "update usersInfo set unitSystem = ? where id = ?"
            self.__cursor.execute(query, (unitSystem, uID))

    def getUnitSystemFromUser(self, uID: str) -> str:
        
        with self.__conn:
            # Obtain unit system from user with specific uID:
            query = "select unitSystem from usersInfo where id = ?"
            res = self.__cursor.execute(query, (uID,)).fetchone()[0]

            return str(res)

    def getCommand(self, uID: str) -> str:

        with self.__conn:
            # Obtain command
            query = "select command from usersInfo where id = ?"
            res = self.__cursor.execute(query, (uID,)).fetchone()[0]

            return str(res)
    
    def resetCommand(self, uID: str):

        with self.__conn:
            # Reset command
            query = "update usersInfo set command = ? where id = ?"
            self.__cursor.execute(query, ("", uID))
        
    def setCommand(self, uID: str, chain: str):
        
        with self.__conn:
            # Return requested command
            query = "update usersInfo set command = ? where id = ?"
            self.__cursor.execute(query, (chain, uID))

    def getFeaturedPlaces(self, uID: str) -> list[str]:

        # Obtain featured places for specific user
        with self.__conn:
            query = "select featuredPlaces from usersInfo where id = ?"
            res = self.__cursor.execute(query, (uID,)).fetchone()[0].split(":")

            res = list(filter(lambda place: place if place else False, res))

            return res
    
    def removePlaceFromFeatured(self, uID: str, place: str):

        # Get existing places
        existing = self.getFeaturedPlaces(uID=uID)

        place = place.split(":")
        # Remove places from existing

        for pls in place:

            if pls in existing:
                existing.remove(pls)

        existing = ":".join(existing)

        self.addPlaceToFeaturedList(uID=uID, place=existing, appendMode=False)

    def addPlaceToFeaturedList(self, uID: str , place: str, appendMode=True):

        with self.__conn:
            updated = place
            if appendMode:
                # Get existing places
                existing = self.getFeaturedPlaces(uID=uID)

                # Join new place to the end
                toAdd = place.split(":")
                toAdd = [pls.strip(" ") for pls in toAdd]
                existing.extend(toAdd)
                existing = list(filter(lambda pls: pls if pls else False, existing))
                updated = ":".join(existing)

            query = "update usersInfo set featuredPlaces = ? where id = ?"
            self.__cursor.execute(query, (updated, uID))

    def addNewUser(self, uID: str, unitSystem="metric"):

        with self.__conn:
            # Add user to database:
            query = "insert into usersInfo values (?, ?, ?, ?)"
            self.__cursor.execute(query, (uID, unitSystem, False, ""))


    def close(self):
        
        # Close connection
        self.__conn.close()
