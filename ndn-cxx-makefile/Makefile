CXXFLAGS  =-std=c++11 $(shell pkg-config --cflags libndn-cxx)
LDFLAGS =-std=c++11 $(shell pkg-config --libs libndn-cxx)
CC = $(CXX)

app: client server

client: client.o

server: server.o

clean:
	rm -Rf client server *.o
