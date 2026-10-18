
void FUN_1015289c8(long *param_1,long *param_2,int param_3,undefined4 *param_4,long param_5)

{
  code *pcVar1;
  int iVar2;
  undefined8 uVar3;
  long lVar4;
  long lVar5;
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  undefined1 auStack_68 [8];
  undefined1 auStack_60 [8];
  int local_58;
  undefined4 uStack_54;
  int local_4c;
  int local_48;
  int local_44;
  
  lVar5 = param_2[0x15];
  param_2[0x15] = param_5;
  (**(code **)(*param_2 + 0x40))();
  if ((*(byte *)((long)param_2 + 0x29) & 1) == 0) {
    lVar4 = param_2[7];
    if (((lVar4 == 0) || ((*(uint *)(lVar4 + 4) & 0xfffffffe) != 2)) &&
       (iVar2 = FUN_101514e30(param_2 + 7,&local_44,&local_48,&local_4c), iVar2 != 0)) {
      if ((int)param_2[0xb] < local_44) {
LAB_101528b1c:
        FUN_101528e2c(&local_58,param_2);
        if ((CONCAT44(uStack_54,local_58) != 0) &&
           ((*(uint *)(CONCAT44(uStack_54,local_58) + 4) & 0xfffffffe) == 2)) {
          uVar3 = FUN_1011d9c38(&local_58,local_44);
          uVar3 = FUN_101528fa4(uVar3,0x2e);
          FUN_1011d9c38(uVar3,local_48);
        }
        uVar3 = ___cxa_allocate_exception(0x30);
        FUN_1014335f8(auStack_60,param_2[3]);
        FUN_1011cb734(auStack_68);
        FUN_1011cb734(auStack_70);
        FUN_1011cb734(auStack_78);
        FUN_101242ce8(uVar3,&DAT_106f50538,auStack_60,&local_58,auStack_68,auStack_70,auStack_78);
                    /* WARNING: Subroutine does not return */
        ___cxa_throw(uVar3,&PTR_vtable_106661270,FUN_10124335c);
      }
      if ((local_44 == (int)param_2[0xb]) && (*(int *)((long)param_2 + 0x5c) < local_48))
      goto LAB_101528b1c;
      iVar2 = FUN_101514f7c(local_44,local_48,&local_58);
      if ((iVar2 != 0) && (local_58 < local_4c)) {
        FUN_101528c84(param_2);
        goto LAB_101528bdc;
      }
    }
    if ((char)param_2[0xc] != '\x01') {
      if ((char)param_2[5] == '\x01') {
                    /* WARNING: Subroutine does not return */
        FUN_10148229c(param_2[3],param_2 + 6);
      }
      lVar4 = param_2[0x14];
      if (lVar4 != 0) {
        if ((char)param_2[0x19] == '\x01') {
          uVar3 = FUN_1015147bc(param_2[0x16]);
          if (param_3 != 0) {
            FUN_101471148(param_2[0x14],uVar3,param_2[0x15]);
          }
          *param_4 = (int)uVar3;
          lVar4 = param_2[0x14];
        }
        *param_1 = lVar4;
        param_2[0x14] = 0;
        param_2[0x15] = lVar5;
        return;
      }
      FUN_101488e64(param_2[3],"No document found");
      goto LAB_101528bdc;
    }
  }
  FUN_101528c84(param_2);
LAB_101528bdc:
                    /* WARNING: Does not return */
  pcVar1 = (code *)SoftwareBreakpoint(1,0x101528be0);
  (*pcVar1)();
}

