# RoamFirebaseBackup
RoamFirebaseBackup is a Python script for backing up remote files stored in Firebase from Roam Research. It extracts remote file links from Roam JSON/EDN files, downloads the files to a local folder, and stores them in different subfolders based on file type. The script also maintains a log file to track downloaded files to avoid re-downloading in future runs.

## Implemented Features
- Backup and categorized storage of all Firebase files in Roam Research
- Concise log files to record original download paths and local storage locations
- Downloaded files are not re-downloaded
- Automatically completes missing items in log content and downloaded files

## Features to be Implemented
- [ ] ~~Use MD5 to verify file integrity~~
  - Firebase storage does not provide MD5 verification, so this feature is currently impossible in principle
- [ ] Implement local EDN file to MD file conversion
- [ ] Convert remote links in MD files to local links
- [x] Implement deletion of downloaded files along with EDN file deletion
  - Implemented in RoamFirebaseBackup_with_autocleaner.py, where cleaned historical files are placed in a newly created `Trash` folder, with transfer logs recorded in a log file.

## Usage
- Install required Python libraries
- Run command: `python roam_image_backup.py [your-roam-json-file] [image-storage-dir]`

## Postscript
All the basic functionalities that can be implemented for Roam Research attachment backup are now complete. The remaining two are related to format conversion; after some simple tests in the past few days, the conversion effect was mediocre and cumbersome, and due to limited personal capabilities, these are indefinitely shelved for now.

## Reference
Wang Shuyi (wshuyi): https://github.com/wshuyi/demo-roam-image-bak
