import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
#for i in range(50):
model_output = libmpc.run_model(0.8735901 , 0.60731104, 0.91117012, 0.25800549, 0.4598458)
#print(time.time() - start)
print(model_output)