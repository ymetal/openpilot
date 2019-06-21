import os

if os.environ.get('LOGGERD_ROOT', False):
  ROOT = os.environ['LOGGERD_ROOT']
  print("Custom loggerd root: ", ROOT)
else:
  ROOT = '/data/media/0/realdata/'

SEGMENT_LENGTH = 60
<<<<<<< HEAD
=======


def get_available_percent():
    try:
      statvfs = os.statvfs(ROOT)
      available_percent = 100.0 * statvfs.f_bavail / statvfs.f_blocks
    except OSError:
      available_percent = 100.0

    return available_percent
>>>>>>> 7d5332833b11570db288f35657a963ed0d8cad0a
