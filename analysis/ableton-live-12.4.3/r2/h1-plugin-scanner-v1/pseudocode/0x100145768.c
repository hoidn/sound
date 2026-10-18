
undefined8 FUN_100145768(undefined8 *param_1)

{
  ulong uVar1;
  long *plVar2;
  long *plVar3;
  byte bVar4;
  
  plVar3 = (long *)*param_1;
  do {
    if (plVar3 == (long *)param_1[1]) {
      return 0;
    }
    bVar4 = *(byte *)((long)plVar3 + 0x17);
    uVar1 = plVar3[1];
    if (-1 < (char)bVar4) {
      uVar1 = (ulong)bVar4;
    }
    if (uVar1 == 10) {
      plVar2 = (long *)*plVar3;
      if (-1 < (char)bVar4) {
        plVar2 = plVar3;
      }
      if (*plVar2 == 0x656d757274736e49 && *(short *)(plVar2 + 1) == 0x746e) {
        return 1;
      }
    }
    plVar3 = plVar3 + 3;
  } while( true );
}

