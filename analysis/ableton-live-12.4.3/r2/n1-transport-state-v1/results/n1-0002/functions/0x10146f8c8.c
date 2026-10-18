
/* bool AAbstractNode::GetValue<bool>() const */

bool __thiscall AAbstractNode::GetValue<bool>(AAbstractNode *this)

{
  code *pcVar1;
  int iVar2;
  long *plVar3;
  long lVar4;
  undefined8 uVar5;
  ulong uVar6;
  ulong uVar7;
  undefined1 auStack_58 [16];
  undefined1 auStack_48 [8];
  undefined8 local_40;
  undefined *puStack_38;
  undefined8 local_30;
  undefined *puStack_28;
  
  plVar3 = (long *)(**(code **)(*(long *)this + 0x138))();
  lVar4 = (**(code **)(*plVar3 + 0x10))();
  uVar6 = *(ulong *)(lVar4 + 8);
  uVar7 = *(ulong *)(PTR_typeinfo_1064f86f0 + 8);
  if ((uVar6 != uVar7) &&
     ((-1 < (long)(uVar7 & uVar6) ||
      (iVar2 = _strcmp((char *)(uVar6 & 0x7fffffffffffffff),(char *)(uVar7 & 0x7fffffffffffffff)),
      iVar2 != 0)))) {
    FUN_10120d830(auStack_58,0);
    uVar5 = FUN_10120e26c(auStack_58);
    (**(code **)(*(long *)this + 0x28))(this);
    local_30 = FUN_10120e26c();
    puStack_38 = PTR_format_custom<TString>_106509e70;
    puStack_28 = PTR_format_custom<TString>_106509e70;
    local_40 = uVar5;
    FUN_10143e88c(auStack_48,
                  L"Type mismatch: expected to get a value of type {}, but the document contained a value of type {}"
                  ,0x60,0xff,&local_40);
    FUN_10146d168(this,auStack_48);
                    /* WARNING: Does not return */
    pcVar1 = (code *)SoftwareBreakpoint(1,0x10146f9a4);
    (*pcVar1)();
  }
  return (bool)(char)plVar3[1];
}

