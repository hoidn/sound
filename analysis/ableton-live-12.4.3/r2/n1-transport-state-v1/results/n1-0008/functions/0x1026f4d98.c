
void FUN_1026f4d98(long *param_1,undefined8 param_2)

{
  int iVar1;
  long lVar2;
  undefined8 uVar3;
  int *local_40;
  long local_38;
  
  lVar2 = FUN_1012d9850(0x30);
  FUN_101575288(0x3f800000,0x3dcccccd);
  if (lVar2 != 0) {
    *(int *)(lVar2 + 8) = *(int *)(lVar2 + 8) + 1;
  }
  local_38 = lVar2;
  uVar3 = FUN_1012d9850(0x20);
  FUN_10153e8dc(uVar3,0xffffffff);
  FUN_101574f58(lVar2,uVar3);
  uVar3 = FUN_10143b610();
  FUN_101427680(&local_40,"Song Tempo");
  FUN_1026f0bcc(0x41a00000,0x4479c000,0x42f00000,param_1,param_2,lVar2,uVar3,&local_40,0);
  if (local_40 != (int *)0x0) {
    iVar1 = *local_40;
    *local_40 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = (**(code **)(*param_1 + 0x2b0))(param_1);
  FUN_1024dd238(0,uVar3,0,200,0);
  FUN_1026f1850(param_1,0);
  *(undefined4 *)(param_1 + 0x25) = 10;
  FUN_1026f4fac(param_1);
  if (lVar2 != 0) {
    iVar1 = *(int *)(lVar2 + 8) + -1;
    *(int *)(lVar2 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0(lVar2);
    }
  }
  return;
}

