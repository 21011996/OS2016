#include <unistd.h>

struct execargs_t {
    char** argv;
};

struct execargs_t new_args(int argc, char** argv);
int runpiped(struct execargs_t** programs, size_t n);