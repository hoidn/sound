
void FUN_1030cb214(undefined4 param_1,undefined8 param_2,undefined8 param_3,undefined8 *param_4)

{
  undefined8 uVar1;
  int iVar2;
  long lVar3;
  int *local_68;
  undefined4 local_5c;
  undefined8 local_58;
  
  if (((DAT_1070270b0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_1070270b0), iVar2 != 0)) {
    lVar3 = FUN_1012d9850(0x38);
    FUN_101575868(0xc0a00000,0x40a00000,0x3d4ccccc,0x3ba3d70b);
    DAT_1070270a8 = lVar3;
    if (lVar3 != 0) {
      *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
    }
    ___cxa_atexit(FUN_1019a2da0,&DAT_1070270a8,0x100000000);
    ___cxa_guard_release(&DAT_1070270b0);
  }
  if (((DAT_1070270c0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_1070270c0), iVar2 != 0)) {
    local_5c = 0x3e4ccccd;
    FUN_1030ee7c4(&local_58,&local_5c);
    DAT_1070270b8 = local_58;
    local_58 = 0;
    FUN_1030ee830(&local_58);
    ___cxa_atexit(FUN_101437c58,&DAT_1070270b8,0x100000000);
    ___cxa_guard_release(&DAT_1070270c0);
  }
  uVar1 = DAT_1070270b8;
  lVar3 = DAT_1070270a8;
  local_68 = (int *)*param_4;
  if (local_68 != (int *)0x0) {
    *local_68 = *local_68 + 1;
  }
  FUN_1026f0b58(0xc0a00000,0x40a00000,param_1,param_3,param_2,lVar3,uVar1,&local_68,2);
  if (local_68 != (int *)0x0) {
    iVar2 = *local_68;
    *local_68 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

