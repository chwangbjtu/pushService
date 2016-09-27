##target lib###
LIBS=libvisitor.a
DEST=./

##complier##
CXX=g++
CXXFLAGS=${flags}
LDFLAGS=

##include dir and source dir##
#        -I ../../../../../../Library/funshion/src/netsvc/0.1.4/src/include \

INCLUDE_DIRS=   \
        -I ../netsvc/include \
        -I ../soc_mgr/include \
        -I ../include \
        -I ./include \

SRC_DIRS=.

##objects##
OBJS=$(patsubst %.cpp, %.o, $(wildcard $(SRC_DIRS)/*.cpp))
SRC=$(wildcard $(SRC_DIRS)/%.cpp)

vpath %.h $(INCLUDE_DIRS)
vpath %.cpp $(SRC_DIRS)

$(LIBS):$(OBJS)

	#-@if [ ! -d ${DEST} ]; then mkdir -p ${DEST}; fi
	ar r $(DEST)/$@ $^


$(OBJS):%.o:%.cpp 
	$(CXX) $(CXXFLAGS) $(INCLUDE_DIRS) -c $< $(LDFLAGS) -o $@
    
.PHONY : clean

clean:
	rm -rf $(OBJS)


