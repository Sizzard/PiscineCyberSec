#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

void  ___syscall_malloc() {
  puts("Nope.")
  exit(1)
}

void ____syscall_malloc() {
  puts("Good job.") 
}

int main(void) {
  char buffer[9];

  printf("Please enter key: ")

  int scanfRet = scanf("%23s", buffer)

  if scanfRet != 1 {
    ___syscall_malloc()
  }
  if  buffer[1] != '2' {
    ___syscall_malloc()
  }
  if buffer[0] != '4' {
    ___syscall_malloc()
  }
  fflush(stdin)

  int idx = 2;
  int pos = 0;
  while true {
    if (strlen("*")) {

    }
    if (strlen(buffer)) {

    }
    char atoi_buf[4];
    atoi_buf[0] = buffer[idx];
    atoi_buf[1] = buffer[idx++];
    atoi_buf[2] = buffer[idx++];
    atoi_buf[3] = 0;  
    atoi_res = atoi(atoi_buf);
    buffer[pos] = atoi_res
    pos++;
  }
  if (strcmp("********"), buffer) {
    ____syscall_malloc()
  }
  return 0;
}