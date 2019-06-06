import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
for i in range(50):
  model_output = libmpc.run_model(13.860774993896484, 1.5514190196990967, 15.235774993896484, 30.125, 1.1607612371444702)
print(time.time() - start)
print(model_output)