#! python3
import os

def main():
    print("File Extension Corrector v0.0.2\n")
    dir = runoptions()
    scanfiles(dir)
    input("Press ENTER to close the program...")

def runoptions():
    cd = os.getcwd()
    print("The current directory is " + cd)
    inputstr = input("Is this the directory you wish to scan for file extension issues? (Y/N): ").lower()
    if inputstr == "y":
        return cd
    if inputstr == "n":
        cd = input("Please input the absolute path to the directory to be scanned:\n")
        print("Scan directory set to " + cd)
        return cd
    print("Unknown option. Terminating.")
    exit()

def scanfiles(dir):
    for file in os.scandir(dir):
        if not file.is_dir() and file.name != "driver.py":
            print("Scanning " + file.name + ":", end=" ")
            with open(file, "rb") as f:
                header = f.read(10).hex()
                printHeader(header)
                extension = ".jpg" if isjpg(header) else ""
                extension = ".png" if ispng(header) else extension
                extension = ".gif" if isgif(header) else extension
                if extension == "":
                    print(": Not JPEG/PNG/GIF!")

def printHeader(header):
    for i in range(10):
        print(header[2*i:2*i+2], end=" ")

def isjpg(header):
    # JFIF : FF D8 FF E0 xx xx 4A 46 49 46
    # EXIF : FF D8 FF E1 xx xx 45 78 69 66
    if header[0:8] == "ffd8ffe0" and header[12:] == "4a464946":
        print(": JPEG/JFIF")
        return True
    if header[0:8] == "ffd8ffe1" and header[12:] == "45786966":
        print(": JPEG/EXIF")
        return True
    return False

def ispng(header):
    # PNG : 89 50 4E 47 0D 0A 1A 0A
    if header[0:16] == "89504e470d0a1a0a":
        print(": PNG")
        return True
    return False

def isgif(header):
    # GIF87a : 47 49 46 38 37 61
    # GIF89a : 47 49 46 38 39 61
    if header[0:12] == "474946383761":
        print(": GIF/87a")
        return True
    if header[0:12] == "474946383961":
        print(": GIF/89a")
        return True
    return False

if __name__ == "__main__":
    main()
