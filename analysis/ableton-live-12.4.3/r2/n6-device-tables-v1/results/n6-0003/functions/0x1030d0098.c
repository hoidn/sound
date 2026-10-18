
void FUN_1030d0098(long param_1,long param_2)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  
  puVar1 = *(undefined8 **)(param_2 + 8);
  if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
    *puVar1 = *(undefined8 *)(param_1 + 0x30);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d00f8;
LAB_1030d022c:
    *puVar1 = *(undefined8 *)(param_1 + 0x48);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d026c;
LAB_1030d0114:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x58);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d0130;
LAB_1030d02ac:
    *puVar1 = *(undefined8 *)(param_1 + 0x78);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d02ec;
LAB_1030d014c:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x88);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d0168;
LAB_1030d032c:
    *puVar1 = *(undefined8 *)(param_1 + 0xa8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d036c;
LAB_1030d0184:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0xb8);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d01a0;
LAB_1030d03ac:
    *puVar1 = *(undefined8 *)(param_1 + 0xd8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d03ec;
LAB_1030d01bc:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0xe8);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
LAB_1030d042c:
      *puVar1 = *(undefined8 *)(param_1 + 0x108);
      puVar1[1] = 0;
      puVar1[2] = 0x8000000000000000;
      puVar1[3] = 0x7f7fffff7f7fffff;
      *(undefined1 *)(puVar1 + 4) = 0;
      puVar1[5] = 0;
      *(undefined4 *)(puVar1 + 6) = 0;
      *(undefined1 *)((long)puVar1 + 0x34) = 0;
      puVar1 = puVar1 + 7;
      *(undefined8 **)(param_2 + 8) = puVar1;
      if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d046c;
      goto LAB_1030d01f4;
    }
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_2,param_1 + 0x28);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d022c;
LAB_1030d00f8:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x40);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d0114;
LAB_1030d026c:
    *puVar1 = *(undefined8 *)(param_1 + 0x60);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d02ac;
LAB_1030d0130:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x70);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d014c;
LAB_1030d02ec:
    *puVar1 = *(undefined8 *)(param_1 + 0x90);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d032c;
LAB_1030d0168:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0xa0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d0184;
LAB_1030d036c:
    *puVar1 = *(undefined8 *)(param_1 + 0xc0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d03ac;
LAB_1030d01a0:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0xd0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d01bc;
LAB_1030d03ec:
    *puVar1 = *(undefined8 *)(param_1 + 0xf0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d042c;
  }
  puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x100);
  *(undefined8 **)(param_2 + 8) = puVar1;
  if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
LAB_1030d046c:
    *puVar1 = *(undefined8 *)(param_1 + 0x120);
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
LAB_1030d01f4:
  uVar2 = FUN_1030c50c0(param_2,param_1 + 0x118);
  *(undefined8 *)(param_2 + 8) = uVar2;
  return;
}

