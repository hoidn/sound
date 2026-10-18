
void FUN_1030ca45c(undefined8 *param_1,long param_2)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  puVar1 = (undefined8 *)FUN_1030ed054(param_1,param_2 + 0x248);
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
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_1,param_2 + 0x260);
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
    param_1[1] = puVar1 + 7;
    return;
  }
  uVar2 = FUN_1030ed054(param_1,param_2 + 0x278);
  param_1[1] = uVar2;
  return;
}

