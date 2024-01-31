import api
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

def getFiles() -> list:
    filesList = {}
    for (dirpath, dirnames, filenames) in os.walk("."):
        for file in filenames:
            if file[-4:] == ".mp3":
                tubeName = (ID3(dirpath+"/"+file))['TALB'].text[0]
                if tubeName in filesList:
                    filesList[tubeName].append(dirpath+"/"+file)
                else:
                    filesList[tubeName] = [dirpath+"/"+file]
    for files in filesList:
        filesList[files].sort()
    return filesList

def createNfoFile(file : list, filesList : dict) -> None:
    nfoFile = open(f"{file}.nfo", "w")
    globalInfosID3 = ID3(filesList[file][0])
    globalInfosMP3 = MP3(filesList[file][0])
    api.writeMinus(nfoFile)
    api.writeCentered(nfoFile, f'{globalInfosID3["TPE1"].text[0]} - {globalInfosID3["TALB"].text[0]}')
    api.writeMinus(nfoFile)
    nfoFile.write("\n")
    for func in ["artist", "album", "genre", "year", "ripper", "format", "quality", "channels", "sampling_rate", "mode", "cover"]:
        getattr(api, func)(nfoFile, globalInfosID3, globalInfosMP3)
    nfoFile.write("\n\n")
    api.writeMinus(nfoFile)
    api.writeCentered(nfoFile, "Tracklisting")
    api.writeMinus(nfoFile)
    nfoFile.write("\n")
    totalTime = 0
    totalSize = 0
    for music in filesList[file]:
        nfoFile.write(f"    {music[2+len(globalInfosID3['TPE1'].text[0]):]}")
        musicInfo = MP3(music)
        for loop in range(59-len(music[2+len(globalInfosID3['TPE1'].text[0]):])):
            nfoFile.write(" ")
        minutes = str(int(musicInfo.info.length//60))
        if int(musicInfo.info.length//60) < 10:
            minutes = "0" + minutes
        seconds = str(int(musicInfo.info.length-60*int(minutes)))
        if int(musicInfo.info.length-60*int(minutes)) < 10:
            seconds = "0" + seconds
        nfoFile.write(f"[{minutes}:{seconds}]\n")
        totalSize += os.path.getsize(music[2:])
        totalTime += musicInfo.info.length
    nfoFile.write("\n")
    api.playing_time(nfoFile, totalTime)
    api.total_size(nfoFile, totalSize)

if __name__ == "__main__":
    filesList = getFiles()
    for files in filesList:
        createNfoFile(files, filesList)
