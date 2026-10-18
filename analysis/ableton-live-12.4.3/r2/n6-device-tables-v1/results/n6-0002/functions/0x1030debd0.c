
void FUN_1030debd0(undefined8 *param_1,long param_2)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  long lVar3;
  undefined4 local_34;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  FUN_1030d0098(*(undefined8 *)(param_2 + 0x250),param_1);
  FUN_1030d2eb0(*(undefined8 *)(param_2 + 0x268),param_1);
  FUN_1030d8ebc(*(undefined8 *)(param_2 + 0x280),param_1);
  FUN_1030d8ebc(*(undefined8 *)(param_2 + 0x298),param_1);
  puVar1 = (undefined8 *)param_1[1];
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
  FUN_1030ce134(*(undefined8 *)(param_2 + 0x2c8),param_1,1);
  FUN_1030ce134(*(undefined8 *)(param_2 + 0x2e0),param_1,2);
  puVar1 = (undefined8 *)param_1[1];
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
  lVar3 = *(long *)(param_2 + 0x370);
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x48);
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
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,lVar3 + 0x40);
  }
  param_1[1] = puVar1;
  local_34 = 8;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x60);
    puVar1[1] = 0;
    puVar1[2] = DAT_10584d6d0;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,lVar3 + 0x58,&local_34);
  }
  param_1[1] = puVar1;
  lVar3 = *(long *)(param_2 + 0x388);
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x48);
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
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,lVar3 + 0x40);
  }
  param_1[1] = puVar1;
  local_34 = 8;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x60);
    puVar1[1] = 0;
    puVar1[2] = DAT_10584d6d0;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,lVar3 + 0x58,&local_34);
  }
  param_1[1] = puVar1;
  lVar3 = *(long *)(param_2 + 0x3a0);
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x48);
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
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,lVar3 + 0x40);
  }
  param_1[1] = puVar1;
  local_34 = 8;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x60);
    puVar1[1] = 0;
    puVar1[2] = DAT_10584d6d0;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,lVar3 + 0x58,&local_34);
  }
  param_1[1] = puVar1;
  lVar3 = *(long *)(param_2 + 0x3b8);
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x48);
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
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,lVar3 + 0x40);
  }
  param_1[1] = puVar1;
  local_34 = 8;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x60);
    puVar1[1] = 0;
    puVar1[2] = DAT_10584d6d0;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,lVar3 + 0x58,&local_34);
  }
  param_1[1] = puVar1;
  lVar3 = *(long *)(param_2 + 0x3d0);
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x48);
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
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,lVar3 + 0x40);
  }
  param_1[1] = puVar1;
  local_34 = 8;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x60);
    puVar1[1] = 0;
    puVar1[2] = DAT_10584d6d0;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,lVar3 + 0x58,&local_34);
  }
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
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
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0x3e0);
  }
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
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
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x3f8);
  }
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
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
  param_1[1] = puVar1;
  if (puVar1 < (undefined8 *)param_1[2]) {
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
    puVar1 = (undefined8 *)FUN_1030c50c0(param_1,param_2 + 0x488);
  }
  param_1[1] = puVar1;
  lVar3 = *(long *)(param_2 + 0x340);
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x48);
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
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,lVar3 + 0x40);
  }
  param_1[1] = puVar1;
  local_34 = 8;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x60);
    puVar1[1] = 0;
    puVar1[2] = DAT_10584d6d0;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed63c(param_1,lVar3 + 0x58,&local_34);
  }
  param_1[1] = puVar1;
  lVar3 = *(long *)(param_2 + 0x358);
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x48);
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
    puVar1 = (undefined8 *)FUN_1030ed054(param_1,lVar3 + 0x40);
  }
  param_1[1] = puVar1;
  local_34 = 8;
  if (puVar1 < (undefined8 *)param_1[2]) {
    *puVar1 = *(undefined8 *)(lVar3 + 0x60);
    puVar1[1] = 0;
    puVar1[2] = DAT_10584d6d0;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    param_1[1] = puVar1 + 7;
    return;
  }
  uVar2 = FUN_1030ed63c(param_1,lVar3 + 0x58,&local_34);
  param_1[1] = uVar2;
  return;
}

