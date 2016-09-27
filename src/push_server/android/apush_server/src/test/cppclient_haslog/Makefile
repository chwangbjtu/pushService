##target lib###
CXX=g++
TARGET=aclient_h
FUNSHION_LIB := .
LOGINSERVER_LIB := .

LIB := ./visitor/libvisitor.a
LIB += ./netsvc/libnetsvc.a
LIB += ./en_crypt/libencrypt.a
LIB += ./soc_mgr/libsoc_mgr.a
LIB += $(LOGINSERVER_LIB)/libjson_linux-gcc-4.1.2_libmt.a




HEADER_DIR := ./netsvc/include/
HEADER_DIR += ./soc_mgr/include/
HEADER_DIR += ./visitor/include/
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

