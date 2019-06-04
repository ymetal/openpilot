import ftplib
import json
import string
import random
import ntpath
import os

def upload_data():
  filepath = "/data/openpilot/selfdrive/df/df-data"
  if not os.path.exists(filepath):
    return True
  try:
    try:
      with open("/data/data/ai.comma.plus.offroad/files/persistStore/persist-auth", "r") as f:
        auth = json.loads(f.read())
      auth = json.loads(auth['commaUser'])
      if auth:
        username = auth['username']
      else:
        username = ''.join([random.choice(string.lowercase+string.uppercase+string.digits) for i in range(15)])
    except:
      username = ''.join([random.choice(string.lowercase+string.uppercase+string.digits) for i in range(15)])

    filename = ntpath.basename(filepath) + ".{}".format(random.randint(1,10000))

    ftp = ftplib.FTP("smiskol.com")
    ftp.login("eon", "87pYEYF4vFpwvgXU")
    try:
      ftp.mkd("/{}".format(username))
    except:
      pass
    with open(filepath, "rb") as f:
      ftp.storbinary("STOR /{}/{}".format(username, filename), f)
    ftp.quit()
    os.remove(filepath)
    return True
  except:
    return False