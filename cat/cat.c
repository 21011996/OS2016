#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

ssize_t write_(int fd, const void *buf, size_t counter) {
    ssize_t total_written = 0;
    ssize_t bytes_written = 0;
    while (total_written < counter) {
        bytes_written = write(fd, buf + total_written, counter - total_written);
        if (bytes_written <= 0 && errno!=EINTR) {
            return bytes_written;
        } else {
            total_written += bytes_written;
        }
    }
    if (bytes_written < 0 && errno!=EINTR) {
        return -1;
    }
    return total_written;
}

int main(int argc, char * argv[]) {

    char buffer[1024];
	int f;
	if (argc<2) {
		f = 0;
	} else {
		f = open(argv[1],O_RDONLY);
	}
    while (1) {
        ssize_t bytes_read = read(f, buffer, 1024);
     	if (bytes_read == 0 && errno != EINTR) {
            break;
        }
        
		if (write_(STDOUT_FILENO, buffer, bytes_read) == -1){
			return -1;
		}
    }

    return 0;
}