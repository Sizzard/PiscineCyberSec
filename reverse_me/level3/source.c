#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

void  ___syscall_malloc() {
  puts("Nope.");
  exit(1);
}

void ____syscall_malloc() {
  puts("Good job.") ;
}

int main(void) {
  char scanf_res[80];
  char buffer[9];
  
  printf("Please enter key: ");
  int scanf_ret = scanf("%23s", scanf_res);
  if (scanf_ret != 1) {
    ___syscall_malloc();
  }
  if (scanf_res[1] != '2') {
    ___syscall_malloc();
  }
  if (scanf_res[0] != '4') {
    ___syscall_malloc();
  }
  fflush(stdin);
  memset(buffer, 0, 9);
  buffer[0] = '*';
  int i = 2;
  int pos = 1;
  while (true) {
    int buf_len = strlen(buffer);
    if (buf_len >= 8) {
      break;
    }
    int scanf_len = strlen(scanf_res);
    if (pos >= scanf_len) {
      break;
    }
    char atoi_ptr[4];
    atoi_ptr[0] = scanf_res[i];
    atoi_ptr[1] = scanf_res[i+1];
    atoi_ptr[2] = scanf_res[i+2];
    atoi_ptr[3] = 0;

    char atoi_ret = atoi(atoi_ptr);
    buffer[pos] = atoi_ret;
    i += 3;
    pos++;
  }
  buffer[pos] = 0;
  if (strcmp(buffer, "********") == 0) {
    ____syscall_malloc();
  }
  else {
    ___syscall_malloc();
  }
  return 0;
}