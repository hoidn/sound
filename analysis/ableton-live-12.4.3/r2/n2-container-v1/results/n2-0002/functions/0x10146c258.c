
void FUN_10146c258(long *param_1,long *param_2,undefined8 param_3,undefined8 param_4,
                  undefined8 param_5,undefined8 param_6,int *param_7,undefined8 param_8)

{
  int iVar1;
  long lVar2;
  long *plVar3;
  undefined8 uVar4;
  undefined1 auStack_b8 [8];
  undefined1 auStack_b0 [8];
  undefined1 auStack_a8 [8];
  int local_a0 [2];
  long *local_98;
  long *local_90 [3];
  long *local_78;
  int *local_70;
  byte local_61;
  char local_5e;
  char local_5d;
  int local_5c;
  long *local_58;
  
  local_58 = param_2;
  FUN_101433700(param_2,&local_5e,2,&local_5c);
  if (local_5c == 2) {
    if ((local_5e == '\x1f') && (local_5d == -0x75)) {
      (**(code **)(*param_2 + 0x78))(&local_78,param_2);
      if (-1 < (char)local_61) {
        local_70 = (int *)(ulong)local_61;
      }
      if (local_70 == (int *)0x0) goto LAB_10146c5e4;
      local_98 = (long *)0x0;
      FUN_10146208c(local_90);
      local_98 = local_90[0];
      (**(code **)(*local_90[0] + 0x98))(local_90[0],&local_78);
      (**(code **)(*local_90[0] + 0x68))(local_90[0],0);
      FUN_10146c258(param_1,local_90[0],param_3,param_4,param_5,param_6,param_7,param_8);
      iVar1 = (int)local_90[0][1] + -1;
      *(int *)(local_90[0] + 1) = iVar1;
      if (iVar1 == 0) {
        FUN_10128eea0(local_90[0]);
      }
      if ((char)local_61 < '\0') {
        operator_delete(local_78);
      }
    }
    else if ((local_5e == '<') && (local_5d == '?')) {
      if ((int)param_6 != 0) {
        uVar4 = ___cxa_allocate_exception(0x30);
        FUN_101447188(&local_78,&DAT_106e0cc01,"CompoundTool doesn\'t support XML documents");
        FUN_1011cb734(local_90);
        FUN_1011cb734(&local_98);
        FUN_1011cb734(local_a0);
        FUN_1011cb734(auStack_a8);
        FUN_1011cb734(auStack_b0);
        FUN_101242ce8(uVar4,&local_78,local_90,&local_98,local_a0,auStack_a8,auStack_b0);
                    /* WARNING: Subroutine does not return */
        ___cxa_throw(uVar4,&PTR_vtable_106661270,FUN_10124335c);
      }
      lVar2 = (**(code **)(*param_2 + 0x38))(param_2);
      (**(code **)(*param_2 + 0x40))(param_2,lVar2 + -2);
      local_90[0] = (long *)0x0;
      plVar3 = (long *)FUN_1012d9850(0xd8);
      thunk_FUN_1015286a4();
      if (plVar3 != (long *)0x0) {
        *(int *)(plVar3 + 1) = (int)plVar3[1] + 1;
      }
      local_78 = plVar3;
      if ((local_90[0] != (long *)0x0) &&
         (iVar1 = (int)local_90[0][1] + -1, *(int *)(local_90[0] + 1) = iVar1, iVar1 == 0)) {
        FUN_10128eea0();
      }
      local_90[0] = plVar3;
      (**(code **)(*plVar3 + 0x28))(plVar3,local_58);
      FUN_101529908(local_90[0],param_3);
      FUN_101529900(local_90[0],param_4,param_5);
      FUN_1015289c8(&local_78,local_90[0],1,param_7,param_8);
      *param_1 = (long)local_78;
      if (((local_90[0] != (long *)0x0) &&
          ((**(code **)(*local_90[0] + 0x18))(), local_90[0] != (long *)0x0)) &&
         (iVar1 = (int)local_90[0][1] + -1, *(int *)(local_90[0] + 1) = iVar1, iVar1 == 0)) {
        FUN_10128eea0();
      }
    }
    else if ((local_5e == -0x55) && (local_5d == '\x1e')) {
      local_78 = (long *)((ulong)local_78 & 0xffffffff00000000);
      local_90[0] = (long *)0x0;
      FUN_101478258(local_90,&local_58,&local_78);
      FUN_10120d708(&local_78);
      FUN_101485d48(local_90[0],&local_78,local_a0,auStack_a8,param_8);
      *param_7 = local_a0[0];
      if ((int)param_6 != 0) {
        local_a0[0] = 0;
      }
      iVar1 = local_a0[0];
      if (DAT_106f4f600 == DAT_106f4f608) {
        if (0 < local_a0[0]) goto LAB_10146c558;
      }
      else if (*(int *)(DAT_106f4f608 + -0x28) < local_a0[0]) {
LAB_10146c558:
        FUN_1015183fc(local_90[0]);
                    /* WARNING: Subroutine does not return */
        FUN_101488ec0();
      }
      FUN_101470fb4(&local_98,local_90[0],&local_78,param_8);
      if (local_98 == (long *)0x0) {
        *param_1 = 0;
      }
      else {
        FUN_101471148(local_98,iVar1,param_8);
        *param_1 = (long)local_98;
      }
      if ((local_70 != (int *)0x0) && (iVar1 = *local_70, *local_70 = iVar1 + -1, iVar1 + -1 == 0))
      {
        FUN_101449efc();
      }
      if (((local_90[0] != (long *)0x0) &&
          ((**(code **)(*local_90[0] + 0x18))(), local_90[0] != (long *)0x0)) &&
         (iVar1 = (int)local_90[0][1] + -1, *(int *)(local_90[0] + 1) = iVar1, iVar1 == 0)) {
        FUN_10128eea0();
      }
    }
    else {
      *param_1 = 0;
    }
    return;
  }
  FUN_101488e64(param_2,"Unknown Compound Stream Type");
LAB_10146c5e4:
  uVar4 = ___cxa_allocate_exception(0x30);
  FUN_101447188(local_90,&DAT_106e0cc01,"Can\'t read a gzip\'ed document from a non-file");
  FUN_1011cb734(&local_98);
  FUN_1011cb734(local_a0);
  FUN_1011cb734(auStack_a8);
  FUN_1011cb734(auStack_b0);
  FUN_1011cb734(auStack_b8);
  FUN_101242ce8(uVar4,local_90,&local_98,local_a0,auStack_a8,auStack_b0,auStack_b8);
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(uVar4,&PTR_vtable_106661270,FUN_10124335c);
}

