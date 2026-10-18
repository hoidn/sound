// 0x1025e6af0 FUN_1025e6af0 exported-with-warnings  sig: undefined FUN_1025e6af0()

void FUN_1025e6af0(int *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  long *plVar1;
  undefined8 uVar2;
  undefined8 *puVar3;
  long lVar4;
  undefined8 *puVar5;
  undefined8 *puVar6;
  int iVar7;
  int iVar8;
  undefined8 local_60 [3];
  undefined8 local_48;
  
  puVar3 = *(undefined8 **)(param_1 + 6);
  puVar5 = puVar3;
  do {
    local_48 = param_4;
    if (puVar5 == (undefined8 *)0x0) {
      uVar2 = ___cxa_allocate_exception(0x10);
      FUN_1002aa2a4(local_60,"Unknown from state");
      FUN_1025e6714(uVar2,local_60,param_2);
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(uVar2,&PTR_vtable_1067e3928,std::runtime_error::~runtime_error);
    }
    iVar7 = (int)param_2;
    if (*(int *)(puVar5 + 4) <= iVar7) {
      puVar6 = puVar3;
      if (iVar7 <= *(int *)(puVar5 + 4)) break;
      puVar5 = puVar5 + 1;
    }
    puVar5 = (undefined8 *)*puVar5;
  } while( true );
LAB_1025e6b58:
  iVar8 = (int)param_3;
  if (*(int *)(puVar6 + 4) <= iVar8) {
    if (iVar8 <= *(int *)(puVar6 + 4)) goto LAB_1025e6b78;
    puVar6 = puVar6 + 1;
  }
  puVar6 = (undefined8 *)*puVar6;
  if (puVar6 == (undefined8 *)0x0) {
    uVar2 = ___cxa_allocate_exception(0x10);
    FUN_1002aa2a4(local_60,"Unknown to state");
    FUN_1025e6714(uVar2,local_60,param_3);
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar2,&PTR_vtable_1067e3928,std::runtime_error::~runtime_error);
  }
  goto LAB_1025e6b58;
LAB_1025e6b78:
  puVar5 = puVar3;
  if (iVar7 < *(int *)(puVar5 + 4)) {
    puVar3 = (undefined8 *)*puVar5;
    puVar6 = puVar5;
    if ((undefined8 *)*puVar5 == (undefined8 *)0x0) goto LAB_1025e6ba0;
    goto LAB_1025e6b78;
  }
  if (iVar7 <= *(int *)(puVar5 + 4)) {
    plVar1 = (long *)FUN_1025e6dc8(puVar5 + 5,local_60,&local_48);
    lVar4 = *plVar1;
    puVar3 = puVar5;
    goto joined_r0x0001025e6c4c;
  }
  puVar3 = (undefined8 *)puVar5[1];
  if ((undefined8 *)puVar5[1] == (undefined8 *)0x0) {
    puVar6 = puVar5 + 1;
LAB_1025e6ba0:
    puVar3 = operator_new(0x40);
    *(int *)(puVar3 + 4) = iVar7;
    puVar3[7] = 0;
    puVar3[6] = 0;
    puVar3[5] = puVar3 + 6;
    *puVar3 = 0;
    puVar3[1] = 0;
    puVar3[2] = puVar5;
    *puVar6 = puVar3;
    puVar5 = puVar3;
    if (**(long **)(param_1 + 4) != 0) {
      *(long *)(param_1 + 4) = **(long **)(param_1 + 4);
      puVar5 = (undefined8 *)*puVar6;
    }
    FUN_100255d54(*(undefined8 *)(param_1 + 6),puVar5);
    *(long *)(param_1 + 8) = *(long *)(param_1 + 8) + 1;
    plVar1 = (long *)FUN_1025e6dc8(puVar3 + 5,local_60,&local_48);
    lVar4 = *plVar1;
joined_r0x0001025e6c4c:
    if (lVar4 == 0) {
      puVar5 = operator_new(0x28);
      *(undefined8 *)((long)puVar5 + 0x1c) = local_48;
      *(int *)((long)puVar5 + 0x24) = iVar8;
      *puVar5 = 0;
      puVar5[1] = 0;
      puVar5[2] = local_60[0];
      *plVar1 = (long)puVar5;
      if (*(long *)puVar3[5] != 0) {
        puVar3[5] = *(long *)puVar3[5];
        puVar5 = (undefined8 *)*plVar1;
      }
      FUN_100255d54(puVar3[6],puVar5);
      puVar3[7] = puVar3[7] + 1;
      iVar8 = *param_1;
    }
    else {
      iVar8 = *param_1;
    }
    if (iVar8 != iVar7) {
      return;
    }
    FUN_1025e4da0(param_1,param_2);
    return;
  }
  goto LAB_1025e6b78;
}


