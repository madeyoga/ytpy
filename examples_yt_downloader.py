from ytpy.youtube import YoutubeService
import os
import sys

key, threads = sys.argv[1], sys.argv[2]
print("searching for: " + key)

## download video destination / path
os.chdir(r'C:\Users\MYPC\Desktop\Nano_clone\myYoutubeDownloader\video')

try:
    int(threads)
except Exception as e:
    print("not a valid threads input")
    sys.exit(1)

## Build Youtube Service Object
ys = YoutubeService()
## search video with keyword
search_result = ys.search(keyword=key, max_results=10)

for i, r in enumerate(search_result):
    print("{}. {} - {}".format(i + 1, r.title, r.url))
    # print(r.desc)
    # print(r.thumbnails)

print("\neg. input `1 2 4 7`, this will download video with entry number 1 2 4 7")
picked_entry_numbers = input('Choose video to download: ').split(" ")

## Download
for entry_number in picked_entry_numbers:
    video = search_result[int(entry_number) - 1]
    print('Downloading {}...'.format(video.title))
    ys.download(video.url, threads)

print('Downloaded {} videos.'.format(len(picked_entry_numbers)))
