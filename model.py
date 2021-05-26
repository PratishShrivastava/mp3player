import cx_Oracle
from traceback import *
from cx_Oracle import connect


class model:
    def __init__(self):

        self.song_dict = {}
        print("song_dict:", self.song_dict)
        self.db_status = True
        print("db:", self.db_status)
        self.conn = None
        # print("conn:", self.conn)
        self.cur = None
        print("cur:", self.cur)
        try:
            self.conn=cx_Oracle.connect("mouzikka/music@127.0.0.1/xe")
            print("connected")
            self.cur=self.conn.cursor()
        except cx_Oracle.DatabaseError:
            self.db_status = False
            print("db error", format_exc())

    def get_db_status(self):
        return self.db_status
    def get_song_count(self):
        return len(self.song_dict)
    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
            print("cursor closed")
        if self.conn is not None:
            self.conn.close()
            print("connection closed")

    def add_song(self, song_name, song_path):
        self.song_dict[song_name] = song_path
        print("song added", self.song_dict[song_name])

    def get_song_path(self, song_name):
        return self.song_dict[song_name]

    def remove_song(self, song_name):
        self.song_dict.pop(song_name)
        print("After deleion", self.song_dict)

    def search_song_in_fav(self, song_name):
        self.cur.execute("select song_name from mysong where song_name=:1", (song_name,))
        song_tuple = self.cur.fetchone()
        if song_tuple is None:
            return False
        else:
            return False

    def add_song_to_fav(self, song_name, song_path):
        is_song_present = self.search_song_in_fav(song_name)
        if is_song_present == True:
            return "Song already present"
        self.cur.execute("select max(song_id) from mysong")
        last_song_id = self.cur.fetchone()[0]
        next_song_id = 1
        if last_song_id is not None:
            next_song_id = last_song_id + 1
        self.cur.execute("insert into mysong values (:1, :2, :3)", (next_song_id, song_name, song_path))
        self.conn.commit()
        return "song added to your fav"

    def load_song_from_fav(self):
        self.cur.execute("select song_name, song_path from mysong")
        songs_present = False
        for song_name, song_path in self.cur:
            self.song_dict[song_name] = song_path
            songs_present = True
        if songs_present:
            return "list populated from your fav"
        else:
            return "no songs populated from your fav"

    def remove_songs_from_favourites(self, song_name):
        self.cur.execute("delete from mysong where song_name=:1", (song_name,))
        count = self.cur.rowcount
        if count == 0:
            return "song not present in favorites"
        else:
            self.song_dict.pop(song_name)
            self.conn.commit()
            return "song deleted from fav"
mymodel = model()
print(mymodel)
