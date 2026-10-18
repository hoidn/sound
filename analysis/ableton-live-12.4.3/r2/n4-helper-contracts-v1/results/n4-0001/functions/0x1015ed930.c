
/* WARNING: Type propagation algorithm not settling */

void FUN_1015ed930(undefined8 param_1,undefined8 *param_2)

{
  ulong uVar1;
  int iVar2;
  bool bVar3;
  undefined8 *******pppppppuVar4;
  ulong uVar5;
  undefined8 *******pppppppuVar6;
  undefined8 *******local_c8;
  ulong local_c0;
  char local_b1;
  undefined8 *******local_b0;
  ulong uStack_a8;
  ulong local_a0;
  long local_90;
  long *local_88;
  void *local_80;
  undefined8 uStack_78;
  long local_70;
  undefined8 *******local_60;
  ulong uStack_58;
  undefined8 local_50;
  
  if (*(char *)((long)param_2 + 0x17) < '\0') {
    if (param_2[1] == 0) goto LAB_1015ed98c;
    FUN_10023448c(&local_80,*param_2);
    bVar3 = false;
  }
  else if (*(char *)((long)param_2 + 0x17) == '\0') {
LAB_1015ed98c:
    FUN_1011db938(&local_90);
    (**(code **)(*local_88 + 0x48))(&local_80);
    bVar3 = true;
  }
  else {
    bVar3 = false;
    uStack_78 = param_2[1];
    local_80 = (void *)*param_2;
    local_70 = param_2[2];
  }
  local_60 = (undefined8 *******)CONCAT44(local_60._4_4_,1);
  FUN_103f94148(&local_c8,"Live-plugins-{}.db",0x12,1,&local_60);
  uVar5 = (ulong)local_b1;
  if ((long)uVar5 < 0) {
    if (0x7ffffffffffffff7 < local_c0) {
                    /* WARNING: Subroutine does not return */
      FUN_100234518(&local_60);
    }
    uVar5 = local_c0;
    pppppppuVar6 = local_c8;
    if (local_c0 < 0x17) goto LAB_1015ed9e4;
LAB_1015eda10:
    uVar1 = 0x19;
    if ((uVar5 | 7) != 0x17) {
      uVar1 = (uVar5 | 7) + 1;
    }
    pppppppuVar4 = operator_new(uVar1);
    local_50 = uVar1 | 0x8000000000000000;
    local_60 = pppppppuVar4;
    uStack_58 = uVar5;
  }
  else {
    local_c0 = uVar5;
    pppppppuVar6 = &local_c8;
    if (0x16 < uVar5) goto LAB_1015eda10;
LAB_1015ed9e4:
    local_50 = CONCAT17((char)local_c0,(undefined7)local_50);
    pppppppuVar4 = &local_60;
    uVar5 = local_c0;
    if (local_c0 == 0) goto LAB_1015eda48;
  }
  _memmove(pppppppuVar4,pppppppuVar6,uVar5);
  local_c0 = uVar5;
LAB_1015eda48:
  *(undefined1 *)((long)pppppppuVar4 + local_c0) = 0;
  uStack_a8 = uStack_58;
  local_b0 = local_60;
  local_a0 = local_50;
  FUN_100241e54(param_1,&local_80,&local_b0);
  if ((long)local_a0 < 0) {
    operator_delete(local_b0);
  }
  if (local_b1 < '\0') {
    operator_delete(local_c8);
  }
  if (local_70 < 0) {
    operator_delete(local_80);
  }
  if (((bVar3) && (local_90 != 0)) &&
     (iVar2 = *(int *)(local_90 + 8) + -1, *(int *)(local_90 + 8) = iVar2, iVar2 == 0)) {
    FUN_10128eea0();
  }
  return;
}

