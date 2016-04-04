#include <signal.h>
#include <stdio.h>
#include <errno.h>

int interrupted = 0;

void sig_handler_1(int signum, siginfo_t *siginfo, void *context) {
	int sender_pid = siginfo->si_pid;
	if (interrupted == 0) {
		printf("SIGUSR1 from %d\n", sender_pid);
	}
	interrupted = 1;
	
}

void sig_handler_2(int signum, siginfo_t *siginfo, void *context) {
	int sender_pid = siginfo->si_pid;
	if (interrupted == 0) {
		printf("SIGUSR2 from %d\n", sender_pid);
	}
	interrupted = 2;
}

int main() {
	struct sigaction action1;
	action1.sa_sigaction = sig_handler_1;
	action1.sa_flags = SA_SIGINFO;
	if (sigaction(SIGUSR1, &action1, NULL)) {
		perror("Can't setup action1");
		return 1;
	}
	
	struct sigaction action2;
	action2.sa_sigaction = sig_handler_2;
	action2.sa_flags = SA_SIGINFO;
	if (sigaction(SIGUSR2, &action2, NULL)) {
		perror("Can't setup action2");
		return 2;
	}
	
	sleep(10);
	if (interrupted == 0) {
		printf("No signals were caught.\n");
	}
	return 0;
}