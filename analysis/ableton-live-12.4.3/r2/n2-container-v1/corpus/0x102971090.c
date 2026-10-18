
undefined8 FUN_102971090(undefined8 param_1,undefined8 param_2)

{
  int iVar1;
  undefined8 uVar2;
  long *plVar3;
  long lVar4;
  long *local_60;
  long *local_58 [2];
  char local_41;
  int local_40 [2];
  undefined8 local_38;
  
  local_40[0] = 0;
  local_38 = std::system_category();
  FUN_103e96bc4(local_58,param_2);
  FUN_103e8aeec(local_58,local_40);
  if (local_41 < '\0') {
    operator_delete(local_58[0]);
  }
  if (local_40[0] != 0) {
    uVar2 = std::chrono::system_clock::now();
    FUN_103f3ffec(&local_60,4,uVar2);
    iVar1 = FUN_103f3c8b8(&local_60);
    if (iVar1 != 0) {
      uVar2 = FUN_103f39a78(&local_60,"Preferences: Failed to create preference folder: ");
      std::error_code::message();
      FUN_103f3a958(uVar2,local_58);
      if (local_41 < '\0') {
        operator_delete(local_58[0]);
      }
    }
    thunk_FUN_103f395e4(&local_60);
  }
  local_60 = (long *)0x0;
  FUN_101463eb4(local_58);
  if ((local_60 != (long *)0x0) &&
     (iVar1 = (int)local_60[1] + -1, *(int *)(local_60 + 1) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  local_60 = local_58[0];
  (**(code **)(*local_58[0] + 0x98))(local_58[0],param_2);
  plVar3 = (long *)FUN_1014ed3e4();
  lVar4 = FUN_1012d9850(0x50);
  if (plVar3 != (long *)0x0) {
    *(int *)(plVar3 + 1) = (int)plVar3[1] + 1;
  }
  local_58[0] = plVar3;
  FUN_1014ea3fc(lVar4,local_58);
  if (lVar4 != 0) {
    *(int *)(lVar4 + 8) = *(int *)(lVar4 + 8) + 1;
  }
  if ((local_58[0] != (long *)0x0) &&
     (iVar1 = (int)local_58[0][1] + -1, *(int *)(local_58[0] + 1) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  FUN_1014ea68c(lVar4,1);
  FUN_1014ecba8(local_58,lVar4);
  (**(code **)(*local_60 + 0xa0))(local_60,10,1);
  (**(code **)(*local_60 + 0x68))(local_60,1);
  FUN_101485c50(param_1,local_60,4,0,0,0);
  FUN_1014ecc88(local_58);
  (**(code **)(*local_60 + 0x70))();
  if ((lVar4 != 0) && (iVar1 = *(int *)(lVar4 + 8) + -1, *(int *)(lVar4 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  if (((local_60 != (long *)0x0) && ((**(code **)(*local_60 + 0x18))(), local_60 != (long *)0x0)) &&
     (iVar1 = (int)local_60[1] + -1, *(int *)(local_60 + 1) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  return 1;
}

