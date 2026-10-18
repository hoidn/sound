
void FUN_101529024(long param_1)

{
  uint uVar1;
  long lVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  long *plVar5;
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  undefined1 auStack_68 [8];
  undefined1 auStack_60 [8];
  undefined1 auStack_58 [8];
  undefined1 auStack_50 [8];
  undefined1 auStack_48 [24];
  
  uVar1 = *(uint *)(param_1 + 0xbc);
  if (uVar1 == 0) {
    uVar4 = ___cxa_allocate_exception(0x30);
    FUN_101447188(auStack_48,&DAT_106e0cc01,
                  "MajorVersion attribute missing from \'Ableton\' root node");
    FUN_1011cb734(auStack_50);
    FUN_1011cb734(auStack_58);
    FUN_1011cb734(auStack_60);
    FUN_1011cb734(auStack_68);
    FUN_1011cb734(auStack_70);
    FUN_101242ce8(uVar4,auStack_48,auStack_50,auStack_58,auStack_60,auStack_68,auStack_70);
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar4,&PTR_vtable_106661270,FUN_10124335c);
  }
  plVar5 = (long *)(param_1 + 0xc0);
  if ((*plVar5 != 0) && ((*(uint *)(*plVar5 + 4) & 0xfffffffe) == 2)) {
    uVar4 = ___cxa_allocate_exception(0x30);
    FUN_101447188(auStack_48,&DAT_106e0cc01,
                  "MinorVersion attribute missing from \'Ableton\' root node");
    FUN_1011cb734(auStack_50);
    FUN_1011cb734(auStack_58);
    FUN_1011cb734(auStack_60);
    FUN_1011cb734(auStack_68);
    FUN_1011cb734(auStack_70);
    FUN_101242ce8(uVar4,auStack_48,auStack_50,auStack_58,auStack_60,auStack_68,auStack_70);
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar4,&PTR_vtable_106661270,FUN_10124335c);
  }
  if ((uVar1 & 0xfffffffe) != 4) {
    if (5 < (int)uVar1) {
      *(undefined1 *)(param_1 + 0x29) = 1;
    }
    uVar4 = ___cxa_allocate_exception(0x30);
    FUN_101427680(auStack_50,"Unsupported MajorVersion (");
    uVar3 = FUN_1011d9c38(auStack_50,*(undefined4 *)(param_1 + 0xbc));
    uVar3 = FUN_1002e40c8(uVar3,")");
    FUN_10144672c(auStack_48,&DAT_106e0cc01,uVar3);
    FUN_1011cb734(auStack_58);
    FUN_1011cb734(auStack_60);
    FUN_1011cb734(auStack_68);
    FUN_1011cb734(auStack_70);
    FUN_1011cb734(auStack_78);
    FUN_101242ce8(uVar4,auStack_48,auStack_58,auStack_60,auStack_68,auStack_70,auStack_78);
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar4,&PTR_vtable_106661270,FUN_10124335c);
  }
  lVar2 = FUN_101514c6c(plVar5);
  *(long *)(param_1 + 0xb0) = lVar2;
  if (lVar2 != 0) {
    return;
  }
  FUN_101529468(param_1 + 0x38,plVar5);
  uVar4 = ___cxa_allocate_exception(0x30);
  FUN_101447188(auStack_48,&DAT_106e0cc01,"Unsupported MinorVersion ($1)");
  FUN_1011cb734(auStack_50);
  FUN_1011cb734(auStack_58);
  FUN_1011cb734(auStack_60);
  FUN_1011cb734(auStack_68);
  FUN_101242ce8(uVar4,auStack_48,plVar5,auStack_50,auStack_58,auStack_60,auStack_68);
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(uVar4,&PTR_vtable_106661270,FUN_10124335c);
}

