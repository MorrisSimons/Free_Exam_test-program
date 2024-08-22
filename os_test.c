#include <stdio.h>
#include <unistd.h>
int main()
{
int pid = 0;
pid = fork();
printf("Hello\n");
pid = fork();
printf("Hello\n");
return 0;
}