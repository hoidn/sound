
void FUN_101471148(undefined8 param_1,int param_2,undefined8 param_3)

{
  int *piVar1;
  long lVar2;
  long lVar3;
  undefined8 uVar4;
  int *piVar5;
  int iVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  long lVar9;
  ulong uVar10;
  long *plVar11;
  int iVar12;
  
  uVar4 = DAT_106f4f5e0;
  if (DAT_106f4f600 == DAT_106f4f608) {
    iVar12 = 0;
    if (param_2 == 0) {
      return;
    }
  }
  else {
    iVar12 = DAT_106f4f608[-10];
    if (iVar12 == param_2) {
      return;
    }
  }
  DAT_106f4f5e0 = param_1;
  FUN_101478be8(&DAT_106f4f618,DAT_106f4f620);
  piVar5 = DAT_106f4f608;
  DAT_106f4f618 = &DAT_106f4f620;
  DAT_106f4f628 = 0;
  DAT_106f4f620 = (long *)0x0;
  piVar1 = DAT_106f4f600;
  do {
    if ((piVar1 == piVar5) || (iVar12 < *piVar1)) {
      DAT_106f4f5e0 = uVar4;
      return;
    }
    if (param_2 < *piVar1) {
      lVar3 = *(long *)(piVar1 + 4);
      for (lVar2 = *(long *)(piVar1 + 2); lVar2 != lVar3; lVar2 = lVar2 + 0x10) {
        uVar7 = FUN_101522fb0(param_3);
        uVar8 = FUN_10120e26c(lVar2);
        lVar9 = FUN_101479bb8(uVar7,uVar8);
        plVar11 = DAT_106f4f620;
        if (lVar9 != 0) {
LAB_1014711f4:
          FUN_10146baa0(piVar1,param_1,param_1);
          break;
        }
        for (; plVar11 != (long *)0x0; plVar11 = (long *)*plVar11) {
          uVar10 = FUN_10120e19c(lVar2,plVar11 + 4);
          if ((uVar10 & 1) == 0) {
            iVar6 = FUN_10120e19c(plVar11 + 4,lVar2);
            if (iVar6 == 0) goto LAB_1014711f4;
            plVar11 = plVar11 + 1;
          }
        }
      }
    }
    piVar1 = piVar1 + 10;
  } while( true );
}

