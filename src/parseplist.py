#######################################################################
# Python script to parse an iTunes XML file and output the data to a CSV file
#######################################################################

import plistlib
import datetime
from pathlib import Path

####################################################################### 
# These are global variables used to control the output of the script
#######################################################################

count = 0 # This is a counter for the number of tracks processed
write_csv = True # Set to True to write to a CSV file
printout = False # Set to True to print to the console

#######################################################################
# These are the paths to the files that will be used in the script
#######################################################################

trackLine = "" # This is the line that will be written to the CSV file
csv_file_path = None # This is the file that will be written to if used
today = datetime.datetime.now() # This is the current date and time
today = today.strftime("%m-%d-%YT%H-%M-%S") # This is the current date and time as a string

# This is the file that will be read from - add your own path heres
plist_file_path = Path('../data/iTunes-Library.xml')

# If the flag is set to write to a CSV file, this is the file that will 
# be written to - add your own path here
if write_csv:
    csv_file_path = open('../data/' + today + '_Playlist_Export.csv', 'a')
    trackLine = "TrackName,ArtistName,Album,DateAdded,Time,Plays,BPM\r\n"
    csv_file_path.write(trackLine)
    trackLine = ""

#######################################################################
# This is the main part of the script that reads the plist file
#######################################################################

with open(plist_file_path, 'rb') as infile:
    plist = plistlib.load(infile)
    
    #print(plist["Tracks"])

    for key in plist["Tracks"]:
        count += 1      

        if "Name" in plist["Tracks"][key]:
            if printout:
                print("Track Name: " + plist["Tracks"][key]["Name"])
            if write_csv:
                trackLine += "\"" + plist["Tracks"][key]["Name"] + "\","
        else:    
            if printout:
                print("Track Name: N/A")
            if write_csv:
                trackLine += "N/A,"

        if "Artist" in plist["Tracks"][key]:
            if printout:
                print("Artist Name: " + plist["Tracks"][key]["Artist"])
            if write_csv:
                trackLine += "\"" + plist["Tracks"][key]["Artist"] + "\","
        else:
            if printout:
                print("Artist Name: N/A")
            if write_csv:
                trackLine += "N/A,"

        if "Album" in plist["Tracks"][key]:
            if printout:
                print("Album Name: " + plist["Tracks"][key]["Album"])
            if write_csv:
                trackLine += "\"" + plist["Tracks"][key]["Album"] + "\","
        else:
            if printout:
                print("Album Name: N/A")
            if write_csv:
                trackLine += "N/A,"

        if "Date Added" in plist["Tracks"][key]:
            if printout:
                print("Date Added: " + str(plist["Tracks"][key]["Date Added"]))
            if write_csv:
                trackLine += (str(plist["Tracks"][key]["Date Added"])[:10]) + ","
        else:
            if printout:
                print("Date Added: N/A")
            if write_csv:
                trackLine += "N/A,"

        if "Total Time" in plist["Tracks"][key]:
            mill_sec = plist["Tracks"][key]["Total Time"]
            total_sec = mill_sec / 1000
            min = int(total_sec // 60)
            sec = int(total_sec % 60)
            
            if sec < 10: # left pad with 0 if sec is less than 10
                sec = "0" + str(sec)
            else:
                sec = str(sec)
            
            if printout:
                print("Time: " + str(min) + ":" + sec)
            if write_csv:
                trackLine += str(min) + ":" + sec + ","
        else:
            if printout:
                print("Time: N/A")
            if write_csv:
                trackLine += "N/A,"

        if "Play Count" in plist["Tracks"][key]:
            if printout:
                print("Play Count: " + str(plist["Tracks"][key]["Play Count"]))
            if write_csv:
                trackLine += (str(plist["Tracks"][key]["Play Count"])) + ","
        else:
            if printout:
                print("Play Count: N/A")
            if write_csv:
                trackLine += "N/A,"

        if "BPM" in plist["Tracks"][key]:
            if printout:
                print("Beats Per Minute: " + str(plist["Tracks"][key]["BPM"]))
            if write_csv:
                trackLine += str(plist["Tracks"][key]["BPM"]) + "\r\n"
        else:
            if printout:
                print("Beats Per Minute: N/A")
            if write_csv:
                trackLine += "N/A\r\n"

        
        if printout:
            print('\n')
        if write_csv:
            csv_file_path.write(trackLine)

        trackLine = ""
        
if write_csv:
    csv_file_path.close()

print("Total Tracks Processed: " + str(count))