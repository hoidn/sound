
void FUN_101432520(undefined8 param_1,long param_2,int param_3)

{
  undefined8 ***pppuVar1;
  byte bVar2;
  int iVar3;
  long lVar4;
  uint uVar5;
  undefined8 **local_48;
  uint uStack_40;
  byte local_31;
  
  FUN_103f47c98(&local_48,param_2,param_2 + param_3);
  bVar2 = local_31;
  uVar5 = (uint)local_31;
  pppuVar1 = (undefined8 ***)local_48;
  if (-1 < (char)local_31) {
    pppuVar1 = &local_48;
  }
  FUN_101449838(param_1);
  if (-1 < (char)bVar2) {
    uStack_40 = uVar5;
  }
  iVar3 = FUN_1011c4d68(pppuVar1,(long)(int)uStack_40);
  lVar4 = FUN_101449848(param_1,iVar3 * 2 + 2);
  FUN_1011c4e24(lVar4,pppuVar1,(long)iVar3);
  *(undefined2 *)(lVar4 + (long)iVar3 * 2) = 0;
  if (-1 < (char)local_31) {
    return;
  }
  operator_delete(local_48);
  return;
}

