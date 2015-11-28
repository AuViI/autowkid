#!/usr/bin/env python3
import requests
import json
import os

debug = True

class wmsapi:

    def __init__(self, username, password, url="http://wms.viwetter.de/api/index.php"):
        self.username = username
        self.password = password
        self.url = url

    def post(self, data=None, files=None):
        if not data:
            data = {"username":self.username,"password":self.password}
        r = requests.post(self.url, data=data, files=files)
        return r

    def ping(self):
        return valid(self.url, self.username, self.password)

    def prepfile(self, path):
        return open(path, "rb")


    def uploadfile(self, path, data=None):
        f = self.prepfile(path)
        ans = self.post(data, {"file": f})
        f.close()
        return ans

    def newCycle(self, path, target):
        data = {"username":self.username, "password": self.password, "target": target, "function": "newcycle"}
        ret = self.uploadfile(path, data)
        if debug:
            print(ret.text)
        return ret


    def delLastCycle(self, target):
        data = {"username": self.username, "password": self.password, "target": target, "function": "deloldest"}
        return self.post(data)

    def getFolderSize(self, target):
        data = {"target": target, "function": "dirsize"}
        return int(self.post(data).text)

class kiddies:
    def __init__(self, username, password, url="http://wms.viwetter.de/api/index.php", target=10, goalnum=2):
        self.api = wmsapi(username, password, url)
        self.target = target
        self.goal = goalnum

    def cyclekid(self, npath):
        self.api.newCycle(npath,self.target)
        if self.api.getFolderSize(self.target) > self.goal:
            self.api.delLastCycle(self.target)

def valid(url, username, password):
    return "valid" == (requests.post(url, data={"username":username,"password":password,"function":"ping"})).text
