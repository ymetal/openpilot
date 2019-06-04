import ftplib

ftp = ftplib.FTP("smiskol.com")
ftp.login("eon", "87pYEYF4vFpwvgXU")
with open("main.py", "rb") as f:
  ftp.storbinary("STOR main.py", f.read())
ftp.quit()