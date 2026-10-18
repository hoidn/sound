
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1031ad110(undefined8 *param_1,long param_2)

{
  undefined8 *puVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  double dVar4;
  undefined4 local_34;
  undefined8 local_30;
  undefined4 local_24;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  local_24 = 5;
  local_30 = 0;
  local_34 = 7;
  puVar1 = (undefined8 *)FUN_103199734(param_1,param_2 + 0x248,&local_24,&local_30,&local_34);
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(param_2 + 0x268);
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
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x260);
  }
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(param_2 + 0x280);
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
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x278);
  }
  param_1[1] = puVar1;
  local_30._0_4_ = 0x3f800000;
  local_24 = 0x40400000;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(param_2 + 0x370);
    puVar1[1] = 0;
    uVar3 = DAT_105657a88;
    puVar1[2] = DAT_1055d1ec0;
    puVar1[3] = uVar3;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    puVar2 = puVar1 + 7;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030ed9c0(param_1,param_2 + 0x368,&local_30,&local_24);
  }
  param_1[1] = puVar2;
  local_30 = CONCAT44(local_30._4_4_,0x3f800000);
  local_24 = 0x41400000;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x3a0);
    puVar2[1] = 0;
    uVar3 = _DAT_1058ca458;
    puVar2[2] = DAT_1055d1ec0;
    puVar2[3] = uVar3;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    puVar1 = puVar2 + 7;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    param_1[1] = puVar1;
    if (puVar1 < (undefined8 *)param_1[2]) goto LAB_1031ad2c8;
LAB_1031ad324:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x3c8);
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed9c0(param_1,param_2 + 0x398,&local_30,&local_24);
    param_1[1] = puVar1;
    if ((undefined8 *)param_1[2] <= puVar1) goto LAB_1031ad324;
LAB_1031ad2c8:
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
  param_1[1] = puVar1;
  local_30 = CONCAT44(local_30._4_4_,2);
  if (puVar1 < (undefined8 *)param_1[2]) {
    uVar3 = *(undefined8 *)(param_2 + 0x400);
    *puVar1 = *(undefined8 *)(param_2 + 1000);
    puVar1[1] = uVar3;
    puVar1[2] = DAT_1055f9a70;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    puVar2 = puVar1 + 7;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    param_1[1] = puVar2;
    if ((undefined8 *)param_1[2] <= puVar2) {
LAB_1031ad3ec:
      local_30 = 0;
      puVar2 = (undefined8 *)FUN_1031998c0(param_1,&local_30);
      goto LAB_1031ad3f8;
    }
  }
  else {
    puVar2 = (undefined8 *)FUN_103199a30(param_1,param_2 + 0x3e0,&local_30,param_2 + 0x3f8);
    param_1[1] = puVar2;
    if ((undefined8 *)param_1[2] <= puVar2) goto LAB_1031ad3ec;
  }
  local_30 = 0;
  *puVar2 = 0;
  puVar2[1] = 0;
  puVar2[2] = 0x8000000000000000;
  puVar2[3] = 0x7f7fffff7f7fffff;
  *(undefined1 *)(puVar2 + 4) = 0;
  puVar2[5] = 0;
  *(undefined4 *)(puVar2 + 6) = 0;
  *(undefined1 *)((long)puVar2 + 0x34) = 0;
  puVar2 = puVar2 + 7;
LAB_1031ad3f8:
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x418);
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
    puVar2 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0x410);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x430);
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
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x428);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x448);
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
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x440);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x460);
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
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x458);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x478);
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
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x470);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x490);
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
    puVar2 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x488);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x4a8);
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
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x4a0);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x4c0);
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
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x4b8);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x4d8);
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
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x4d0);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x4f0);
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
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x4e8);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x508);
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
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x500);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x520);
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
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x518);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x538);
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
    puVar2 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x530);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x550);
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
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x548);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x568);
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
    puVar2 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0x560);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x580);
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
    puVar2 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x578);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x598);
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
    puVar2 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x590);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x5b0);
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
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x5a8);
  }
  param_1[1] = puVar2;
  local_30 = CONCAT44(local_30._4_4_,0xbf800000);
  local_24 = 0x3f800000;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x5c8);
    puVar2[1] = 0;
    dVar4 = (double)NEON_fmov(0xbf800000,4);
    puVar2[2] = DAT_1055d1ec0;
    puVar2[3] = -dVar4;
    *(undefined1 *)(puVar2 + 4) = 0;
    puVar2[5] = 0;
    *(undefined4 *)(puVar2 + 6) = 0;
    *(undefined1 *)((long)puVar2 + 0x34) = 0;
    puVar2 = puVar2 + 7;
  }
  else {
    puVar2 = (undefined8 *)FUN_1030ed9c0(param_1,param_2 + 0x5c0,&local_30,&local_24);
  }
  param_1[1] = puVar2;
  if (puVar2 < (undefined8 *)param_1[2]) {
    *puVar2 = *(undefined8 *)(param_2 + 0x5e0);
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
    puVar2 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x5d8);
  }
  param_1[1] = puVar2;
  FUN_1031adde8(*(undefined8 *)(param_2 + 0x688),param_1);
  FUN_1031adde8(*(undefined8 *)(param_2 + 0x6a0),param_1);
  puVar1 = (undefined8 *)param_1[1];
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(param_2 + 0x6e8);
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
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x6e0);
  }
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(param_2 + 0x2b0);
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
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0x2a8);
  }
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(param_2 + 0x2c8);
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
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x2c0);
  }
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(param_2 + 0x2e0);
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
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0x2d8);
  }
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(param_2 + 0x2f8);
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
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x2f0);
  }
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(param_2 + 0x310);
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
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0x308);
  }
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
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
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 800);
  }
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
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
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0x338);
  }
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(param_2 + 0x358);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    param_1[1] = puVar1 + 7;
    return;
  }
  uVar3 = FUN_1030c50c0(param_1,param_2 + 0x350);
  param_1[1] = uVar3;
  return;
}

