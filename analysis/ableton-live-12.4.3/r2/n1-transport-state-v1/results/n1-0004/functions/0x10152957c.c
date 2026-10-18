
void FUN_10152957c(undefined8 *param_1,long *param_2)

{
  uint uVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  int *piVar5;
  int iVar6;
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  int *local_68;
  int *local_60;
  int *local_58 [3];
  
  uVar3 = FUN_101428734(param_2,0x2e,1,0);
  uVar1 = (uint)uVar3;
  if ((int)uVar1 < 0) {
    piVar5 = (int *)*param_2;
    *param_1 = piVar5;
    if (piVar5 == (int *)0x0) {
      return;
    }
    *piVar5 = *piVar5 + 1;
    return;
  }
  iVar6 = uVar1 + 1;
  do {
    if (*param_2 == 0) {
      if (-2 < iVar6) goto LAB_101529690;
    }
    else if (*(int *)(*param_2 + 4) / 2 + -1 <= iVar6) {
LAB_101529690:
      FUN_10142881c(&local_60,param_2,0,uVar3);
      FUN_101427680(local_58,"[");
      uVar3 = FUN_10142da5c(&local_60,local_58);
      if ((local_58[0] != (int *)0x0) &&
         (iVar6 = *local_58[0], *local_58[0] = iVar6 + -1, iVar6 + -1 == 0)) {
        FUN_101449efc();
      }
      if (*param_2 == 0) {
        iVar6 = -1;
      }
      else {
        iVar6 = *(int *)(*param_2 + 4) / 2 + -1;
      }
      FUN_10142881c(&local_68,param_2,uVar1 + 1,iVar6 + ~uVar1);
      uVar3 = FUN_10142da5c(uVar3,&local_68);
      FUN_101427680(local_58,"]");
      puVar4 = (undefined8 *)FUN_10142da5c(uVar3,local_58);
      if ((local_58[0] != (int *)0x0) &&
         (iVar6 = *local_58[0], *local_58[0] = iVar6 + -1, iVar6 + -1 == 0)) {
        FUN_101449efc();
      }
      piVar5 = (int *)*puVar4;
      *param_1 = piVar5;
      if (piVar5 != (int *)0x0) {
        *piVar5 = *piVar5 + 1;
      }
      if ((local_68 != (int *)0x0) && (iVar6 = *local_68, *local_68 = iVar6 + -1, iVar6 + -1 == 0))
      {
        FUN_101449efc();
      }
      if (local_60 == (int *)0x0) {
        return;
      }
      iVar6 = *local_60;
      *local_60 = iVar6 + -1;
      if (iVar6 + -1 != 0) {
        return;
      }
      FUN_101449efc();
      return;
    }
    iVar2 = FUN_101428974(param_2,iVar6);
    iVar6 = iVar6 + 1;
    if (9 < iVar2 - 0x30U) {
      uVar3 = ___cxa_allocate_exception(0x30);
      FUN_101447188(local_58,&DAT_106e0cc01,"Illegal tag format \'$1\'");
      FUN_1011cb734(&local_60);
      FUN_1011cb734(&local_68);
      FUN_1011cb734(auStack_70);
      FUN_1011cb734(auStack_78);
      FUN_101242ce8(uVar3,local_58,param_2,&local_60,&local_68,auStack_70,auStack_78);
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(uVar3,&PTR_vtable_106661270,FUN_10124335c);
    }
  } while( true );
}

