CC = clang
CXX = clang++

PHONELIBS = ../../phonelibs

WARN_FLAGS = -Werror=implicit-function-declaration \
             -Werror=incompatible-pointer-types \
             -Werror=int-conversion \
             -Werror=return-type \
             -Werror=format-extra-args \
             -Wno-deprecated-declarations

CFLAGS = -std=gnu11 -fPIC -O2 $(WARN_FLAGS)
CXXFLAGS = -std=c++14 -fPIC -O2 $(WARN_FLAGS)

SNPE_FLAGS = -I$(PHONELIBS)/snpe/include/
SNPE_LIBS = -lSNPE -lsymphony-cpu -lsymphonypower

OBJS = dynamic_follow.o
OUTPUT = dynamic_follow.so

.PHONY: all
all: $(OUTPUT)

include ../common/cereal.mk

#MODEL_DATA = ../../models/driving_bigmodel.dlc ../../models/monitoring_model.dlc
MODEL_DATA = ../../models/driving_model.dlc ../../models/monitoring_model.dlc ../../models/posenet.dlc
MODEL_OBJS = $(MODEL_DATA:.dlc=.o)

ifeq ($(RELEASE),1)
CFLAGS += -DCLU_NO_SRC
CXXFLAGS += -DCLU_NO_SRC
CLCACHE_FILES = $(wildcard /tmp/clcache/*.clb)
CLCACHE_OBJS += $(CLCACHE_FILES:.clb=.o)

clutil.o: clcache_bins.h
clcache_bins.h: $(CLCACHE_FILES) /tmp/clcache/index.cli
	rm -f '$@'
	for hash in $(basename $(notdir $(CLCACHE_FILES))) ; do \
		echo "extern const uint8_t clb_$$hash[] asm(\"_binary_$${hash}_clb_start\");" ; \
		echo "extern const uint8_t clb_$${hash}_end[] asm(\"_binary_$${hash}_clb_end\");" ; \
	done >> '$@'
	echo "static const CLUProgramIndex clu_index[] = {" >> '$@'
	while read idx_hash code_hash; do \
		echo "{ 0x$$idx_hash, clb_$${code_hash}, clb_$${code_hash}_end }," ; \
	done < /tmp/clcache/index.cli >> '$@'
	echo "};" >> '$@'


LDFLAGS += -s
endif

DEPS := $(OBJS:.o=.d)

$(OUTPUT): $(OBJS)
	@echo "[ LINK ] $@"
	$(CXX) -fPIC -o '$@' $^ \
        $(LDFLAGS) \
        $(SNPE_LIBS) \
        -shared

%.o: %.cc
	@echo "[ CXX ] $@"
	$(CXX) $(CXXFLAGS) -MMD \
           -Iinclude -I.. -I../.. \
           $(SNPE_FLAGS) \
           -c -o '$@' '$<'


.PHONY: clean
clean:
	rm -f $(OBJS) $(DEPS)

-include $(DEPS)
