
/* WARNING: Removing unreachable block (ram,0x00010019aa80) */
/* WARNING: Removing unreachable block (ram,0x00010019aa7c) */
/* WARNING: Removing unreachable block (ram,0x00010019aa94) */

void FUN_10019a9d8(undefined8 param_1,undefined8 param_2)

{
  void *local_120;
  undefined8 uStack_118;
  long local_110;
  undefined1 auStack_108 [104];
  undefined **local_a0 [2];
  undefined1 auStack_90 [8];
  undefined8 local_88;
  undefined1 auStack_78 [8];
  undefined8 local_70;
  undefined1 auStack_60 [8];
  undefined8 local_58;
  void *local_48;
  void *local_40;
  
  FUN_10069f714(auStack_108);
  local_120 = (void *)0x0;
  uStack_118 = 0;
  local_110 = 0;
  FUN_100193668(local_a0,param_1,auStack_108,1,&local_120);
  if (local_110 < 0) {
    operator_delete(local_120);
  }
  FUN_100134fdc(auStack_108);
  FUN_100199cf4(local_a0,param_2);
  if (local_48 != (void *)0x0) {
    for (; local_40 != local_48; local_40 = (void *)((long)local_40 + -0x30)) {
    }
    local_40 = local_48;
    operator_delete(local_48);
  }
  local_a0[0] = &PTR_FUN_100b46480;
  FUN_1001369c4(auStack_60,local_58);
  FUN_10013637c(auStack_78,local_70);
  FUN_100135da4(auStack_90,local_88);
  return;
}

