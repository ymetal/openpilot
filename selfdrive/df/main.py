import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
#for i in range(50):
model_output = libmpc.run_model(0.38932858, 0.24922614, 0.29498888, 0.24680073, 0.34690347)
#print(time.time() - start)
print(model_output)