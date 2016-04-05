#include <unistd.h>
#include <stdlib.h>
#include <string.h>

typedef int fd_t;

struct execargs_t {
    char** argv;
};

struct execargs_t new_args(int argc, char** argv);
int runpiped(struct execargs_t** programs, size_t n, fd_t socket);