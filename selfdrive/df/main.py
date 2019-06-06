import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
#for i in range(50):
model_output = libmpc.run_model(0.5768718769009631,
 0.46805728618371273,
 0.32030169041054785,
 0.21043000914913082,
 0.44063347852102075)
#print(time.time() - start)
print(model_output)