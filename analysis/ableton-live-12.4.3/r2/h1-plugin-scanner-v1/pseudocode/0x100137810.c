
void FUN_100137810(long *param_1,void *param_2,ulong param_3,char *param_4)

{
  ulong uVar1;
  char cVar2;
  int iVar3;
  size_t sVar4;
  void *pvVar5;
  long lVar6;
  ulong uVar7;
  ulong uVar8;
  
  sVar4 = _strlen(param_4);
  if (sVar4 == 0) {
    uVar7 = 0;
LAB_100137864:
    uVar1 = uVar7 + sVar4;
    uVar8 = param_3 - uVar1;
    if (param_3 < uVar1) {
                    /* WARNING: Subroutine does not return */
      FUN_100137d38("string_view::substr");
    }
    if (uVar7 <= param_3) {
      param_3 = uVar7;
    }
    *param_1 = (long)param_2;
    param_1[1] = param_3;
    param_1[2] = (long)param_2 + uVar1;
    lVar6 = 0x18;
  }
  else {
    if ((long)sVar4 <= (long)param_3) {
      cVar2 = *param_4;
      pvVar5 = param_2;
      uVar7 = param_3;
      do {
        if ((0xfffffffffffffffe < uVar7 - sVar4) ||
           (pvVar5 = _memchr(pvVar5,(int)cVar2,(uVar7 - sVar4) + 1), pvVar5 == (void *)0x0)) break;
        iVar3 = _memcmp(pvVar5,param_4,sVar4);
        if (iVar3 == 0) {
          if ((pvVar5 != (void *)((long)param_2 + param_3)) &&
             (uVar7 = (long)pvVar5 - (long)param_2, uVar7 != 0xffffffffffffffff))
          goto LAB_100137864;
          break;
        }
        pvVar5 = (void *)((long)pvVar5 + 1);
        uVar7 = (long)((long)param_2 + param_3) - (long)pvVar5;
      } while ((long)sVar4 <= (long)uVar7);
    }
    param_1[2] = 0;
    param_1[3] = 0;
    lVar6 = 8;
    *param_1 = (long)param_2;
    uVar8 = param_3;
  }
  *(ulong *)((long)param_1 + lVar6) = uVar8;
  return;
}

