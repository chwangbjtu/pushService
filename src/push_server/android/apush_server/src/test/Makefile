##target lib###
CXX=g++
TARGET=cppcache_server
FUNSHION_LIB := ../../../../../workspace/Library/funshion/lib
LOGINSERVER_LIB := ../lib
DEST_ETC := ../bin/etc/
DEST_LOG := ../bin/log/

LIB := $(FUNSHION_LIB)/mongodb/cxx_driver/2.0/libmongoclient.a
LIB += $(FUNSHION_LIB)/boost/linux_64/libboost_thread.a
LIB += $(FUNSHION_LIB)/boost/linux_64/libboost_filesystem.a
LIB += $(FUNSHION_LIB)/boost/linux_64/libboost_system.a




#HEADER_DIR := ./include
#HEADER_DIR += ../../../../../../workspace/Library/funshion/include/mongodb/cxx_driver/2.0
HEADER_DIR := ../../../../../workspace/Library/funshion/include/boost/boost_1_40/
HEADER_DIR += ../../../../../workspace/Library/funshion/include/mongodb/cxx_driver/2.0/
HEADER_DIR += ./include


INCLUDE := $(addprefix -I ,$(HEADER_DIR)) 

CXXFLAGS :=${flags} -DMAKEFILEBUILD_DATE="\"`date '+%Y-%m-%d %H:%M:%S'`"\"

SRCS := $(wildcard *.cpp $(SRCDIR)/*.cpp)
OBJS := $(patsubst %.cpp,%.o,$(SRCS))

$(TARGET):$(OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@  $(LIB)  -lpthread -lm -lrt -ldl -lcrypto -lssl -lmagic
	#cp $(TARGET) ../bin/
	#-@if [ ! -d ${DEST_ETC} ]; then mkdir -p ${DEST_ETC}; fi
	#-@if [ ! -d ${DEST_LOG} ]; then mkdir -p ${DEST_LOG}; fi
	#cp -f ../etc/* $(DEST_ETC)

$(OBJS):%.o:%.cpp 
	$(CXX) $(INCLUDE) $(CXXFLAGS) -c $< -o $@    

echo:
	echo $(SRCS)
clean:
	-rm -rf $(TARGET) *.o	

check:
	cppcheck -j 4 --enable=all $(INCLUDE) -f -q . 2>cppcheck.log

