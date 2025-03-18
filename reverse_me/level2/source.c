#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

void no()
{
  puts("Nope.");
  exit(1);
}

int ok()
{
  return puts("Good job.");
}

int main(void)
{

  char scanf_res[80];
  char buffer[9];

  printf("Please enter key: ");
  int scanf_ret = scanf("%23s", scanf_res);
  if (scanf_ret != 1) {
    no();
  }
  if (scanf_res[0] != '0') {
    no();
  }
  if (scanf_res[1] != '0') {
    no();
  }
  fflush(stdin);
  memset(buffer,0,9);
  buffer[0] = 'd';
  int pos = 1;
  int i = 2;
  char atoi_buf[4];
  while(1) {
    int len_1 = strlen(buffer);
    if (len_1 >= 8) {
      break;
    } 
    int scanf_len = strlen(scanf_res);
    if (i >= scanf_len) {
      break;
    }

    atoi_buf[0] = scanf_res[i];
    atoi_buf[1] = scanf_res[i+1];
    atoi_buf[2] = scanf_res[i+2];
    atoi_buf[3] = 0;

    int atoi_ret = atoi(atoi_buf);
    buffer[pos] = atoi_ret;
    i += 3;
    pos++;
  }

  if (!strcmp(buffer, "delabere")) {
    ok();
  }
  else {
    no();
  }
}