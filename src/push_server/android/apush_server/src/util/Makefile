##target lib###
LIBS=libutil.a
DEST=../../lib

#		-I ../../../../../Library/funshion/include/thread/0.1.0 \
##complier##
CXX=g++
CXXFLAGS=${flags}
LDFLAGS=

##include dir and source dir##
INCLUDE_DIRS=	\
		-I ../../../../../../../Library/funshion/include/kernel/0.1.2 \
		-I ../../../../../../../Library/funshion/include/zlib/1.2.4 \
		-I ../http/include \
		-I ./include \
		-I ../include \

SRC_DIRS=.

##objects##
OBJS=$(patsubst %.cpp, %.o, $(wildcard $(SRC_DIRS)/*.cpp))
SRC=$(wildcard $(SRC_DIRS)/%.cpp)

vpath %.h $(INCLUDE_DIRS)
vpath %.cpp $(SRC_DIRS)

$(LIBS):$(OBJS)
	
	-@if [ ! -d ${DEST} ]; then mkdir -p ${DEST}; fi
	ar r $(DEST)/$@ $^


$(OBJS):%.o:%.cpp 
	$(CXX) $(CXXFLAGS) $(INCLUDE_DIRS) -c $< $(LDFLAGS) -o $@
	
.PHONY : clean

clean:
	rm -rf $(OBJS)
