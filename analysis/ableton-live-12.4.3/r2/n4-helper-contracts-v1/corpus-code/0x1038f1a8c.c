// 0x1038f1a8c FUN_1038f1a8c exported-with-warnings  sig: undefined FUN_1038f1a8c()

void FUN_1038f1a8c(long *param_1,undefined8 *param_2,undefined8 *param_3,undefined8 *param_4,
                  char *param_5,long *param_6,undefined4 *param_7,undefined4 *param_8)

{
  ulong uVar1;
  int iVar2;
  undefined8 *puVar3;
  long lVar4;
  size_t sVar5;
  undefined8 ***pppuVar6;
  int *piVar7;
  undefined8 *puVar8;
  char *pcVar9;
  long local_d8;
  undefined8 **local_d0;
  size_t local_c8;
  undefined8 uStack_c0;
  undefined8 **local_b8;
  size_t local_b0;
  undefined8 uStack_a8;
  undefined8 *local_a0;
  undefined8 *puStack_98;
  undefined8 local_90;
  void *local_80;
  undefined8 uStack_78;
  long local_70;
  
  lVar4 = FUN_1012d9850(0xa8);
  uStack_78 = param_2[1];
  local_80 = (void *)*param_2;
  local_70 = param_2[2];
  *param_2 = 0;
  param_2[1] = 0;
  param_2[2] = 0;
  puStack_98 = (undefined8 *)param_3[1];
  local_a0 = (undefined8 *)*param_3;
  local_90 = param_3[2];
  *param_3 = 0;
  param_3[1] = 0;
  param_3[2] = 0;
  pcVar9 = (char *)*param_4;
  sVar5 = _strlen(pcVar9);
  if (0x7ffffffffffffff7 < sVar5) {
                    /* WARNING: Subroutine does not return */
    FUN_100234518(&local_b8);
  }
  if (sVar5 < 0x17) {
    uStack_a8 = CONCAT17((char)sVar5,(undefined7)uStack_a8);
    pppuVar6 = &local_b8;
    if (sVar5 != 0) goto LAB_1038f1b88;
  }
  else {
    uVar1 = 0x19;
    if ((sVar5 | 7) != 0x17) {
      uVar1 = (sVar5 | 7) + 1;
    }
    pppuVar6 = operator_new(uVar1);
    uStack_a8 = uVar1 | 0x8000000000000000;
    local_b8 = pppuVar6;
    local_b0 = sVar5;
LAB_1038f1b88:
    _memmove(pppuVar6,pcVar9,sVar5);
  }
  *(undefined1 *)((long)pppuVar6 + sVar5) = 0;
  sVar5 = _strlen(param_5);
  if (0x7ffffffffffffff7 < sVar5) {
                    /* WARNING: Subroutine does not return */
    FUN_100234518(&local_d0);
  }
  if (sVar5 < 0x17) {
    uStack_c0 = CONCAT17((char)sVar5,(undefined7)uStack_c0);
    pppuVar6 = &local_d0;
    if (sVar5 == 0) goto LAB_1038f1c00;
  }
  else {
    uVar1 = 0x19;
    if ((sVar5 | 7) != 0x17) {
      uVar1 = (sVar5 | 7) + 1;
    }
    pppuVar6 = operator_new(uVar1);
    uStack_c0 = uVar1 | 0x8000000000000000;
    local_d0 = pppuVar6;
    local_c8 = sVar5;
  }
  _memcpy(pppuVar6,param_5,sVar5);
LAB_1038f1c00:
  *(undefined1 *)((long)pppuVar6 + sVar5) = 0;
  local_d8 = *param_6;
  *param_6 = 0;
  FUN_1038f022c(lVar4,&local_80,&local_a0,&local_b8,&local_d0,&local_d8,*param_7,*param_8);
  *param_1 = lVar4;
  if (lVar4 != 0) {
    *(int *)(lVar4 + 8) = *(int *)(lVar4 + 8) + 1;
  }
  if ((local_d8 != 0) &&
     (iVar2 = *(int *)(local_d8 + 8) + -1, *(int *)(local_d8 + 8) = iVar2, iVar2 == 0)) {
    FUN_10128eea0();
  }
  if ((long)uStack_c0 < 0) {
    operator_delete(local_d0);
  }
  puVar3 = local_a0;
  puVar8 = puStack_98;
  if ((long)uStack_a8 < 0) {
    operator_delete(local_b8);
    puVar3 = local_a0;
    puVar8 = puStack_98;
  }
  local_a0 = puVar3;
  puStack_98 = puVar8;
  if (puVar3 != (undefined8 *)0x0) {
    while (puVar8 != puVar3) {
      puVar8 = puVar8 + -1;
      piVar7 = (int *)*puVar8;
      if ((piVar7 != (int *)0x0) && (iVar2 = *piVar7, *piVar7 = iVar2 + -1, iVar2 + -1 == 0)) {
        FUN_101449efc();
      }
    }
    operator_delete(puVar3);
  }
  if (local_70 < 0) {
    operator_delete(local_80);
  }
  return;
}


