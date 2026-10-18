
void FUN_10152a570(long param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  ulong uVar1;
  int iVar2;
  int iVar3;
  long lVar4;
  undefined8 uVar5;
  long lVar6;
  long *plVar7;
  ulong uVar8;
  long local_88;
  int *local_80;
  long local_78;
  undefined7 uStack_70;
  undefined1 uStack_69;
  undefined2 uStack_68;
  undefined1 uStack_66;
  undefined1 auStack_60 [8];
  undefined1 auStack_58 [8];
  undefined1 auStack_50 [8];
  long local_48;
  
  if (*(char *)(param_1 + 200) == '\x01') {
    lVar4 = FUN_10151479c(*(undefined8 *)(param_1 + 0xb0),param_2);
  }
  else {
    lVar4 = FUN_101485c8c(param_2,0,0);
  }
  if (lVar4 != 0) {
    uVar5 = FUN_1014812d8(lVar4);
    lVar6 = FUN_10146cf50(0x40);
    FUN_101471f38(lVar6,uVar5);
    if (lVar6 != 0) {
      *(int *)(lVar6 + 8) = *(int *)(lVar6 + 8) + 2;
    }
    local_88 = lVar6;
    local_48 = lVar6;
    FUN_1011cb734(&local_80);
    uStack_70 = 0;
    uStack_69 = 0x80;
    uStack_68 = 0;
    uStack_66 = 0;
    local_78 = lVar4;
    FUN_10152b77c(param_1,&local_88,param_3,param_4);
    lVar4 = *(long *)(param_1 + 0x70);
    uVar1 = 0;
    if (*(long *)(param_1 + 0x78) != lVar4) {
      uVar1 = (*(long *)(param_1 + 0x78) - lVar4 >> 3) * 0x66 - 1;
    }
    uVar8 = *(long *)(param_1 + 0x90) + *(long *)(param_1 + 0x88);
    if (uVar1 == uVar8) {
      FUN_101532f08(param_1 + 0x68);
      lVar4 = *(long *)(param_1 + 0x70);
      uVar8 = *(long *)(param_1 + 0x90) + *(long *)(param_1 + 0x88);
    }
    plVar7 = (long *)(*(long *)(lVar4 + (uVar8 / 0x66) * 8) + (uVar8 % 0x66) * 0x28);
    *plVar7 = local_88;
    if (local_88 != 0) {
      *(int *)(local_88 + 8) = *(int *)(local_88 + 8) + 1;
    }
    plVar7[1] = (long)local_80;
    if (local_80 != (int *)0x0) {
      *local_80 = *local_80 + 1;
    }
    *(uint *)((long)plVar7 + 0x1f) = CONCAT13(uStack_66,CONCAT21(uStack_68,uStack_69));
    plVar7[3] = CONCAT17(uStack_69,uStack_70);
    plVar7[2] = local_78;
    *(long *)(param_1 + 0x90) = *(long *)(param_1 + 0x90) + 1;
    if (local_80 != (int *)0x0) {
      iVar2 = *local_80;
      *local_80 = iVar2 + -1;
      if (iVar2 + -1 == 0) {
        FUN_101449efc();
      }
    }
    if (local_88 != 0) {
      iVar2 = *(int *)(local_88 + 8) + -1;
      *(int *)(local_88 + 8) = iVar2;
      if (iVar2 == 0) {
        FUN_10128eea0();
      }
    }
    if (lVar6 != 0) {
      iVar2 = *(int *)(lVar6 + 8) + -1;
      *(int *)(lVar6 + 8) = iVar2;
      if (iVar2 == 0) {
        FUN_10128eea0(lVar6);
      }
    }
    return;
  }
  if ((*(char *)(param_1 + 200) == '\x01') &&
     (iVar2 = *(int *)(param_1 + 0x40), iVar3 = FUN_1015147cc(*(undefined8 *)(param_1 + 0xb0)),
     iVar3 < iVar2)) {
    *(undefined1 *)(param_1 + 0x60) = 1;
  }
  uVar5 = ___cxa_allocate_exception(0x30);
  FUN_101447188(&local_88,&DAT_106e0cc01,"Unknown class \'$1\' encountered");
  FUN_1011cb734(&local_48);
  FUN_1011cb734(auStack_50);
  FUN_1011cb734(auStack_58);
  FUN_1011cb734(auStack_60);
  FUN_101242ce8(uVar5,&local_88,param_2,&local_48,auStack_50,auStack_58,auStack_60);
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(uVar5,&PTR_vtable_106661270,FUN_10124335c);
}

