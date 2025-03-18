#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

void  ___syscall_malloc() {
  puts("Nope.");
  exit(1);
}

void ____syscall_malloc() {
  puts("Good job.");
}

int main(void) {
  char buffer[9];
  char scanf_res[80];

  printf("Please enter key: ");

  int scanfRet = scanf("%23s", scanf_res);

  if (scanfRet != 1) {
    ___syscall_malloc();
  }
  if  (scanf_res[1] != '2') {
    ___syscall_malloc();
  }
  if (scanf_res[0] != '4') {
    ___syscall_malloc();
  }
  fflush(stdin);
  memset(buffer,0,9);
  buffer[0] = '*';
  int idx = 2;
  int pos = 0;
  int q = 1;
  while( true ) {
    int buff_len = strlen(buffer);
    if (buff_len < 8) {
      int scanf_len = strlen(scanf_res);
      if (scanf_len > buff_len) {
          printf("%d\n", scanf_len > buff_len);
          break;
      }
    }
    char atoi_ptr[4];
    atoi_ptr[0] = scanf_res[idx];
    atoi_ptr[1] = scanf_res[idx + 1];
    atoi_ptr[2] = scanf_res[idx + 2];
    atoi_ptr[3] = 0;
    int atoi_res = atoi(atoi_ptr);
    buffer[pos] = (char)atoi_res;
    printf("buff : %c ;pos : %d\n",buffer[pos], pos);
    pos = pos + 1;
    idx += 3;
  }
  buffer[pos] = '\0';
  printf("%s\n", buffer);
  int cmp_res = strcmp(buffer,"********");
  if (cmp_res == -2) {
    ___syscall_malloc();
  }
  else if (cmp_res == -1) {
    ___syscall_malloc();
  }
  else if (cmp_res == 0) {
    ____syscall_malloc();
  }
  else if (cmp_res == 1) {
    ___syscall_malloc();
  }
  else if (cmp_res == 2) {
    ___syscall_malloc();
  }
  else if (cmp_res == 3) {
    ___syscall_malloc();
  }
  else if (cmp_res == 4) {
    ___syscall_malloc();
  }
  else if (cmp_res == 5) {
    ___syscall_malloc();
  }
  else if (cmp_res == 0x73) {
    ___syscall_malloc();
  }
  else {
    ___syscall_malloc();
  }
  return 0;
}
