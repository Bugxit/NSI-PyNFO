from math import floor
import os

def cover(file, infosID3, infosMP3) -> None:
    global size_save
    for (dirpath, dirnames, filenames) in os.walk("./GreenDay"):
        fileList = filenames
    for files in fileList:
        if files[-4:] == ".jpg":
            jpgIn = True
            size_save = os.path.getsize(f'{dirpath}/{files}')
            break
    if jpgIn:
        file.write("Cover")
        writeDot(file, 15)
        file.write('Front')

def total_size(file, size) -> None:
    file.write("Total size")
    writeDot(file, 10)
    file.write(f"{round((size+size_save)/1048576, 2)} MB")

def playing_time(file, time) -> None:
    file.write("Playing time")
    writeDot(file, 8)
    minutes = str(int(time//60))
    if int(time//60) < 10:
        minutes = "0" + minutes
    seconds = str(int(time-60*int(minutes)))
    if int(time-60*int(minutes)) < 10:
        seconds = "0" + seconds
    file.write(f"{minutes}:{seconds}\n")

def mode(file, infosID3, infosMP3) -> None:
    file.write("Mode")
    writeDot(file, 16)
    file.write(f'{infosMP3.info.mode}\n')

def sampling_rate(file, infosID3, infosMP3) -> None:
    file.write("Sampling rate")
    writeDot(file, 7)
    file.write(f'{infosMP3.info.sample_rate}\n')

def channels(file, infosID3, infosMP3) -> None:
    file.write("Channels")
    writeDot(file, 12)
    file.write(f'{infosMP3.info.channels}\n')

def quality(file, infosID3, infosMP3) -> None:
    file.write("Quality")
    writeDot(file, 13)
    file.write(f'{infosMP3.info.bitrate}\n')

def format(file, infosID3, infosMP3) -> None:
    file.write("Format..............: MPEG Audio Layer 3 (MP3)\n")

def ripper(file, infosID3, infosMP3) -> None:
    file.write("Ripper")
    writeDot(file, 14)
    file.write(f'{infosMP3.info.encoder_info}\n')

def year(file, infosID3, infosMP3) -> None:
    file.write("Year")
    writeDot(file, 16)
    file.write(f'{infosID3["TDRC"].text[0]}\n')

def genre(file, infosID3, infosMP3) -> None:
    file.write("Genre")
    writeDot(file, 15)
    file.write(f'{infosID3["TCON"].text[0]}\n')

def album(file, infosID3, infosMP3) -> None:
    file.write("Album")
    writeDot(file, 15)
    file.write(f"{infosID3['TALB'].text[0]}\n")    

def artist(file, infosID3, infosMP3) -> None:
    file.write("Artist")
    writeDot(file, 14)
    file.write(f"{infosID3['TPE1'].text[0]}\n")

def writeCentered(file, text: str) -> None:
    for loop in range(floor((70-len(text))/2)):
        file.write(" ")
    file.write(f"{text}\n")

def writeDot(file, number : int) -> None:
    for loop in range(number):
        file.write(".")
    file.write(": ")

def writeMinus(file) -> None:
    for loop in range(70):
        file.write("-")
    file.write('\n')