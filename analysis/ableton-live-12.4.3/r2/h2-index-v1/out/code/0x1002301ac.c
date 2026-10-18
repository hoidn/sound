// 0x1002301ac FUN_1002301ac state=exported-with-warnings body_bytes=436 warnings=3 chunk=chunk-00095.jsonl

/* WARNING: Removing unreachable block (ram,0x000100230250) */
/* WARNING: Removing unreachable block (ram,0x00010023023c) */
/* WARNING: Removing unreachable block (ram,0x000100230348) */

void FUN_1002301ac(long *param_1)

{
  int iVar1;
  undefined8 uVar2;
  ulong uVar3;
  void *local_78 [2];
  char local_61;
  void *local_60;
  ulong uStack_58;
  byte bStack_49;
  int *local_40;
  void *local_38;
  ulong uStack_30;
  byte bStack_21;
  
  if ((*(byte *)((long)param_1 + 0x9c) & 1) == 0) {
    uVar2 = std::chrono::system_clock::now();
    FUN_10073cdf4(&local_38,3,uVar2);
    iVar1 = FUN_1007396c0(&local_38);
    if (iVar1 != 0) {
      FUN_100736880(&local_38,"Database: database corrupted; must be fixed on next start-up");
    }
    thunk_FUN_1007363ec(&local_38);
    (**(code **)(*param_1 + 0x48))(local_78,param_1);
    FUN_10075f5c0(&local_38,local_78);
    uStack_58 = uStack_30;
    local_60 = local_38;
    bStack_49 = bStack_21;
    FUN_1001d0b68(&local_40,&local_60);
    FUN_100473eb8(&local_40);
    if ((local_40 != (int *)0x0) && (iVar1 = *local_40, *local_40 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_100469e84();
    }
    if ((char)bStack_49 < '\0') {
      operator_delete(local_60);
    }
    if (local_61 < '\0') {
      operator_delete(local_78[0]);
    }
    *(undefined1 *)((long)param_1 + 0x9c) = 1;
    (**(code **)(*param_1 + 0x48))(&local_38,param_1);
    if (-1 < (char)bStack_21) {
      uStack_30 = (ulong)bStack_21;
    }
    if ((uStack_30 != 0) && (uVar3 = FUN_1008241a0(&local_38), (uVar3 & 1) == 0)) {
      *(undefined1 *)((long)param_1 + 0x9c) = 0;
      uVar2 = std::chrono::system_clock::now();
      FUN_10073cdf4(&local_60,4,uVar2);
      iVar1 = FUN_1007396c0(&local_60);
      if (iVar1 != 0) {
        FUN_100736880(&local_60,
                      "Database: Failed to write corrupted database indicator file. Database will not be rebuilt on next start-up."
                     );
      }
      thunk_FUN_1007363ec(&local_60);
    }
  }
  return;
}

