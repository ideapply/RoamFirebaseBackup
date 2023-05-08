# RoamFirebaseBackup
RoamFirebaseBackup 是一个用于备份 Roam Research 中 Firebase 存储的远程文件的 Python 脚本。它从 Roam JSON 文件中提取远程文件链接，将文件下载到本地文件夹，并根据文件类型将其存储在不同的子文件夹中。该脚本同时维护了一个记录文件，用于追踪已下载的文件，以便在将来运行时避免重复下载。

## 已实现功能
- Roam Research中所有Firebase文件的备份和分文件夹存储
- 简洁的日志文件用以记录原下载路径和本地存放位置
- 已下载的文件不会重复下载
- 自动补全日志内容缺失项和已下载文件缺失项

## 待实现功能
- [ ] 利用Hex校对文件的完整性
- [ ] 实现本地edn文件转md文件
- [ ] 实现md文件中的远程链接转本地链接
- [ ] 实现已下载文件随edn文件删除而删除

## 用法
- 安装调用的python库文件
- 运行命令： `python roam_image_backup.py [your-roam-json-file] [image-storage-dir]`

## 参考
王树义wshuyi：https://github.com/wshuyi/demo-roam-image-bak
