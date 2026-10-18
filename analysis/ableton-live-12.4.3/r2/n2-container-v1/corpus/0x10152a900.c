
ulong FUN_10152a900(uint param_1,long param_2,char *param_3)

{
  char *pcVar1;
  char *pcVar2;
  char *pcVar3;
  int iVar4;
  size_t sVar5;
  size_t sVar6;
  undefined8 uVar7;
  ulong uVar8;
  undefined8 *puVar9;
  undefined1 auStack_90 [8];
  undefined1 auStack_88 [8];
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  undefined1 auStack_68 [24];
  
  if (0 < (int)param_1) {
    pcVar1 = "";
    pcVar2 = pcVar1;
    if (param_3 != (char *)0x0) {
      pcVar2 = param_3;
    }
    sVar5 = _strlen(pcVar2);
    uVar8 = (ulong)param_1;
    puVar9 = (undefined8 *)(param_2 + 8);
    do {
      pcVar3 = pcVar1;
      if ((char *)puVar9[-1] != (char *)0x0) {
        pcVar3 = (char *)puVar9[-1];
      }
      sVar6 = _strlen(pcVar3);
      if (((int)sVar6 == (int)sVar5) &&
         (iVar4 = _memcmp(pcVar3,pcVar2,(long)(int)sVar5), iVar4 == 0)) {
        if ((char *)*puVar9 != (char *)0x0) {
          pcVar1 = (char *)*puVar9;
        }
        sVar5 = _strlen(pcVar1);
        uVar8 = FUN_1002fd908(pcVar1,(long)(int)sVar5);
        if ((uVar8 >> 0x20 & 1) != 0) {
          return uVar8;
        }
        uVar7 = ___cxa_allocate_exception(0x30);
        FUN_101447188(auStack_68,&DAT_106e0cc01,"Illegal value for int attribute: $1");
        FUN_101432520(auStack_70,pcVar1,sVar5);
        FUN_1011cb734(auStack_78);
        FUN_1011cb734(auStack_80);
        FUN_1011cb734(auStack_88);
        FUN_1011cb734(auStack_90);
        FUN_101242ce8(uVar7,auStack_68,auStack_70,auStack_78,auStack_80,auStack_88,auStack_90);
                    /* WARNING: Subroutine does not return */
        ___cxa_throw(uVar7,&PTR_vtable_106661270,FUN_10124335c);
      }
      puVar9 = puVar9 + 2;
      uVar8 = uVar8 - 1;
    } while (uVar8 != 0);
  }
  return 0;
}

