#include "bufio.h"

#include <sys/types.h>

struct buf_t * buf_new(size_t capacity) {
    struct buf_t * buf = (struct buf_t *) malloc(sizeof(struct buf_t));
    if (buf == NULL) {
        return NULL;
    } else {
        buf->data = malloc(capacity);
        if (buf->data == NULL) {
            free(buf);
            return NULL;
        } else {
            buf->capacity = capacity;
            buf->size = 0;
            return buf;
        }
    }
}

void buf_free(struct buf_t * buf) {

    free(buf->data);
    free(buf);
}

size_t buf_capacity(struct buf_t * buf) {

    return buf->capacity;
}

size_t buf_size(struct buf_t * buf) {

    return buf->size;
}

ssize_t buf_fill(fd_t fd, struct buf_t * buf, size_t required) {

    size_t bread;

    buf->size = 0;

    do {
        bread = read(fd, buf->data + buf->size, buf->capacity - buf->size);

        if (bread == -1) {
            return -1;
        }

        buf->size += bread;
    } while (buf->size < required && bread > 0);

    return buf->size;
}

ssize_t buf_flush(fd_t fd, struct buf_t * buf, size_t required) {

    size_t bwritten = 0;
    size_t twritten;
    int error = 0;

    if (required > buf->size) {
        required = buf->size;
    }

    do {
        twritten = write(fd, buf->data + bwritten, buf->size);

        if (twritten == -1) {
            error = 1;
            break;
        }

        bwritten += twritten;
        buf->size -= twritten;
    } while (bwritten < required && twritten > 0);

    memcpy(buf->data, buf->data + bwritten, buf->size);

    if (error) {
        return -1;
    } else {
        return buf->size;
    }
	

}

ssize_t delim_lookup(char* buffer, int len, char delim) {
    for (size_t i = 0; i < len; i++) {
        if (buffer[i] == 0)
            break; 
        if (buffer[i] == delim)
            return i;
    }
    return -1;
}

ssize_t buf_readuntil(fd_t fd, struct buf_t * buf, char delim) {
	ssize_t pos;
    int res;
    while ((pos = delim_lookup(buf->data, buf->size, delim)) < 0) {
        res = read(fd, buf->data + buf->size, buf->capacity - buf->size);
        if (res == 0)
            break;
        if (res > 0) 
            buf->size += res;
        else 
            return -3; 

    }
    if (res == 0)
        return -2;
    return pos;
}