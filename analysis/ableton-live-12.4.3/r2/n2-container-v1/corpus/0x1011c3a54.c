
/* WARNING: Type propagation algorithm not settling */

undefined1 * FUN_1011c3a54(undefined1 *param_1,undefined1 *param_2)

{
  ulong uVar1;
  byte bVar2;
  char cVar3;
  undefined8 *puVar4;
  long *plVar5;
  undefined8 *puVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  
  puVar6 = (undefined8 *)(param_1 + 8);
  *param_1 = *param_2;
  if (param_1 == param_2) {
    uVar7 = *(undefined8 *)(param_2 + 0xe0);
    param_1[0xe8] = param_2[0xe8];
    *(undefined8 *)(param_1 + 0xe0) = uVar7;
    uVar8 = *(undefined8 *)(param_2 + 0x128);
    uVar7 = *(undefined8 *)(param_2 + 0x120);
    *(undefined8 *)(param_1 + 0x12d) = *(undefined8 *)(param_2 + 0x12d);
    *(undefined8 *)(param_1 + 0x128) = uVar8;
    *(undefined8 *)(param_1 + 0x120) = uVar7;
    return param_1;
  }
  bVar2 = param_2[0x1f];
  if ((char)param_1[0x1f] < '\0') {
    uVar1 = *(ulong *)(param_2 + 0x10);
    puVar4 = *(undefined8 **)(param_2 + 8);
    if (-1 < (char)bVar2) {
      uVar1 = (ulong)bVar2;
      puVar4 = (undefined8 *)(param_2 + 8);
    }
    FUN_100251bd8(puVar6,puVar4,uVar1);
    cVar3 = param_1[0x37];
    bVar2 = param_2[0x37];
  }
  else if ((char)bVar2 < '\0') {
    FUN_100251b18(puVar6,*(undefined8 *)(param_2 + 8),*(undefined8 *)(param_2 + 0x10));
    cVar3 = param_1[0x37];
    bVar2 = param_2[0x37];
  }
  else {
    uVar8 = *(undefined8 *)(param_2 + 0x10);
    uVar7 = *(undefined8 *)(param_2 + 8);
    *(undefined8 *)(param_1 + 0x18) = *(undefined8 *)(param_2 + 0x18);
    *(undefined8 *)(param_1 + 0x10) = uVar8;
    *puVar6 = uVar7;
    cVar3 = param_1[0x37];
    bVar2 = param_2[0x37];
  }
  if (cVar3 < '\0') {
    uVar1 = *(ulong *)(param_2 + 0x28);
    plVar5 = (long *)*(long *)(param_2 + 0x20);
    if (-1 < (char)bVar2) {
      uVar1 = (ulong)bVar2;
      plVar5 = (long *)(param_2 + 0x20);
    }
    FUN_100251bd8(param_1 + 0x20,plVar5,uVar1);
    cVar3 = param_1[0x4f];
    bVar2 = param_2[0x4f];
  }
  else if ((char)bVar2 < '\0') {
    FUN_100251b18(param_1 + 0x20,*(undefined8 *)(param_2 + 0x20),*(undefined8 *)(param_2 + 0x28));
    cVar3 = param_1[0x4f];
    bVar2 = param_2[0x4f];
  }
  else {
    uVar8 = *(undefined8 *)(param_2 + 0x28);
    uVar7 = *(undefined8 *)(param_2 + 0x20);
    *(undefined8 *)(param_1 + 0x30) = *(undefined8 *)(param_2 + 0x30);
    *(undefined8 *)(param_1 + 0x28) = uVar8;
    *(undefined8 *)(param_1 + 0x20) = uVar7;
    cVar3 = param_1[0x4f];
    bVar2 = param_2[0x4f];
  }
  if (cVar3 < '\0') {
    uVar1 = *(ulong *)(param_2 + 0x40);
    plVar5 = (long *)*(long *)(param_2 + 0x38);
    if (-1 < (char)bVar2) {
      uVar1 = (ulong)bVar2;
      plVar5 = (long *)(param_2 + 0x38);
    }
    FUN_100251bd8(param_1 + 0x38,plVar5,uVar1);
    cVar3 = param_1[0x67];
    bVar2 = param_2[0x67];
  }
  else if ((char)bVar2 < '\0') {
    FUN_100251b18(param_1 + 0x38,*(undefined8 *)(param_2 + 0x38),*(undefined8 *)(param_2 + 0x40));
    cVar3 = param_1[0x67];
    bVar2 = param_2[0x67];
  }
  else {
    uVar8 = *(undefined8 *)(param_2 + 0x40);
    uVar7 = *(undefined8 *)(param_2 + 0x38);
    *(undefined8 *)(param_1 + 0x48) = *(undefined8 *)(param_2 + 0x48);
    *(undefined8 *)(param_1 + 0x40) = uVar8;
    *(undefined8 *)(param_1 + 0x38) = uVar7;
    cVar3 = param_1[0x67];
    bVar2 = param_2[0x67];
  }
  if (cVar3 < '\0') {
    uVar1 = *(ulong *)(param_2 + 0x58);
    plVar5 = (long *)*(long *)(param_2 + 0x50);
    if (-1 < (char)bVar2) {
      uVar1 = (ulong)bVar2;
      plVar5 = (long *)(param_2 + 0x50);
    }
    FUN_100251bd8(param_1 + 0x50,plVar5,uVar1);
    cVar3 = param_1[0x7f];
    bVar2 = param_2[0x7f];
  }
  else if ((char)bVar2 < '\0') {
    FUN_100251b18(param_1 + 0x50,*(undefined8 *)(param_2 + 0x50),*(undefined8 *)(param_2 + 0x58));
    cVar3 = param_1[0x7f];
    bVar2 = param_2[0x7f];
  }
  else {
    uVar8 = *(undefined8 *)(param_2 + 0x58);
    uVar7 = *(undefined8 *)(param_2 + 0x50);
    *(undefined8 *)(param_1 + 0x60) = *(undefined8 *)(param_2 + 0x60);
    *(undefined8 *)(param_1 + 0x58) = uVar8;
    *(undefined8 *)(param_1 + 0x50) = uVar7;
    cVar3 = param_1[0x7f];
    bVar2 = param_2[0x7f];
  }
  if (cVar3 < '\0') {
    uVar1 = *(ulong *)(param_2 + 0x70);
    plVar5 = (long *)*(long *)(param_2 + 0x68);
    if (-1 < (char)bVar2) {
      uVar1 = (ulong)bVar2;
      plVar5 = (long *)(param_2 + 0x68);
    }
    FUN_100251bd8(param_1 + 0x68,plVar5,uVar1);
    cVar3 = param_1[0x97];
    bVar2 = param_2[0x97];
  }
  else if ((char)bVar2 < '\0') {
    FUN_100251b18(param_1 + 0x68,*(undefined8 *)(param_2 + 0x68),*(undefined8 *)(param_2 + 0x70));
    cVar3 = param_1[0x97];
    bVar2 = param_2[0x97];
  }
  else {
    uVar8 = *(undefined8 *)(param_2 + 0x70);
    uVar7 = *(undefined8 *)(param_2 + 0x68);
    *(undefined8 *)(param_1 + 0x78) = *(undefined8 *)(param_2 + 0x78);
    *(undefined8 *)(param_1 + 0x70) = uVar8;
    *(undefined8 *)(param_1 + 0x68) = uVar7;
    cVar3 = param_1[0x97];
    bVar2 = param_2[0x97];
  }
  if (cVar3 < '\0') {
    uVar1 = *(ulong *)(param_2 + 0x88);
    plVar5 = (long *)*(long *)(param_2 + 0x80);
    if (-1 < (char)bVar2) {
      uVar1 = (ulong)bVar2;
      plVar5 = (long *)(param_2 + 0x80);
    }
    FUN_100251bd8(param_1 + 0x80,plVar5,uVar1);
    cVar3 = param_1[0xaf];
    bVar2 = param_2[0xaf];
  }
  else if ((char)bVar2 < '\0') {
    FUN_100251b18(param_1 + 0x80,*(undefined8 *)(param_2 + 0x80),*(undefined8 *)(param_2 + 0x88));
    cVar3 = param_1[0xaf];
    bVar2 = param_2[0xaf];
  }
  else {
    uVar8 = *(undefined8 *)(param_2 + 0x88);
    uVar7 = *(undefined8 *)(param_2 + 0x80);
    *(undefined8 *)(param_1 + 0x90) = *(undefined8 *)(param_2 + 0x90);
    *(undefined8 *)(param_1 + 0x88) = uVar8;
    *(undefined8 *)(param_1 + 0x80) = uVar7;
    cVar3 = param_1[0xaf];
    bVar2 = param_2[0xaf];
  }
  if (cVar3 < '\0') {
    uVar1 = *(ulong *)(param_2 + 0xa0);
    plVar5 = (long *)*(long *)(param_2 + 0x98);
    if (-1 < (char)bVar2) {
      uVar1 = (ulong)bVar2;
      plVar5 = (long *)(param_2 + 0x98);
    }
    FUN_100251bd8(param_1 + 0x98,plVar5,uVar1);
    cVar3 = param_1[199];
    bVar2 = param_2[199];
  }
  else if ((char)bVar2 < '\0') {
    FUN_100251b18(param_1 + 0x98,*(undefined8 *)(param_2 + 0x98),*(undefined8 *)(param_2 + 0xa0));
    cVar3 = param_1[199];
    bVar2 = param_2[199];
  }
  else {
    uVar8 = *(undefined8 *)(param_2 + 0xa0);
    uVar7 = *(undefined8 *)(param_2 + 0x98);
    *(undefined8 *)(param_1 + 0xa8) = *(undefined8 *)(param_2 + 0xa8);
    *(undefined8 *)(param_1 + 0xa0) = uVar8;
    *(undefined8 *)(param_1 + 0x98) = uVar7;
    cVar3 = param_1[199];
    bVar2 = param_2[199];
  }
  if (cVar3 < '\0') {
    uVar1 = *(ulong *)(param_2 + 0xb8);
    plVar5 = (long *)*(long *)(param_2 + 0xb0);
    if (-1 < (char)bVar2) {
      uVar1 = (ulong)bVar2;
      plVar5 = (long *)(param_2 + 0xb0);
    }
    FUN_100251bd8(param_1 + 0xb0,plVar5,uVar1);
    cVar3 = param_1[0xdf];
    bVar2 = param_2[0xdf];
  }
  else if ((char)bVar2 < '\0') {
    FUN_100251b18(param_1 + 0xb0,*(undefined8 *)(param_2 + 0xb0),*(undefined8 *)(param_2 + 0xb8));
    cVar3 = param_1[0xdf];
    bVar2 = param_2[0xdf];
  }
  else {
    uVar8 = *(undefined8 *)(param_2 + 0xb8);
    uVar7 = *(undefined8 *)(param_2 + 0xb0);
    *(undefined8 *)(param_1 + 0xc0) = *(undefined8 *)(param_2 + 0xc0);
    *(undefined8 *)(param_1 + 0xb8) = uVar8;
    *(undefined8 *)(param_1 + 0xb0) = uVar7;
    cVar3 = param_1[0xdf];
    bVar2 = param_2[0xdf];
  }
  if (cVar3 < '\0') {
    uVar1 = *(ulong *)(param_2 + 0xd0);
    plVar5 = (long *)*(long *)(param_2 + 200);
    if (-1 < (char)bVar2) {
      uVar1 = (ulong)bVar2;
      plVar5 = (long *)(param_2 + 200);
    }
    FUN_100251bd8(param_1 + 200,plVar5,uVar1);
  }
  else if ((char)bVar2 < '\0') {
    FUN_100251b18(param_1 + 200,*(undefined8 *)(param_2 + 200),*(undefined8 *)(param_2 + 0xd0));
  }
  else {
    uVar8 = *(undefined8 *)(param_2 + 0xd0);
    uVar7 = *(undefined8 *)(param_2 + 200);
    *(undefined8 *)(param_1 + 0xd8) = *(undefined8 *)(param_2 + 0xd8);
    *(undefined8 *)(param_1 + 0xd0) = uVar8;
    *(undefined8 *)(param_1 + 200) = uVar7;
  }
  uVar7 = *(undefined8 *)(param_2 + 0xe0);
  param_1[0xe8] = param_2[0xe8];
  *(undefined8 *)(param_1 + 0xe0) = uVar7;
  bVar2 = param_2[0x107];
  if ((char)param_1[0x107] < '\0') {
    uVar1 = *(ulong *)(param_2 + 0xf8);
    puVar6 = *(undefined8 **)(param_2 + 0xf0);
    if (-1 < (char)bVar2) {
      uVar1 = (ulong)bVar2;
      puVar6 = (undefined8 *)(param_2 + 0xf0);
    }
    FUN_100251bd8(param_1 + 0xf0,puVar6,uVar1);
    cVar3 = param_1[0x11f];
    bVar2 = param_2[0x11f];
  }
  else if ((char)bVar2 < '\0') {
    FUN_100251b18(param_1 + 0xf0,*(undefined8 *)(param_2 + 0xf0),*(undefined8 *)(param_2 + 0xf8));
    cVar3 = param_1[0x11f];
    bVar2 = param_2[0x11f];
  }
  else {
    uVar8 = *(undefined8 *)(param_2 + 0xf8);
    uVar7 = *(undefined8 *)(param_2 + 0xf0);
    *(undefined8 *)(param_1 + 0x100) = *(undefined8 *)(param_2 + 0x100);
    *(undefined8 *)(param_1 + 0xf8) = uVar8;
    *(undefined8 *)(param_1 + 0xf0) = uVar7;
    cVar3 = param_1[0x11f];
    bVar2 = param_2[0x11f];
  }
  if (cVar3 < '\0') {
    uVar1 = *(ulong *)(param_2 + 0x110);
    plVar5 = (long *)*(long *)(param_2 + 0x108);
    if (-1 < (char)bVar2) {
      uVar1 = (ulong)bVar2;
      plVar5 = (long *)(param_2 + 0x108);
    }
    FUN_100251bd8(param_1 + 0x108,plVar5,uVar1);
  }
  else if ((char)bVar2 < '\0') {
    FUN_100251b18(param_1 + 0x108,*(undefined8 *)(param_2 + 0x108),*(undefined8 *)(param_2 + 0x110))
    ;
  }
  else {
    uVar8 = *(undefined8 *)(param_2 + 0x110);
    uVar7 = *(undefined8 *)(param_2 + 0x108);
    *(undefined8 *)(param_1 + 0x118) = *(undefined8 *)(param_2 + 0x118);
    *(undefined8 *)(param_1 + 0x110) = uVar8;
    *(undefined8 *)(param_1 + 0x108) = uVar7;
  }
  uVar8 = *(undefined8 *)(param_2 + 0x128);
  uVar7 = *(undefined8 *)(param_2 + 0x120);
  *(undefined8 *)(param_1 + 0x12d) = *(undefined8 *)(param_2 + 0x12d);
  *(undefined8 *)(param_1 + 0x128) = uVar8;
  *(undefined8 *)(param_1 + 0x120) = uVar7;
  puVar6 = (undefined8 *)(param_1 + 0x138);
  bVar2 = param_2[0x14f];
  if ((char)param_1[0x14f] < '\0') {
    uVar1 = *(ulong *)(param_2 + 0x140);
    puVar4 = *(undefined8 **)(param_2 + 0x138);
    if (-1 < (char)bVar2) {
      uVar1 = (ulong)bVar2;
      puVar4 = (undefined8 *)(param_2 + 0x138);
    }
    FUN_100251bd8(puVar6,puVar4,uVar1);
    cVar3 = param_1[0x167];
    bVar2 = param_2[0x167];
  }
  else if ((char)bVar2 < '\0') {
    FUN_100251b18(puVar6,*(undefined8 *)(param_2 + 0x138),*(undefined8 *)(param_2 + 0x140));
    cVar3 = param_1[0x167];
    bVar2 = param_2[0x167];
  }
  else {
    uVar8 = *(undefined8 *)(param_2 + 0x140);
    uVar7 = *(undefined8 *)(param_2 + 0x138);
    *(undefined8 *)(param_1 + 0x148) = *(undefined8 *)(param_2 + 0x148);
    *(undefined8 *)(param_1 + 0x140) = uVar8;
    *puVar6 = uVar7;
    cVar3 = param_1[0x167];
    bVar2 = param_2[0x167];
  }
  if (-1 < cVar3) {
    if (-1 < (char)bVar2) {
      uVar8 = *(undefined8 *)(param_2 + 0x158);
      uVar7 = *(undefined8 *)(param_2 + 0x150);
      *(undefined8 *)(param_1 + 0x160) = *(undefined8 *)(param_2 + 0x160);
      *(undefined8 *)(param_1 + 0x158) = uVar8;
      *(undefined8 *)(param_1 + 0x150) = uVar7;
      return param_1;
    }
    FUN_100251b18(param_1 + 0x150,*(undefined8 *)(param_2 + 0x150),*(undefined8 *)(param_2 + 0x158))
    ;
    return param_1;
  }
  uVar1 = *(ulong *)(param_2 + 0x158);
  plVar5 = (long *)*(long *)(param_2 + 0x150);
  if (-1 < (char)bVar2) {
    uVar1 = (ulong)bVar2;
    plVar5 = (long *)(param_2 + 0x150);
  }
  FUN_100251bd8(param_1 + 0x150,plVar5,uVar1);
  return param_1;
}

