# autowkid
Automatically generate WMS_Kiddy images, either with online or offline Database

## Goal
- [ ] Routine for filling local database
- [ ] Pull data from local database
- [ ] Generate WMS_Kiddy Images
- [ ] Automatically upload to wms system

### Part-Goals
- [ ] Sqlite3
- [x] Drawing image
- [ ] Secure Uploading 50%
- [x] Calculate needed Week(days)
- [ ] XML-Parser

# WMS-API
This is the generall usage:
```python
import wmsapi
# general api instance
api = wmsapi.wmsapi("uname", "passw")
api.ping()                      # returns true if login is correct
api.newCycle("path/to/file", 5) # <num> is folder dir, to add image to
api.delLastCycle(5)             # deletes oldes img from folder <num>
api.getFolderSize(5)            # returns num of images in folder <num>

# kiddies api instance
kid = wmsapi.kiddies("uname", "passw")
kid.cyclekid("path/to/new/image")
# kid also contains a general api as kid.api
```
## TODO
- [ ] delete specific id
- [ ] create new folders
- [ ] create new users
- [ ] more information-queries (folders, users, changes, ...)
