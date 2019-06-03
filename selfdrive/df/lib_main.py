from cffi import FFI
import os
import subprocess


if not os.path.isfile('/data/openpilot/selfdrive/df/d_f.so'):
    Makefile = "/data/openpilot/selfdrive/df/Makefile.sh"
    os.chmod(Makefile, 0775)
    os.system("exec " + Makefile)


'''mpc_dir = "/data/openpilot/selfdrive/df"

if platform.machine() == "x86_64":
  try:
    FFI().dlopen(os.path.join(mpc_dir, "main"))
  except OSError:
    print("Error!!")'''

#subprocess.check_call(["make", "-j4"], cwd=mpc_dir)

def get_libmpc():
    libmpc_fn = "/data/openpilot/selfdrive/df/d_f.so"


    ffi = FFI()
    ffi.cdef("""
    typedef struct {
      float testvar;
    } testvar_t;
    
    float run_model(float v_ego, float a_ego, float v_lead, float x_lead, float a_lead);
    void init_model();
    """)

    return (ffi, ffi.dlopen(libmpc_fn))

'''mpcs = [_get_libmpc(1), _get_libmpc(2)]

def get_libmpc(mpc_id):
    return mpcs[mpc_id - 1]'''


'''start=time.time()
output = subprocess.check_output(['/data/openpilot/selfdrive/df/main', '.8', '.5', '.2', '.4', '.5'])
print(float(output))
print(time.time()-start)'''