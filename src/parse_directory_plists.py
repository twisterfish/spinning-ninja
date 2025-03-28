#######################################################################
# Python script that will search through the specified directory and
# parse all iTunes export files and generate CSV or SQL files from the XML
# data. The script will read the XML data and extract the track name, artist
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
#    in the variable 'search_path' on the paths section of the script
# 4. Change the path to the output CSV and/or SQL files you wish to create
#    in the variables 'target_csv' and/or 'target_sql' in the paths section of the script
# 5. Save the script changes
# 6. Run the script by typing 'python3 parse_directory_plists.py' in the terminal
#######################################################################

import plistlib
import datetime
import re
import os
from pathlib import Path
import xml.etree.ElementTree as ET

####################################################################### 
# These are global variables used to control the output of the script
#######################################################################

# Flags to control the output of the script - set to True to enable the output
write_csv = False # Set to True to write to a CSV file
write_sql = True # Set to True to write out a SQL import file
printout = False # Set to True to print to the console

# Variables used to store data for the CSV and SQL files
csvLine = "" # This is the line buffer that will be written to the CSV file
sqlLine = "" # This is the line buffer that will be written to the SQL file
csv_file_handle = None # This is the CSV file that will be written to if used
sql_file_handle = None # This is the SQL file that will be written to if used
plist_file_path = Path('') # This is the PLIST file that will be read after binding to the search path

# Informational variables
today = datetime.datetime.now() # This is the current date and time
today = today.strftime("%m-%d-%YT%H-%M-%SZ") # This is the current date and time as a string
count = 0 # This is a counter for the number of tracks processed

#######################################################################
# These are the paths to the files that will be used in the script
#######################################################################

# This is the directory that will be searched for the PLIST files
# Add the directory path here
search_path = Path('../data/OneDrive-2024-11-27')

# This is the CSV file that will be written to - 
# Add the file path and name here
target_csv = Path('../data/' + 'Playlist_Export.' + today + '.csv')

# This is the SQL file that will be written to - 
# Add the file path and name here
target_sql = Path('../data/' + 'Playlist_Export.' + today + '.sql')

#######################################################################
# Function to check if a file is an XML file
#######################################################################
def is_xml_file(filename):
    try:
        ET.parse(filename)
        return True
    except ET.ParseError:
        return False
    
#######################################################################
#######################################################################

#######################################################################
# This is the main part of the script that reads the plist file
#######################################################################

 # If the flag is set to write to a CSV file, write the header line first
if write_csv:
    csv_file_handle = open( target_csv, 'a' )
    csvLine = "date_played,track_name,artist_name,album_name,date_added,track_length,num_plays,beats_per_minute\r\n" # This is the header line for the CSV file
    csv_file_handle.write(csvLine)
    csvLine = "" # Reset the line variable

# If the flag is set to write to a SQL file, write the 'insert' clause line first
if write_sql:
    sql_file_handle = open( target_sql, 'a' )
    sqlLine = "INSERT INTO spin_playlists (date_played,track_name, artist_name, album_name, date_added, track_length, num_plays, beats_per_minute) VALUES \r\n" # This is the header line for the SQL file
    sql_file_handle.write(sqlLine)
    sqlLine = "" # Reset the line variable


for file in os.listdir(search_path):
    
    if file.endswith(".xml") and is_xml_file(os.path.join(search_path, file)):
        # Print the file name to the console
        print(os.path.join(search_path, file))
        # Set the path to the plist file
        plist_file_path = Path(os.path.join(search_path, file))

        # Parse the date from the file name and then reformat it to be in the format YYYY-MM-DD
        parsedDate = re.search("[0-9][0-9]-[0-9][0-9]-[0-9][0-9]", plist_file_path.stem).group(0)
        correctformat = parsedDate.split("-")
        parsedDate = "20" + correctformat[2] + "-" + correctformat[0] + "-" + correctformat[1]

        # Open the plist file and load the data
        with open(plist_file_path, 'rb') as infile:
            plist = plistlib.load(infile)
            # Loop through the tracks in the plist file
            for key in plist["Tracks"]:
                count += 1  

                if "Name" in plist["Tracks"][key]:
                    scrubbedField = plist["Tracks"][key]["Name"].replace("\"", "")                     
                    if printout:
                        print("Track Name: " + scrubbedField )
                    if write_csv:
                        csvLine += parsedDate + ",\"" + scrubbedField + "\","
                    if write_sql:
                        sqlLine += "(\"" + parsedDate + "\",\"" + scrubbedField + "\","
                else:    
                    if printout:
                        print("Track Name: N/A")
                    if write_csv:
                        csvLine += "N/A,"
                    if write_sql:
                        sqlLine += "\"N/A\","

                if "Artist" in plist["Tracks"][key]:
                    scrubbedField = plist["Tracks"][key]["Artist"].replace("\"", "") 
                    if printout:
                        print("Artist Name: " + scrubbedField)
                    if write_csv:
                        csvLine += "\"" + scrubbedField + "\","
                    if write_sql:
                        sqlLine += "\"" + scrubbedField + "\","
                    
                else:
                    if printout:
                        print("Artist Name: N/A")
                    if write_csv:
                        csvLine += "N/A,"
                    if write_sql:
                        sqlLine += "\"N/A\","

                if "Album" in plist["Tracks"][key]:
                    scrubbedField = plist["Tracks"][key]["Album"].replace("\"", "")  
                    if printout:
                        print("Album Name: " + scrubbedField)
                    if write_csv:
                        csvLine += "\"" + scrubbedField + "\","
                    if write_sql:
                        sqlLine += "\"" + scrubbedField + "\","
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

        # Close the plist file so we don't leak file handles
        infile.close() 
    else:
        print("This is not a valid XML file: " + os.path.join(search_path, file). __str__())
            
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