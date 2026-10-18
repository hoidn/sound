
void FUN_10152ab04(undefined8 *param_1,uint param_2,long param_3,char *param_4,int *param_5)

{
  char *pcVar1;
  char *pcVar2;
  char *pcVar3;
  int iVar4;
  size_t sVar5;
  size_t sVar6;
  ulong uVar7;
  undefined8 *puVar8;
  
  if (0 < (int)param_2) {
    pcVar1 = "";
    pcVar2 = pcVar1;
    if (param_4 != (char *)0x0) {
      pcVar2 = param_4;
    }
    sVar5 = _strlen(pcVar2);
    uVar7 = (ulong)param_2;
    puVar8 = (undefined8 *)(param_3 + 8);
    do {
      pcVar3 = pcVar1;
      if ((char *)puVar8[-1] != (char *)0x0) {
        pcVar3 = (char *)puVar8[-1];
      }
      sVar6 = _strlen(pcVar3);
      if (((int)sVar6 == (int)sVar5) &&
         (iVar4 = _memcmp(pcVar3,pcVar2,(long)(int)sVar5), iVar4 == 0)) {
        if ((char *)*puVar8 != (char *)0x0) {
          pcVar1 = (char *)*puVar8;
        }
        sVar5 = _strlen(pcVar1);
        FUN_101432520(param_1,pcVar1,sVar5);
        return;
      }
      puVar8 = puVar8 + 2;
      uVar7 = uVar7 - 1;
    } while (uVar7 != 0);
  }
  *param_1 = param_5;
  if (param_5 != (int *)0x0) {
    *param_5 = *param_5 + 1;
  }
  return;
}

