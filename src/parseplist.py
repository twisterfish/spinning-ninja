#######################################################################
# Python script to parse an iTunes XML file and output the data to a CSV file
# Instructions:
# 1. Open the script in your favorite text editor
# 2. Change the path to the iTunes XML file on line 47
# 3. Change the path to the output CSV file on line 53
# 4. Save the script changes
# 5. Run the script by typing 'python3 parseplist.py' in the terminal
#######################################################################

import plistlib
import datetime
from pathlib import Path

####################################################################### 
# These are global variables used to control the output of the script
# Set the flags to True to enable the output for that type
#######################################################################

write_csv = True # Set to True to write to a CSV file
write_sql = True # Set to True to write out a SQL import file
printout = False # Set to True to print to the console

count = 0 # This is a counter for the number of tracks processed

today = datetime.datetime.now() # This is the current date and time
today = today.strftime("%m-%d-%YT%H-%M-%S") # This is the current date and time as a string

#######################################################################
# These are the paths to the files that will be used in the script
#######################################################################

# This is the PLIST file that will be read from - add the file path here
plist_file_path = Path('../data/iTunes-Library.xml')

# This is the CSV file that will be written to - add the file path here
target_csv = Path('../data/' + 'Playlist_Export.' + today + '.csv')

# This is the SQL file that will be written to - add the file path here
target_sql = Path('../data/' + 'Playlist_Export.' + today + '.sql')

#######################################################################
# This is the main part of the script that reads the plist file
#######################################################################

# initialize the variables
csvLine = "" # This is the line that will be written to the CSV file
sqlLine = "" # This is the line that will be written to the SQL file
csv_file_handle = None # This is the CSV file that will be written to if used
sql_file_handle = None # This is the SQL file that will be written to if used

# If the flag is set to write to a CSV file, write the header line first
if write_csv:
    csv_file_handle = open( target_csv, 'a' )
    csvLine = "TrackName,ArtistName,Album,DateAdded,Time,Plays,BPM\r\n" # This is the header line for the CSV file
    csv_file_handle.write(csvLine)
    csvLine = "" # Reset the line variable

if write_sql:
    sql_file_handle = open( target_sql, 'a' )
    sqlLine = "INSERT INTO playlists (TrackName, ArtistName, Album, DateAdded, Time, Plays, BPM) VALUES " # This is the header line for the SQL file
    sql_file_handle.write(sqlLine)
    sqlLine = "" # Reset the line variable


# Open the plist file and load the data
with open(plist_file_path, 'rb') as infile:
    plist = plistlib.load(infile)
    # Loop through the tracks in the plist file
    for key in plist["Tracks"]:
        count += 1      

        if "Name" in plist["Tracks"][key]:
            if printout:
                print("Track Name: " + plist["Tracks"][key]["Name"])
            if write_csv:
                csvLine += "\"" + plist["Tracks"][key]["Name"] + "\","
            if write_sql:
                sqlLine += "(\"" + plist["Tracks"][key]["Name"] + "\","
        else:    
            if printout:
                print("Track Name: N/A")
            if write_csv:
                csvLine += "N/A,"
            if write_sql:
                sqlLine += "(\"N/A\","

        if "Artist" in plist["Tracks"][key]:
            if printout:
                print("Artist Name: " + plist["Tracks"][key]["Artist"])
            if write_csv:
                csvLine += "\"" + plist["Tracks"][key]["Artist"] + "\","
            if write_sql:
                sqlLine += "\"" + plist["Tracks"][key]["Artist"] + "\","
            
        else:
            if printout:
                print("Artist Name: N/A")
            if write_csv:
                csvLine += "N/A,"
            if write_sql:
                sqlLine += "\"N/A\","

        if "Album" in plist["Tracks"][key]:
            if printout:
                print("Album Name: " + plist["Tracks"][key]["Album"])
            if write_csv:
                csvLine += "\"" + plist["Tracks"][key]["Album"] + "\","
            if write_sql:
                sqlLine += "\"" + plist["Tracks"][key]["Album"] + "\","
        else:
            if printout:
                print("Album Name: N/A")
            if write_csv:
                csvLine += "N/A,"
            if write_sql:
                sqlLine += "\"N/A\","

        if "Date Added" in plist["Tracks"][key]:
            if printout:
                print("Date Added: " + str(plist["Tracks"][key]["Date Added"]))
            if write_csv:
                csvLine += (str(plist["Tracks"][key]["Date Added"])[:10]) + ","
            if write_sql:
                sqlLine += (str(plist["Tracks"][key]["Date Added"])[:10]) + ","
        else:
            if printout:
                print("Date Added: N/A")
            if write_csv:
                csvLine += "N/A,"
            if write_sql:
                sqlLine += "\"N/A\","

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
                csvLine += str(min) + ":" + sec + ","
            if write_sql:
                sqlLine += "\"" + str(min) + ":" + sec + "\","
        else:
            if printout:
                print("Time: N/A")
            if write_csv:
                csvLine += "N/A,"
            if write_sql:
                sqlLine += "\"N/A\","

        if "Play Count" in plist["Tracks"][key]:
            if printout:
                print("Play Count: " + str(plist["Tracks"][key]["Play Count"]))
            if write_csv:
                csvLine += (str(plist["Tracks"][key]["Play Count"])) + ","
            if write_sql:
                sqlLine += (str(plist["Tracks"][key]["Play Count"])) + ","
        else:
            if printout:
                print("Play Count: N/A")
            if write_csv:
                csvLine += "N/A,"
            if write_sql:
                sqlLine += "\"N/A\","

        if "BPM" in plist["Tracks"][key]:
            if printout:
                print("Beats Per Minute: " + str(plist["Tracks"][key]["BPM"]))
            if write_csv:
                csvLine += str(plist["Tracks"][key]["BPM"]) + "\r\n"
            if write_sql:
                sqlLine += str(plist["Tracks"][key]["BPM"]) + "),"
        else:
            if printout:
                print("Beats Per Minute: N/A")
            if write_csv:
                csvLine += "N/A\r\n"
            if write_sql:
                sqlLine += "\"N/A\"),"

        
        if printout:
            print('\n')
        if write_csv:
            csv_file_handle.write(csvLine)
        if write_sql:
            sql_file_handle.write(sqlLine)

        csvLine = ""
        sqlLine = ""
        
if write_csv:
    csv_file_handle.close()
if write_sql:
    sql_file_handle.write(";")
    sql_file_handle.close()

print("Total Tracks Processed: " + str(count))