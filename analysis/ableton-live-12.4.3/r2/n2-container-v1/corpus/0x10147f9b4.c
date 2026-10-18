
void FUN_10147f9b4(void)

{
  long *plVar1;
  long *plVar2;
  undefined4 *puVar3;
  long *plVar4;
  int iVar5;
  void *pvVar6;
  undefined4 *puVar7;
  long lVar8;
  int *piVar9;
  void *local_50;
  undefined4 *local_48;
  undefined4 *local_40;
  undefined4 *local_38;
  
  local_48 = (undefined4 *)0x0;
  local_40 = (undefined4 *)0x0;
  local_38 = (undefined4 *)0x0;
  plVar1 = DAT_106f4f768;
  plVar2 = DAT_106f4f770;
  puVar3 = local_40;
  if (((DAT_106f4f658 & 1) == 0) &&
     (iVar5 = ___cxa_guard_acquire(&DAT_106f4f658), plVar1 = DAT_106f4f768, plVar2 = DAT_106f4f770,
     puVar3 = local_40, iVar5 != 0)) {
    DAT_106f4f768 = (long *)0x0;
    DAT_106f4f770 = (long *)0x0;
    DAT_106f4f778 = (long *)0x0;
    DAT_106f4f768 = operator_new(0x8000);
    DAT_106f4f778 = DAT_106f4f768 + 0x1000;
    DAT_106f4f770 = DAT_106f4f768;
    ___cxa_atexit(FUN_10147e790,&DAT_106f4f768,0x100000000);
    ___cxa_guard_release(&DAT_106f4f658);
    plVar1 = DAT_106f4f768;
    plVar2 = DAT_106f4f770;
    puVar3 = local_40;
  }
  for (; plVar4 = DAT_106f4f770, local_40 = puVar3, plVar1 != DAT_106f4f770; plVar1 = plVar1 + 1) {
    lVar8 = *plVar1;
    puVar7 = *(undefined4 **)(lVar8 + 0xb0);
    DAT_106f4f770 = plVar2;
    if (((puVar7[6] == 0) && (*(char *)(lVar8 + 0xbe) == '\x01')) &&
       ((*(byte *)(lVar8 + 0xbd) & 1) == 0)) {
      if (puVar3 < local_38) {
        *puVar3 = *puVar7;
        piVar9 = *(int **)(puVar7 + 2);
        *(int **)(puVar3 + 2) = piVar9;
        if (piVar9 != (int *)0x0) {
          *piVar9 = *piVar9 + 1;
        }
        piVar9 = *(int **)(puVar7 + 4);
        *(int **)(puVar3 + 4) = piVar9;
        if (piVar9 != (int *)0x0) {
          *piVar9 = *piVar9 + 1;
        }
        *(undefined8 *)(puVar3 + 8) = 0;
        puVar3[6] = 0;
        *(undefined8 *)(puVar3 + 10) = 0;
        *(undefined8 *)(puVar3 + 0xc) = 0;
        FUN_101489f3c(puVar3 + 8,*(long *)(puVar7 + 8),*(long *)(puVar7 + 10),
                      (*(long *)(puVar7 + 10) - *(long *)(puVar7 + 8) >> 3) * 0x6db6db6db6db6db7);
        local_40 = puVar3 + 0xe;
      }
      else {
        local_40 = (undefined4 *)FUN_101489d0c(&local_48);
      }
    }
    plVar2 = DAT_106f4f770;
    puVar3 = local_40;
    DAT_106f4f770 = plVar4;
  }
  lVar8 = 0;
  if (puVar3 != local_48) {
    lVar8 = LZCOUNT(((long)puVar3 - (long)local_48 >> 3) * 0x6db6db6db6db6db7) * -2 + 0x7e;
  }
  DAT_106f4f770 = plVar2;
  FUN_10148a1d0(local_48,puVar3,lVar8,1);
  pvVar6 = operator_new(0x70);
  FUN_1015146c0(pvVar6,0x80000000,0x80000000);
  local_50 = pvVar6;
  FUN_1015146f0(pvVar6,&local_48);
  FUN_101515628(&local_50);
  pvVar6 = local_50;
  local_50 = (void *)0x0;
  if (pvVar6 != (void *)0x0) {
    pvVar6 = (void *)FUN_10148dbd4();
    operator_delete(pvVar6);
  }
  puVar7 = local_48;
  puVar3 = local_40;
  if (local_48 != (undefined4 *)0x0) {
    while (puVar3 != puVar7) {
      FUN_10148a13c(puVar3 + -0xe);
      puVar3 = puVar3 + -0xe;
    }
    local_40 = puVar7;
    operator_delete(local_48);
  }
  return;
}

