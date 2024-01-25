from os import walk
from math import floor, ceil
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

def getFiles() -> list:
    filesList = []
    for (dirpath, dirnames, filenames) in walk("."):
        for file in filenames:
            if file[-4:] == ".mp3":
                tubeName = (ID3(dirpath+"/"+file))['TALB'].text[0]
                for position, tube in enumerate(filesList+[' ']):
                    if tubeName == tube[0]:
                        filesList[position].append(dirpath+"/"+file)
                        break
                    elif tube[0] == ' ':
                        filesList.append([tubeName, dirpath+"/"+file])
    for files in filesList:
        files[1:].sort()

    return filesList

def createNfoFile(files : list) -> None:
    nfoFile = open(f"{files[0]}.nfo", "w")
    globalInfos = ID3(files[1])
    writeMinus(nfoFile)
    writeCentered(nfoFile, f'{globalInfos["TPE1"].text[0]} - {files[0]}')
    writeMinus(nfoFile)
    nfoFile.write("\n")
    for func in ["artist", "album", "genre"]:
        globals()[func](nfoFile, globalInfos)

def genre(file, infos) -> None:
    file.write("Genre")
    writeDot(file, 15)
    file.write(f'{infos["TCON"].text[0]}\n')

def album(file, infos) -> None:
    file.write("Album")
    writeDot(file, 15)
    file.write(f"{infos['TALB'].text[0]}\n")    

def artist(file, infos) -> None:
    file.write("Artist")
    writeDot(file, 14)
    file.write(f"{infos['TPE1'].text[0]}\n")

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

if __name__ == "__main__":
    filesList = getFiles()
    for files in filesList:
        createNfoFile(files)
