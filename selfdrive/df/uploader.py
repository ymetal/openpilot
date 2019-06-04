import ftplib

ftp = ftplib.FTP("smiskol.com")
ftp.login("eon", "87pYEYF4vFpwvgXU")
with open("../models/driving_model.dlc", "rb") as f:
  ftp.storbinary("STOR /tmpuser/driving_model", f)
ftp.quit()