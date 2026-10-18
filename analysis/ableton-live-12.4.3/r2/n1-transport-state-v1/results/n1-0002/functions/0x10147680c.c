
void FUN_10147680c(undefined8 param_1,long *param_2,undefined8 param_3,int param_4,
                  undefined8 param_5)

{
  code *pcVar1;
  int iVar2;
  undefined8 uVar3;
  ulong uVar4;
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  undefined8 local_70;
  undefined *puStack_68;
  undefined8 local_60;
  undefined *puStack_58;
  undefined1 *local_50;
  undefined *puStack_48;
  
  (**(code **)(*param_2 + 0x28))(param_2);
  uVar3 = FUN_10120e26c();
  uVar4 = FUN_10142de38(uVar3,param_3);
  if (((uVar4 & 1) == 0) && (iVar2 = (**(code **)(*param_2 + 0x140))(param_2), iVar2 == param_4)) {
    return;
  }
  (**(code **)(*param_2 + 0x28))(param_2);
  uVar3 = FUN_10120e26c();
  (**(code **)(*param_2 + 0x140))(param_2);
  FUN_101430a10(auStack_80);
  puStack_68 = PTR_format_custom<TString>_106509e70;
  puStack_58 = PTR_format_custom<TString>_106509e70;
  puStack_48 = PTR_format_custom<TString>_106509e70;
  local_70 = param_5;
  local_60 = uVar3;
  local_50 = auStack_80;
  FUN_10143e88c(auStack_78,L"Member {} has wrong class ({}) or type ({})",0x2b,0xfff,&local_70);
  FUN_10146d168(param_1,auStack_78);
                    /* WARNING: Does not return */
  pcVar1 = (code *)SoftwareBreakpoint(1,0x1014768fc);
  (*pcVar1)();
}

