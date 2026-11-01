from database.DB_connect import DBConnect
from model.artista import Artista

class DAO():

    @staticmethod
    def getNodi():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT a.ArtistId AS aId, a.Name AS name
                FROM artist a, album ab, track t
                WHERE a.ArtistId = ab.ArtistId AND ab.AlbumId = t.AlbumId
                """

        cursor.execute(query)

        for row in cursor:
            a = Artista(row["aId"], row["name"])
            results.append(a)
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCoppia():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT ab.ArtistId as aId, p.PlaylistId as pId
                FROM album ab, track t, playlisttrack p
                WHERE ab.AlbumId = t.AlbumId AND t.TrackId = p.TrackId
                ORDER BY ab.ArtistId, p.PlaylistId
                """

        cursor.execute(query)

        for row in cursor:
            results.append((row["aId"],row["pId"]))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getTracks():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT ab.ArtistId as abI, t.TrackId as tId 
                FROM album ab, track t
                WHERE ab.AlbumId = t.AlbumId 
                ORDER BY ab.ArtistId, t.TrackId
                """

        cursor.execute(query)

        for row in cursor:
            results.append((row["abI"],row["tId"]))
        cursor.close()
        conn.close()
        return results

