// 0x193e70 _mf0p_FreeHandle | undefined _mf0p_FreeHandle() | state=exported | chunk-00006.jsonl

void _mf0p_FreeHandle(undefined8 *param_1)

{
  void *pvVar1;
  undefined8 *puVar2;
  int *piVar3;
  
  if (param_1 == (undefined8 *)0x0) {
    return;
  }
  pvVar1 = (void *)param_1[3];
  if (*(int *)((long)pvVar1 + 0xbc) == 0) {
    FUN_00006ff0(param_1[1]);
    FUN_00029ce0(param_1[3]);
    _fwrite("\r   Process to cancel set ...   \n",1,0x21,*(FILE **)PTR____stderrp_0046e300);
    FUN_00006fd0(param_1[1]);
    pvVar1 = (void *)param_1[3];
    do {
    } while (*(int *)((long)pvVar1 + 0xbc) != 0);
  }
  if (pvVar1 != (void *)0x0) {
    FUN_0002e8d0(pvVar1);
    operator_delete(pvVar1);
  }
  pvVar1 = (void *)param_1[1];
  if (pvVar1 != (void *)0x0) {
    FUN_00006eb0(pvVar1);
    operator_delete(pvVar1);
  }
  pvVar1 = (void *)*param_1;
  if (pvVar1 != (void *)0x0) {
    FUN_00006d70(pvVar1);
    operator_delete(pvVar1);
  }
  pvVar1 = (void *)param_1[2];
  if (pvVar1 != (void *)0x0) {
    piVar3 = *(int **)((long)pvVar1 + 0x130);
    if ((piVar3 != (int *)0x0) && (*piVar3 = *piVar3 + -1, *piVar3 < 1)) {
      if (*(char *)((long)pvVar1 + 0x138) != '\0') {
        puVar2 = *(undefined8 **)((long)pvVar1 + 0x128);
        if ((void *)*puVar2 != (void *)0x0) {
          _free((void *)*puVar2);
          puVar2 = *(undefined8 **)((long)pvVar1 + 0x128);
        }
        _free(puVar2);
        piVar3 = *(int **)((long)pvVar1 + 0x130);
      }
      _free(piVar3);
    }
    piVar3 = *(int **)((long)pvVar1 + 0xe8);
    if ((piVar3 != (int *)0x0) && (*piVar3 = *piVar3 + -1, *piVar3 < 1)) {
      if (*(char *)((long)pvVar1 + 0xf0) != '\0') {
        puVar2 = *(undefined8 **)((long)pvVar1 + 0xe0);
        if ((void *)*puVar2 != (void *)0x0) {
          _free((void *)*puVar2);
          puVar2 = *(undefined8 **)((long)pvVar1 + 0xe0);
        }
        _free(puVar2);
        piVar3 = *(int **)((long)pvVar1 + 0xe8);
      }
      _free(piVar3);
    }
    piVar3 = *(int **)((long)pvVar1 + 0x50);
    if ((piVar3 != (int *)0x0) && (*piVar3 = *piVar3 + -1, *piVar3 < 1)) {
      if (*(char *)((long)pvVar1 + 0x58) != '\0') {
        puVar2 = *(undefined8 **)((long)pvVar1 + 0x48);
        if ((void *)*puVar2 != (void *)0x0) {
          _free((void *)*puVar2);
          puVar2 = *(undefined8 **)((long)pvVar1 + 0x48);
        }
        _free(puVar2);
        piVar3 = *(int **)((long)pvVar1 + 0x50);
      }
      _free(piVar3);
    }
    operator_delete(pvVar1);
  }
  operator_delete(param_1);
  return;
}

