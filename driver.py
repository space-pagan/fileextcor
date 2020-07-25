#! python3
import os

def main():
    print("File Extension Corrector v0.0.2\n")
    dir, printSkipped = setup()
    skippedFiles = scanfiles(dir)
    if printSkipped:
        printSkippedList(skippedFiles)
    pauseandquit()

def setup():
    cd = os.getcwd()
    print("The current directory is " + cd)
    inputstr = input("Is this the directory you wish to scan for file extension issues? (Y/N): ").lower()
    if inputstr == "y":
        pass
    elif inputstr == "n":
        cd = input("Please input the absolute path to the directory to be scanned:\n")
        print("Scan directory set to " + cd)
    else:
        print("Unknown option. Terminating.")
        pauseandquit()
    inputstr = input("Would you like a list of skipped files to be printed after processing? (Y/N): ").lower()
    if inputstr == "y":
        return cd, True
    elif inputstr == "n":
        return cd, False
    else:
        print("Unknown option. Terminating.")
        pauseandquit()

def printSkippedList(skippedFiles):
    print("\n{} files skipped (not JPG/PNG/GIF):".format(len(skippedFiles)))
    for f in skippedFiles:
        print(f)

def pauseandquit():
    try:
        os.system("pause")
    except:
        os.system("read -n 1 -s -r -p $'Press any key to continue...\n'")
    exit()

def scanfiles(dir):
    skippedFiles = []
    for file in os.scandir(dir):
        if notNoneIfSkipped := processFile(file):
            skippedFiles.append(notNoneIfSkipped)
    return skippedFiles

def processFile(file):
    if file.is_file():
        print("Scanning " + file.name + ":", end=" ")
        f = open(file, "rb")
        newext = getFileExtensionFromHeader(f.read(10).hex())
        f.close()
        if newext:
            renameFileToHaveExtension(file, newext)
        else:
            return file.name

def renameFileToHaveExtension(file, newext):
    curext, newpath = getCurrentExtensionAndNewPath(file, newext)
    if curext != newext:
        print(": {} -> {}".format(curext, newext))
        os.rename(file.path, newpath)
    else:
        print(": Already {}!".format(curext))

def getCurrentExtensionAndNewPath(file, newext):
    extpos = getPosOfChrInStr(file.name, '.')
    if (extlen := len(file.name) - extpos) <= 5:
        return file.name[extpos:].lower(), file.path[:-extlen] + newext
    return "", file.path + newext

def getPosOfChrInStr(str, chr):
    pos = -1
    try:
        pos = str.rindex(chr)
    except:
        pass
    return pos

def getFileExtensionFromHeader(header):
    printHeader(header)
    extension = ""
    if isjpg(header):
        extension = ".jpg"
    elif ispng(header):
        extension = ".png"
    elif isgif(header):
        extension = ".gif"
    else:
        print(": Not JPG/PNG/GIF! Skipping...")
    return extension

def printHeader(header):
    for i in range(10):
        print(header[2*i:2*i+2], end=" ")

def isjpg(header):
    # JFIF : FF D8 FF E0 xx xx 4A 46 49 46
    # EXIF : FF D8 FF E1 xx xx 45 78 69 66
    if header[0:8] == "ffd8ffe0" and header[12:] == "4a464946":
        print(": JPEG/JFIF", end=" ")
        return True
    if header[0:8] == "ffd8ffe1" and header[12:] == "45786966":
        print(": JPEG/EXIF", end=" ")
        return True
    return False

def ispng(header):
    # PNG : 89 50 4E 47 0D 0A 1A 0A
    if header[0:16] == "89504e470d0a1a0a":
        print(": PNG", end=" ")
        return True
    return False

def isgif(header):
    # GIF87a : 47 49 46 38 37 61
    # GIF89a : 47 49 46 38 39 61
    if header[0:12] == "474946383761":
        print(": GIF/87a", end=" ")
        return True
    if header[0:12] == "474946383961":
        print(": GIF/89a", end=" ")
        return True
    return False

if __name__ == "__main__":
    main()
