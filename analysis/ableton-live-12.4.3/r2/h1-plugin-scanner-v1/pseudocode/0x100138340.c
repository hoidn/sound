
void FUN_100138340(long *param_1,long param_2,undefined8 param_3)

{
  int iVar1;
  undefined8 uVar2;
  long *plVar3;
  undefined1 auStack_60 [8];
  int local_58 [2];
  undefined8 local_50;
  undefined4 local_48;
  uint uStack_44;
  char local_31;
  
  local_58[0] = 0;
  local_50 = std::system_category();
  uVar2 = FUN_1001a2514();
  FUN_100145d24(param_1,param_3,param_2 + 8,uVar2,local_58);
  plVar3 = (long *)*param_1;
  if (plVar3 != (long *)0x0) {
    if (local_58[0] == 0) {
      return;
    }
    *param_1 = 0;
    (**(code **)(*plVar3 + 8))();
  }
  local_31 = '\x04';
  local_48 = 0x72726563;
  uStack_44 = uStack_44 & 0xffffff00;
  uVar2 = std::chrono::system_clock::now();
  FUN_1006a284c(auStack_60,4,&local_48,uVar2);
  if (local_31 < '\0') {
    operator_delete((void *)CONCAT44(uStack_44,local_48));
  }
  iVar1 = FUN_10069f1d8(auStack_60);
  if (iVar1 != 0) {
    uVar2 = FUN_10069c398(auStack_60,"VST2: Failed to load plugin: ");
    std::error_code::message();
    FUN_10069d278(uVar2,&local_48);
    if (local_31 < '\0') {
      operator_delete((void *)CONCAT44(uStack_44,local_48));
    }
  }
  thunk_FUN_10069bf04(auStack_60);
  *param_1 = 0;
  return;
}

