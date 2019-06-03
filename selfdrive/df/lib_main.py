from cffi import FFI
import os

if not os.path.isfile('/data/openpilot/selfdrive/df/d_f.so'):
    Makefile = "/data/openpilot/selfdrive/df/Makefile.sh"
    os.chmod(Makefile, 0775)
    os.system("exec " + Makefile)

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