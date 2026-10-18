
long FUN_102183abc(long param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                  undefined8 param_5)

{
  int iVar1;
  undefined8 *puVar2;
  long lVar3;
  long lVar4;
  
  puVar2 = (undefined8 *)FUN_10128ed98();
  *puVar2 = &PTR_FUN_106774f60;
  puVar2[3] = 0;
  lVar3 = FUN_1012d9850(0x30);
  FUN_1014371e0(0xc051800000000000,lVar3,param_2,param_3,param_4,1,param_5);
  if (lVar3 != 0) {
    *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
  }
  lVar4 = puVar2[3];
  if (lVar4 != 0) {
    iVar1 = *(int *)(lVar4 + 8) + -1;
    *(int *)(lVar4 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(long *)(param_1 + 0x18) = lVar3;
  return param_1;
}

