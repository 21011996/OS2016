#include <stdio.h>
#include <unistd.h>

ssize_t write_(int fd, const void *buf, size_t counter) {
    ssize_t total_written = 0;
    ssize_t bytes_written = 0;
    while (total_written < counter) {
        bytes_written = write(fd, buf + total_written, counter - total_written);
        if (bytes_written <= 0) {
            return bytes_written;
        } else {
            total_written += bytes_written;
        }
    }
    if (bytes_written < 0) {
        return -1;
    }
    return total_written;
}

int main() {

    char buffer[1024];
    while (1) {
        ssize_t bytes_read = read(0, buffer, 1024);
        if (bytes_read == 0) {
            break;
        }
        write_(STDOUT_FILENO, buffer, bytes_read);
    }

    return 0;
}