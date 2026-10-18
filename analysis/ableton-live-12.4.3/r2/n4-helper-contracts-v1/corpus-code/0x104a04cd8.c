// 0x104a04cd8 FUN_104a04cd8 exported  sig: undefined FUN_104a04cd8()

void FUN_104a04cd8(undefined8 *param_1,undefined8 *param_2,undefined8 *param_3)

{
  ulong uVar1;
  ulong uVar2;
  ulong uVar3;
  undefined8 *puVar4;
  undefined4 *puVar5;
  ulong uVar6;
  ulong uVar7;
  
  uVar2 = param_2[1];
  if (-1 < (char)*(byte *)((long)param_2 + 0x17)) {
    uVar2 = (ulong)*(byte *)((long)param_2 + 0x17);
  }
  uVar3 = param_3[1];
  if (-1 < (char)*(byte *)((long)param_3 + 0x17)) {
    uVar3 = (ulong)*(byte *)((long)param_3 + 0x17);
  }
  uVar6 = uVar2 & 0xffffffff;
  uVar7 = uVar3 & 0xffffffff;
  param_1[1] = 0;
  param_1[2] = 0;
  uVar1 = uVar6 + uVar7 + 8;
  *param_1 = 0;
  puVar5 = operator_new(uVar1);
  *param_1 = puVar5;
  param_1[2] = (long)puVar5 + uVar1;
  _bzero(puVar5,uVar1);
  param_1[1] = (long)puVar5 + uVar1;
  *puVar5 = (int)uVar2;
  puVar5[1] = (int)uVar3;
  if (uVar6 != 0) {
    puVar4 = (void *)*param_2;
    if (-1 < *(char *)((long)param_2 + 0x17)) {
      puVar4 = param_2;
    }
    _memmove(puVar5 + 2,puVar4,uVar6);
  }
  if (uVar7 != 0) {
    puVar4 = (void *)*param_3;
    if (-1 < *(char *)((long)param_3 + 0x17)) {
      puVar4 = param_3;
    }
    _memmove((void *)((long)(puVar5 + 2) + uVar6),puVar4,uVar7);
    return;
  }
  return;
}


