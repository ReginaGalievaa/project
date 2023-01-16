import pandas as pd
import csv
import json
from datetime import datetime
import math
import matplotlib.pyplot as plt
import numpy as np


def date_convertion(date_str):
  ''' Функция приведения даты формата str из столбца 'Release Date' датасета 'spotify_songs_top_100.csv' к единному формату.
      Функция принимает только даты в форматах '%d.%B.%y' и '%d %B %Y '''
  if '.' in date_str:
    date_obj = datetime.strptime(date_str, '%d.%B.%y')
  else:
    date_obj = datetime.strptime(date_str, '%d %B %Y')
  return date_obj


assert date_convertion('10 September 1991') == datetime(1991, 9, 10)
assert date_convertion('10.May.19') == datetime(2019, 5, 10)


def ed_sheeran_song(str_artist, str_song):
  '''Функция для нахождения песен, которые исполняет Ed Sheeran.
     Функция принимает имя исполнителя и название песни, которую он исполняет'''
  if 'Ed Sheeran' in str_artist:
    return str_song


def old_song(str_date, str_song):
  '''Функция для нахождения трех самых старых песен.'''
  d = datetime(2000, 1, 1, 00, 00) # На гистограмме видно, что три самые старые песни были выпущены до 2000 года
  if d > date_convertion(str_date):
    return str_song
    

ed_sheeran_songs = []
old_songs = []
streams = {}

with open('spotify_songs_top_100.csv') as f:
    reader = csv.reader(f)

    row = next(reader)
    artist_ind = row.index('Artist')
    song_ind = row.index('Song')
    date_ind = row.index("Release Date")
    stream_ind = row.index('Streams (Billions)')

    for row in reader:
      song1 = ed_sheeran_song(row[artist_ind], row[song_ind])
      if song1 != None:
        ed_sheeran_songs.append(song1)
      song2 = old_song(row[date_ind], row[song_ind])
      if song2 != None:
        old_songs.append(song2)
      artist = row[artist_ind]
      stream = float(row[stream_ind].replace(',', '.'))
      if artist in streams:
        streams[artist] += stream
      else:
        streams[artist] = stream

answers = [
    {
        "Ed Sheeran": ed_sheeran_songs
    },
    {
        "Top 3 old songs": old_songs
    },
        streams
]

with open('answers.json', 'w') as f:
    json.dump(answers, f, indent=4, sort_keys=True)
    
    
# Создание нового столбца в датасете 'Date Object' с датами в единном формате для построения гистограммы
with open('spotify_songs_top_100.csv') as f:
    reader = csv.reader(f)

    row = next(reader)
    date_ind = row.index("Release Date")

    list_date = []
    for row in reader:
      date_string = row[date_ind]
      list_date.append(date_convertion(date_string))

df = pd.read_csv('spotify_songs_top_100.csv')
df.insert(5, 'Date Object', list_date, True)
df

# Построение гистограммы
plt.hist(df['Date Object'],
         label="All songs", 
         bins=100, 
         color='blue', 
         alpha=0.5)

plt.title('Number of songs by year')
plt.xlabel('Year')
plt.ylabel('Number of songs')
plt.legend()
plt.show()
plt.savefig('Number_of_songs_by_year.png')
