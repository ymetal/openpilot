import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
#for i in range(50):
model_output = libmpc.run_model(0.7571233503307875, 0.4175185966920483, 0.8440064518777697, 0.5402193784277879, 0.5435700507563265)
#print(time.time() - start)
print(model_output)