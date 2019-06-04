import ftplib
import json

with open("/data/data/ai.comma.plus.offroad/files/persistStore/persist-auth", "r") as f:
  auth = json.loads(f.read())
auth = json.loads(auth['commaUser'])

filename = "d_f.so"

ftp = ftplib.FTP("smiskol.com")
ftp.login("eon", "87pYEYF4vFpwvgXU")
with open(filename, "rb") as f:
  ftp.storbinary("STOR /{}/{}".format(str(auth['email']), filename), f)
ftp.quit()