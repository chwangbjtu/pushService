
# this script only for static library build


# the target file
TG:=oupload
TGDIR:=.
DEST_BIN := ./upload/


# the compiler flag
CXX:=g++
CXXFLAGS:=${flags} -Wall -DMAKEFILEBUILD_DATE="\"`date '+%Y-%m-%d %H:%M:%S'`"\"

version:=0.1.7

# where to find .h
INCLUDE:=-I ./include\
	 -I ./util/include\
	 -I ./info_manager/include\
	 -I ./visitor/include\
	 -I ./receptor/include\
         -I ./ctrl/include \
	 -I ./common/include\
	 -I ./sync_disk/include\
	 -I ./mgmt/include\
	 -I ./http/include\
	 -I ./json/0.1.1/src/include\
	 -I ./json/0.1.1/jsoncpp-src-0.5.0/include\
	 -I ../../../../Library/funshion/src/thread/0.1.1/src/include\
	 -I ../../../../Library/funshion/src/netsvc/0.1.4/src/include\
	 -I ../../../../Library/funshion/src/kernel/0.1.2/include\
	 -I ../../../../Library/funshion/src/timer/0.1.0/src/include\
	 -I ../../../../Library/funshion/src/logger/0.2.0/src/include\
	 -I ../../../../Library/funshion/src/msgq/0.1.3/src/include


STATIC_LIBS := ./info_manager/libinfo_manager.a
STATIC_LIBS += ./receptor/libreceptor.a
STATIC_LIBS += ./sync_disk/libsync_disk.a
STATIC_LIBS += ./mgmt/libmgmt.a
STATIC_LIBS += ./visitor/libvisitor.a
STATIC_LIBS += ./ctrl/libtigress_ctrl.a
STATIC_LIBS += ./common/libtigress_common.a
STATIC_LIBS += ./util/libtigress_util.a
STATIC_LIBS += ./http/libhttp.a
STATIC_LIBS += ./json/0.1.1/src/libjson.a
STATIC_LIBS += ../../../../Library/funshion/lib/thread/0.1.1/libthread.a
STATIC_LIBS += ../../../../Library/funshion/lib/netsvc/0.1.4/libnetsvc.a
STATIC_LIBS += ../../../../Library/funshion/lib/kernel/0.1.2/libkernel.a
STATIC_LIBS += ../../../../Library/funshion/lib/timer/0.1.0/libtimer.a
STATIC_LIBS += ../../../../Library/funshion/lib/logger/0.2.0/liblogger.a
STATIC_LIBS += ../../../../Library/funshion/lib/msgq/0.1.3/libmsgq.a

# where to find .cpp
SRC_DIRS:=./
#SRC_DIRS+=../../../../../Library/funshion/src/kernel/0.1.2/



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
OBJS:=$(patsubst %.cpp, ${OBJDIR}/%.o, ${SRC})
DEPS:=$(patsubst %.cpp, ${OBJDIR}/%.d, ${SRC})


SLD_FLAGS:=-lpthread -lrt -lz -lssl


# 搜寻路径
#vpath %.h ${INCLUDE}
vpath %.cpp ${SRC_DIRS}


# real target
TARGET:= $(addprefix ${TGDIR}/, ${TG})

${TARGET}:${OBJS} ${DEPS}
	${CXX} ${CXXFLAGS} -o ${TARGET} ${OBJS} ${STATIC_LIBS} ${SLD_FLAGS}
	-@if [ ! -d ${DEST_BIN} ]; then mkdir -p ${DEST_BIN}; fi
	cp -f $(TARGET) ./upload/upload

${OBJS}:${OBJDIR}/%.o:%.cpp
	@${CXX} ${CXXFLAGS} ${INCLUDE} -c $< -o $@ -DTIGRESS_VERSION=\"${version}\"


# 文件依赖项
-include ${DEPS}
${OBJDIR}/%.d:%.cpp
	@set -e; \
	rm -f $@; \
	${CXX} -MM ${INCLUDE} ${CXXFLAGS} $< > $@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
	rm -f $@.$$$$

cppcheck:
	cppcheck -q -v --enable=all --platform=unix64 ${INCLUDE} .


# clean
.PHONY : clean

clean:
	-@rm -rf ${OBJS}
	-@rm -rf ${DEPS}
	-@rm -rf ${TARGET}


