
void FUN_101493140(long *param_1)

{
  int iVar1;
  uint uVar2;
  long *plVar3;
  undefined8 uVar4;
  float fVar5;
  
  iVar1 = (**(code **)(*param_1 + 0x70))(param_1,"LaunchQuantisation");
  if (iVar1 == 0) {
    return;
  }
  plVar3 = (long *)(**(code **)(*param_1 + 0x60))(param_1,"LaunchQuantisation");
  uVar4 = (**(code **)(*plVar3 + 0x60))(plVar3,"Value");
  uVar2 = AAbstractNode::GetValue<int>();
  if (uVar2 < 0xb) {
    AAbstractNode::SetValue<int>((int)uVar4);
    return;
  }
  plVar3 = (long *)FUN_101471a98(uVar4,"Enum value out of range");
  plVar3 = (long *)(**(code **)(*plVar3 + 0x60))(plVar3,"Quantisation");
  uVar4 = (**(code **)(*plVar3 + 0x60))(plVar3,"Value");
  uVar2 = AAbstractNode::GetValue<int>();
  if (uVar2 < 7) {
    AAbstractNode::SetValue<int>((int)uVar4);
    return;
  }
  plVar3 = (long *)FUN_101471a98(uVar4,"Enum value out of range");
  iVar1 = (**(code **)(*plVar3 + 0x70))(plVar3,"SampleVolume");
  if (iVar1 != 0) {
    plVar3 = (long *)(**(code **)(*plVar3 + 0x60))(plVar3,"SampleVolume");
    (**(code **)(*plVar3 + 0x48))(plVar3,"Value");
    fVar5 = AAbstractNode::GetValue<float>();
    if (((DAT_106f4f820 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_106f4f820), iVar1 != 0)) {
      DAT_106f4f818 = (long *)FUN_1015269f8(3);
      if (DAT_106f4f818 != (long *)0x0) {
        *(int *)(DAT_106f4f818 + 1) = (int)DAT_106f4f818[1] + 1;
      }
      ___cxa_atexit(FUN_1014ee434,&DAT_106f4f818,0x100000000);
      ___cxa_guard_release(&DAT_106f4f820);
    }
    ___exp10f(fVar5 * 0.05);
    fVar5 = (float)(**(code **)(*DAT_106f4f818 + 0x30))();
    AAbstractNode::SetValue<float>(fVar5);
    return;
  }
  return;
}

