import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
for i in range(50):
  model_output = libmpc.run_model(.542, .2, .15, .2, .5)
print(time.time() - start)
print(model_output)