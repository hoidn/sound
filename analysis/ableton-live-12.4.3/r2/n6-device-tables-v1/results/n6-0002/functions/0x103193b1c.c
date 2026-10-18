
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_103193b1c(undefined8 *param_1,long param_2)

{
  undefined8 *puVar1;
  undefined8 *puVar2;
  ulong uVar3;
  undefined8 uVar4;
  ulong *puVar5;
  ulong *puVar6;
  undefined4 local_44;
  undefined8 local_40;
  undefined4 local_34;
  
  puVar5 = param_1 + 1;
  *puVar5 = 0;
  puVar6 = param_1 + 2;
  *puVar6 = 0;
  *param_1 = 0;
  local_34 = 5;
  local_40 = 0;
  local_44 = 7;
  puVar1 = (undefined8 *)FUN_103199734(param_1,param_2 + 0x248,&local_34,&local_40,&local_44);
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,0x3daaaaab);
  local_34 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x268);
    puVar1[1] = 0;
    uVar4 = DAT_1058ca450;
    puVar1[2] = DAT_1055d1ec0;
    puVar1[3] = uVar4;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    puVar2 = puVar1 + 7;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030ed9c0(param_1,param_2 + 0x260,&local_40,&local_34);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = 0;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = 0;
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  local_40._0_4_ = 0x3f800000;
  local_34 = 0x40400000;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0x280);
    puVar2[1] = 0;
    uVar4 = DAT_105657a88;
    puVar2[2] = DAT_1055d1ec0;
    puVar2[3] = uVar4;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    puVar1 = puVar2 + 7;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed9c0(param_1,param_2 + 0x278,&local_40,&local_34);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,0x3f800000);
  local_34 = 0x41400000;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x2b0);
    puVar1[1] = 0;
    uVar4 = _DAT_1058ca458;
    puVar1[2] = DAT_1055d1ec0;
    puVar1[3] = uVar4;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    puVar2 = puVar1 + 7;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    *puVar5 = (ulong)puVar2;
    if (puVar2 < (undefined8 *)*puVar6) goto LAB_103193d00;
