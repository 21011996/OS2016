#include "helpers.h"
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>
#include <fcntl.h>

int spawn(const char * file, char * const argv []) {
    pid_t child_pid;
    if (!(child_pid = fork()))
        if (execvp(file, argv) < 0)
            return -1;
    int ret_code;
    if (waitpid(child_pid, &ret_code, 0) < 0)
        return -2;
    if (WIFEXITED(ret_code)) 
        return WEXITSTATUS(ret_code);
    else 
        return -3;
}

struct execargs_t new_args(int argc, char** argv)
{
    struct execargs_t result;
    result.argv = (char**) malloc((argc + 1) * sizeof(char*));
    int i;
    for (i = 0; i < argc; i++) 
        result.argv[i] = strdup(argv[i]); 
    result.argv[argc] = NULL;
    return result;
}

int childcount;
int* childarray;

void sig_handler(int signo) {
    int i = 0;
    for (i = 0; i < childcount; i++)
        kill(childarray[i], SIGKILL);
    childcount = 0;
}

int runpiped(struct execargs_t** programs, size_t n, fd_t socket) {
	if (n == 0)
        return 0;
    int pipefd[n - 1][2];
	int childpid[n];
    int i = 0;
	for (i = 0; i < n - 1; i++)
        if (pipe2(pipefd[i], O_CLOEXEC) < 0)
            return -1;
    pipefd[0][0] = socket;
    pipefd[n-1][1] = socket;
    i = 0;
	for (i = 0; i < n; i++) {
		if (!(childpid[i] = fork())) {
            if (i != 0)
				dup2(pipefd[i - 1][0], STDIN_FILENO);
			if (i != n - 1)
				dup2(pipefd[i][1], STDOUT_FILENO);
			_exit(execvp(programs[i]->argv[0], programs[i]->argv));	
		}
        if (childpid[i] == -1)
            return -1;
	}
    i = 0;
	for (i = 0; i < n - 1; i++) {
		close(pipefd[i][0]);
		close(pipefd[i][1]);
	}
    
    childcount = n;
    childarray = (int*) childpid;
	
    struct sigaction act; //totally not copy pasted from net(
    memset(&act, '\0', sizeof(act));
    act.sa_handler = &sig_handler;
   
    if (sigaction(SIGINT, &act, NULL) < 0) 
        return -1;

	int status;
    i = 0;
	for (i = 0; i < n; i++)
        waitpid(childpid[i], &status, 0);
    childcount = 0;
    return 0;
}