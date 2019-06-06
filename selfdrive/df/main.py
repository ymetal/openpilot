import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
#for i in range(50):
model_output = libmpc.run_model(0.8653078153514447,
 0.46805728618371273,
 0.8591260060867878,
 0.6495882891125343,
 0.5192517358961403)
#print(time.time() - start)
print(model_output)