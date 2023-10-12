import sys
import os
import time
import shutil
from pathlib import Path


# function that return the args passed from the terminal
def getArgs():
    argsList = sys.argv[1:]
    return argsList


# function that write logs in the specific file
def writeInLogFile(path,text):
    with open(path, "a") as file:
        file.write(text + "\n")
        print(text)

# function that reads and returns the content of a txt file
def getFileContent(filePath):
    with open(filePath,"r") as file:
        content = file.read()
        return content


#this function return in a list the content of a folder
#the list will contain dictionaties with this specific data: type of a file, path of a component, and content if type = file
def folderContent(initialFolderPath):

    # list of all the directories including the source directory
    folderPathList = []

    # list of content
    folderContent = []

    folderPathList.append(initialFolderPath)

    # for each directory
    for folderPath in folderPathList:
        folderPathContent = os.listdir(folderPath)

        # content of a directory
        for item in folderPathContent:

            itemPath = Path(folderPath) / item
            dict = {}
            dict["path"] = itemPath

            if itemPath.is_dir():
                folderPathList.append(itemPath)
                dict["type"] = "directory"

            elif itemPath.is_file():
                dict["type"] = "file"
                dict["content"] = getFileContent(itemPath)


            folderContent.append(dict)

    return folderContent





# delete a txt file or a directory by giving its path
def deletePath(path,type,logFilePath):
    # delete a txt file
    if type == "file":
        if os.path.exists(path):
            os.remove(path)
            writeInLogFile(logFilePath,f"File {path} has been deleted")
        else:
            writeInLogFile(logFilePath, f"File {path} has already been deleted")
    # delete a folder
    else:
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                writeInLogFile(logFilePath, f"The directory at {path} has been deleted.")
            except PermissionError as e:
                print(f"PermissionError: {e}")
        else:
            writeInLogFile(logFilePath, f"Diretory {path} has already been deleted")



#  function that compare the content of the 2 folders and syncronizing them
def folderSyncronization(path, path2, logFilePath):

    contentFolderList = folderContent(path)
    contentFolderListPath = [str(x["path"]) for x in contentFolderList]

    contentFolderCopyList = folderContent(path2)
    contentFolderCopyListPath = [str(x["path"]) for x in contentFolderCopyList]

    # this case deletes any path from the copy folder that does not appear in the source folder
    for item in contentFolderCopyList:
        itemPath = str(item["path"]).replace(path2,path)
        if itemPath not in contentFolderListPath:
            deletePath(str(item["path"]), item["type"],logFilePath)


    # this case add new content or updates content of the copy folder
    for item in contentFolderList:
        itemPath = str(item["path"]).replace(path,path2)

        if itemPath not in contentFolderCopyListPath:
            writeInLogFile(logFilePath, f"Creating file {itemPath}")

        else:
            writeInLogFile(logFilePath, f"Coping file {itemPath}")


        if item["type"] == "file":
            with open(itemPath,"w") as file:
                file.write(item["content"])
        else:
            os.makedirs(itemPath, exist_ok=True)


# this funtion apply the timer for the syncronization of the 2 folders
def folderSyncronizationPeriod():
    argsList = getArgs()

    path = argsList[0]
    path2 = argsList[1]
    duration = int(argsList[2])
    logFilePath = argsList[3]

    i = 1

    while True:
        writeInLogFile(logFilePath, f"Log Number: {i}")
        folderSyncronization(path,path2,logFilePath)
        writeInLogFile(logFilePath, "\n")

        i+=1
        time.sleep(duration)



def main():

    folderSyncronizationPeriod()


if __name__ == "__main__":
    main()



# python main.py C:\other\An3\Sem2\python\folderSyn\folder1 C:\other\An3\Sem2\python\folderSyn\folderCopy 15  C:\other\An3\Sem2\python\folderSyn\log_file.txt