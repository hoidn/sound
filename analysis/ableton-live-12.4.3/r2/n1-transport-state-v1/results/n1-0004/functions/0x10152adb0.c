
void FUN_10152adb0(long param_1,long *param_2,undefined8 param_3,undefined8 param_4)

{
  char cVar1;
  undefined4 uVar2;
  int iVar3;
  long *plVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  long lVar7;
  long lVar8;
  undefined4 *puVar9;
  ulong uVar10;
  int *piVar11;
  int *piVar12;
  undefined8 uVar13;
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  undefined1 auStack_68 [8];
  undefined1 auStack_60 [8];
  undefined4 local_58 [2];
  int *local_50;
  
  plVar4 = (long *)FUN_1014810cc(param_3);
  piVar12 = (int *)*plVar4;
  if (piVar12 != (int *)0x0) {
    *piVar12 = *piVar12 + 1;
  }
  piVar11 = (int *)param_2[1];
  if ((piVar11 == (int *)0x0) || (iVar3 = *piVar11, *piVar11 = iVar3 + -1, iVar3 + -1 != 0)) {
    param_2[1] = (long)piVar12;
    uVar5 = FUN_1014810d8(param_3);
    uVar6 = FUN_10120e310();
    iVar3 = (int)uVar6;
  }
  else {
    FUN_101449efc(piVar11);
    param_2[1] = *plVar4;
    uVar5 = FUN_1014810d8(param_3);
    uVar6 = FUN_10120e310();
    iVar3 = (int)uVar6;
  }
  if (iVar3 != 0) {
    *(undefined4 *)(param_2 + 3) = 0xfffffffc;
    FUN_10152b45c(uVar6,param_2,uVar5,param_4);
    return;
  }
  uVar2 = FUN_1014810e8(param_3);
  *(undefined4 *)(param_2 + 3) = uVar2;
  iVar3 = FUN_1014810e8(param_3);
  if (iVar3 < -1) {
    if (iVar3 == -3) {
      iVar3 = FUN_101471d8c();
      if (iVar3 == 0) {
        puVar9 = (undefined4 *)FUN_1014810e0(param_3);
        local_58[0] = *puVar9;
        local_50 = *(int **)(puVar9 + 2);
        if (local_50 != (int *)0x0) {
          *local_50 = *local_50 + 1;
        }
        uVar10 = FUN_101471738(local_58);
        if ((uVar10 & 1) == 0) {
          lVar7 = FUN_10146cf50(0x58);
          thunk_FUN_101474784(lVar7,uVar5,local_58);
          if (lVar7 != 0) {
            *(int *)(lVar7 + 8) = *(int *)(lVar7 + 8) + 1;
          }
          lVar8 = *param_2;
          if ((lVar8 != 0) &&
             (iVar3 = *(int *)(lVar8 + 8) + -1, *(int *)(lVar8 + 8) = iVar3, iVar3 == 0)) {
            FUN_10128eea0();
          }
        }
        else {
          lVar7 = FUN_10146cf50(0x40);
          FUN_10147407c(lVar7,uVar5);
          if (lVar7 != 0) {
            *(int *)(lVar7 + 8) = *(int *)(lVar7 + 8) + 1;
          }
          lVar8 = *param_2;
          if ((lVar8 != 0) &&
             (iVar3 = *(int *)(lVar8 + 8) + -1, *(int *)(lVar8 + 8) = iVar3, iVar3 == 0)) {
            FUN_10128eea0();
          }
        }
        *param_2 = lVar7;
        if ((local_50 != (int *)0x0) && (iVar3 = *local_50, *local_50 = iVar3 + -1, iVar3 + -1 == 0)
           ) {
          FUN_101449efc();
        }
      }
      else {
        *(undefined1 *)((long)param_2 + 0x22) = 1;
      }
      return;
    }
    if (iVar3 == -2) {
      uVar5 = ___cxa_allocate_exception(0x30);
      FUN_101447188(local_58,&DAT_106e0cc01,"ByteBags are not supported in XML streams");
      FUN_1011cb734(auStack_60);
      FUN_1011cb734(auStack_68);
      FUN_1011cb734(auStack_70);
      FUN_1011cb734(auStack_78);
      FUN_1011cb734(auStack_80);
      FUN_101242ce8(uVar5,local_58,auStack_60,auStack_68,auStack_70,auStack_78,auStack_80);
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(uVar5,&PTR_vtable_106661270,FUN_10124335c);
    }
  }
  else {
    if (iVar3 == -1) {
      lVar7 = FUN_10146cf50(0x48);
      FUN_101473af8(lVar7,uVar5);
      if (lVar7 != 0) {
        *(int *)(lVar7 + 8) = *(int *)(lVar7 + 8) + 1;
      }
      lVar8 = *param_2;
      if ((lVar8 != 0) &&
         (iVar3 = *(int *)(lVar8 + 8) + -1, *(int *)(lVar8 + 8) = iVar3, iVar3 == 0)) {
        FUN_10128eea0();
      }
      *param_2 = lVar7;
      return;
    }
    if (iVar3 == 0) {
      lVar7 = FUN_10146cf50(0x40);
      FUN_101471f38(lVar7,uVar5);
      if (lVar7 != 0) {
        *(int *)(lVar7 + 8) = *(int *)(lVar7 + 8) + 1;
      }
      lVar8 = *param_2;
      if ((lVar8 == 0) ||
         (iVar3 = *(int *)(lVar8 + 8) + -1, *(int *)(lVar8 + 8) = iVar3, iVar3 != 0)) {
        *param_2 = lVar7;
        cVar1 = *(char *)(param_1 + 200);
      }
      else {
        FUN_10128eea0();
        *param_2 = lVar7;
        cVar1 = *(char *)(param_1 + 200);
      }
      if (cVar1 == '\x01') {
        uVar13 = *(undefined8 *)(param_1 + 0xb0);
        uVar6 = FUN_10120e26c(uVar5);
        lVar7 = FUN_10151477c(uVar13,uVar6);
      }
      else {
        uVar6 = FUN_10120e26c(uVar5);
        lVar7 = FUN_101485c8c(uVar6,0,0);
      }
      param_2[2] = lVar7;
      if (lVar7 == 0) {
        uVar6 = ___cxa_allocate_exception(0x30);
        FUN_101447188(local_58,&DAT_106e0cc01,"Unknown class \'$1\' encountered");
        uVar5 = FUN_10120e26c(uVar5);
        FUN_1011cb734(auStack_60);
        FUN_1011cb734(auStack_68);
        FUN_1011cb734(auStack_70);
        FUN_1011cb734(auStack_78);
        FUN_101242ce8(uVar6,local_58,uVar5,auStack_60,auStack_68,auStack_70,auStack_78);
                    /* WARNING: Subroutine does not return */
        ___cxa_throw(uVar6,&PTR_vtable_106661270,FUN_10124335c);
      }
      FUN_10152b77c(param_1,param_2,param_4,0);
      return;
    }
  }
  uVar5 = ___cxa_allocate_exception(0x30);
  FUN_101447188(local_58,&DAT_106e0cc01,"The document appears to be corrupt.");
  FUN_1011cb734(auStack_60);
  FUN_1011cb734(auStack_68);
  FUN_1011cb734(auStack_70);
  FUN_1011cb734(auStack_78);
  FUN_1011cb734(auStack_80);
  FUN_101242ce8(uVar5,local_58,auStack_60,auStack_68,auStack_70,auStack_78,auStack_80);
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(uVar5,&PTR_vtable_106661270,FUN_10124335c);
}

