// 0x100233210 FUN_100233210 state=exported-with-warnings body_bytes=444 warnings=1 chunk=chunk-00096.jsonl

void FUN_100233210(long *param_1,undefined8 param_2,undefined8 param_3)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  undefined8 *puVar3;
  undefined1 auStack_60 [8];
  undefined1 auStack_58 [8];
  undefined1 auStack_50 [8];
  undefined1 auStack_48 [8];
  undefined1 auStack_40 [8];
  undefined4 local_38;
  undefined4 local_34;
  
  local_34 = 0;
  local_38 = 0;
  uVar2 = (**(code **)(*param_1 + 0x30))();
  uVar2 = FUN_10023344c(param_1,uVar2,2,&local_34,&local_38);
  if (*(char *)((long)param_1 + 0x29) == '\x01') {
    FUN_100232eb4(param_1,uVar2,local_34,param_2,param_3);
  }
  else {
    if ((int)uVar2 != 0) {
      uVar2 = ___cxa_allocate_exception(0x30);
      FUN_1001d4d4c(auStack_40);
      FUN_1001d4d4c(auStack_48);
      FUN_1001d4d4c(auStack_50);
      FUN_1001d4d4c(auStack_58);
      FUN_1001d4d4c(auStack_60);
      FUN_10025df70(uVar2,&DAT_100e2bde8,auStack_40,auStack_48,auStack_50,auStack_58,auStack_60);
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(uVar2,&PTR_vtable_100d923c8,FUN_10025e5e4);
    }
    (**(code **)(*param_1 + 0x50))(param_1);
    (**(code **)(*param_1 + 0x58))(param_1);
    puVar1 = (undefined8 *)param_1[0xb];
    for (puVar3 = (undefined8 *)param_1[10]; puVar3 != puVar1; puVar3 = puVar3 + 1) {
      (**(code **)(*(long *)*puVar3 + 0x10))();
    }
    if (*(char *)((long)param_1 + 0x29) == '\x01') {
      (**(code **)(*param_1 + 0x68))(param_1);
      puVar1 = (undefined8 *)param_1[0xb];
      for (puVar3 = (undefined8 *)param_1[10]; puVar3 != puVar1; puVar3 = puVar3 + 1) {
        (**(code **)(*(long *)*puVar3 + 8))();
      }
    }
    else {
      (**(code **)(*param_1 + 0x60))(param_1);
      puVar1 = (undefined8 *)param_1[0xb];
      for (puVar3 = (undefined8 *)param_1[10]; puVar3 != puVar1; puVar3 = puVar3 + 1) {
        (*(code *)**(undefined8 **)*puVar3)();
      }
    }
  }
  return;
}

