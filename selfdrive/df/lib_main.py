from cffi import FFI
import os
import subprocess

Makefile = "/data/openpilot/selfdrive/df/Makefile"

subprocess.check_call(["make", "-j4"], cwd="/data/openpilot/selfdrive/df")

def get_libmpc():
    libmpc_fn = "/data/openpilot/selfdrive/df/dynamic_follow.o"

    ffi = FFI()
    ffi.cdef("""
    typedef struct {
      float testvar;
    } testvar_t;
    
    float run_model(float v_ego, float a_ego, float v_lead, float x_lead, float a_lead);
    void init_model();
    """)

    return (ffi, ffi.dlopen(libmpc_fn))