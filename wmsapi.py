#!/usr/bin/env python3
"""
WMS-API bindings for puthon,
conatining a general wmsapi class,
and a easy-to-use kiddies class.
"""

import requests
import json
import os

debug = True

class wmsapi:
    """
    general wms-api class
    constructed with username and password
    wmsapi.wmsapi(username, password [, url])
    """

    def __init__(self, username, password, url="http://wms.viwetter.de/api/index.php"):
        """
        wmsapi.wmsapi(username, password [, url])
        """
        self.username = username
        self.password = password
        self.url = url

    def post(self, data=None, files=None):
        """
        post([data, files])
        general post request handler
        uses self.url as request target

        arguments:
        data  -- post data (fills username and password if not provided)
        files -- files array
        """
        if not data:
            data = {"username":self.username,"password":self.password}
        if "username" not in data:
            data["username"]=self.username
        if "password" not in data:
            data["password"]=self.password
        r = requests.post(self.url, data=data, files=files)
        return r

    def ping(self):
        """
        ping()
        returns true if the server is up and the login data is correct,
        otherwise false
        """
        return valid(self.url, self.username, self.password)

    def prepfile(self, path):
        """
        prepfile(path)
        opens file in the correct format to be sent over post

        arguments:
        path -- path to file
        """
        return open(path, "rb")


    def uploadfile(self, path, data=None):
        """
        uploadfile(path [, data])
        tries to upload file at <path> to self.url
        <data> is passed through, and necessary for the server
        to accept the file(s)

        arguments:
        path -- path to file
        data -- post data
        """
        f = self.prepfile(path)
        ans = self.post(data, {"file": f})
        f.close()
        return ans

    def newCycle(self, path, target):
        """
        newCycle(path, target)
        adds file at <path> to folder with <target> id
        to query for the id use getTableDict(table)

        arguments:
        path   -- path to file
        target -- target folder id
        """
        data = {"target": target, "function": "newcycle"}
        ret = self.uploadfile(path, data)
        if debug:
            print(ret.text)
        return ret


    def delLastCycle(self, target):
        """
        delLastCycle(target)
        deletes oldst file from folder target

        arguments:
        target -- target folder id
        """
        data = {"target": target, "function": "deloldest"}
        return self.post(data)

    def getFolderSize(self, target):
        """
        getFolderSize(target)
        returns the number of active files in folder with id <target>
        if non-existant returns 0

        arguments:
        target -- target folder id
        """
        data = {"target": target, "function": "dirsize"}
        return int(self.post(data).text)

    def getTableJson(self, table):
        """
        getTableJson(table)
        returns a json string from table <table>
        can be a huge amout of text to be received
        raises LookupError when table doesn't exist

        arguments:
        table -- name of the table [entries, folders, logins]
        """
        if table in ["entries", "folders", "logins"]:
            return self.post({"function":"tablejson", "table": table}).text
        else:
            raise LookupError(str(table) + " not a table")

    def getTableDict(self, table):
        """
        getTableDict(table)
        return a dictionary containing all rows from table <table>
        raises LookupError when table doesn't exist

        arguments:
        table -- name of the table [entries, folders, logins]
        """
        return json.loads(self.getTableJson(table))

    def nicePrintTables(self, tofile=None):
        """
        nicePrintTables([tofile])
        Printing contents of all tables to console or to a
        file if <tofile> is set

        arguments:
        tofile -- destination file (overwrites file)
        """
        dicts = []
        ellipse = 10
        tables = ["entries", "folders", "logins"]
        if tofile:
            with open(tofile, "w") as f: pass
        for tab in tables:
            dicts.append(self.getTableDict(tab))
        for d in dicts:
            form = ""
            length = {}
            for row in d:
                for key in row:
                    if len(row[key])>ellipse:
                        row[key] = row[key][:ellipse+1]+"..."
                    if key in length:
                        if len(row[key])>length[key]:
                            length[key]=len(row[key])
                    else:
                        length[key]=0
            keyname = {}
            for key in d[0]:
                keyname[key]=key
                form += "{"+key+":<"+str(min(length[key]+1,14))+"} "
            if tofile:
                with open(tofile, "a") as f:
                    f.write(form.format(**keyname)+"\n")
                    for row in d:
                        f.write(form.format(**row)+"\n")
                    f.write("\n")
            else:
                print(form.format(**keyname))
                for row in d:
                    print(form.format(**row))
                print("")



class kiddies:
    """
    KIDS wrapper for wmsapi
    generally easier to use, but fewer options

    wmsapi.kiddies(username, password [, target, goalnum])

    arguments:
    username -- username to log in to the wms interface
    password -- self explanatory
    target   -- target folder id to cycle KIDS images
    goalnum  -- number of images to cycle through

    kiddies.cyclekid(npath)
        to add a new image to cycle through

    kiddies.ping()
        pings the server, tests for valid login
    """

    def __init__(self, username, password, url="http://wms.viwetter.de/api/index.php", target=10, goalnum=2):
        self.api = wmsapi(username, password, url)
        self.target = target
        self.goal = goalnum

    def cyclekid(self, npath):
        """
        cyclekid(npath)
        adds the file at <npath> to the default target, this object
        was initialized with.
        if more than self.goalnum images reside at self.target it deletes
        the oldest one after uploading
        """
        self.api.newCycle(npath,self.target)
        if self.api.getFolderSize(self.target) > self.goal:
            self.api.delLastCycle(self.target)

    def ping():
        """
        ping()
        pings the server and return true if login data is correct
        """
        return self.api.ping()

def valid(url, username, password):
    """
    valid(url, username, password)
    procedural version of wmsapi.ping(), tries to access the url and login
    returns true if server is on and accepts the login data
    be aware that you are sending your unencrypted password to the url

    arguments:
    url      -- php file to send the data to (needs to be the FILE*)
    username -- username to log in to the wms interface
    password -- self explanatory

    * doesn't work with \"http://wms.viwetter.de/api\" for example,
      it has to be \"http://wms.viwetter.de/api/index.php\" !
    """
    return "valid" == (requests.post(url, data={"username":username,"password":password,"function":"ping"})).text
