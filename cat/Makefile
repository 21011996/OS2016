all: cat

clean:
	rm -f cat cat.o

cat.o: cat.c
	gcc $< -o $@ -c

cat: cat.o
	gcc $< -o $@