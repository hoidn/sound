
void FUN_101471638(int param_1,int param_2)

{
  int local_24;
  
  local_24 = param_1 * 1000 + param_2 * 100;
  if (*(long *)(DAT_106f4f608 + -2) == 0) {
    DAT_106f4f608[-10] = local_24;
    return;
  }
  if (DAT_106f4f608 < DAT_106f4f610) {
    *DAT_106f4f608 = local_24;
    DAT_106f4f608[4] = 0;
    DAT_106f4f608[5] = 0;
    DAT_106f4f608[2] = 0;
    DAT_106f4f608[3] = 0;
    DAT_106f4f608[8] = 0;
    DAT_106f4f608[9] = 0;
    DAT_106f4f608[6] = 0;
    DAT_106f4f608[7] = 0;
    DAT_106f4f608 = DAT_106f4f608 + 10;
    return;
  }
  DAT_106f4f608 = (int *)FUN_101478984(&DAT_106f4f600,&local_24);
  return;
}

