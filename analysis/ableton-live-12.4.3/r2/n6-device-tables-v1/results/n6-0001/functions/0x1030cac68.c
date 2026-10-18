
void FUN_1030cac68(long param_1,undefined8 param_2,undefined8 *param_3,undefined8 param_4,
                  undefined8 *param_5,undefined8 param_6,int param_7)

{
  int iVar1;
  undefined8 uVar2;
  long lVar3;
  int *piVar4;
  int *local_80;
  long local_78;
  int *local_70;
  int *local_68;
  
  uVar2 = *(undefined8 *)(param_1 + 0x30);
  local_68 = (int *)*param_3;
  if (local_68 != (int *)0x0) {
    *local_68 = *local_68 + 1;
  }
  FUN_10156fa68(uVar2,&local_68);
  if (local_68 != (int *)0x0) {
    iVar1 = *local_68;
    *local_68 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (((DAT_107026e90 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107026e90), iVar1 != 0)) {
    FUN_1030cb02c(&DAT_107027338,0);
    FUN_1030cb02c(&DAT_107027350,1);
    FUN_1030cb02c(&DAT_107027368,2);
    ___cxa_atexit(thunk_FUN_1030ed344,&DAT_107027338,0x100000000);
    ___cxa_guard_release(&DAT_107026e90);
  }
  uVar2 = *(undefined8 *)(param_1 + 0x48);
  local_70 = (int *)*param_3;
  if (local_70 != (int *)0x0) {
    *local_70 = *local_70 + 1;
  }
  FUN_1026ef060(uVar2,0,&DAT_107027338 + (long)param_7 * 0x18,&local_70,1);
  if (local_70 != (int *)0x0) {
    iVar1 = *local_70;
    *local_70 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  (**(code **)(**(long **)(param_1 + 0x48) + 0x298))(*(long **)(param_1 + 0x48),param_4);
  if (((DAT_107026e98 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107026e98), iVar1 != 0)) {
    FUN_1030cb120(&DAT_107027380,0);
    FUN_1030cb120(&DAT_107027398,1);
    FUN_1030cb120(&DAT_1070273b0,2);
    ___cxa_atexit(thunk_FUN_1030ed344,&DAT_107027380,0x100000000);
    ___cxa_guard_release(&DAT_107026e98);
  }
  uVar2 = *(undefined8 *)(param_1 + 0x48);
  lVar3 = FUN_1012d9850(0x20);
  FUN_10143bd04(lVar3,&DAT_107027380 + (long)param_7 * 0x18);
  if (lVar3 != 0) {
    *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
  }
  local_78 = lVar3;
  FUN_1026efa48(uVar2,lVar3);
  if (lVar3 != 0) {
    iVar1 = *(int *)(lVar3 + 8) + -1;
    *(int *)(lVar3 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0(lVar3);
    }
  }
  uVar2 = *(undefined8 *)(param_1 + 0x60);
  piVar4 = (int *)*param_5;
  if (piVar4 != (int *)0x0) {
    *piVar4 = *piVar4 + 1;
  }
  local_80 = piVar4;
  FUN_1030cb214(0x40200000,param_2,uVar2,&local_80);
  if (piVar4 != (int *)0x0) {
    iVar1 = *piVar4;
    *piVar4 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc(piVar4);
    }
  }
  (**(code **)(**(long **)(param_1 + 0x60) + 0x298))(*(long **)(param_1 + 0x60),param_6);
  return;
}

