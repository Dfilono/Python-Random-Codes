'''
YouTube video downloader and file converter.

How To Use:
- Run the file, from the terminal using:
    python PATH/TO/FILE/youtube.py

- When prompted by the terminal, enter the url of the video you want
- Select the save path for your files
- Answer yes to the second terminal prompt to also generate an audio file from the video
'''


import os
from pytube import YouTube
from moviepy.editor import *
import tkinter as tk
from tkinter import filedialog

def downloadVideo(url, path):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        highestRes = streams.get_highest_resolution()
        highestRes.download(output_path=path)
        print("Video Downloaded Successfully!")

    except Exception as e:
        print(e)

def openFileDiag():
    folder = filedialog.askdirectory()

    if folder:
        print(f"Selected folder: {folder}")
    
    return folder

def convert2Audio(videoPath, savePath):
    try:
        video = VideoFileClip(videoPath)
        video.audio.write_audiofile(savePath)

        print('Audio file created successfully!')

    except Exception as e:
        print(e)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() 

    videoURL = input("Please enter a YouTube url: ")
    saveDir = openFileDiag()
    audioConvert = input("Do you want to convert the video to an audio file?(Y/N): ")

    if not saveDir:
        print("Invalid save location")
    else:
        print("Download Started...")
        downloadVideo(videoURL, saveDir)

    if str(audioConvert).lower() == 'y' or str(audioConvert).lower() == 'yes':
        print('Creating audio file...')
        fileExtension = ".mp4"
        for base, dir, files in os.walk(saveDir):
            for file in files:
                if fileExtension in file:
                    convert2Audio(saveDir + "/" + file, saveDir + "/" + file[:-4] + '.mp3')
    else:
        print("Enjoy your video!")