
void FUN_1031b5104(long param_1,long param_2)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  
  puVar1 = *(undefined8 **)(param_2 + 8);
  if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
    *puVar1 = *(undefined8 *)(param_1 + 0x58);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1031b5164;
LAB_1031b52b4:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1031b52f4;
LAB_1031b5180:
    puVar1 = (undefined8 *)FUN_1030ed054(param_2,param_1 + 0x80);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1031b519c;
LAB_1031b5334:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1031b5374;
LAB_1031b51b8:
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_2,param_1 + 0xb0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1031b51d4;
LAB_1031b53b4:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1031b53f4;
LAB_1031b51f0:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0xe0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1031b520c;
LAB_1031b5434:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1031b5474;
LAB_1031b5228:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x110);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1031b5244;
LAB_1031b54b4:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1031b54f4;
  }
  else {
    puVar1 = (undefined8 *)FUN_1031c280c(param_2,param_1 + 0x50);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1031b52b4;
LAB_1031b5164:
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_2,param_1 + 0x68);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1031b5180;
LAB_1031b52f4:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1031b5334;
LAB_1031b519c:
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_2,param_1 + 0x98);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1031b51b8;
LAB_1031b5374:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1031b53b4;
LAB_1031b51d4:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 200);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1031b51f0;
LAB_1031b53f4:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1031b5434;
LAB_1031b520c:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0xf8);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1031b5228;
LAB_1031b5474:
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
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1031b54b4;
LAB_1031b5244:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x128);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
LAB_1031b54f4:
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
      if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1031b5534;
      goto LAB_1031b527c;
    }
  }
  puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x140);
  *(undefined8 **)(param_2 + 8) = puVar1;
  if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
LAB_1031b5534:
    *puVar1 = *(undefined8 *)(param_1 + 0x160);
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
LAB_1031b527c:
  uVar2 = FUN_1030c50c0(param_2,param_1 + 0x158);
  *(undefined8 *)(param_2 + 8) = uVar2;
  return;
}

