// 0x1001ccc6c FUN_1001ccc6c state=exported-with-warnings role=Live browser database path
// source chunk chunk-00082.jsonl; code_sha256=465fee916d360cdbcc3ba615ba7f437eeeca70fab03640f87f1bd441d2147429

/* WARNING: Removing unreachable block (ram,0x0001001cce18) */

void FUN_1001ccc6c(undefined8 *param_1)

{
  int iVar1;
  ulong uVar2;
  undefined8 uVar3;
  void *local_90 [2];
  char local_79;
  void *local_78 [2];
  char local_61;
  void *local_60 [2];
  char local_49;
  undefined1 local_48 [24];
  
  if (((DAT_101decfc0 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_101decfc0), iVar1 != 0)) {
    FUN_100281684(local_60);
    FUN_1001ccf34(local_78,"Ableton/Live Database");
    FUN_1001a63f8(local_48,local_60,local_78);
    uVar3 = FUN_10063e968();
    FUN_10017f204(local_90,"Live");
    FUN_10063e970(&DAT_101decfc8,local_48,uVar3,local_90);
    if (local_79 < '\0') {
      operator_delete(local_90[0]);
    }
    if (local_61 < '\0') {
      operator_delete(local_78[0]);
    }
    if (local_49 < '\0') {
      operator_delete(local_60[0]);
    }
    ___cxa_atexit(FUN_1001ccc34,&DAT_101decfc8,0x100000000);
    ___cxa_guard_release(&DAT_101decfc0);
  }
  uVar2 = FUN_1003220f8(&DAT_101decfc8);
  uVar3 = DAT_101decfc8;
  if ((uVar2 & 1) == 0) {
    uVar3 = std::chrono::system_clock::now();
    FUN_1003324b0(local_48,4,uVar3);
    iVar1 = FUN_10032ece8(local_48);
    if (iVar1 != 0) {
      uVar3 = FUN_10032bea8(local_48,"Database file does not exist:");
      FUN_1001ccff4(uVar3,&DAT_101decfc8);
    }
    thunk_FUN_10032ba14(local_48);
    *param_1 = 0;
    param_1[1] = 0;
    param_1[2] = 0;
    return;
  }
  if (DAT_101decfd8._7_1_ < '\0') {
    FUN_10018127c(param_1,DAT_101decfc8,DAT_101decfd0);
    return;
  }
  param_1[1] = DAT_101decfd0;
  *param_1 = uVar3;
  param_1[2] = CONCAT17(DAT_101decfd8._7_1_,(undefined7)DAT_101decfd8);
  return;
}

