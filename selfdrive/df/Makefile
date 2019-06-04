CXX = clang++

CXXFLAGS = -std=c++14 -fPIC

PHONELIBS = /data/openpilot/phonelibs
SNPE_FLAGS = -I$(PHONELIBS)/snpe/include/
SNPE_LIBS = -lSNPE -lsymphony-cpu -lsymphonypower

OBJS = dynamic_follow.o
OUTPUT = dynamic_follow.so

all: $(OUTPUT)
	clang++ -c dynamic_follow.cc

$(OUTPUT): $(OBJS)
	@echo "[ LINK ] $@"
	$(CXX) -fPIC -o -shared '$@' $^ \
        $(SNPE_LIBS)

%.so: %.cc
	@echo "[ CXX ] $@"
	$(CXX) $(CXXFLAGS) -MMD \
           -Iinclude -I.. -I../.. \
           $(SNPE_FLAGS) \
           -c -o '$@' '$<'

