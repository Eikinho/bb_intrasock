// gcc -Wall -pedantic -std=gnu99 -Og -o main main.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <netinet/in.h>
#include <unistd.h>

#define SOCKET_NAME "/tmp/9Lq7BNBnBycd6nxy.socket"

int main(int argc, char *argv[])
{
    int ID = 0;
    char * id_t;
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t readf;

    fp = fopen("gen_prices.txt", 'r');
    if (fp == NULL)
    {
        exit(EXIT_FAILURE);
    }

    int sock = 0, connfd = 0;
    char sendBuff[1025];
        char recvBuff[1025];
        memset(sendBuff, '0', sizeof(sendBuff));

    unlink(SOCKET_NAME);

    sock = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in svaddr;
    memset(&svaddr, '0', sizeof(svaddr));

    svaddr.sin_family = AF_INET;
    svaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    svaddr.sin_port = htons(5000);

    bind(sock, (const struct sockaddr *) &svaddr, sizeof(struct sockaddr_un));

    listen(sock, 20);
    connfd = accept(sock, (struct sockaddr *) NULL, NULL);

    while(1)
    {
        while ((readf = getline(&line, &len, fp)) != -1)
        {
            sprintf(line, "%s,%d", line, ID);
            printf("Enviando valor: %s \n", line);
            snsprintf(sendBuff, sizeof(sendBuff), line);
            write(connfd, sendBuff, strlen(sendBuff));

            int n = 0;
            if ((n = read(connfd, recvBuff, sizeof(recvBuff)-1)) > 0) 
            {
                recvBuff[n] = 0;
                printf("Ordem Recebida: ");
                fputs(recvBuff, stdout);
                ID ++;
            }
        }

        fclose(fp);
        
        if (line)
            free(line);
        
        exit(EXIT_SUCCESS);
    }

    close(connfd);
}