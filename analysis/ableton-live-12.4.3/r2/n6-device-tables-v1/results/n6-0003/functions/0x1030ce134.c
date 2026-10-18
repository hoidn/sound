
void FUN_1030ce134(long param_1,long param_2,undefined8 param_3)

{
  undefined8 *puVar1;
  
  puVar1 = *(undefined8 **)(param_2 + 8);
  if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
    *puVar1 = *(undefined8 *)(param_1 + 0x70);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030ce19c;
LAB_1030ce2a8:
    *puVar1 = *(undefined8 *)(param_1 + 0x88);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030ce2e8;
LAB_1030ce1b8:
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_2,param_1 + 0x98);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030ce1d4;
LAB_1030ce328:
    *puVar1 = *(undefined8 *)(param_1 + 0xb8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030ce368;
LAB_1030ce1f0:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 200);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030ce20c;
LAB_1030ce3a8:
    *puVar1 = *(undefined8 *)(param_1 + 0xe8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030ce3e8;
LAB_1030ce228:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x110);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030ce244;
LAB_1030ce428:
    *puVar1 = *(undefined8 *)(param_1 + 0x130);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030ce468;
LAB_1030ce260:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x140);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
LAB_1030ce4a8:
      *puVar1 = *(undefined8 *)(param_1 + 0x160);
      puVar1[1] = 0;
      puVar1[2] = 0x8000000000000000;
      puVar1[3] = 0x7f7fffff7f7fffff;
      *(undefined1 *)(puVar1 + 4) = 0;
      puVar1[5] = 0;
      *(undefined4 *)(puVar1 + 6) = 0;
      *(undefined1 *)((long)puVar1 + 0x34) = 0;
      puVar1 = puVar1 + 7;
      goto LAB_1030ce4d8;
    }
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_2,param_1 + 0x68);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030ce2a8;
LAB_1030ce19c:
    puVar1 = (undefined8 *)FUN_1030ed054(param_2,param_1 + 0x80);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030ce1b8;
LAB_1030ce2e8:
    *puVar1 = *(undefined8 *)(param_1 + 0xa0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030ce328;
LAB_1030ce1d4:
    puVar1 = (undefined8 *)FUN_1030ed054(param_2,param_1 + 0xb0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030ce1f0;
LAB_1030ce368:
    *puVar1 = *(undefined8 *)(param_1 + 0xd0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030ce3a8;
LAB_1030ce20c:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0xe0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030ce228;
LAB_1030ce3e8:
    *puVar1 = *(undefined8 *)(param_1 + 0x118);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030ce428;
LAB_1030ce244:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x128);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030ce260;
LAB_1030ce468:
    *puVar1 = *(undefined8 *)(param_1 + 0x148);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030ce4a8;
  }
  puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x158);
LAB_1030ce4d8:
  *(undefined8 **)(param_2 + 8) = puVar1;
  FUN_1030cb434(*(undefined8 *)(param_1 + 0x178),param_2,param_3);
  FUN_1030cb434(*(undefined8 *)(param_1 + 400),param_2,param_3);
  return;
}

