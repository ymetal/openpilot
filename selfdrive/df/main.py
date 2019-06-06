import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
#for i in range(50):
model_output = libmpc.run_model(0.56969978, 0.45996605, 0.63368414, 0.28545288, 0.55364933)
#print(time.time() - start)
print(model_output)