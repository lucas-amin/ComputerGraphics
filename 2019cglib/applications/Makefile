CC = g++

INC  = ../include
LIB  = ../lib
OBJ  = ../obj
BIN  = .

PFLAGS = -Wall -W -Wpointer-arith -Wcast-qual \
         -Wcast-align -Wmissing-declarations \
         -Winline -O3 -g

GLLIBS = -lglut -lGLEW -lGL

$(LIB)/libcg.a:
	cd ..; make; cd applications
        
appWindow: $(LIB)/libcg.a appWindow.cpp
	$(CC) $(PFLAGS) appWindow.cpp -o $(BIN)/appWindow -I$(INC) -L$(LIB) -lcg $(GLLIBS)

appTriangles: $(LIB)/libcg.a appTriangles.cpp
	$(CC) $(PFLAGS) shader.cpp appTriangles.cpp -o $(BIN)/appTriangles -I$(INC) -L$(LIB) -lcg $(GLLIBS)

appColoredTriangle: $(LIB)/libcg.a appColoredTriangle.cpp
	$(CC) $(PFLAGS) shader.cpp appColoredTriangle.cpp -o $(BIN)/appColoredTriangle -I$(INC) -L$(LIB) -lcg $(GLLIBS)

appColoredCube: $(LIB)/libcg.a appColoredCube.cpp
	$(CC) $(PFLAGS) shader.cpp appColoredCube.cpp -o $(BIN)/appColoredCube -I$(INC) -L$(LIB)  $(GLLIBS)

appPoints: $(LIB)/libcg.a appPoints.cpp
	$(CC) $(PFLAGS) shader.cpp appPoints.cpp -o $(BIN)/appPoints -I$(INC) -L$(LIB) -lcg $(GLLIBS)

appImage: $(LIB)/libcg.a appImage.cpp
	$(CC) $(PFLAGS) appImage.cpp -o $(BIN)/appImage -I$(INC) -L$(LIB) -lcg 


.PHONY: clean

clean:
	cd ../; make clean; cd applications
	rm -f appWindow appTriangles appColoredTriangle appColoredCube \
	      appImage appPoints
