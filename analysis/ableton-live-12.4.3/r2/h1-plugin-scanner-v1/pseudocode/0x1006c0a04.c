
__darwin_time_t FUN_1006c0a04(char *param_1,undefined8 *param_2)

{
  char *pcVar1;
  int iVar2;
  stat sStack_b0;
  
  if (param_2 != (undefined8 *)0x0) {
    *param_2 = 0;
    param_2[1] = 0;
    param_2[2] = 0;
  }
  pcVar1 = *(char **)param_1;
  if (-1 < param_1[0x17]) {
    pcVar1 = param_1;
  }
  iVar2 = _stat(pcVar1,&sStack_b0);
  if (-1 < iVar2) {
    return sStack_b0.st_mtimespec.tv_sec;
  }
  FUN_10096dc9c(param_1,param_2);
  return 0x8000000000000000;
}

