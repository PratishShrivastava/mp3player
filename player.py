import model
from pygame import mixer
from tkinter import filedialog
import os
from mutagen.mp3 import MP3


class player:
    def __init__(self):
        self.song_dict = {}
        self.audio_tag = None
        print("audio:", self.audio_tag)
        mixer.init()
        self.my_model = model.model()
        print("model:", self.my_model)

    def get_db_status(self):
        return self.my_model.get_db_status()

    def get_song_count(self):
        return len(self.song_dict)

    def close_player(self):
        mixer.music.stop()
        self.my_model.close_db_connection()

    def set_volume(self, volume_level):
        mixer.music.set_volume(volume_level)

    def add_song(self):
        song_list=[]
        song_paths = filedialog.askopenfilenames(title="Select your song" ,filetypes=[("mp3 files", "*.mp3")])
        if song_paths == " ":
            return
        for song_path in song_paths:
            song_name = os.path.basename(song_path)
            if song_name in self.my_model.song_dict:
                song_list.append("song already present")
            else:
                song_list.append(song_name)
            self.my_model.add_song(song_name, song_path)
        return song_list






    def remove_song(self, song_name):
        self.my_model.remove_song(song_name)

    def get_song_length(self, song_name):
        self.song_path = self.my_model.get_song_path(song_name)
        self.audio_tag = MP3(self.song_path)
        song_length = self.audio_tag.info.length
        return song_length

    def play_song(self):
        mixer.quit()
        mixer.init(frequency=self.audio_tag.info.sample_rate)
        mixer.music.load(self.song_path)
        mixer.music.play()

    def stop_song(self):
        mixer.music.stop()

    def pause_song(self):
        mixer.music.pause()

    def unpause_song(self):
        mixer.music.unpause()


    def set_song_pos(self,pos):
        mixer.music.set_pos(pos)



    def add_song_to_fav(self, song_name):
        song_path = self.my_model.get_song_path(song_name)
        result = self.my_model.add_song_to_fav(song_name, song_path)
        return result

    def load_song_from_fav(self):
        result = self.my_model.load_song_from_fav()
        return result, self.my_model.song_dict

    def remove_songs_from_favourites(self, song_name):
        result = self.my_model.remove_songs_from_favourites(song_name)
        return result
