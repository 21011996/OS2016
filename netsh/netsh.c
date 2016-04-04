#include <sys/socket.h>
#include <sys/epoll.h>
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

struct addres_info {
    int flag;
    int family;
    int socktype;
    int protocol;
    size_t addres_length;
    struct sockaddr *address;
    char canonical_name;
    struct addres_info *next;
};

int create_and_bind(char *port) {
    struct addrinfo type;
    struct addrinfo *result;

    memset (&type, 0, sizeof (struct addrinfo));
    type.ai_family = AF_INET;
    type.ai_socktype = SOCK_STREAM;
    type.ai_protocol = IPPROTO_TCP;


    int gai_result = getaddrinfo (NULL, port, &type, &result);
    if (gai_result == -1)
    {
       print_err("Can't get address info");
    }

    //bind
    int socket_fd = 0;
    struct addrinfo *i;
    for (i = result; i != NULL; i = i->ai_next)
    {
        // Try to bind with every addr
        socket_fd = socket (AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (socket_fd == -1)
            continue;

        int bind_status = bind (socket_fd, i->ai_addr, i->ai_addrlen);
        if (bind_status == 0)
        {
            // Has been able to bind
            break;
        }

        close (socket_fd);
    }

    if (i == NULL)
    {
        print_err("Could not bind");
        return -1;
    }

    freeaddrinfo (result);

    return socket_fd;
}

 int make_socket_non_blocking(int socket_fd) {
     int flags = fcntl(socket_fd, F_GETFL, 0);
     if (flags == -1) {
         print_err("Can't get flags");
     }

     flags |= O_NONBLOCK;
     int status = fcntl(socket_fd, F_SETFL, flags);
     if (status == -1) {
         print_err("Can't set non blocking flag");
     }

     return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        print_err("Arguments failure");
    }

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
    //Done pre part

    const int epoll_size = 32;
    struct epoll_event event;
    struct epoll_event *events;

    //prepare socket
    int socket_fd = create_and_bind(argv[1]);
    make_socket_non_blocking(socket_fd);
    if (listen(socket_fd, SOMAXCONN) == -1) {
        print_err("Can't setup listener");
    }

    //Setup epoll
    int epoll_fd = epoll_create1(0);
    if (epoll_fd == -1) {
        print_err("Can't create epoll");
    }
    event.data.fd = socket_fd;
    event.events = EPOLLIN | EPOLLET;
    int ectl_status = epoll_ctl(epoll_fd, EPOLL_CTL_ADD, socket_fd, &event);
    if (ectl_status == -1) {
        print_err("Can't register fd in epoll");
    }

    events = calloc(epoll_size, sizeof(event));

    while (1) // next code is from open source example
    {
        int n, i;

        n = epoll_wait (epoll_fd, events, epoll_size, -1);
        for (i = 0; i < n; i++)
        {
            if ((events[i].events & EPOLLERR) ||
                (events[i].events & EPOLLHUP) ||
                (!(events[i].events & EPOLLIN)))
            {
                //print_err("Epoll error");
                close (events[i].data.fd);
                continue;
            }

            else if (socket_fd == events[i].data.fd)
            {
                /* We have a notification on the listening socket, which
                   means one or more incoming connections. */
                while (1)
                {
                    struct sockaddr in_addr;
                    socklen_t in_len;
                    int infd;
                    char hbuf[NI_MAXHOST], sbuf[NI_MAXSERV];

                    in_len = sizeof in_addr;
                    infd = accept (socket_fd, &in_addr, &in_len);
                    if (infd == -1)
                    {
                        if ((errno == EAGAIN) ||
                            (errno == EWOULDBLOCK))
                        {
                            /* We have processed all incoming
                               connections. */
                            break;
                        }
                        else
                        {
                            perror ("Can't accept");
                            break;
                        }
                    }
                    /* Make the incoming socket non-blocking and add it to the
                       list of fds to monitor. */
                    int unblock_status = make_socket_non_blocking (infd);
                    if (unblock_status == -1)
                        print_err("Can't unblock socket");

                    event.data.fd = infd;
                    event.events = EPOLLIN | EPOLLET;
                    int epc_status = epoll_ctl (epoll_fd, EPOLL_CTL_ADD, infd, &event);
                    if (epc_status == -1)
                    {
                        print_err("Can't add flags");
                    }
                }
                continue;
            }
            else if (events[i].events == EPOLLIN)
            {
                /* We have data on the fd waiting to be read. Read and
                   display it. We must read whatever data is available
                   completely, as we are running in edge-triggered mode
                   and won't get a notification again for the same
                   data. */
                int done = 0;

                /*while (1)
                {
                    ssize_t count;
                    char buf[4096];

                    count = read (events[i].data.fd, buf, sizeof buf);
                    if (count == -1)
                    {
                        // If errno == EAGAIN, that means we have read all
                         //  data. So go back to the main loop.
                        if (errno != EAGAIN)
                        {
                            perror ("read");
                            done = 1;
                        }
                        break;
                    }
                    else if (count == 0)
                    {
                        // End of file. The remote has closed the
                           //connection.
                        done = 1;
                        break;
                    }

                    // Write the buffer to standard output
                    int s = write (events[i].data.fd, buf, count);
                    if (s == -1)
                    {
                        perror ("write");
                        abort ();
                    }
                }*/

                read_and_exec(events[i].data.fd);

                if (1)
                {
                    /* Closing the descriptor will make epoll remove it
                       from the set of descriptors which are monitored. */
                    close (events[i].data.fd);
                }
            } else if (events[i].events == EPOLLOUT) {

            }
        }
    }
    return 0;
}
