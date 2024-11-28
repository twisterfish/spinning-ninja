#######################################################################
# Python script to parse an iTunes XML file specified and generate 
# CSV or SQL files from the XML.
# The script will read the XML data and extract the track name, artist
# name, album name, date added, track length, number of plays, and beats per
# minute. The script will then write the data to a CSV or SQL file based on
# the flags set in the script. The script will also print the data to the
# console if the printout flag is set to True.  
# This script is designed to be run from the command line and will require 
# the user to modify the path to the iTunes XML file, the output CSV and SQL files,
# and the flags to control the output of the script. The script will also
# generate a timestamp to append to the output file names to ensure that
# the files are unique. The script will use the file name to extract the date
# that the playlist was created and then reformat the date to be in the format
# YYYY-MM-DD. 
# Instructions:
# 1. Open the script in your favorite text editor
# 2. Set the flags to true or false to control the output of the script
# 3. Change the path to the directory where the iTunes XML files are stored
#    in the variable 'plist_file_path' in the paths section of the script
# 4. Change the path to the output CSV and/or SQL files you wish to create
#    in the variables 'target_csv'and/or 'target_sql' in the paths section of the script
# 5. Save the script changes
# 6. Run the script by typing 'python3 parseplist.py' in the terminal
#######################################################################

import plistlib
import datetime
import re
import os
from pathlib import Path

####################################################################### 
# These are global variables used to control the output of the script
# Set the flags to True to enable the output for that type
#######################################################################

write_csv = False # Set to True to write to a CSV file
write_sql = True # Set to True to write out a SQL import file
printout = False # Set to True to print to the console

count = 0 # This is a counter for the number of tracks processed

today = datetime.datetime.now() # This is the current date and time
today = today.strftime("%m-%d-%YT%H-%M-%S") # This is the current date and time as a string

#######################################################################
# These are the paths to the files that will be used in the script
#######################################################################

# This is the PLIST file that will be read from - add the file path here
plist_file_path = Path('../data/Equinox-09-15-24.xml')

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

# Parse the date from the file name and then reformat it to be in the format YYYY-MM-DD
parsedDate = re.search("[0-9][0-9]-[0-9][0-9]-[0-9][0-9]", plist_file_path.stem).group(0)
correctformat = parsedDate.split("-")
parsedDate = "20" + correctformat[2] + "-" + correctformat[0] + "-" + correctformat[1]

# If the flag is set to write to a CSV file, write the header line first
if write_csv:
    csv_file_handle = open( target_csv, 'a' )
    csvLine = "date_played,track_name,artist_name,album_name,date_added,track_length,num_plays,beats_per_minute\r\n" # This is the header line for the CSV file
    csv_file_handle.write(csvLine)
    csvLine = "" # Reset the line variable
# If the flag is set to write to a SQL file, write the header line first
if write_sql:
    sql_file_handle = open( target_sql, 'a' )
    sqlLine = "INSERT INTO spin_playlists (date_played,track_name, artist_name, album_name, date_added, track_length, num_plays, beats_per_minute) VALUES \r\n" # This is the header line for the SQL file
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
                csvLine += parsedDate + ",\"" + plist["Tracks"][key]["Name"] + "\","
            if write_sql:
                sqlLine += "(\"" + parsedDate + "\",\"" + plist["Tracks"][key]["Name"] + "\","
        else:    
            if printout:
                print("Track Name: N/A")
            if write_csv:
                csvLine += "N/A,"
            if write_sql:
                sqlLine += "\"N/A\","

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
                csvLine += "\"" + (str(plist["Tracks"][key]["Date Added"])[:10]) + "\","
            if write_sql:
                sqlLine += "\"" + (str(plist["Tracks"][key]["Date Added"])[:10]) + "\","
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
            sql_file_handle.write(sqlLine + "\r\n")

        csvLine = ""
        sqlLine = ""
        
if write_csv:
    csv_file_handle.close()
if write_sql:
    # Remove the last comma and add a semicolon to the end of the file
    # This is needed to make the SQL file importable to a DB
    sql_file_handle.seek(sql_file_handle.tell() - 3, os.SEEK_SET)
    sql_file_handle.truncate()
    sql_file_handle.seek(0, os.SEEK_END)
    sql_file_handle.write(";")
    sql_file_handle.close()

print("Total Tracks Processed: " + str(count))