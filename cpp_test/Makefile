CPPFLAG = -g -Wall
OBJS =run.o test.o block.o type_class.o 
app : $(OBJS) 
	g++ -o app $(OBJS)
run.o : 
	g++ $(CPPFLAG) -c run.cpp
test.o : test.h
	g++ $(CPPFLAG) -c test.cpp
block.o : block.h
	g++ $(CPPFLAG) -c block.cpp
type_class.o : type_class.h
	g++ $(CPPFLAG) -c type_class.cpp

clean:
	rm -f app $(OBJS)
