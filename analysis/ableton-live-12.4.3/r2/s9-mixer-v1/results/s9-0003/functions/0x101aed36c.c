
void FUN_101aed36c(void)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  int iVar3;
  int *piVar4;
  ulong uVar5;
  undefined4 uVar6;
  double dVar7;
  
  DAT_106f7ec08 = operator_new__(0x38);
  puVar1 = operator_new(0x28);
  puVar1[1] = 0;
  *(undefined4 *)(puVar1 + 2) = 0;
  *(undefined1 *)((long)puVar1 + 0x14) = 0;
  *puVar1 = &PTR_FUN_106755fa8;
  piVar4 = (int *)(puVar1 + 3);
  piVar4[0] = 0;
  piVar4[1] = 0;
  puVar1[4] = 0;
  *piVar4 = 0x80;
  uVar2 = thunk_FUN_101aa0414(0x20c);
  puVar1[1] = uVar2;
  *(undefined4 *)(puVar1 + 2) = 0x83;
  *(undefined1 *)((long)puVar1 + 0x14) = 1;
  iVar3 = *(int *)(puVar1 + 3);
  if (-3 < iVar3) {
    uVar5 = 0;
    do {
      uVar6 = OCrossFadeHelper::CrossfadeToLevelNormalDip
                        (((float)(uVar5 & 0xffffffff) / 128.0) * 2.0 + -1.0);
      *(undefined4 *)(puVar1[1] + uVar5 * 4) = uVar6;
      uVar5 = uVar5 + 1;
    } while ((iVar3 + 2U & ((int)(iVar3 + 2U) >> 0x1f ^ 0xffffffffU)) + 1 != uVar5);
    iVar3 = *piVar4;
  }
  dVar7 = (double)NEON_fmov(0x3f800000,4);
  dVar7 = -dVar7;
  *(double *)((long)puVar1 + 0x1c) = dVar7;
  *(float *)((long)puVar1 + 0x24) = (float)iVar3 / 2.0;
  *DAT_106f7ec08 = puVar1;
  puVar1 = operator_new(0x28);
  puVar1[1] = 0;
  *(undefined4 *)(puVar1 + 2) = 0;
  *(undefined1 *)((long)puVar1 + 0x14) = 0;
  *puVar1 = &PTR_FUN_106755fa8;
  piVar4 = (int *)(puVar1 + 3);
  piVar4[0] = 0;
  piVar4[1] = 0;
  puVar1[4] = 0;
  *piVar4 = 0x80;
  uVar2 = thunk_FUN_101aa0414(0x20c);
  puVar1[1] = uVar2;
  *(undefined4 *)(puVar1 + 2) = 0x83;
  *(undefined1 *)((long)puVar1 + 0x14) = 1;
  iVar3 = *(int *)(puVar1 + 3);
  if (-3 < iVar3) {
    uVar5 = 0;
    do {
      uVar6 = OCrossFadeHelper::CrossfadeToLevelSlightDip
                        (((float)(uVar5 & 0xffffffff) / 128.0) * 2.0 + -1.0);
      *(undefined4 *)(puVar1[1] + uVar5 * 4) = uVar6;
      uVar5 = uVar5 + 1;
    } while ((iVar3 + 2U & ((int)(iVar3 + 2U) >> 0x1f ^ 0xffffffffU)) + 1 != uVar5);
    iVar3 = *piVar4;
  }
  *(double *)((long)puVar1 + 0x1c) = dVar7;
  *(float *)((long)puVar1 + 0x24) = (float)iVar3 / 2.0;
  DAT_106f7ec08[1] = puVar1;
  puVar1 = operator_new(0x28);
  puVar1[1] = 0;
  *(undefined4 *)(puVar1 + 2) = 0;
  *(undefined1 *)((long)puVar1 + 0x14) = 0;
  *puVar1 = &PTR_FUN_106755fa8;
  piVar4 = (int *)(puVar1 + 3);
  piVar4[0] = 0;
  piVar4[1] = 0;
  puVar1[4] = 0;
  *piVar4 = 0x80;
  uVar2 = thunk_FUN_101aa0414(0x20c);
  puVar1[1] = uVar2;
  *(undefined4 *)(puVar1 + 2) = 0x83;
  *(undefined1 *)((long)puVar1 + 0x14) = 1;
  iVar3 = *(int *)(puVar1 + 3);
  if (-3 < iVar3) {
    uVar5 = 0;
    do {
      uVar6 = OCrossFadeHelper::CrossfadeToLevelConstantPower
                        (((float)(uVar5 & 0xffffffff) / 128.0) * 2.0 + -1.0);
      *(undefined4 *)(puVar1[1] + uVar5 * 4) = uVar6;
      uVar5 = uVar5 + 1;
    } while ((iVar3 + 2U & ((int)(iVar3 + 2U) >> 0x1f ^ 0xffffffffU)) + 1 != uVar5);
    iVar3 = *piVar4;
  }
  *(double *)((long)puVar1 + 0x1c) = dVar7;
  *(float *)((long)puVar1 + 0x24) = (float)iVar3 / 2.0;
  DAT_106f7ec08[2] = puVar1;
  puVar1 = operator_new(0x28);
  puVar1[1] = 0;
  *(undefined4 *)(puVar1 + 2) = 0;
  *(undefined1 *)((long)puVar1 + 0x14) = 0;
  *puVar1 = &PTR_FUN_106755fa8;
  piVar4 = (int *)(puVar1 + 3);
  piVar4[0] = 0;
  piVar4[1] = 0;
  puVar1[4] = 0;
  *piVar4 = 0x80;
  uVar2 = thunk_FUN_101aa0414(0x20c);
  puVar1[1] = uVar2;
  *(undefined4 *)(puVar1 + 2) = 0x83;
  *(undefined1 *)((long)puVar1 + 0x14) = 1;
  iVar3 = *(int *)(puVar1 + 3);
  if (-3 < iVar3) {
    uVar5 = 0;
    do {
      uVar6 = OCrossFadeHelper::CrossfadeToLevelDipless
                        (((float)(uVar5 & 0xffffffff) / 128.0) * 2.0 + -1.0);
      *(undefined4 *)(puVar1[1] + uVar5 * 4) = uVar6;
      uVar5 = uVar5 + 1;
    } while ((iVar3 + 2U & ((int)(iVar3 + 2U) >> 0x1f ^ 0xffffffffU)) + 1 != uVar5);
    iVar3 = *piVar4;
  }
  *(double *)((long)puVar1 + 0x1c) = dVar7;
  *(float *)((long)puVar1 + 0x24) = (float)iVar3 / 2.0;
  DAT_106f7ec08[3] = puVar1;
  puVar1 = operator_new(0x28);
  puVar1[1] = 0;
  *(undefined4 *)(puVar1 + 2) = 0;
  *(undefined1 *)((long)puVar1 + 0x14) = 0;
  *puVar1 = &PTR_FUN_106755fa8;
  piVar4 = (int *)(puVar1 + 3);
  piVar4[0] = 0;
  piVar4[1] = 0;
  puVar1[4] = 0;
  *piVar4 = 0x80;
  uVar2 = thunk_FUN_101aa0414(0x20c);
  puVar1[1] = uVar2;
  *(undefined4 *)(puVar1 + 2) = 0x83;
  *(undefined1 *)((long)puVar1 + 0x14) = 1;
  iVar3 = *(int *)(puVar1 + 3);
  if (-3 < iVar3) {
    uVar5 = 0;
    do {
      uVar6 = OCrossFadeHelper::CrossfadeToLevelSlowCut
                        (((float)(uVar5 & 0xffffffff) / 128.0) * 2.0 + -1.0);
      *(undefined4 *)(puVar1[1] + uVar5 * 4) = uVar6;
      uVar5 = uVar5 + 1;
    } while ((iVar3 + 2U & ((int)(iVar3 + 2U) >> 0x1f ^ 0xffffffffU)) + 1 != uVar5);
    iVar3 = *piVar4;
  }
  *(double *)((long)puVar1 + 0x1c) = dVar7;
  *(float *)((long)puVar1 + 0x24) = (float)iVar3 / 2.0;
  DAT_106f7ec08[4] = puVar1;
  puVar1 = operator_new(0x28);
  puVar1[1] = 0;
  *(undefined4 *)(puVar1 + 2) = 0;
  *(undefined1 *)((long)puVar1 + 0x14) = 0;
  *puVar1 = &PTR_FUN_106755fa8;
  piVar4 = (int *)(puVar1 + 3);
  piVar4[0] = 0;
  piVar4[1] = 0;
  puVar1[4] = 0;
  *piVar4 = 0x80;
  uVar2 = thunk_FUN_101aa0414(0x20c);
  puVar1[1] = uVar2;
  *(undefined4 *)(puVar1 + 2) = 0x83;
  *(undefined1 *)((long)puVar1 + 0x14) = 1;
  iVar3 = *(int *)(puVar1 + 3);
  if (-3 < iVar3) {
    uVar5 = 0;
    do {
      uVar6 = OCrossFadeHelper::CrossfadeToLevelFastCut
                        (((float)(uVar5 & 0xffffffff) / 128.0) * 2.0 + -1.0);
      *(undefined4 *)(puVar1[1] + uVar5 * 4) = uVar6;
      uVar5 = uVar5 + 1;
    } while ((iVar3 + 2U & ((int)(iVar3 + 2U) >> 0x1f ^ 0xffffffffU)) + 1 != uVar5);
    iVar3 = *piVar4;
  }
  *(double *)((long)puVar1 + 0x1c) = dVar7;
  *(float *)((long)puVar1 + 0x24) = (float)iVar3 / 2.0;
  DAT_106f7ec08[5] = puVar1;
  puVar1 = operator_new(0x28);
  puVar1[1] = 0;
  *(undefined4 *)(puVar1 + 2) = 0;
  *(undefined1 *)((long)puVar1 + 0x14) = 0;
  *puVar1 = &PTR_FUN_106755fa8;
  piVar4 = (int *)(puVar1 + 3);
  piVar4[0] = 0;
  piVar4[1] = 0;
  puVar1[4] = 0;
  *piVar4 = 0x80;
  uVar2 = thunk_FUN_101aa0414(0x20c);
  puVar1[1] = uVar2;
  *(undefined4 *)(puVar1 + 2) = 0x83;
  *(undefined1 *)((long)puVar1 + 0x14) = 1;
  iVar3 = *(int *)(puVar1 + 3);
  if (-3 < iVar3) {
    uVar5 = 0;
    do {
      uVar6 = OCrossFadeHelper::CrossfadeToLevelTransition
                        (((float)(uVar5 & 0xffffffff) / 128.0) * 2.0 + -1.0);
      *(undefined4 *)(puVar1[1] + uVar5 * 4) = uVar6;
      uVar5 = uVar5 + 1;
    } while ((iVar3 + 2U & ((int)(iVar3 + 2U) >> 0x1f ^ 0xffffffffU)) + 1 != uVar5);
    iVar3 = *piVar4;
  }
  *(double *)((long)puVar1 + 0x1c) = dVar7;
  *(float *)((long)puVar1 + 0x24) = (float)iVar3 / 2.0;
  DAT_106f7ec08[6] = puVar1;
  return;
}

