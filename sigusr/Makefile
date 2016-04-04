TARGET=sigusr

all: $(TARGET)

clean: 
	rm -f $(TARGET) $(TARGET).o

$(TARGET).o: $(TARGET).c
	gcc $< -o $@ -c

$(TARGET): $(TARGET).o
	gcc $< -o $@ 