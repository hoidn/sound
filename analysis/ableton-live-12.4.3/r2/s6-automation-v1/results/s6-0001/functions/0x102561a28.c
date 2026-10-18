
void FUN_102561a28(long param_1,undefined8 param_2)

{
  int iVar1;
  undefined8 *puVar2;
  long lVar3;
  long *plVar4;
  undefined8 uVar5;
  _Unwind_Exception *exception_object;
  long *plVar6;
  long lVar7;
  undefined1 auStack_40 [8];
  undefined1 auStack_38 [8];
  
  plVar6 = *(long **)(param_1 + 0x58);
  puVar2 = (undefined8 *)(**(code **)(*plVar6 + 0x60))(plVar6);
  lVar3 = (**(code **)*puVar2)(puVar2,plVar6);
  lVar7 = *(long *)(lVar3 + 0x18);
  if (lVar7 != lVar3) {
    if (lVar7 != 0) {
      plVar4 = (long *)(**(code **)(*plVar6 + 0x60))(plVar6);
      lVar3 = (**(code **)(*plVar4 + 0x20))(plVar4,plVar6,lVar7);
      if (*(double *)(*(long *)(lVar3 + 8) + 0x50) != -63072000.0) {
        plVar4 = (long *)(**(code **)(*plVar6 + 0x60))(plVar6);
        lVar3 = (**(code **)(*plVar4 + 0x20))(plVar4,plVar6,lVar7);
        if (*(double *)(*(long *)(lVar3 + 8) + 0x50) != 0.0) goto LAB_102561b0c;
      }
    }
    return;
  }
  FUN_101488e64(param_2,"Automation has no events.");
LAB_102561b0c:
  std::chrono::system_clock::now();
  FUN_103f40190(auStack_38);
  iVar1 = FUN_103f3c8b8(auStack_38);
  if (iVar1 != 0) {
    uVar5 = FUN_103f39a78(auStack_38,"DocumentCorrupt: ");
    plVar4 = (long *)(**(code **)(*plVar6 + 0x60))(plVar6);
    lVar3 = (**(code **)(*plVar4 + 0x20))(plVar4,plVar6,lVar7);
    FUN_102561bd8(auStack_40,*(undefined8 *)(lVar3 + 8));
    FUN_101432ff0(uVar5,auStack_40);
    FUN_100234444(auStack_40);
  }
  thunk_FUN_103f395e4(auStack_38);
  exception_object =
       (_Unwind_Exception *)FUN_101488e64(param_2,"First automation event has invalid time.");
  FUN_100234444(auStack_40);
  thunk_FUN_103f395e4(auStack_38);
                    /* WARNING: Subroutine does not return */
  __Unwind_Resume(exception_object);
}

