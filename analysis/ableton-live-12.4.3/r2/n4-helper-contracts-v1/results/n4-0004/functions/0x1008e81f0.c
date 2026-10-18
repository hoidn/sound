
void FUN_1008e81f0(long param_1,int param_2)

{
  int iVar1;
  long lVar2;
  long lVar3;
  undefined8 *puVar4;
  undefined8 uVar5;
  undefined8 *local_58;
  undefined8 *puStack_50;
  long local_48;
  undefined4 local_40;
  int *local_38;
  
  FUN_10185128c(*(undefined8 *)(param_1 + 0x18),*(undefined8 *)(param_1 + 0x30));
  if (param_2 < 4) {
    if (param_2 == 1) {
      FUN_1011c4144();
      FUN_101427680(&local_38);
      FUN_1008e878c(&local_48,&local_38,param_1 + 0x38);
      if ((local_38 != (int *)0x0) && (iVar1 = *local_38, *local_38 = iVar1 + -1, iVar1 + -1 == 0))
      {
        FUN_101449efc();
      }
    }
    else if (param_2 == 2) {
      FUN_1008e9570(&local_48,param_1 + 0x38);
    }
    else {
      if (param_2 != 3) {
LAB_1008e82cc:
        local_48 = 0;
        local_40 = 0;
        goto LAB_1008e82fc;
      }
      FUN_1008e9b38(&local_48,param_1 + 0x38);
    }
  }
  else if (param_2 == 4) {
    FUN_1008ea468(&local_48);
  }
  else if (param_2 == 5) {
    FUN_1008ea508(&local_48,param_1 + 0x38);
  }
  else {
    if (param_2 != 6) goto LAB_1008e82cc;
    FUN_1008ea7c8(&local_48);
  }
  if (local_48 != 0) {
    *(int *)(local_48 + 8) = *(int *)(local_48 + 8) + 1;
  }
LAB_1008e82fc:
  lVar2 = local_48;
  lVar3 = *(long *)(param_1 + 0x30);
  if ((lVar3 != 0) && (iVar1 = *(int *)(lVar3 + 8) + -1, *(int *)(lVar3 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  *(long *)(param_1 + 0x30) = lVar2;
  if (lVar2 != 0) {
    uVar5 = *(undefined8 *)(param_1 + 0x18);
    puVar4 = (undefined8 *)FUN_1012d9850(0x30);
    FUN_10128ed98();
    *puVar4 = &PTR_FUN_106603ba0;
    puStack_50 = puVar4 + 3;
    *puStack_50 = &PTR_FUN_106603be8;
    puVar4[4] = lVar2;
    *(int *)(lVar2 + 8) = *(int *)(lVar2 + 8) + 1;
    *(int *)(puVar4 + 1) = *(int *)(puVar4 + 1) + 1;
    local_58 = puVar4;
    FUN_101851190(uVar5,&local_58,local_40,3);
    if ((local_58 != (undefined8 *)0x0) &&
       (iVar1 = *(int *)(local_58 + 1), *(int *)(local_58 + 1) = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_10128eea0();
    }
    iVar1 = *(int *)(lVar2 + 8) + -1;
    *(int *)(lVar2 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0(lVar2);
    }
  }
  return;
}

