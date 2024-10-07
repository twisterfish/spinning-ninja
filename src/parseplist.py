import plistlib
import json
from pathlib import Path

file_path = Path('../data/iTunes-Library.xml')
file_content = file_path.read_bytes()

count = 0

with open(file_path, 'rb') as infile:
    plist = plistlib.load(infile)
    #print(plist["Tracks"])

    for key in plist["Tracks"]:
        count += 1      
        # print(key)
        if "Name" in plist["Tracks"][key]:
            print("Track Name: " + plist["Tracks"][key]["Name"])
        else:    
            print("Track Name: N/A")

        if "Artist" in plist["Tracks"][key]:
            print("Artist Name: " + plist["Tracks"][key]["Artist"])
        else:
            print("Artist Name: N/A")

        if "Album" in plist["Tracks"][key]:
            print("Album Name: " + plist["Tracks"][key]["Album"])
        else:
            print("Album Name: N/A")

        if "Date Added" in plist["Tracks"][key]:
            print("Date Added: " + str(plist["Tracks"][key]["Date Added"]))
        else:
            print("Date Added: N/A")

        if "BPM" in plist["Tracks"][key]:
            print("Beats Per Minute: " + str(plist["Tracks"][key]["BPM"]))
        else:
            print("Beats Per Minute: N/A")

        print('\n')



# print(plist["Date"])