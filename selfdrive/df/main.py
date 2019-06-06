import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
#for i in range(50):
model_output = libmpc.run_model(0.8653078153514447,
 0.46805728618371273,
 0.7687240569853148,
 0.43000914913083255,
 0.48780443294609244)
#print(time.time() - start)
print(model_output)