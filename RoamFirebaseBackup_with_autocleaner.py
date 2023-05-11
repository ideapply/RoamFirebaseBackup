#!/usr/bin/env python
# coding: utf-8
# 2023-05-06：增加了文件夹筛选下载，去除了所有路径文件夹，已实现功能
# 2023-05-08：优化日志log，消除重复下载的现象，自动补全日志log和下载文件的缺省
# 2023-05-11：1/100概率删除并重建日志log，1/2概率清理已删除文件
# InsightSphere公共知识库中使用，作者：ideapply

import os
import sys
import re
from pathlib import Path
import requests
import shutil
import json
from urllib.parse import urlparse, unquote
from datetime import datetime
import random

def validate_and_move_files(file_storage_dir, firebase_local_records, move_dir, move_record_file):
    move_dir_path = Path(move_dir).expanduser().resolve()
    if not move_dir_path.exists():
        move_dir_path.mkdir()

    move_record_file_path = Path(move_record_file).expanduser().resolve()
    if move_record_file_path.exists():
        with open(move_record_file_path, 'r') as f:
            move_records = json.load(f)
    else:
        move_records = []

    for file_type_folder in ['images', 'pdfs', 'videos', 'others']:
        file_type_path = file_storage_dir / file_type_folder
        if file_type_path.exists():
            for file in file_type_path.iterdir():
                if str(file) not in firebase_local_records.values():
                    new_file_path = move_dir_path / file.name
                    if new_file_path.exists():
                        print(f"File {file} not in records and name conflict. Replacing in {move_dir_path}")
                        os.remove(new_file_path)
                        note = 'Replaced'
                    else:
                        print(f"File {file} not in records. Moving to {move_dir_path}")
                        note = 'Moved'

                    shutil.move(str(file), move_dir_path)
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    record = next((item for item in move_records if item["original_path"] == str(file)), None)
                    if record:
                        record.update({"date_time": timestamp, "new_path": str(new_file_path), "note": note})
                    else:
                        move_records.append({
                            "date_time": timestamp,
                            "original_path": str(file),
                            "new_path": str(new_file_path),
                            "note": note
                        })

    with open(move_record_file_path, 'w') as f:
        json.dump(move_records, f, indent=4)




def get_subfolder_and_filepath(remote_file, file_storage_dir):
    # Extract the folder name and the original filename from the remote_file URL
    url_path = urlparse(remote_file).path
    original_filename = unquote(url_path.split('%2F')[-1])
    file_extension = os.path.splitext(original_filename)[1].lower()

    if file_extension in {'.jpg', '.jpeg', '.png', '.gif'}:
        subfolder = 'images'
    elif file_extension == '.pdf':
        subfolder = 'pdfs'
    elif file_extension in {'.mp4', '.webm', '.avi', '.mov', '.mkv'}:
        subfolder = 'videos'
    else:
        subfolder = 'others'

    download_file_filepath = file_storage_dir / subfolder / original_filename
    return subfolder, download_file_filepath


def download_firebase_file(remote_file, file_storage_dir, firebase_local_records):
    subfolder, download_file_filepath = get_subfolder_and_filepath(remote_file, file_storage_dir)

    if remote_file in firebase_local_records:
        if os.path.exists(download_file_filepath):
#             print("Already downloaded!")
            return
        else:
            print("File record exists, but local file is missing. Re-downloading...")

    elif os.path.exists(download_file_filepath):
        print("No download record, but file exists. Updating the record.")
        firebase_local_records[remote_file] = str(download_file_filepath)
        return

    download_file_directory = download_file_filepath.parent
    if not download_file_directory.exists():
        download_file_directory.mkdir(parents=True)

    r = requests.get(remote_file, stream=True)
    with open(download_file_filepath, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    firebase_local_records[remote_file] = str(download_file_filepath)


if len(sys.argv) < 3:
    print("usage: python roam_file_backup.py [your-roam-json-file] [file-storage-dir]")
    exit()

myjson = Path(sys.argv[1]).expanduser().resolve()
file_storage_dir = Path(sys.argv[2]).expanduser().resolve()

if not file_storage_dir.exists():
    file_storage_dir.mkdir()

for folder in ['images', 'pdfs', 'videos', 'others']:
    subfolder = file_storage_dir / folder
    if not subfolder.exists():
        subfolder.mkdir()

firebase_download_record_json = file_storage_dir / "firebase_local_records.json"

with open(myjson) as f:
    data = f.read()

# Deleting and recreating firebase_local_records.json with probability
if firebase_download_record_json.exists():
    if random.random() < 0.01:  # 1/100 probability
        print("Deleting and recreating firebase_local_records.json with 1/100 probability")
        os.remove(firebase_download_record_json)
        firebase_local_records = {}
        with open(firebase_download_record_json, 'w') as f:
            json.dump(firebase_local_records, f)
    else:
        with open(firebase_download_record_json, 'r') as f:
            firebase_local_records = json.load(f)
else:
    print("Creating new firebase_local_records.json")
    firebase_local_records = {}
    with open(firebase_download_record_json, 'w') as f:
        json.dump(firebase_local_records, f)

remote_files = re.findall(r'https://firebasestorage.googleapis.com/[^)"}\\\]]+', data)
print(f"Found {len(remote_files)} remote files")

for remote_file in remote_files:
    download_firebase_file(remote_file, file_storage_dir, firebase_local_records)

print("Saving firebase_local_records.json")
with firebase_download_record_json.open('w') as f:
    json.dump(firebase_local_records, f, indent=4)
    

# Detecting and moving files not in records with probability
move_dir = file_storage_dir / ".." / "Trash"
move_record_file = move_dir / "move_record.json"

if random.random() < 1/2:  # 1/2 probability
    print("Detecting and moving files not in records with 1/2 probability")
    validate_and_move_files(file_storage_dir, firebase_local_records, move_dir, move_record_file)
