import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
#for i in range(50):
model_output = libmpc.run_model(0.01942212, 0.47561208, 0.03928652, 0.01829826, 0.52718099)
#print(time.time() - start)
print(model_output)