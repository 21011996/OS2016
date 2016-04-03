#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>
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

int read_and_exec(int fdin, int fdout) {
    struct buf_t* buf = buf_new(8049);
    int pos = buf_readuntil(fdin, buf, '\n');
    if (pos == -2)
        return 0;
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
        for (int i = 0; i < argc; i++) {
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
    runpiped(arguments, k);
    buf_free(buf);
    return 0;
}

void print_err(char *string) {
    fprintf(stderr, "%s\n", string);
    exit(EXIT_FAILURE);
}

int main(int argc, char *argv[]) {
    /*if (argc != 2) {
        print_err("Arguments failure");
    }*/

    pid_t main_pid = fork();
    switch(main_pid) {
        case 0:
            break;
        case -1:
            print_err("Can't fork main");
        default:
            exit(0);
    }

    if(setsid()<0) {
        print_err("Can't start new session");
    }
    pid_t nsession_pid = fork();
    switch(nsession_pid) {
        case 0:
            break;
        case -1:
            print_err("Can't fork from deamon");
        default:
            return 0;
    }

    pid_t deamon_pid = getpid();
    char netsh_pid_file[420];
    mkdir("tmp", S_IRWXU | S_IRWXG | S_IRWXO);
    snprintf(netsh_pid_file, sizeof(netsh_pid_file), "tmp/netsh.pid");
    FILE* f = fopen(netsh_pid_file, "w");
    if (f < 0) {
        print_err("Can't create file");
    }
    fprintf(f,"%d", deamon_pid);
    fclose(f);

    int code = read_and_exec(STDIN_FILENO, STDOUT_FILENO);
    return 0;
}