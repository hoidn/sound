// 0x1011ac014 FUN_1011ac014 exported-with-warnings  sig: undefined FUN_1011ac014()

/* WARNING: Removing unreachable block (ram,0x0001011ac060) */

ulong FUN_1011ac014(long *param_1,uint param_2,ulong param_3)

{
  long lVar1;
  char *pcVar2;
  uint local_14;
  
  if (((int)param_2 < 1) ||
     (lVar1 = *(long *)(*param_1 + 0x50),
     (int)((ulong)(*(long *)(*param_1 + 0x58) - lVar1) >> 3) * -0x55555555 < (int)param_2)) {
    pcVar2 = "";
  }
  else {
    pcVar2 = (char *)(lVar1 + (ulong)param_2 * 0x18 + -0x18);
  }
  if (*pcVar2 != '\0') {
    FUN_1011bfe6c(pcVar2,"%d");
    param_3 = (ulong)local_14;
  }
  return param_3;
}


