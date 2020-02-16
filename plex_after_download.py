#!/usr/bin/env python3

#This script is run after the file is downloaded by transmission.
#It then determines if the folder is a tv-show or a film and will move the files to their respected
#directories for plex to pickup correctly.

import os,subprocess,shutil,logging,time
from datetime import datetime

LOG_FILENAME = '/var/log/plex_script.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)


path = "/mnt/sdb/transmission/complete/"
dest_path = "/mnt/sdb/plexmediaserver/movies/"
dir_contents = os.listdir(path)
script_start_time = datetime.now()

logging.debug("----------Beggining of log Entry----------\n")
logging.debug("The script started")
logging.debug(datetime.now())


global_path = []
for x in dir_contents: #take the array of directory contents and add the full path to each item and store it in global path array
    global_path.append(path + x)       

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

for i in global_path:
    try:
        if os.path.isfile(i) and get_length(i) > 5000:
            try:
                os.makedirs(dest_path + i.lstrip(path)+"/") # make a dir with that name #THIS DON'T LOOK RIGHT, NEED TO REWORK!
            except Exception as e:   
                logging.error(e)
            finally:
                shutil.move(i, dest_path + i.lstrip(path)+"/") # copy the file to destination
                pass
    except Exception as e:
        logging.error(e)
        pass
    else:
        try:
            items_inside_directory = len(os.listdir(i))    
            if items_inside_directory > 3: # needs to be less than three (currently > for testing purposes)
                duration_of_each_item = []
                for f in os.listdir(i):
                    duration_of_each_item.append(get_length(i +"/"+ f)) # Get duration of each and every item and add to array
                if max(duration_of_each_item) < 5000: # if the longest duration of the item is less than 5000s, pass
                    logging.debug("Skipping ->"+ "'"+i+"'" +" is less than 5000, likely a TV Show")
            else:
                try:
                    shutil.move(i, dest_path + i.lstrip(path)+"/")  # copy the directory to destination
                except Exception as e:
                    logging.error(e)
                pass
        except Exception as e:
            logging.error(e)   #check if ffmpeg can read video file duration      
                
script_end_time = datetime.now()                
logging.debug("The script finished successfully!")
logging.debug("Completed in:")
logging.debug(script_end_time - script_start_time)
exit(logging.debug("-------------End of log Entry-------------\n"))