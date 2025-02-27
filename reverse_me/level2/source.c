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



int main(int argc, const char **argv, const char **envp)
{
  char v3; // al
  size_t v5; // [esp+10h] [ebp-48h]
  bool v6; // [esp+17h] [ebp-41h]
  char nptr[4]; // [esp+1Fh] [ebp-39h] BYREF
  char v8; // [esp+23h] [ebp-35h] BYREF
  char v9[23]; // [esp+24h] [ebp-34h]
  char s[9]; // [esp+3Bh] [ebp-1Dh] BYREF
  size_t v11; // [esp+44h] [ebp-14h]
  int i; // [esp+48h] [ebp-10h]
  int v13; // [esp+4Ch] [ebp-Ch]
  int v14; // [esp+50h] [ebp-8h]

  v14 = 0;
  printf("Please enter key: ");
  v13 = scanf("%23s", &v8);
  if ( v13 != 1 )
    no();
  if ( v9[0] != 48 )
    no();
  if ( v8 != 48 )
    no();
  fflush(stdin);
  memset(s, 0, sizeof(s));
  s[0] = 100;
  nptr[3] = 0;
  v11 = 2;
  for ( i = 1; ; ++i )
  {
    v6 = 0;
    if ( strlen(s) < 8 )
    {
      v5 = v11;
      v6 = v5 < strlen(&v8);
    }
    if ( !v6 )
      break;
    nptr[0] = v9[v11 - 1];
    nptr[1] = v9[v11];
    nptr[2] = v9[v11 + 1];
    v3 = atoi(nptr);
    s[i] = v3;
    v11 += 3;
  }
  s[i] = 0;
  if ( strcmp(s, "delabere") )
    no();
  ok();
  return 0;
}