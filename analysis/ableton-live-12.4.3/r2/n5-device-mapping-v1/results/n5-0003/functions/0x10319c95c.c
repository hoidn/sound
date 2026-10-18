
void FUN_10319c95c(long *param_1,undefined8 param_2,long *param_3)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  long lVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  char *local_68;
  undefined1 local_60;
  long local_58;
  
  if (param_3 != (long *)0x0) {
    uVar2 = (**(code **)(*param_3 + 0x170))(param_3);
    uVar3 = FUN_1026f0200();
    iVar1 = FUN_10147fd68(uVar2,uVar3);
    if (((iVar1 != 0) && (lVar4 = (**(code **)(*param_3 + 800))(param_3), lVar4 != 0)) &&
       (lVar4 = ___dynamic_cast(lVar4,&PTR_vtable_10658f048,&DAT_106680fb8,0), lVar4 != 0)) {
      FUN_10246b53c(&local_58);
      local_68 = "Converter";
      local_60 = 0;
      FUN_10246b68c(local_58,&local_68);
      uVar2 = (**(code **)(*param_3 + 0x278))(param_3);
      lVar4 = local_58;
      uVar5 = FUN_10157486c();
      uVar6 = FUN_101574874(uVar2);
      uVar7 = FUN_1015748cc(uVar2);
      uVar8 = FUN_1015748e8(uVar2);
      FUN_10246b784(uVar5,uVar6,uVar7,uVar8,lVar4);
      *param_1 = local_58;
      if (local_58 == 0) {
        return;
      }
      if (*(int *)(local_58 + 8) != 0) {
        return;
      }
      FUN_10128eea0();
      return;
    }
  }
  *param_1 = 0;
  return;
}

