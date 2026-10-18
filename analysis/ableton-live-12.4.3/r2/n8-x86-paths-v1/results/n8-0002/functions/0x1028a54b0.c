
void FUN_1028a54b0(ulong param_1,double param_2,long param_3,uint param_4,byte param_5,byte param_6,
                  undefined8 *param_7)

{
  long *plVar1;
  char cVar2;
  byte bVar3;
  undefined1 uVar4;
  
  *(undefined8 *)(param_3 + 0x970) = *param_7;
  cVar2 = FUN_1015544c0(*(undefined8 *)(param_3 + 0x788));
  if (param_4 == 0) {
    if (cVar2 == '\x01' && param_5 == 0) {
      uVar4 = *(undefined1 *)(param_3 + 0x8b1);
      *(undefined1 *)(param_3 + 0x8b1) = 0;
      (**(code **)(**(long **)(param_3 + 0x5d8) + 0x248))(*(long **)(param_3 + 0x5d8),0);
      *(undefined1 *)(param_3 + 0x8b1) = uVar4;
    }
  }
  else if (cVar2 == '\0') {
    if ((*(double *)(param_3 + 0x968) != DAT_105b3ce00) ||
       (NAN(*(double *)(param_3 + 0x968)) || NAN(DAT_105b3ce00))) {
      *(undefined8 *)(param_3 + 0x968) = 0x7fefffffffffffff;
      FUN_1027bd560(*(undefined8 *)(param_3 + 0x48));
    }
    FUN_1027c0d60(*(undefined8 *)(param_3 + 0x48));
  }
  *(ulong *)(param_3 + 0x950) = param_1;
  *(ulong *)(param_3 + 0x958) =
       ~-(ulong)(param_2 < 0.0) & param_1 | (ulong)param_2 & -(ulong)(param_2 < 0.0);
  bVar3 = FUN_1015544c0(*(undefined8 *)(param_3 + 0x788));
  if (((byte)(bVar3 ^ (byte)param_4 | param_5) == 1) && (*(char *)(param_3 + 0x900) == '\0')) {
    if (param_5 != 0) {
      (**(code **)(**(long **)(param_3 + 600) + 0x1e8))();
    }
    FUN_1028a3220(param_3);
    if ((byte)param_4 == 0) {
      uVar4 = FUN_1015544c0(*(undefined8 *)(param_3 + 0x788));
      param_5 = 0;
    }
    else {
      param_5 = ~param_6 & param_5;
      uVar4 = 0;
    }
    FUN_102629540(*(undefined8 *)(param_3 + 0x858),uVar4,param_5);
  }
  plVar1 = *(long **)(param_3 + 0x788);
  if (*(char *)(param_3 + 0x900) == '\x01') {
    FUN_101554650(plVar1,param_4 & 0xff);
    return;
  }
  (**(code **)(*plVar1 + 0x248))(plVar1,param_4 & 0xff);
  uVar4 = *(undefined1 *)(param_3 + 0x8b0);
  *(undefined1 *)(param_3 + 0x8b0) = 0;
  (**(code **)(**(long **)(param_3 + 0x5a8) + 0x248))(*(long **)(param_3 + 0x5a8),param_4 & 0xff);
  *(undefined1 *)(param_3 + 0x8b0) = uVar4;
  return;
}

