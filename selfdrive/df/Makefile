CXX = clang++

CXXFLAGS = -std=c++14 -fPIC -shared

PHONELIBS = /data/openpilot/phonelibs
SNPE_FLAGS = -I$(PHONELIBS)/snpe/include/
SNPE_LIBS = -lSNPE -lsymphony-cpu -lsymphonypower

OBJS = dynamic_follow.o

all: dynamic_follow.so

dynamic_follow.so: dynamic_follow.cc dynamic_follow.h
  clang++ dynamic_follow.cc

$(OUTPUT): $(OBJS)
	@echo "[ LINK ] $@"
	$(CXX) -fPIC -o '$@' $^ \
        $(SNPE_LIBS)

%.o: %.cc
	@echo "[ CXX ] $@"
	$(CXX) $(CXXFLAGS) -MMD \
           -Iinclude -I.. -I../.. \
           $(SNPE_FLAGS) \
           -c -o '$@' '$<'
