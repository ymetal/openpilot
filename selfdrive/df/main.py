import time
from selfdrive.df import lib_main
ffi, libmpc = lib_main.get_libmpc()
libmpc.init_model()
start = time.time()
#for i in range(50):
model_output = libmpc.run_model(0.5064629289493703, 0.585489275313391, 0.5548046719786361, 0.06855575868372943, 0.6555515986699871)
#print(time.time() - start)
print(model_output)