##target lib###
LIBS=libhttp
#DEST= ../../../lib/http/
DEST= .
DEST_INCLUDE= ../../../include/http/
##complier##
CXX=g++ -Wall -Werror
CXXFLAGS=${flags} -static
LDFLAGS=
##include dir and source dir##
INCLUDE_DIRS=-I./include \
	     -I ../../../../../Library/funshion/include/kernel/0.1.2 \
	     -I ../../../../../Library/funshion/include/zlib/1.2.4
SRC_DIRS=.

##objects##
OBJS=$(patsubst %.cpp, %.o, $(wildcard $(SRC_DIRS)/*.cpp))
SRC=$(wildcard $(SRC_DIRS)/%.cpp)

vpath %.h $(INCLUDE_DIRS)
vpath %.cpp $(SRC_DIRS)

$(LIBS):$(OBJS)
	
	@if [ ! -d ${DEST} ]; then mkdir -p ${DEST}; fi
	@if [ ! -z "${flags}" ] && [[ "${flags}" =~ ((^)|([[:blank:]]))-g(([[:blank:]])|($$)) ]];then ar r $(DEST)/$@.a $^; else ar r $(DEST)/$@.a $^; fi
	#@if [ ! -d ${DEST_INCLUDE} ]; then mkdir -p ${DEST_INCLUDE}; fi
	#@rm -f ${DEST_INCLUDE}/*
	#@cp include/* ${DEST_INCLUDE}

$(OBJS):%.o:%.cpp 
	@$(CXX) $(CXXFLAGS) $(INCLUDE_DIRS) -c $< $(LDFLAGS) -o $@ 
	
.PHONY : clean

clean:
	@rm -rf $(OBJS)
	@rm -rf *.a

