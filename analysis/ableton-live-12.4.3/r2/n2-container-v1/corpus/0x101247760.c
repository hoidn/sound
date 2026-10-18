
void FUN_101247760(long param_1,undefined8 param_2,undefined8 param_3)

{
  int iVar1;
  undefined4 uVar2;
  long *plVar3;
  int *local_68;
  undefined8 local_60;
  undefined *puStack_58;
  undefined4 local_50;
  undefined4 local_40;
  
  uVar2 = FUN_1049f8c04(*(undefined8 *)(param_1 + 0x18));
  local_40 = FUN_1049f8c60(*(undefined8 *)(param_1 + 0x18));
  plVar3 = *(long **)(param_1 + 0x38);
  puStack_58 = PTR_format_custom<TString>_106509e70;
  local_60 = param_3;
  local_50 = uVar2;
  FUN_10143e88c(&local_68,L"{} (at line {}, column {})",0x1a,0x11f,&local_60);
  (**(code **)(*plVar3 + 0x68))(plVar3,param_2,&local_68);
  if (local_68 != (int *)0x0) {
    iVar1 = *local_68;
    *local_68 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

