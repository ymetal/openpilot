import os
from panda import build_st

<<<<<<< HEAD
def test_build_legacy():
  build_st("obj/comma.bin", "Makefile.legacy")

def test_build_bootstub_legacy():
  build_st("obj/bootstub.comma.bin", "Makefile.legacy")

=======
>>>>>>> 7d5332833b11570db288f35657a963ed0d8cad0a
def test_build_panda():
  build_st("obj/panda.bin")

def test_build_bootstub_panda():
  build_st("obj/bootstub.panda.bin")

