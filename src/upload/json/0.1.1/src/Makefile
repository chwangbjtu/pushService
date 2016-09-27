SRC=../jsoncpp-src-0.5.0
CXX=g++
DEST_INCLUDE=../../../../include/json/
#DEST_LIB=../../../../lib/json/
DEST_LIB=./

INCLUDE= -I $(SRC)/include \
	 -I ./include 

LIB_LOCATION=$(SRC)/libs/

JSON_LIBS=$(shell find $(LIB_LOCATION) -name "*.a")
OBJS=$(patsubst %.cpp,%.o,$(wildcard ./*.cpp))

LIBS=libjson.a

$(LIBS):$(OBJS)
	@ar x $(JSON_LIBS)
	@ar r $@ *.o
	-@if [ ! -d ${DEST_INCLUDE} ]; then mkdir -p ${DEST_INCLUDE}; fi
	-@if [ ! -d ${DEST_LIB} ]; then mkdir -p ${DEST_LIB}; fi
	#cp $@ ${DEST_LIB}
	#cp -rf include/* ${DEST_INCLUDE}


$(OBJS):%.o:%.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $< $(LDFLAGS) 

clean:
	-@rm $(LIBS) *.o

