
undefined4 *
FUN_1005d235c(undefined4 *param_1,undefined4 *param_2,undefined8 *param_3,undefined8 *param_4,
             undefined4 *param_5,undefined4 *param_6,undefined4 *param_7,undefined8 *param_8,
             undefined8 *param_9)

{
  undefined8 uVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined1 uVar6;
  undefined1 uVar7;
  long lVar8;
  int *piVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  undefined8 uVar12;
  undefined1 local_51;
  undefined7 uStack_50;
  undefined7 local_48;
  undefined1 uStack_41;
  
  lVar8 = *(long *)PTR____stack_chk_guard_100b1c378;
  uVar2 = *param_2;
  uVar11 = *param_3;
  local_48 = (undefined7)param_3[1];
  uVar10 = *(undefined8 *)((long)param_3 + 0xf);
  uStack_41 = (undefined1)uVar10;
  uVar6 = *(undefined1 *)((long)param_3 + 0x17);
  param_3[1] = 0;
  param_3[2] = 0;
  *param_3 = 0;
  uVar12 = *param_4;
  uVar1 = param_4[1];
  uStack_50 = (undefined7)((ulong)*(undefined8 *)((long)param_4 + 0xf) >> 8);
  local_51 = (undefined1)((ulong)uVar1 >> 0x38);
  uVar7 = *(undefined1 *)((long)param_4 + 0x17);
  param_4[1] = 0;
  param_4[2] = 0;
  *param_4 = 0;
  uVar3 = *param_5;
  uVar4 = *param_6;
  uVar5 = *param_7;
  *param_1 = uVar2;
  *(undefined8 *)((long)param_1 + 0x17) = uVar10;
  *(undefined8 *)(param_1 + 2) = uVar11;
  *(ulong *)(param_1 + 4) = CONCAT17(uStack_41,local_48);
  *(undefined1 *)((long)param_1 + 0x1f) = uVar6;
  *(undefined8 *)(param_1 + 8) = uVar12;
  *(undefined8 *)(param_1 + 10) = uVar1;
  *(ulong *)((long)param_1 + 0x2f) = CONCAT71(uStack_50,local_51);
  *(undefined1 *)((long)param_1 + 0x37) = uVar7;
  param_1[0xe] = uVar3;
  param_1[0xf] = uVar4;
  param_1[0x10] = uVar5;
  piVar9 = (int *)*param_8;
  *(int **)(param_1 + 0x12) = piVar9;
  if (piVar9 != (int *)0x0) {
    *piVar9 = *piVar9 + 1;
  }
  if (*(char *)((long)param_9 + 0x17) < '\0') {
    FUN_100135b64(param_1 + 0x14,*param_9,param_9[1]);
  }
  else {
    uVar12 = param_9[1];
    uVar11 = *param_9;
    *(undefined8 *)(param_1 + 0x18) = param_9[2];
    *(undefined8 *)(param_1 + 0x16) = uVar12;
    *(undefined8 *)(param_1 + 0x14) = uVar11;
  }
  if (*(long *)PTR____stack_chk_guard_100b1c378 == lVar8) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

