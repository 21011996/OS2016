CC=gcc

all: clean netsh

netsh:
	gcc -Wall netsh.c bufio.c helpers.c -o netsh

clean:
	rm -f netsh
	rm -f *.o $(TASK)
	rm -f *.exe $(TASK)
