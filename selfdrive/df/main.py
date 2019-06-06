import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
#for i in range(50):
model_output = libmpc.run_model(0.5768718769009631,
 0.46805728618371273,
 0.7329015159297991,
 0.14250687077767613,
 0.6764882506463793)
#print(time.time() - start)
print(model_output)