import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
#for i in range(50):
model_output = libmpc.run_model(0.56774114, 0.45166676, 0.63579264, 0.3074108 , 0.53351793)
#print(time.time() - start)
print(model_output)