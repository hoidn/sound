
void FUN_101492afc(long *param_1)

{
  code *pcVar1;
  int iVar2;
  int iVar3;
  long *plVar4;
  long *plVar5;
  undefined8 uVar6;
  undefined8 *puVar7;
  float fVar8;
  double dVar9;
  int *local_40;
  undefined1 auStack_38 [8];
  
  plVar4 = (long *)(**(code **)(*param_1 + 0x48))(param_1,"ArrangerAutomation/Events");
  FUN_10146b5c4(auStack_38,plVar4);
  plVar5 = (long *)FUN_10146b8e0(auStack_38);
  FUN_10146b6f0(auStack_38);
  (**(code **)(*plVar5 + 0x60))(plVar5,"Time");
  dVar9 = AAbstractNode::GetValue<double>();
  if (dVar9 == 0.0) {
    iVar2 = (**(code **)(*plVar4 + 0xd0))(plVar4);
    if (iVar2 == 1) {
      (**(code **)(*plVar5 + 0x60))(plVar5,"Time");
      AAbstractNode::SetValue<double>(-63072000.0);
      return;
    }
    (**(code **)(*plVar5 + 0x28))(plVar5);
    uVar6 = FUN_10120e26c();
    plVar4 = (long *)(**(code **)(*plVar4 + 0x118))(plVar4,uVar6,1,0);
    (**(code **)(*plVar4 + 0x80))(plVar4,"Double",0,"Time");
    AAbstractNode::SetValue<double>(-63072000.0);
    plVar5 = (long *)(**(code **)(*plVar5 + 0x60))(plVar5,"Value");
    (**(code **)(*plVar5 + 0x28))();
    uVar6 = FUN_10120e26c();
    iVar2 = (**(code **)(*plVar4 + 0x88))(plVar4,uVar6,0,"Value");
    (**(code **)(*plVar5 + 0x28))(plVar5);
    iVar3 = FUN_10120e264();
    if (iVar3 == 0x12) {
      fVar8 = AAbstractNode::GetValue<float>();
      AAbstractNode::SetValue<float>(fVar8);
      return;
    }
    (**(code **)(*plVar5 + 0x28))(plVar5);
    iVar3 = FUN_10120e264();
    if (iVar3 == 0x10) {
      AAbstractNode::GetValue<bool>();
      AAbstractNode::SetValue<bool>(SUB41(iVar2,0));
      return;
    }
    (**(code **)(*plVar5 + 0x28))(plVar5);
    iVar3 = FUN_10120e264();
    if (iVar3 == 0x11) {
      AAbstractNode::GetValue<int>();
      AAbstractNode::SetValue<int>(iVar2);
      return;
    }
  }
  else {
    FUN_101471a98(plVar5,"Event of unautomated parameter is not at 0.0");
  }
  FUN_101427680(auStack_38,"Unknown event type found: ");
  (**(code **)(*plVar5 + 0x28))(plVar5);
  uVar6 = FUN_10120e26c();
  puVar7 = (undefined8 *)FUN_10142da5c(auStack_38,uVar6);
  local_40 = (int *)*puVar7;
  if (local_40 != (int *)0x0) {
    *local_40 = *local_40 + 1;
  }
  FUN_10146d168(plVar5,&local_40);
                    /* WARNING: Does not return */
  pcVar1 = (code *)SoftwareBreakpoint(1,0x101492da0);
  (*pcVar1)();
}

