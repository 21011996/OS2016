#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <netdb.h>
#include "bufio.h"
#include "helpers.h"

int space_or_delim(char c, char delim) {
    return c == delim || c == '\0' || c == ' ' || c == '\t';
}

int count_words(char* buffer, char delim) {
    if (buffer[0] == '\0')
        return 0;
    int count = 0;
    int i = 1;
    while (1) {
        if (!space_or_delim(buffer[i - 1], delim)
            && space_or_delim(buffer[i], delim))
            count++;
        if (buffer[i] == '\0' || buffer[i] == delim)
            return count;
        i++;
    }
}

char* get_word(char* buffer, char* delim, int* new_pos) {
    int i = 0;
    while (buffer[i] == ' ' || buffer[i] == '\t')
        i++;
    int start = i;
    while (buffer[i] != ' ' && buffer[i] != '\t' && buffer[i] != '\0' && buffer[i] != *delim)
        i++;
    int end = i;
    *delim = buffer[i];
    *new_pos = end;
    if (start == end)
        return 0;
    return strndup(buffer + start, end - start);
}

int get_delim(char* buffer, char delim) {
    int i = 0;
    while (buffer[i] == ' ' || buffer[i] == '\t')
        i++;
    if (buffer[i] == delim)
        i++;
    return i;
}

int read_and_exec(int socket) {
    struct buf_t* buf = buf_new(8049);
    int pos = buf_readuntil(socket, buf, '\n');
    if (pos < 0)
        return -1;
    char* buffer = buf->data;
    buffer[pos] = '\0';
    struct execargs_t* arguments[1024];
    int k = 0;
    while (1) {
        char delim;
        int argc = count_words(buffer, '|');
        if (argc == 0)
            break;
        char* argv[argc];
        int shift;
        int i = 0;
        for (i = 0; i < argc; i++) {
            delim = '|';
            argv[i] = get_word(buffer, &delim, &shift);
            buffer += shift;
        }
        arguments[k] = (struct execargs_t*) malloc(sizeof(struct execargs_t));
        *arguments[k] = new_args(argc, argv);
        shift = get_delim(buffer, '|');
        buffer+=shift;
        k++;
    }
    buf->size -= (buffer - (char*) buf->data + 1);
    runpiped(arguments, k, socket);
    buf_free(buf);
    return 0;
}

void print_err(char *string) {
    fprintf(stderr, "%s\n", string);
    exit(EXIT_FAILURE);
}

int main() {
	while (1) {
		write(STDOUT_FILENO, "$\n", 2);
		int code = read_and_exec(STDIN_FILENO);
		if (code < 0) {
			return 0;
		}
	}
    return 0;
}
