# RoamFirebaseBackup
RoamFirebaseBackup 是一个用于备份 Roam Research 中 Firebase 存储的远程文件的 Python 脚本。它从 Roam JSON 文件中提取远程文件链接，将文件下载到本地文件夹，并根据文件类型将其存储在不同的子文件夹中。该脚本同时维护了一个记录文件，用于追踪已下载的文件，以便在将来运行时避免重复下载。
