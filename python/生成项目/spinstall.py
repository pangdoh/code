import sys
import os
import shutil

if len(sys.argv) == 1:
    print('请给出一个参数作为项目名。')
    print('Please give a parameter as the project name.')
else:
    projectName = sys.argv[1]
    if projectName == '-h':
        print('执行：spinstall projectName')
        sys.exit(0)
    print('创建项目:', projectName)

for folder, folderLst, fileList in os.walk('Spango'):
    print(folder)
    print(folderLst)
    print(fileList)

    if folder == 'Spango':
        directory = projectName
    else:
        directory = projectName + folder[6:]

    if not os.path.exists(directory):
        os.makedirs(directory)

    for file in fileList:
        shutil.copyfile(os.path.join(folder, file), os.path.join(directory, file))
