import sqlite3
import os

class Database:
    def __init__(self) -> None:
        self.__dbFile = os.path.join(os.getenv("DATABASE_PATH"), "GetWeather", "users.db")
       
        self.__conn = sqlite3.connect(self.__dbFile)
        self.__cursor = self.__conn.cursor()

    def userExists(self, uID: str) -> bool:

        # Return does user exists
        query = "select id from usersInfo where id = ?"
        res = self.__cursor.execute(query, (uID,)).fetchone()
        return bool(res)

    def updateNotificationStatus(self, uID: str, status: bool):

        # Update notification status
        query = "update usersInfo set notifications = ? where id = ?"
        self.__cursor.execute(query, (status, uID))
    
        self.__conn.commit()
        
    def updateUnitSystem(self, uID: str, unitSystem: str):
        
        # Update subscription status
        query = "update usersInfo set unitSystem = ? where id = ?"
        self.__cursor.execute(query, (unitSystem, uID))
        
        self.__conn.commit()

    def getUnitSystemFromUser(self, uID: str) -> str:
        
        # Obtain unit system from user with specific uID:
        query = "select unitSystem from usersInfo where id = ?"
        res = self.__cursor.execute(query, (uID,)).fetchone()[0]

        return str(res)

    def getCommand(self, uID: str) -> str:

        # Obtain command
        query = "select command from usersInfo where id = ?"
        res = self.__cursor.execute(query, (uID,)).fetchone()[0]

        return str(res)
    
    def resetCommand(self, uID: str):

        # Reset command
        query = "update usersInfo set command = ? where id = ?"
        self.__cursor.execute(query, ("", uID))

        self.__conn.commit()
        
    def setCommand(self, uID: str, chain: str):
        
        # Return requested command
        query = "update usersInfo set command = ? where id = ?"
        self.__cursor.execute(query, (chain, uID))
        
        self.__conn.commit()

    def getFeaturedPlaces(self, uID: str) -> list[str]:

        # Obtain featured places for specific user
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
            print(f"Updated {updated}")

        query = "update usersInfo set featuredPlaces = ? where id = ?"
        self.__cursor.execute(query, (updated, uID))

        self.__conn.commit()

    def addNewUser(self, uID: str, unitSystem="metric"):

        # Add user to database:
        query = "insert into usersInfo values (?, ?, ?, ?)"
        self.__cursor.execute(query, (uID, unitSystem, False, ""))
        self.__conn.commit()


    def close(self):
        
        # Close connection
        self.__conn.close()
