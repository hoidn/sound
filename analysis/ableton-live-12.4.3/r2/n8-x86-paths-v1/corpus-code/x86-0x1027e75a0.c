// x86 0x1027e75a0 FUN_1027e75a0 state=exported chunk=chunk-01874.jsonl code_sha256=50f898e3877e3627b85dd4cf3232d47683f7153c832352e7ed4829ab578f2899

void FUN_1027e75a0(undefined8 param_1)

{
  long lVar1;
  long lVar2;
  undefined8 uVar3;
  undefined8 local_40;
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined4 local_20;
  undefined1 local_1b;
  undefined1 local_1a;
  undefined1 local_19;
  
  FUN_101ac4450(param_1,&local_20);
  lVar1 = FUN_1014fa860(local_20);
  if ((lVar1 != 0) && (*(long *)(lVar1 + 0x78) != 0)) {
    lVar2 = (**(code **)(**(long **)(lVar1 + 8) + 0x198))();
    if (lVar2 != 0) {
      uVar3 = FUN_101ac4410(param_1,&local_1b);
      uVar3 = FUN_101ac44d0(uVar3,&local_40);
      uVar3 = FUN_101ac44d0(uVar3,&local_38);
      uVar3 = FUN_101ac4410(uVar3,&local_1a);
      uVar3 = FUN_101ac4410(uVar3,&local_19);
      FUN_101ac4470(uVar3,&local_30);
      local_28 = local_30;
      uVar3 = FUN_1027b2e10(*(undefined8 *)(lVar1 + 0x78));
      FUN_1028a54b0(local_40,local_38,uVar3,local_1b,local_1a,local_19,&local_28);
    }
  }
  return;
}

