CC = g++
FLAGS = -O2 -march=native -Wall -std=c++0x
LIBS = -lboost_thread -lpq
OBJ_FILES = ConfigReader.o TEException.o DBMgr.o

all: TrendExtractor

TrendExtractor: TrendExtractor.cpp $(OBJ_FILES)
	$(CC) $(FLAGS) -o TrendExtractor $(OBJ_FILES) $(LIBS) TrendExtractor.cpp 
	
ConfigReader.o: ConfigReader.cpp ConfigReader.hpp
	$(CC) $(FLAGS) ConfigReader.cpp -c

TEException.o: TEException.cpp TEException.hpp
	$(CC) $(FLAGS) TEException.cpp -c
	
DBMgr.o: DBMgr.cpp DBMgr.hpp
	$(CC) $(FLAGS) DBMgr.cpp -c
	
clean:
	rm -f *.o
	rm -f TrendExtractor