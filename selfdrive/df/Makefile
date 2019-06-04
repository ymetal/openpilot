CC = clang++ # C compiler
CFLAGS = -fPIC -Wall -Wextra -O2 -g # C flags
LDFLAGS = -shared  # linking flags
RM = rm -f  # rm command
TARGET_LIB = dynamic_follow.so # target lib

SRCS = dynamic_follow.cc # source files
OBJS = $(SRCS:.cc=.o)

.PHONY: all
all: ${TARGET_LIB}

$(TARGET_LIB): $(OBJS)
	$(CC) ${LDFLAGS} -o $@ $^

$(SRCS:.cc=.d):%.d:%.cc
	$(CC) $(CFLAGS) -MM $< >$@

include $(SRCS:.cc=.d)

.PHONY: clean
clean:
	-${RM} ${TARGET_LIB} ${OBJS} $(SRCS:.cc=.d)