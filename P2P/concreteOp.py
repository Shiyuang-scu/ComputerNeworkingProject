import os
from functools import reduce
import json


class UDLoad:
    def __init__(self):
        self.__sharingFileList = []
        self.__sharingDirList = []


    #### Get the detail of files ####

    def getFileDetails(self, filePath):
        size = os.path.getsize(filePath)
        name = os.path.basename(filePath)
        path = os.path.realpath(filePath)
        return {'name': name, 'size': size, 'path': path}

    #### Search in the file list ####
    def searchFileInList(self, list, name):
        return [self.getFileDetails(file['name']) for file in list if
                os.path.basename(file['name']).find(name) != -1 and file['share']]

    #### Get every file in file list ####
    def searchFileInDir(self, pathName, isShare):
        result = []
        current_path = os.path.realpath(pathName)
        for file in os.listdir(current_path):
            path = current_path + '/' + file
            if os.path.isfile(path):
                result.append({'name': path, 'share': isShare})
            elif os.path.isdir(path):
                result = result + self.searchFileInDir(path, isShare)
        return result

    #### Search ####
    def search(self, name):
        query1 = self.searchFileInList(self.__sharingFileList, name)
        query2 = self.searchFileInList(
            reduce(lambda x, y: x + y,
                   [self.searchFileInDir(path['name'], path['share']) for path in self.__sharingDirList], []), name)
        result = [json.dumps(r) for r in query1 + query2]
        result = list(set(result))
        result = [json.loads(r) for r in result]
        return result

    #### Add file ####
    def addShareFile(self, filepath):
        filename = os.path.realpath(filepath)
        if filepath != '':
            for data in self.__sharingFileList:
                if filename == data['name']:
                    data['share'] = True
                    return
            self.__sharingFileList.append({'name': filename, 'share': True})

    #### Add contents of file ####
    def addShareDir(self, dirpath):
        if dirpath != "":
            for data in self.__sharingDirList:
                if dirpath == data['name']:
                    data['share'] = True
                    return
            self.__sharingDirList.append({'name': dirpath, 'share': True})

    def delShare(self, path):
        current_path = os.path.realpath(path)
        if os.path.isdir(current_path):
            for i in self.__sharingDirList:
                if i['name'] == current_path:
                    self.__sharingDirList.remove(i)
                    return
        elif os.path.isfile(current_path):
            for i in self.__sharingFileList:
                if i['name'] == current_path:
                    self.__sharingFileList.remove(i)
                    return

    def changShareState(self, path, state):
        current_path = os.path.realpath(path)
        if os.path.isdir(current_path):
            for data in self.__sharingDirList:
                if data['name'] == current_path:
                    data['share'] = state
                    return
        elif os.path.isfile(current_path):
            for data in self.__sharingFileList:
                if data['name'] == current_path:
                    data['share'] = state
                    return

    def getFileList(self):
        return self.__sharingFileList

    def getDirList(self):
        return self.__sharingDirList

