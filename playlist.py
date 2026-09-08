class Playlist:
    def __init__(self):
        self.songs = []
    
    def add_song(self, name, duration):
        song = {
            "name": name,
            "duration": duration
        }

        self.songs.append(song)
    
    def remove_song(self, name):
        for song in self.songs:
            if song["name"] == name:
                self.songs.remove(song)
                return

        print("Такой песни нет :(")
    
    def total_duration(self):
        total = 0

        for song in self.songs:
            total += song["duration"]

        return total
    
    def __len__(self):
        return len(self.songs)
    
    def show_songs(self):
        if len(self.songs) == 0:
            print("Плейлист пуст")
            return

        for song in self.songs:
            print(song["name"], "-", song["duration"], "сек.")

playlist = Playlist()

print("Пустой плейлист:")
playlist.show_songs()

print("Количество песен:", len(playlist))
print("Общая продолжительность:", playlist.total_duration())

print("\nДобавляем песни:")

playlist.add_song("Why", 171)
playlist.add_song("The Lazy Song", 189)
playlist.add_song("Prayer in C", 179)

playlist.show_songs()

print("\nКоличество песен:", len(playlist))
print("Общая продолжительность:", playlist.total_duration())

print("\nУдаляем The Lazy Song:")

playlist.remove_song("The Lazy Song")

playlist.show_songs()

print("\nКоличество песен:", len(playlist))
print("Общая продолжительность:", playlist.total_duration())

print("\nПытаемся удалить несуществующую песню:")

playlist.remove_song("Unknown Song")
