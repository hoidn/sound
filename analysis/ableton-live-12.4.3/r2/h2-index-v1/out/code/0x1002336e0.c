// 0x1002336e0 FUN_1002336e0 state=exported-with-warnings body_bytes=408 warnings=3 chunk=chunk-00096.jsonl

void FUN_1002336e0(long *param_1,undefined8 param_2,undefined8 *param_3)

{
  undefined8 *puVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  undefined1 auStack_58 [8];
  undefined1 auStack_50 [8];
  undefined1 auStack_48 [8];
  undefined1 auStack_40 [8];
  undefined1 auStack_38 [8];
  
  uVar3 = (**(code **)(*param_1 + 0x30))();
  iVar2 = (*(code *)*param_3)(param_3[1],param_2,uVar3);
  if (iVar2 == 0) {
    uVar3 = ___cxa_allocate_exception(0x30);
    FUN_1001d4d4c(auStack_38);
    FUN_1001d4d4c(auStack_40);
    FUN_1001d4d4c(auStack_48);
    FUN_1001d4d4c(auStack_50);
    FUN_1001d4d4c(auStack_58);
    FUN_10025df70(uVar3,&DAT_100e2bdb8,auStack_38,auStack_40,auStack_48,auStack_50,auStack_58);
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar3,&PTR_vtable_100d923c8,FUN_10025e5e4);
  }
  (**(code **)(*param_1 + 0x50))(param_1);
  (**(code **)(*param_1 + 0x58))(param_1);
  puVar1 = (undefined8 *)param_1[0xb];
  for (puVar4 = (undefined8 *)param_1[10]; puVar4 != puVar1; puVar4 = puVar4 + 1) {
    (**(code **)(*(long *)*puVar4 + 0x10))();
  }
  if (*(char *)((long)param_1 + 0x29) == '\x01') {
    (**(code **)(*param_1 + 0x68))(param_1);
    puVar1 = (undefined8 *)param_1[0xb];
    for (puVar4 = (undefined8 *)param_1[10]; puVar4 != puVar1; puVar4 = puVar4 + 1) {
      (**(code **)(*(long *)*puVar4 + 8))();
    }
  }
  else {
    (**(code **)(*param_1 + 0x60))(param_1);
    puVar1 = (undefined8 *)param_1[0xb];
    for (puVar4 = (undefined8 *)param_1[10]; puVar4 != puVar1; puVar4 = puVar4 + 1) {
      (*(code *)**(undefined8 **)*puVar4)();
    }
  }
                    /* WARNING: Could not recover jumptable at 0x0001002337c8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(*(long *)param_1[4] + 0xc0))((long *)param_1[4],"ANALYZE");
  return;
}

