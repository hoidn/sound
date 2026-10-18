
void FUN_10250416c(undefined8 param_1,long param_2)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  float fVar7;
  float fVar8;
  undefined8 uVar9;
  
  uVar9 = FUN_1015651fc(*(undefined8 *)(param_2 + 0x78));
  iVar1 = FUN_1015645a0(*(undefined8 *)(param_2 + 0x90));
  if (iVar1 == 0) {
    uVar2 = 0x80000000;
  }
  else {
    uVar2 = FUN_1015692c0(*(undefined8 *)(param_2 + 0xa8));
  }
  uVar3 = FUN_1015661b8(*(undefined8 *)(param_2 + 0xc0));
  uVar4 = FUN_1015661b8(*(undefined8 *)(param_2 + 0xd8));
  uVar5 = (**(code **)(**(long **)(param_2 + 0xf0) + 0x210))();
  uVar6 = (**(code **)(**(long **)(param_2 + 0x108) + 0x210))();
  fVar7 = (float)(**(code **)(**(long **)(param_2 + 0x138) + 0x208))();
  fVar8 = (float)(**(code **)(**(long **)(param_2 + 0x150) + 0x208))();
  FUN_101af43fc(uVar9,uVar5,uVar6,param_1,uVar2,uVar3,uVar4,(int)fVar7,(int)fVar8);
  return;
}

