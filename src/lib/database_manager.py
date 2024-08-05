import sqlite3
def getDBConnection():
    return sqlite3.connect("../data/database.db")

def getCursor(connection):
    return connection.cursor()

def closeDatabaseConnection(connection):
    connection.commit()
    connection.close()

def createTable(table_name, cursor):
    if table_name == "webtoon":
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS webtoon (
                    webtoon_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    total_episode INTEGER
                )
        """
        )
    elif table_name == "episode":
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS episode (
            episode_id TEXT PRIMARY KEY,
            episode_number INTEGER NOT NULL,
            episode_url TEXT NOT NULL,
            total_panels INTEGER,
            webtoon_id TEXT,
            FOREIGN KEY (webtoon_id) REFERENCES webtoon (webtoon_id)
            )
        """
        )
    elif table_name == "panel":
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS panel (
                    panel_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    episode_id TEXT,
                    panel_number INTEGER NOT NULL,
                    image_url TEXT NOT NULL,
                    FOREIGN KEY (episode_id) REFERENCES episode (episode_id)
                )
            """
        )

def addWebtoonData(connection,cursor,params):
    cursor.execute("INSERT INTO webtoon (webtoon_id, name, total_episode) VALUES (?,?,?)", (params[0],params[1],params[2]))
    connection.commit()

def addEpisodeData(connection,cursor,params):
    cursor.execute("INSERT INTO episode (episode_id, episode_number, episode_url,total_panels,webtoon_id) VALUES (?,?,?,?,?)", (params[0],params[1],params[2],params[3],params[4]))
    connection.commit()

def addPanelData(connection,cursor,params):
    cursor.execute("INSERT INTO panel (episode_id, panel_number,image_url) VALUES (?,?,?)", (params[0],params[1],params[2]))
    connection.commit()

def initDatabase(connection, cursor):
    table_names = ["webtoon", "episode", "panel"]
    for table_name in table_names:
        createTable(table_name=table_name, cursor=cursor)
    connection.commit()


