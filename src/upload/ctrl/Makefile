
# this script only for static library build


# the target file
TG:=libtigress_ctrl.a
TGDIR:=.


# the compiler flag
CXX:=g++
CXXFLAGS:=${flags} -static -Wall


# where to find .h
INCLUDE:=-I ./include\
         -I ../include \
         -I ../../../../../Library/funshion/include/msgq/0.1.0 \
         -I ../../../../../Library/funshion/src/kernel/0.1.2/include\
	 -I ../../../../../Library/funshion/src/thread/0.1.1/src/include

# where to find .cpp
SRC_DIRS:=./
#SRC_DIRS+=../



# 所有 .cpp .o .d 文件集合
OBJDIR:=./obj
DIRS:=${TGDIR} ${OBJDIR}
#MKDIR:= $(shell if [ ! -d ${OBJDIR} ]; then mkdir -p ${OBJDIR}; fi)
MKDIR := $(shell for d in $(DIRS); \
		       do \
		       [[ -d $$d ]] || mkdir -p $$d ; \
		       done)

SRC1:=$(foreach srcdir, ${SRC_DIRS}, $(wildcard ${srcdir}*.cpp))

SRC:=$(foreach src, ${SRC1},$(notdir ${src}))
#SRC:=$(filter tigress_conf.cpp, $(SRC2))
OBJS:=$(patsubst %.cpp, ${OBJDIR}/%.o, ${SRC})
DEPS:=$(patsubst %.cpp, ${OBJDIR}/%.d, ${SRC})


# 搜寻路径
#vpath %.h ${INCLUDE}
vpath %.cpp ${SRC_DIRS}


# real target
TARGET:= $(addprefix ${TGDIR}/, ${TG})

${TARGET}:${OBJS} ${DEPS}
	ar -r ${TARGET} ${OBJS}

${OBJS}:${OBJDIR}/%.o:%.cpp
	@${CXX} ${CXXFLAGS} ${INCLUDE} -c $< -o $@


# 文件依赖项
-include ${DEPS}
${OBJDIR}/%.d:%.cpp
	@set -e; \
	rm -f $@; \
	${CXX} -MM ${INCLUDE} ${CXXFLAGS} $< > $@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
	rm -f $@.$$$$

cppcheck:
	cppcheck -f -q --enable=all --platform=unix64 ${INCLUDE} ${SRC}

#clean
.PHONY : clean

clean:
	-@rm -rf ${OBJS}
	-@rm -rf ${DEPS}
	-@rm -rf ${TARGET}
