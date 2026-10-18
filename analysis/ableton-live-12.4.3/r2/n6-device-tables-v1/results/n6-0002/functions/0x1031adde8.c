
/* WARNING: Removing unreachable block (ram,0x0001031adf7c) */
/* WARNING: Removing unreachable block (ram,0x0001031adf9c) */
/* WARNING: Removing unreachable block (ram,0x0001031ae270) */
/* WARNING: Removing unreachable block (ram,0x0001031ae290) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1031adde8(long *param_1,long param_2)

{
  undefined8 *puVar1;
  long *plVar2;
  long *plVar3;
  long lVar4;
  undefined8 local_80;
  undefined8 uStack_78;
  long local_70;
  double dStack_68;
  undefined1 local_60;
  long local_58;
  int local_50;
  char local_4c;
  undefined4 local_44;
  
  plVar2 = *(long **)(param_2 + 8);
  if (plVar2 < *(long **)(param_2 + 0x10)) {
    *plVar2 = param_1[0xb];
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031ade80;
LAB_1031ade54:
    plVar2 = (long *)FUN_1030ed054(param_2,param_1 + 0xd);
  }
  else {
    plVar2 = (long *)FUN_1030ed1cc(param_2,param_1 + 10);
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031ade54;
LAB_1031ade80:
    *plVar2 = param_1[0xe];
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
  }
  *(long **)(param_2 + 8) = plVar2;
  local_80 = CONCAT44(local_80._4_4_,0x3f800000);
  local_44 = 0x40400000;
  if (plVar2 < *(long **)(param_2 + 0x10)) {
    *plVar2 = param_1[0x11];
    plVar2[1] = 0;
    lVar4 = DAT_105657a88;
    plVar2[2] = DAT_1055d1ec0;
    plVar2[3] = lVar4;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    plVar3 = plVar2 + 7;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
  }
  else {
    plVar3 = (long *)FUN_1030ed9c0(param_2,param_1 + 0x10,&local_80,&local_44);
  }
  *(long **)(param_2 + 8) = plVar3;
  dStack_68 = (double)_DAT_1058ca458;
  lVar4 = DAT_1055d1ec0;
  local_80 = param_1[0x17];
  uStack_78 = 0;
  local_70 = DAT_1055d1ec0;
  local_60 = 0;
  local_58 = 0;
  local_50 = 0;
  local_4c = '\0';
  if (plVar3 < *(long **)(param_2 + 0x10)) {
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[1] = 0;
    *plVar3 = local_80;
    plVar3[3] = (long)dStack_68;
    plVar3[2] = lVar4;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    local_4c = '\0';
    local_50 = 0;
    local_58 = 0;
    local_60 = 0;
    local_70 = lVar4;
    uStack_78 = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
  }
  else {
    plVar3 = (long *)FUN_1030ed7f0(param_2,&local_80);
  }
  *(long **)(param_2 + 8) = plVar3;
  if ((local_58 != 0) && (local_4c == '\x01')) {
    FUN_101a24778(local_58,(long)local_50 << 2);
    plVar3 = *(long **)(param_2 + 8);
  }
  if (plVar3 < *(long **)(param_2 + 0x10)) {
    *plVar3 = param_1[0x1d];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae0e4;
LAB_1031ae044:
    plVar3 = (long *)FUN_1030c50c0(param_2,param_1 + 0x1f);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae124;
LAB_1031ae060:
    plVar3 = (long *)FUN_1030c50c0(param_2,param_1 + 0x22);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae164;
LAB_1031ae07c:
    plVar3 = (long *)FUN_1030c50c0(param_2,param_1 + 0x25);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae1a4;
LAB_1031ae098:
    plVar3 = (long *)FUN_1030c50c0(param_2,param_1 + 0x28);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae1e4;
LAB_1031ae0b4:
    plVar3 = (long *)FUN_1030c50c0(param_2,param_1 + 0x2b);
  }
  else {
    plVar3 = (long *)FUN_1030ed054(param_2,param_1 + 0x1c);
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae044;
LAB_1031ae0e4:
    *plVar3 = param_1[0x20];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae060;
LAB_1031ae124:
    *plVar3 = param_1[0x23];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae07c;
LAB_1031ae164:
    *plVar3 = param_1[0x26];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae098;
LAB_1031ae1a4:
    *plVar3 = param_1[0x29];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae0b4;
LAB_1031ae1e4:
    *plVar3 = param_1[0x2c];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
  }
  *(long **)(param_2 + 8) = plVar3;
  local_80 = param_1[0x2f];
  uStack_78 = 0;
  dStack_68 = (double)NEON_fmov(0xbf800000,4);
  dStack_68 = -dStack_68;
  local_70 = lVar4;
  local_60 = 0;
  local_58 = 0;
  local_50 = 0;
  local_4c = '\0';
  if (plVar3 < *(long **)(param_2 + 0x10)) {
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[1] = 0;
    *plVar3 = local_80;
    plVar3[3] = (long)dStack_68;
    plVar3[2] = lVar4;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    local_4c = '\0';
    local_50 = 0;
    local_58 = 0;
    local_60 = 0;
    uStack_78 = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
  }
  else {
    plVar3 = (long *)FUN_1030ed7f0(param_2,&local_80);
  }
  *(long **)(param_2 + 8) = plVar3;
  if ((local_58 != 0) && (local_4c == '\x01')) {
    FUN_101a24778(local_58,(long)local_50 << 2);
    plVar3 = *(long **)(param_2 + 8);
  }
  local_80 = CONCAT44(local_80._4_4_,1);
  if (plVar3 < *(long **)(param_2 + 0x10)) {
    *plVar3 = param_1[0x32];
    plVar3[1] = 0;
    plVar3[2] = DAT_1055f9a68;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae56c;
LAB_1031ae344:
    local_80 = 0;
    plVar3 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae5b0;
LAB_1031ae368:
    local_80 = CONCAT44(local_80._4_4_,1);
    plVar3 = (long *)FUN_1030ed63c(param_2,param_1 + 0x34,&local_80);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae5f0;
LAB_1031ae38c:
    local_80 = 0;
    plVar3 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae634;
LAB_1031ae3b0:
    local_80 = CONCAT44(local_80._4_4_,1);
    plVar3 = (long *)FUN_1030ed63c(param_2,param_1 + 0x37,&local_80);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae674;
LAB_1031ae3d4:
    local_80 = 0;
    plVar3 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae6b0;
LAB_1031ae3f0:
    plVar3 = (long *)FUN_1030c50c0(param_2,param_1 + 0x3a);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae6f0;
LAB_1031ae40c:
    plVar3 = (long *)FUN_1030ed1cc(param_2,param_1 + 0x3d);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae738;
LAB_1031ae430:
    local_80 = CONCAT44(local_80._4_4_,3);
    plVar3 = (long *)FUN_103199ed8(param_2,param_1 + 0x40,&local_80);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae77c;
LAB_1031ae454:
    local_80 = 0;
    plVar3 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae7b8;
LAB_1031ae470:
    plVar3 = (long *)FUN_1030ed054(param_2,param_1 + 0x43);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae800;
LAB_1031ae494:
    local_80 = CONCAT44(local_80._4_4_,1);
    plVar3 = (long *)FUN_1030ed63c(param_2,param_1 + 0x46,&local_80);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae840;
LAB_1031ae4b8:
    local_80 = 0;
    plVar3 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae87c;
LAB_1031ae4d4:
    plVar3 = (long *)FUN_1030c50c0(param_2,param_1 + 0x49);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae8c4;
LAB_1031ae4f8:
    local_80 = CONCAT44(local_80._4_4_,1);
    plVar3 = (long *)FUN_1030ed63c(param_2,param_1 + 0x4c,&local_80);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae904;
LAB_1031ae51c:
    local_80 = 0;
    plVar3 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031ae940;
LAB_1031ae538:
    plVar3 = (long *)FUN_1030c50c0(param_2,param_1 + 0x4f);
  }
  else {
    plVar3 = (long *)FUN_1030ed63c(param_2,param_1 + 0x31,&local_80);
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae344;
LAB_1031ae56c:
    *plVar3 = 0;
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    local_80._4_4_ = 0;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae368;
LAB_1031ae5b0:
    *plVar3 = param_1[0x35];
    plVar3[1] = 0;
    plVar3[2] = DAT_1055f9a68;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae38c;
LAB_1031ae5f0:
    *plVar3 = 0;
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    local_80._4_4_ = 0;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae3b0;
LAB_1031ae634:
    *plVar3 = param_1[0x38];
    plVar3[1] = 0;
    plVar3[2] = DAT_1055f9a68;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae3d4;
LAB_1031ae674:
    local_80 = 0;
    *plVar3 = 0;
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae3f0;
LAB_1031ae6b0:
    *plVar3 = param_1[0x3b];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae40c;
LAB_1031ae6f0:
    *plVar3 = param_1[0x3e];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae430;
LAB_1031ae738:
    *plVar3 = param_1[0x41];
    plVar3[1] = 0;
    plVar3[2] = DAT_1055f9a78;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae454;
LAB_1031ae77c:
    local_80 = 0;
    *plVar3 = 0;
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae470;
LAB_1031ae7b8:
    *plVar3 = param_1[0x44];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae494;
LAB_1031ae800:
    *plVar3 = param_1[0x47];
    plVar3[1] = 0;
    plVar3[2] = DAT_1055f9a68;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae4b8;
LAB_1031ae840:
    local_80 = 0;
    *plVar3 = 0;
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae4d4;
LAB_1031ae87c:
    *plVar3 = param_1[0x4a];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae4f8;
LAB_1031ae8c4:
    *plVar3 = param_1[0x4d];
    plVar3[1] = 0;
    plVar3[2] = DAT_1055f9a68;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae51c;
LAB_1031ae904:
    local_80 = 0;
    *plVar3 = 0;
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031ae538;
LAB_1031ae940:
    *plVar3 = param_1[0x50];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
  }
  *(long **)(param_2 + 8) = plVar3;
  local_80 = (**(code **)(*param_1 + 0x1e8))(param_1);
  puVar1 = *(undefined8 **)(param_2 + 8);
  if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
    *puVar1 = local_80;
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    plVar2 = puVar1 + 7;
    *(long **)(param_2 + 8) = plVar2;
    local_80._4_4_ = (undefined4)((ulong)local_80 >> 0x20);
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031aedd4;
LAB_1031ae9d8:
    local_80 = CONCAT44(local_80._4_4_,1);
    plVar2 = (long *)FUN_1030ed63c(param_2,param_1 + 0x52,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031aee14;
LAB_1031ae9fc:
    local_80 = 0;
    plVar2 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031aee58;
LAB_1031aea20:
    local_80 = CONCAT44(local_80._4_4_,1);
    plVar2 = (long *)FUN_1030ed63c(param_2,param_1 + 0x55,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031aee98;
LAB_1031aea44:
    local_80 = 0;
    plVar2 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031aeedc;
LAB_1031aea68:
    local_80 = CONCAT44(local_80._4_4_,1);
    plVar2 = (long *)FUN_1030ed63c(param_2,param_1 + 0x58,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031aef1c;
LAB_1031aea8c:
    local_80 = 0;
    plVar2 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031aef60;
LAB_1031aeab0:
    local_80 = CONCAT44(local_80._4_4_,1);
    plVar2 = (long *)FUN_1030ed63c(param_2,param_1 + 0x5b,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031aefa0;
LAB_1031aead4:
    local_80 = 0;
    plVar2 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031aefdc;
LAB_1031aeaf0:
    plVar2 = (long *)FUN_1030ed1cc(param_2,param_1 + 0x5e);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af024;
LAB_1031aeb14:
    local_80 = CONCAT44(local_80._4_4_,1);
    plVar2 = (long *)FUN_1030ed63c(param_2,param_1 + 0x61,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af064;
LAB_1031aeb38:
    local_80 = 0;
    plVar2 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af0a0;
LAB_1031aeb54:
    plVar2 = (long *)FUN_1030c50c0(param_2,param_1 + 100);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af0e8;
LAB_1031aeb78:
    local_80 = CONCAT44(local_80._4_4_,1);
    plVar2 = (long *)FUN_1030ed63c(param_2,param_1 + 0x67,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af128;
LAB_1031aeb9c:
    local_80 = 0;
    plVar2 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af164;
LAB_1031aebb8:
    plVar2 = (long *)FUN_1030c50c0(param_2,param_1 + 0x6a);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af1ac;
LAB_1031aebdc:
    local_80 = CONCAT44(local_80._4_4_,1);
    plVar2 = (long *)FUN_1030ed63c(param_2,param_1 + 0x6d,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af1ec;
LAB_1031aec00:
    local_80 = 0;
    plVar2 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af230;
LAB_1031aec24:
    local_80 = CONCAT44(local_80._4_4_,1);
    plVar2 = (long *)FUN_1030ed63c(param_2,param_1 + 0x70,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af270;
LAB_1031aec48:
    local_80 = 0;
    plVar2 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af2b4;
LAB_1031aec6c:
    local_80 = CONCAT44(local_80._4_4_,1);
    plVar2 = (long *)FUN_1030ed63c(param_2,param_1 + 0x73,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af2f4;
LAB_1031aec90:
    local_80 = 0;
    plVar2 = (long *)FUN_1031998c0(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af330;
LAB_1031aecac:
    plVar2 = (long *)FUN_1030ed1cc(param_2,param_1 + 0x76);
    *(long **)(param_2 + 8) = plVar2;
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af370;
LAB_1031aecc8:
    plVar2 = (long *)FUN_1030ed054(param_2,param_1 + 0x79);
    *(long **)(param_2 + 8) = plVar2;
    local_80 = CONCAT44(local_80._4_4_,2);
    if (plVar2 < *(long **)(param_2 + 0x10)) goto LAB_1031af3b8;
LAB_1031aecec:
    plVar3 = (long *)FUN_103199d48(param_2,param_1 + 0x7c,&local_80,param_1 + 0x7f);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031af3fc;
LAB_1031aed14:
    plVar3 = (long *)FUN_1030ed1cc(param_2,param_1 + 0x82);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031af43c;
LAB_1031aed30:
    plVar3 = (long *)FUN_1030c50c0(param_2,param_1 + 0x85);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031af47c;
LAB_1031aed4c:
    plVar3 = (long *)FUN_1030c50c0(param_2,param_1 + 0x88);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031af4bc;
LAB_1031aed68:
    plVar3 = (long *)FUN_1030c50c0(param_2,param_1 + 0x8b);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031af4fc;
LAB_1031aed84:
    plVar3 = (long *)FUN_1030c50c0(param_2,param_1 + 0x8e);
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) goto LAB_1031af53c;
  }
  else {
    plVar2 = (long *)FUN_1031c2694(param_2,&local_80);
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031ae9d8;
LAB_1031aedd4:
    *plVar2 = param_1[0x53];
    plVar2[1] = 0;
    plVar2[2] = DAT_1055f9a68;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031ae9fc;
LAB_1031aee14:
    *plVar2 = 0;
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    local_80._4_4_ = 0;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aea20;
LAB_1031aee58:
    *plVar2 = param_1[0x56];
    plVar2[1] = 0;
    plVar2[2] = DAT_1055f9a68;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aea44;
LAB_1031aee98:
    *plVar2 = 0;
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    local_80._4_4_ = 0;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aea68;
LAB_1031aeedc:
    *plVar2 = param_1[0x59];
    plVar2[1] = 0;
    plVar2[2] = DAT_1055f9a68;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aea8c;
LAB_1031aef1c:
    *plVar2 = 0;
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    local_80._4_4_ = 0;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aeab0;
LAB_1031aef60:
    *plVar2 = param_1[0x5c];
    plVar2[1] = 0;
    plVar2[2] = DAT_1055f9a68;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aead4;
LAB_1031aefa0:
    local_80 = 0;
    *plVar2 = 0;
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aeaf0;
LAB_1031aefdc:
    *plVar2 = param_1[0x5f];
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aeb14;
LAB_1031af024:
    *plVar2 = param_1[0x62];
    plVar2[1] = 0;
    plVar2[2] = DAT_1055f9a68;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aeb38;
LAB_1031af064:
    local_80 = 0;
    *plVar2 = 0;
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aeb54;
LAB_1031af0a0:
    *plVar2 = param_1[0x65];
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aeb78;
LAB_1031af0e8:
    *plVar2 = param_1[0x68];
    plVar2[1] = 0;
    plVar2[2] = DAT_1055f9a68;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aeb9c;
LAB_1031af128:
    local_80 = 0;
    *plVar2 = 0;
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aebb8;
LAB_1031af164:
    *plVar2 = param_1[0x6b];
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aebdc;
LAB_1031af1ac:
    *plVar2 = param_1[0x6e];
    plVar2[1] = 0;
    plVar2[2] = DAT_1055f9a68;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aec00;
LAB_1031af1ec:
    *plVar2 = 0;
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    local_80._4_4_ = 0;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aec24;
LAB_1031af230:
    *plVar2 = param_1[0x71];
    plVar2[1] = 0;
    plVar2[2] = DAT_1055f9a68;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aec48;
LAB_1031af270:
    *plVar2 = 0;
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    local_80._4_4_ = 0;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aec6c;
LAB_1031af2b4:
    *plVar2 = param_1[0x74];
    plVar2[1] = 0;
    plVar2[2] = DAT_1055f9a68;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aec90;
LAB_1031af2f4:
    local_80 = 0;
    *plVar2 = 0;
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aecac;
LAB_1031af330:
    *plVar2 = param_1[0x77];
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aecc8;
LAB_1031af370:
    *plVar2 = param_1[0x7a];
    plVar2[1] = 0;
    plVar2[2] = -0x8000000000000000;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    plVar2 = plVar2 + 7;
    *(long **)(param_2 + 8) = plVar2;
    local_80 = CONCAT44(local_80._4_4_,2);
    if (*(long **)(param_2 + 0x10) <= plVar2) goto LAB_1031aecec;
LAB_1031af3b8:
    lVar4 = param_1[0x80];
    *plVar2 = param_1[0x7d];
    plVar2[1] = lVar4;
    plVar2[2] = DAT_1055f9a70;
    plVar2[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar2 + 4) = 0;
    plVar2[5] = 0;
    *(undefined4 *)(plVar2 + 6) = 0;
    plVar3 = plVar2 + 7;
    *(undefined1 *)((long)plVar2 + 0x34) = 0;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031aed14;
LAB_1031af3fc:
    *plVar3 = param_1[0x83];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031aed30;
LAB_1031af43c:
    *plVar3 = param_1[0x86];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031aed4c;
LAB_1031af47c:
    *plVar3 = param_1[0x89];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031aed68;
LAB_1031af4bc:
    *plVar3 = param_1[0x8c];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (*(long **)(param_2 + 0x10) <= plVar3) goto LAB_1031aed84;
LAB_1031af4fc:
    *plVar3 = param_1[0x8f];
    plVar3[1] = 0;
    plVar3[2] = -0x8000000000000000;
    plVar3[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(plVar3 + 4) = 0;
    plVar3[5] = 0;
    *(undefined4 *)(plVar3 + 6) = 0;
    *(undefined1 *)((long)plVar3 + 0x34) = 0;
    plVar3 = plVar3 + 7;
    *(long **)(param_2 + 8) = plVar3;
    if (plVar3 < *(long **)(param_2 + 0x10)) {
LAB_1031af53c:
      *plVar3 = param_1[0x92];
      plVar3[1] = 0;
      plVar3[2] = -0x8000000000000000;
      plVar3[3] = 0x7f7fffff7f7fffff;
      *(undefined1 *)(plVar3 + 4) = 0;
      plVar3[5] = 0;
      *(undefined4 *)(plVar3 + 6) = 0;
      *(undefined1 *)((long)plVar3 + 0x34) = 0;
      plVar3 = plVar3 + 7;
      goto LAB_1031af56c;
    }
  }
  plVar3 = (long *)FUN_1030c50c0(param_2,param_1 + 0x91);
LAB_1031af56c:
  *(long **)(param_2 + 8) = plVar3;
  FUN_1031b5104(param_1[0x9b],param_2);
  FUN_1031b5104(param_1[0x9e],param_2);
  return;
}

