
void FUN_10148389c(undefined8 param_1,long *param_2,undefined8 param_3,undefined8 param_4)

{
  int iVar1;
  long lVar2;
  undefined8 uVar3;
  undefined1 auStack_90 [8];
  undefined1 auStack_88 [8];
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  long *local_70;
  long *local_68 [3];
  char local_50;
  char cStack_4f;
  char cStack_4e;
  undefined5 uStack_4d;
  ulong local_48;
  byte local_39;
  char local_36;
  char local_35;
  int local_34;
  
  FUN_101433700(param_2,&local_36,2,&local_34);
  if (local_34 == 2) {
    if ((local_36 == '\x1f') && (local_35 == -0x75)) {
      (**(code **)(*param_2 + 0x78))(&local_50,param_2);
      if (-1 < (char)local_39) {
        local_48 = (ulong)local_39;
      }
      if (local_48 != 0) {
        local_70 = (long *)0x0;
        FUN_10146208c(local_68);
        local_70 = local_68[0];
        (**(code **)(*local_68[0] + 0x98))(local_68[0],&local_50);
        (**(code **)(*local_68[0] + 0x68))(local_68[0],0);
        FUN_10148389c(param_1,local_68[0],param_3,param_4);
        iVar1 = (int)local_68[0][1] + -1;
        *(int *)(local_68[0] + 1) = iVar1;
        if (iVar1 == 0) {
          FUN_10128eea0(local_68[0]);
        }
        if ((char)local_39 < '\0') {
          operator_delete((void *)CONCAT53(uStack_4d,
                                           CONCAT12(cStack_4e,CONCAT11(cStack_4f,local_50))));
          return;
        }
        return;
      }
      goto LAB_101483b94;
    }
    if (local_36 == -0x55 && local_35 == '\x1e') {
      FUN_101483d00(param_1,param_2,param_3);
      return;
    }
    if ((local_36 == '<') && (local_35 == '?')) {
      lVar2 = (**(code **)(*param_2 + 0x38))(param_2);
      (**(code **)(*param_2 + 0x40))(param_2,lVar2 + -2);
      FUN_101484108(param_1,param_2,param_3,param_4);
      return;
    }
    iVar1 = FUN_10143354c(&local_36);
    if (iVar1 != 0) {
      uVar3 = 0;
LAB_101483a64:
      FUN_1014845f0(param_1,param_2,uVar3,param_3);
      return;
    }
    iVar1 = FUN_101433570(&local_36);
    if (iVar1 != 0) {
      uVar3 = 0;
LAB_101483a98:
      FUN_101484724(param_1,param_2,uVar3,param_3);
      return;
    }
    if ((local_36 == '\0') && (local_35 == 'A')) {
      uVar3 = 2;
      goto LAB_101483a64;
    }
    if ((local_36 == 'A') && (local_35 == '\0')) {
      uVar3 = 2;
      goto LAB_101483a98;
    }
    if ((((local_36 != DAT_10581394d) || (local_35 != DAT_10581394e)) ||
        ((FUN_101433700(param_2,&local_50,3,&local_34), local_34 == 3 &&
         (local_35 = cStack_4e, local_36 = cStack_4f, local_50 == DAT_10581394f)))) &&
       ((local_36 == 'A' && (local_35 == 'b')))) {
      FUN_101484858(param_1,param_2,param_3);
      return;
    }
  }
  FUN_101483cec(param_2);
LAB_101483b94:
  uVar3 = ___cxa_allocate_exception(0x30);
  FUN_101447188(local_68,&DAT_106e0cc01,"Can\'t read a gzip\'ed document from a non-file");
  FUN_1011cb734(&local_70);
  FUN_1011cb734(auStack_78);
  FUN_1011cb734(auStack_80);
  FUN_1011cb734(auStack_88);
  FUN_1011cb734(auStack_90);
  FUN_101242ce8(uVar3,local_68,&local_70,auStack_78,auStack_80,auStack_88,auStack_90);
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(uVar3,&PTR_vtable_106661270,FUN_10124335c);
}

