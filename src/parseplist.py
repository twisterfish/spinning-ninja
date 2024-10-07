import plistlib
import json
from pathlib import Path


file_path = Path('../data/iTunes-Library.xml')
fileExport = open('../data/iTunes-Export.csv', 'a')

trackLine = "TrackName,ArtistName,Album,DateAdded,BPM\r\n"
fileExport.write(trackLine)
trackLine = ""

count = 0

with open(file_path, 'rb') as infile:
    plist = plistlib.load(infile)
    
    #print(plist["Tracks"])

    for key in plist["Tracks"]:
        count += 1      

        if "Name" in plist["Tracks"][key]:
            print("Track Name: " + plist["Tracks"][key]["Name"])
            trackLine += "\"" + plist["Tracks"][key]["Name"] + "\","
        else:    
            print("Track Name: N/A")
            trackLine += "N/A,"

        if "Artist" in plist["Tracks"][key]:
            print("Artist Name: " + plist["Tracks"][key]["Artist"])
            trackLine += "\"" + plist["Tracks"][key]["Artist"] + "\","
        else:
            print("Artist Name: N/A")
            trackLine += "N/A,"

        if "Album" in plist["Tracks"][key]:
            print("Album Name: " + plist["Tracks"][key]["Album"])
            trackLine += "\"" + plist["Tracks"][key]["Album"] + "\","
        else:
            print("Album Name: N/A")
            trackLine += "N/A,"

        if "Date Added" in plist["Tracks"][key]:
            print("Date Added: " + str(plist["Tracks"][key]["Date Added"]))
            trackLine += (str(plist["Tracks"][key]["Date Added"])[:10]) + ","
        else:
            print("Date Added: N/A")
            trackLine += "N/A,"

        if "BPM" in plist["Tracks"][key]:
            print("Beats Per Minute: " + str(plist["Tracks"][key]["BPM"]))
            trackLine += str(plist["Tracks"][key]["BPM"]) + "\r\n"
        else:
            print("Beats Per Minute: N/A")
            trackLine += "N/A\r\n"

        print('\n')
        fileExport.write(trackLine)
        trackLine = ""
        

fileExport.close()

# print(plist["Date"])