
void FUN_1002e6e00(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  void *local_e0 [2];
  char local_c9;
  void *local_c8 [2];
  char local_b1;
  char local_b0;
  void *local_a8;
  char local_91;
  char local_90;
  void *local_88;
  char local_71;
  char local_70;
  void *local_68;
  char local_51;
  char local_50;
  undefined4 local_40 [2];
  int *local_38;
  
  iVar1 = FUN_1011c709c(param_3,DAT_105800cf0,DAT_105800cf8);
  if (iVar1 == 0) {
    FUN_1018536d4(param_1,param_2,param_3,param_4);
    return;
  }
  puVar2 = (undefined4 *)FUN_100310f04();
  local_40[0] = *puVar2;
  local_38 = *(int **)(puVar2 + 2);
  if (local_38 != (int *)0x0) {
    *local_38 = *local_38 + 1;
  }
  FUN_10296885c();
  FUN_10296c728(local_e0);
  FUN_102ff171c(local_c8,local_e0);
  FUN_102ff1dd8(param_1,param_3,local_40,local_c8);
  if ((local_50 == '\x01') && (local_51 < '\0')) {
    operator_delete(local_68);
  }
  if ((local_70 == '\x01') && (local_71 < '\0')) {
    operator_delete(local_88);
  }
  if ((local_90 == '\x01') && (local_91 < '\0')) {
    operator_delete(local_a8);
  }
  if ((local_b0 == '\x01') && (local_b1 < '\0')) {
    operator_delete(local_c8[0]);
  }
  if (local_c9 < '\0') {
    operator_delete(local_e0[0]);
  }
  if ((local_38 != (int *)0x0) && (iVar1 = *local_38, *local_38 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  return;
}

