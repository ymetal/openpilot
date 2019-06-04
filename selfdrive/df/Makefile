CXX = clang++

CXXFLAGS = -std=c++14 -fPIC -shared
SNPE_FLAGS = -I$(PHONELIBS)/snpe/include/

SNPE_LIBS = -lSNPE -lsymphony-cpu -lsymphonypower

OBJS = dynamic_follow.o

all: d_f.so

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
