// 0x100e17004 FUN_100e17004 exported-with-warnings  sig: undefined FUN_100e17004()

void FUN_100e17004(undefined8 *param_1,undefined8 *param_2)

{
  ulong uVar1;
  void *pvVar2;
  void *pvVar3;
  undefined1 *puVar4;
  size_t sVar5;
  
  pvVar2 = (void *)*param_2;
  pvVar3 = (void *)param_2[1];
  sVar5 = (long)pvVar3 - (long)pvVar2;
  param_1[1] = 0;
  param_1[2] = 0;
  *param_1 = 0;
  uVar1 = sVar5 + 1;
  if ((long)uVar1 < 0) {
                    /* WARNING: Subroutine does not return */
    FUN_100397eac(param_1);
  }
  puVar4 = operator_new(uVar1);
  *param_1 = puVar4;
  param_1[2] = puVar4 + uVar1;
  _bzero(puVar4,uVar1);
  param_1[1] = puVar4 + uVar1;
  *puVar4 = 4;
  if (pvVar3 != pvVar2) {
    _memmove(puVar4 + 1,pvVar2,sVar5);
    return;
  }
  return;
}


