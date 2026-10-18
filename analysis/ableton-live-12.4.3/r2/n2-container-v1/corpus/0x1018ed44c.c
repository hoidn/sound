
void FUN_1018ed44c(long *param_1)

{
  long *plVar1;
  int iVar2;
  ulong uVar3;
  undefined8 uVar4;
  void *local_80 [2];
  char local_69;
  void *local_68 [2];
  char local_51;
  long *local_50;
  long *local_48 [2];
  char local_31;
  int local_30 [2];
  undefined8 local_28;
  
  (**(code **)(*param_1 + 0x1e8))();
  FUN_101747a10();
  uVar3 = FUN_101747db8();
  if (((uVar3 & 1) == 0) && (iVar2 = FUN_1011b59ec(), iVar2 != 1)) {
    local_30[0] = 0;
    local_28 = std::system_category();
    FUN_1011db880(local_48);
    FUN_103e8aeec(local_48,local_30);
    if (local_31 < '\0') {
      operator_delete(local_48[0]);
    }
    if (local_30[0] != 0) {
      uVar4 = std::chrono::system_clock::now();
      FUN_103f3ffec(local_68,4,uVar4);
      iVar2 = FUN_103f3c8b8(local_68);
      if (iVar2 != 0) {
        uVar4 = FUN_103f39a78(local_68,"Preferences: Failed to create preference folder: ");
        std::error_code::message();
        FUN_103f3a958(uVar4,local_48);
        if (local_31 < '\0') {
          operator_delete(local_48[0]);
        }
      }
      thunk_FUN_103f395e4(local_68);
    }
    local_50 = (long *)0x0;
    FUN_101463eb4(local_48);
    if ((local_50 != (long *)0x0) &&
       (iVar2 = *(int *)((long)local_50 + 8) + -1, *(int *)((long)local_50 + 8) = iVar2, iVar2 == 0)
       ) {
      FUN_10128eea0();
    }
    plVar1 = local_48[0];
    local_50 = local_48[0];
    FUN_1011db880(local_68);
    FUN_1018ed310(local_80);
    FUN_100241e54(local_48,local_68,local_80);
    (**(code **)(*plVar1 + 0x98))(plVar1,local_48);
    if (local_31 < '\0') {
      operator_delete(local_48[0]);
    }
    if (local_69 < '\0') {
      operator_delete(local_80[0]);
    }
    if (local_51 < '\0') {
      operator_delete(local_68[0]);
    }
    FUN_1018ed778(param_1,local_50);
    (**(code **)(*local_50 + 0x70))();
    if (((local_50 != (long *)0x0) && ((**(code **)(*local_50 + 0x18))(), local_50 != (long *)0x0))
       && (iVar2 = (int)local_50[1] + -1, *(int *)(local_50 + 1) = iVar2, iVar2 == 0)) {
      FUN_10128eea0();
    }
  }
  return;
}

