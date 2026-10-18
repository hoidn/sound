// 0x1014412dc FUN_1014412dc exported  sig: undefined FUN_1014412dc()

void FUN_1014412dc(undefined8 *param_1,ulong param_2)

{
  int iVar1;
  int iVar2;
  uint uVar3;
  uint *puVar4;
  int iVar5;
  int *local_50;
  int *local_48;
  
  iVar2 = (int)param_2;
  iVar5 = iVar2 >> 3;
  iVar1 = iVar2 + 7;
  if (-1 < iVar2) {
    iVar1 = iVar2;
  }
  if ((param_2 & 7) != 0) {
    iVar5 = (iVar1 >> 3) + 1;
  }
  FUN_101449838(&local_48);
  FUN_101449848(&local_48,iVar5 << 2);
  puVar4 = (uint *)FUN_10032ba70(&local_48);
  if (0 < iVar5) {
    do {
      uVar3 = FUN_1011beb30();
      uVar3 = (uVar3 & 0xff00ff00) >> 8 | (uVar3 & 0xff00ff) << 8;
      *puVar4 = uVar3 >> 0x10 | uVar3 << 0x10;
      iVar5 = iVar5 + -1;
      puVar4 = puVar4 + 1;
    } while (iVar5 != 0);
  }
  FUN_101432998(&local_50,&local_48);
  if ((param_2 & 7) == 0) {
    *param_1 = local_50;
  }
  else {
    FUN_10142881c(param_1,&local_50,0,param_2);
    if ((local_50 != (int *)0x0) && (iVar5 = *local_50, *local_50 = iVar5 + -1, iVar5 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  if ((local_48 != (int *)0x0) && (iVar5 = *local_48, *local_48 = iVar5 + -1, iVar5 + -1 == 0)) {
    FUN_101449efc();
  }
  return;
}


