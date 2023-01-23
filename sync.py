import os
import argparse
import time
import hashlib
import shutil
import sys
from pathlib import Path
try:
    src_folder=sys.argv[1]
    rep_folder=sys.argv[2]
    interval=int(sys.argv[3])
    log=sys.argv[4]

except:
    print("Please pass in order:source path,replica path,sync interval(segundos) and log file path")

while True:
    src_files = set(os.listdir(src_folder))
    rep_files = set(os.listdir(rep_folder))

    for file in src_files-rep_files:
        with open(log,"a") as f:
            f.write("Creating file: {}\n".format(file))
            print("Creating file: {}".format(file))
        rep_path=os.path.join(rep_folder,file)
        src_path=os.path.join(src_folder,file)
        if os.path.isdir(src_path): 
            shutil.copytree(src_path,rep_path)
            continue
        with open(src_path,"rb") as src_file, open (rep_path,"wb") as rep_file:
            rep_file.write(src_file.read())
    
    for file in src_files & rep_files:
            src_path = os.path.join(src_folder, file)
            rep_path = os.path.join(rep_folder, file)
            if os.path.isfile(src_path):
                src_hash = hashlib.md5(open(src_path, "rb").read()).hexdigest()
                rep_hash = hashlib.md5(open(rep_path, "rb").read()).hexdigest()
                if src_hash != rep_hash:
                    with open(log, "a") as f:
                        f.write("Updating file: {}\n".format(file))
                        print("Updating file: {}".format(file))
                    with open(src_path, "rb") as src_file, open(rep_path, "wb") as dest_file:
                        dest_file.write(src_file.read())
            else:
                src_dirtime=os.path.getmtime(src_path)
                rep_dirtime=os.path.getmtime(rep_path)
                if src_dirtime>rep_dirtime:
                    with open(log, "a") as f:
                        f.write("Updating file: {}\n".format(file))
                        print("Updating file: {}".format(file))
                shutil.rmtree(rep_path)
                shutil.copytree(src_path,rep_path)

    for file in rep_files-src_files:
        rep_path=os.path.join(rep_folder,file)
        if os.path.isfile(rep_path):
            os.remove(rep_path)
        else:
            shutil.rmtree(rep_path)
        with open(log,"a") as f:
            f.write("Removing file: {}\n".format(file))
            print("Removing file: {}".format(file))
    time.sleep(interval)
