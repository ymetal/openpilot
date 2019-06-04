import ftplib
import json
import string
import random
import ntpath

with open("/data/data/ai.comma.plus.offroad/files/persistStore/persist-auth", "r") as f:
  auth = json.loads(f.read())
auth = json.loads(auth['commaUser'])
if auth:
  username = auth['username']
else:
  username = ''.join([random.choice(string.lowercase+string.uppercase+string.digits) for i in range(15)])
username = "shane@smiskol.com"
filepath = "/data/openpilot/selfdrive/df/gathered_data/df-data"
filename = ntpath.basename(filepath) + ".{}".format(random.randint(1,10000))

ftp = ftplib.FTP("smiskol.com")
ftp.login("eon", "87pYEYF4vFpwvgXU")
print "STOR /{}/{}".format(username, filename)
ftp.mkd("/{}".format(username))
with open(filepath, "rb") as f:
  ftp.storbinary("STOR /{}/{}".format(username, filename), f)
ftp.quit()