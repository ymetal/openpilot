import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
for i in range(50):
  model_output = libmpc.run_model(0.45368120074272156, 0.09261506050825119, 0.9544134140014648, 18.375, 0.0)
print(time.time() - start)
print(model_output)