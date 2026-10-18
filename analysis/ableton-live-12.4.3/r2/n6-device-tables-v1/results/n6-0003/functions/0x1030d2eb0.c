
void FUN_1030d2eb0(long param_1,long param_2)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  
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
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d2f10;
LAB_1030d3098:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d30d8;
LAB_1030d2f2c:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x98);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d2f48;
LAB_1030d3118:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d3158;
LAB_1030d2f64:
    puVar1 = (undefined8 *)FUN_1030ed054(param_2,param_1 + 200);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d2f80;
LAB_1030d3198:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d31d8;
LAB_1030d2f9c:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0xf8);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d2fb8;
LAB_1030d3218:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d3258;
LAB_1030d2fd4:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x128);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d2ff0;
LAB_1030d3298:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d32d8;
LAB_1030d300c:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x158);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d3028;
LAB_1030d3318:
    *puVar1 = *(undefined8 *)(param_1 + 0x178);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d3358;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_2,param_1 + 0x68);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d3098;
LAB_1030d2f10:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x80);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d2f2c;
LAB_1030d30d8:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d3118;
LAB_1030d2f48:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0xb0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d2f64;
LAB_1030d3158:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d3198;
LAB_1030d2f80:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0xe0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d2f9c;
LAB_1030d31d8:
    *puVar1 = *(undefined8 *)(param_1 + 0x100);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d3218;
LAB_1030d2fb8:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x110);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d2fd4;
LAB_1030d3258:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d3298;
LAB_1030d2ff0:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x140);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d300c;
LAB_1030d32d8:
    *puVar1 = *(undefined8 *)(param_1 + 0x160);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d3318;
LAB_1030d3028:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x170);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
LAB_1030d3358:
      *puVar1 = *(undefined8 *)(param_1 + 400);
      puVar1[1] = 0;
      puVar1[2] = 0x8000000000000000;
      puVar1[3] = 0x7f7fffff7f7fffff;
      *(undefined1 *)(puVar1 + 4) = 0;
      puVar1[5] = 0;
      *(undefined4 *)(puVar1 + 6) = 0;
      *(undefined1 *)((long)puVar1 + 0x34) = 0;
      puVar1 = puVar1 + 7;
      *(undefined8 **)(param_2 + 8) = puVar1;
      if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d3398;
      goto LAB_1030d3060;
    }
  }
  puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x188);
  *(undefined8 **)(param_2 + 8) = puVar1;
  if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
LAB_1030d3398:
    *puVar1 = *(undefined8 *)(param_1 + 0x1a8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    *(undefined8 **)(param_2 + 8) = puVar1 + 7;
    return;
  }
LAB_1030d3060:
  uVar2 = FUN_1030c50c0(param_2,param_1 + 0x1a0);
  *(undefined8 *)(param_2 + 8) = uVar2;
  return;
}

