##target lib###
CXX=g++
TARGET=cppserver
FUNSHION_LIB := .
LOGINSERVER_LIB := .

LIB := ./service/libservice.a
LIB += ./netsvc/libnetsvc.a
LIB += ./http/libhttp.a
LIB += ../../../../../../../../Library/funshion/lib/kernel/0.1.2/libkernel.a
LIB += ../../../../../../../../Library/funshion/lib/zlib/1.2.4/libz.a




HEADER_DIR := ../../../../../../../../Library/funshion/include/kernel/0.1.2/
#HEADER_DIR += ../../../../../../../../Library/funshion/include/
HEADER_DIR += ./service/include/
HEADER_DIR += ./http/include/
HEADER_DIR += ./netsvc/include/
HEADER_DIR += ./include/


INCLUDE := $(addprefix -I ,$(HEADER_DIR)) 

CXXFLAGS :=${flags} -DMAKEFILEBUILD_DATE="\"`date '+%Y-%m-%d %H:%M:%S'`"\"

SRCS := $(wildcard *.cpp $(SRCDIR)/*.cpp)
OBJS := $(patsubst %.cpp,%.o,$(SRCS))

$(TARGET):$(OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@  $(LIB)  -lpthread -lm -lrt -ldl
	#$(CXX) $(CXXFLAGS) $^ -o $@  $(LIB)  -lpthread -lm -lrt -ldl -lcrypto -lssl -lmagic

$(OBJS):%.o:%.cpp 
	$(CXX) $(INCLUDE) $(CXXFLAGS) -c $< -o $@    

echo:
	echo $(SRCS)
clean:
	-rm -rf $(TARGET) *.o	

check:
	cppcheck -j 4 --enable=all $(INCLUDE) -f -q . 2>cppcheck.log

