
void FUN_101560424(long param_1,long *param_2,undefined8 param_3)

{
  int iVar1;
  int iVar2;
  long lVar3;
  undefined8 *puVar4;
  long *plVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  long local_68;
  undefined8 local_60;
  undefined *puStack_58;
  undefined8 local_50;
  undefined *puStack_48;
  
  iVar1 = (**(code **)(*param_2 + 0xd0))(param_2);
  if (iVar1 != 0) {
    FUN_10155fff8(param_1 + 0xa8,(long)*(int *)(param_1 + 0xa0) * (long)iVar1);
    lVar3 = (**(code **)(*param_2 + 0x148))(param_2);
    if (lVar3 != 0) {
      FUN_1011a612c(lVar3,*(undefined8 *)(param_1 + 0xa8),*(int *)(param_1 + 0xa0) * iVar1);
      return;
    }
    FUN_1014c0c44(&local_68,param_1 + 0x90);
    if (local_68 == 0) {
      puVar4 = (undefined8 *)0x0;
    }
    else {
      puVar4 = (undefined8 *)
               ___dynamic_cast(local_68,&PTR_vtable_1066749a8,&PTR_vtable_106673618,
                               0xfffffffffffffffe);
    }
    FUN_10146b5c4(auStack_70,param_2);
    FUN_10146b644(auStack_78,param_2);
    iVar1 = 0;
    while (iVar2 = FUN_10146b928(auStack_70,auStack_78), iVar2 == 0) {
      plVar5 = (long *)FUN_10146b8e0(auStack_70);
      uVar6 = (**(code **)(*plVar5 + 0x28))();
      iVar2 = FUN_10120e0f4(uVar6,param_1 + 0x90);
      if (iVar2 != 0) {
        uVar6 = FUN_1015183fc(param_3);
        uVar7 = FUN_10120e26c(param_1 + 0x90);
        (**(code **)(*plVar5 + 0x28))(plVar5);
        local_50 = FUN_10120e26c();
        puStack_58 = PTR_format_custom<TString>_106509e70;
        puStack_48 = PTR_format_custom<TString>_106509e70;
        local_60 = uVar7;
        FUN_10143e88c(auStack_80,L"Class mismatch for array member: expected \'{}\', found \'{}\'",
                      0x3a,0xff,&local_60);
                    /* WARNING: Subroutine does not return */
        FUN_10148229c(uVar6,auStack_80);
      }
      FUN_101487284(local_68,plVar5,param_3);
      (**(code **)*puVar4)
                (puVar4,*(long *)(param_1 + 0xa8) + (long)*(int *)(param_1 + 0xa0) * (long)iVar1);
      iVar1 = iVar1 + 1;
      FUN_10146b8cc(auStack_70);
    }
    FUN_10146b6f0(auStack_78);
    FUN_10146b6f0(auStack_70);
    if (local_68 != 0) {
      iVar1 = *(int *)(local_68 + 8) + -1;
      *(int *)(local_68 + 8) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0();
      }
    }
  }
  return;
}

