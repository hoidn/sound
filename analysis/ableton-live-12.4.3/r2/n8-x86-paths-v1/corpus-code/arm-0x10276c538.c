// arm 0x10276c538 FUN_10276c538 state=exported chunk=chunk-01922.jsonl code_sha256=15fb6d68db1938032fabd306ca408f868a91bcaa1667863e155d8e6b8d5a6feb

void FUN_10276c538(double param_1,double param_2,long param_3,ulong param_4,uint param_5,
                  uint param_6,undefined8 *param_7)

{
  undefined1 uVar1;
  uint uVar2;
  int iVar3;
  long *plVar4;
  undefined8 uVar5;
  
  *(undefined8 *)(param_3 + 0x970) = *param_7;
  uVar2 = FUN_1015645a0(*(undefined8 *)(param_3 + 0x788));
  if ((int)param_4 == 0) {
    if ((uVar2 != 0) && ((param_5 & 1) == 0)) {
      uVar1 = *(undefined1 *)(param_3 + 0x8b1);
      *(undefined1 *)(param_3 + 0x8b1) = 0;
      (**(code **)(**(long **)(param_3 + 0x5d8) + 0x248))(*(long **)(param_3 + 0x5d8),0);
      *(undefined1 *)(param_3 + 0x8b1) = uVar1;
    }
  }
  else if ((uVar2 & 1) == 0) {
    if (*(double *)(param_3 + 0x968) != 1.79769313486232e+308) {
      *(undefined1 **)(param_3 + 0x968) = &DAT_7fefffffffffffff;
      FUN_1026925fc(*(undefined8 *)(param_3 + 0x48));
    }
    FUN_102695718(*(undefined8 *)(param_3 + 0x48));
  }
  if (0.0 <= param_2) {
    param_2 = param_1;
  }
  *(double *)(param_3 + 0x950) = param_1;
  *(double *)(param_3 + 0x958) = param_2;
  iVar3 = FUN_1015645a0(*(undefined8 *)(param_3 + 0x788));
  if ((iVar3 != (int)param_4 || param_5 != 0) && ((*(byte *)(param_3 + 0x900) & 1) == 0)) {
    if (param_5 != 0) {
      (**(code **)(**(long **)(param_3 + 600) + 0x1e8))();
    }
    FUN_10276a4f0(param_3);
    if ((param_4 & 1) == 0) {
      uVar5 = FUN_1015645a0(*(undefined8 *)(param_3 + 0x788));
      param_5 = 0;
    }
    else {
      uVar5 = 0;
      param_5 = param_5 & (param_6 ^ 0xffffffff);
    }
    FUN_102503070(*(undefined8 *)(param_3 + 0x858),uVar5,param_5);
  }
  plVar4 = *(long **)(param_3 + 0x788);
  if (*(char *)(param_3 + 0x900) == '\x01') {
    FUN_1015646f4(plVar4,param_4);
    return;
  }
  (**(code **)(*plVar4 + 0x248))(plVar4,param_4);
  uVar1 = *(undefined1 *)(param_3 + 0x8b0);
  *(undefined1 *)(param_3 + 0x8b0) = 0;
  (**(code **)(**(long **)(param_3 + 0x5a8) + 0x248))(*(long **)(param_3 + 0x5a8),param_4);
  *(undefined1 *)(param_3 + 0x8b0) = uVar1;
  return;
}