LAB_103193d5c:
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x2d8);
  }
  else {
    puVar2 = (undefined8 *)FUN_1030ed9c0(param_1,param_2 + 0x2a8,&local_40,&local_34);
    *puVar5 = (ulong)puVar2;
    if ((undefined8 *)*puVar6 <= puVar2) goto LAB_103193d5c;
LAB_103193d00:
    *puVar2 = *(undefined8 *)(param_2 + 0x2e0);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  *puVar5 = (ulong)puVar2;
  local_40 = CONCAT44(local_40._4_4_,2);
  if (puVar2 < (undefined8 *)*puVar6) {
    uVar4 = *(undefined8 *)(param_2 + 0x2f8);
    *puVar2 = *(undefined8 *)(param_2 + 0x310);
    puVar2[1] = uVar4;
    puVar2[2] = DAT_1055f9a70;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    puVar1 = puVar2 + 7;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    *puVar5 = (ulong)puVar1;
    if (puVar1 < (undefined8 *)*puVar6) goto LAB_103193dc8;
LAB_103193e24:
    local_40 = 0;
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  else {
    puVar1 = (undefined8 *)FUN_103199a30(param_1,param_2 + 0x308,&local_40,param_2 + 0x2f0);
    *puVar5 = (ulong)puVar1;
    if ((undefined8 *)*puVar6 <= puVar1) goto LAB_103193e24;
LAB_103193dc8:
    local_40 = 0;
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x328);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 800);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x340);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x338);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x358);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x350);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x370);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x368);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x388);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x380);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x3a0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x398);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x3b8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x3b0);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x3d0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x3c8);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 1000);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x3e0);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x400);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x3f8);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x418);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x410);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x430);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x428);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x448);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x440);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x460);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x458);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,4);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x478);
    puVar1[1] = 0;
    puVar1[2] = DAT_10584d6c0;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_103199bc0(param_1,param_2 + 0x470,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x490);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x488);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x4a8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x4a0);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x4c0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x4b8);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x4d8);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x4d0,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x4f0);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x4e8,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x508);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x500);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x520);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x518);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x538);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x530,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x550);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x548,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x568);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x560);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x580);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0x578);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x598);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x590);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x5b0);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x5a8,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x5c8);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x5c0,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x5e0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x5d8);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x5f8);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x5f0,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x610);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x608,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x628);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x620);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x640);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x638,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x658);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x650,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x670);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x668);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x688);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x680);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x6a0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x698);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x6b8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x6b0);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x6d0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x6c8);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x6e8);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x6e0,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x700);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x6f8);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x718);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x710,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x730);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x728);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x748);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x740,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x760);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x758);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x778);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x770);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x790);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x788);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x7a8);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x7a0,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x7c0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x7b8);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x7d8);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 2000,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x7f0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x7e8);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x808);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x800);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x820);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x818);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x838);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x830);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x850);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x848);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x868);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x860,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x880);
    puVar1[1] = 0;
    puVar1[2] = DAT_1055f9a68;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x878,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = 0;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x898);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x890);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x8b0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x8a8);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0x8c8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0x8c0);
  }
  *puVar5 = (ulong)puVar1;
  local_40 = CONCAT44(local_40._4_4_,2);
  if (puVar1 < (undefined8 *)*puVar6) {
    uVar4 = *(undefined8 *)(param_2 + 0x8f8);
    *puVar1 = *(undefined8 *)(param_2 + 0x8e0);
    puVar1[1] = uVar4;
    puVar1[2] = DAT_1055f9a70;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    puVar2 = puVar1 + 7;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    *puVar5 = (ulong)puVar2;
    if (puVar2 < (undefined8 *)*puVar6) goto LAB_1031957c4;
LAB_103195820:
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x908);
  }
  else {
    puVar2 = (undefined8 *)FUN_103199d48(param_1,param_2 + 0x8d8,&local_40,param_2 + 0x8f0);
    *puVar5 = (ulong)puVar2;
    if ((undefined8 *)*puVar6 <= puVar2) goto LAB_103195820;
LAB_1031957c4:
    *puVar2 = *(undefined8 *)(param_2 + 0x910);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  *puVar5 = (ulong)puVar2;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0x928);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x920);
  }
  *puVar5 = (ulong)puVar2;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0x940);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x938);
  }
  *puVar5 = (ulong)puVar2;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0x958);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x950);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = CONCAT44(local_40._4_4_,3);
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0x970);
    puVar2[1] = 0;
    puVar2[2] = DAT_1055f9a78;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_103199ed8(param_1,param_2 + 0x968,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = 0;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = 0;
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0x988);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x980);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0x9a0);
    puVar2[1] = 0;
    puVar2[2] = DAT_1055f9a68;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x998,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = 0;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = 0;
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0x9b8);
    puVar2[1] = 0;
    puVar2[2] = DAT_1055f9a68;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x9b0,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = 0;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = 0;
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0x9d0);
    puVar2[1] = 0;
    puVar2[2] = DAT_1055f9a68;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x9c8,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = 0;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = 0;
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0x9e8);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x9e0);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0xa00);
    puVar2[1] = 0;
    puVar2[2] = DAT_1055f9a68;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0x9f8,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = 0;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = 0;
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0xa18);
    puVar2[1] = 0;
    puVar2[2] = DAT_1055f9a68;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0xa10,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = 0;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = 0;
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = CONCAT44(local_40._4_4_,1);
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0xa30);
    puVar2[1] = 0;
    puVar2[2] = DAT_1055f9a68;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030ed63c(param_1,param_2 + 0xa28,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = 0;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = 0;
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1031998c0(param_1,&local_40);
  }
  *puVar5 = (ulong)puVar2;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0xa48);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0xa40);
  }
  *puVar5 = (ulong)puVar2;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0xa60);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xa58);
  }
  *puVar5 = (ulong)puVar2;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0xa78);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xa70);
  }
  *puVar5 = (ulong)puVar2;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0xa90);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xa88);
  }
  *puVar5 = (ulong)puVar2;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0xaa8);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xaa0);
  }
  *puVar5 = (ulong)puVar2;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0xac0);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xab8);
  }
  *puVar5 = (ulong)puVar2;
  if (puVar2 < (undefined8 *)*puVar6) {
    *puVar2 = *(undefined8 *)(param_2 + 0xad8);
    puVar2[1] = 0;
    puVar2[2] = 0x8000000000000000;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xad0);
  }
  *puVar5 = (ulong)puVar2;
  local_40 = CONCAT44(local_40._4_4_,2);
  if (puVar2 < (undefined8 *)*puVar6) {
    uVar4 = *(undefined8 *)(param_2 + 0xaf0);
    *puVar2 = *(undefined8 *)(param_2 + 0xb08);
    puVar2[1] = uVar4;
    puVar2[2] = DAT_1055f9a70;
    puVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    puVar1 = puVar2 + 7;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    *puVar5 = (ulong)puVar1;
    if ((undefined8 *)*puVar6 <= puVar1) {
LAB_103196158:
      puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0xb18);
      goto LAB_103196164;
    }
  }
  else {
    puVar1 = (undefined8 *)FUN_103199a30(param_1,param_2 + 0xb00,&local_40,param_2 + 0xae8);
    *puVar5 = (ulong)puVar1;
    if ((undefined8 *)*puVar6 <= puVar1) goto LAB_103196158;
  }
  *puVar1 = *(undefined8 *)(param_2 + 0xb20);
  puVar1[1] = 0;
  puVar1[2] = 0x8000000000000000;
  puVar1[3] = 0x7f7fffff7f7fffff;
  *(undefined1 *)(puVar1 + 4) = 0;
  puVar1[5] = 0;
  *(undefined4 *)(puVar1 + 6) = 0;
  *(undefined1 *)((long)puVar1 + 0x34) = 0;
  puVar1 = puVar1 + 7;
LAB_103196164:
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xb38);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xb30);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xb68);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xb60);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xb50);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xb48);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xb80);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xb78);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xb98);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xb90);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xcf0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xce8);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xbc8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0xbc0);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xbe0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xbd8);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xbf8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0xbf0);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xc10);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xc08);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xc28);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0xc20);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xc40);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0xc38);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xc58);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0xc50);
  }
  *puVar5 = (ulong)puVar1;
  if (puVar1 < (undefined8 *)*puVar6) {
    *puVar1 = *(undefined8 *)(param_2 + 0xc70);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    *puVar5 = (ulong)(puVar1 + 7);
    return;
  }
  uVar3 = FUN_1030c50c0(param_1,param_2 + 0xc68);
  *puVar5 = uVar3;
  return;
}

