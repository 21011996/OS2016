#include <stdio.h>
#include <unistd.h>

ssize_t read_(int fd, void *buf, size_t counter) {
    ssize_t total_read = 0;
    ssize_t byte_read = 0;
    while (total_read < counter) {
        byte_read = read(fd, buf + total_read, counter - total_read);
        if (byte_read <= 0) {
            break;
        } else {
            total_read += byte_read;
        }
    }
    if (byte_read < 0) {
        return -1;
    }
    return total_read;
}

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

int main(int argc, char * argv[]) {

    char buffer[1024];
    while (1) {
        ssize_t bytes_read = read_(STDIN_FILENO, buffer, 1024);
        if (bytes_read < 0) {
            break;
        }
        write_(STDOUT_FILENO, buffer, bytes_read);
        if (bytes_read == 0) {
            break;
        }
    }

    return 0;
}