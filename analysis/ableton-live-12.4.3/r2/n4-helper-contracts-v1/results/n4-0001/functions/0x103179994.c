
void FUN_103179994(long *param_1,long *param_2)

{
  int iVar1;
  int *piVar2;
  ulong uVar3;
  long lVar4;
  long lVar5;
  undefined8 *puVar6;
  undefined1 uVar7;
  undefined8 *puVar8;
  undefined8 *puVar9;
  long local_68;
  char local_60 [14];
  undefined1 local_52;
  char local_49;
  long local_48;
  code *local_40;
  long *plStack_38;
  
  uVar3 = (**(code **)(*param_1 + 0x28))();
  if ((uVar3 & 1) != 0) {
    return;
  }
  uVar7 = (undefined1)*param_2;
  *(undefined1 *)(param_1 + 0x13) = uVar7;
  if (param_1 + 0x13 != param_2) {
    *(int *)(param_1 + 0x18) = (int)param_2[5];
    FUN_10317aef8(param_1 + 0x14,param_2[3],0);
    uVar7 = (undefined1)param_1[0x13];
  }
  *(undefined1 *)((long)param_1 + 0xcc) = uVar7;
  local_49 = '\x0e';
  local_60[0] = s_plugin_scanner_105be56bf[0];
  local_60[1] = s_plugin_scanner_105be56bf[1];
  local_60[2] = s_plugin_scanner_105be56bf[2];
  local_60[3] = s_plugin_scanner_105be56bf[3];
  local_60[4] = s_plugin_scanner_105be56bf[4];
  local_60[5] = s_plugin_scanner_105be56bf[5];
  local_60[6] = s_plugin_scanner_105be56bf[6];
  local_60[7] = s_plugin_scanner_105be56bf[7];
  local_60[8] = s_plugin_scanner_105be56bf[8];
  local_60[9] = s_plugin_scanner_105be56bf[9];
  local_60[10] = s_plugin_scanner_105be56bf[10];
  local_60[0xb] = s_plugin_scanner_105be56bf[0xb];
  local_60[0xc] = s_plugin_scanner_105be56bf[0xc];
  local_60[0xd] = s_plugin_scanner_105be56bf[0xd];
  local_52 = 0;
  FUN_1026a00e0(&local_68,param_1[0xf]);
  lVar4 = FUN_1025d90d4(local_60,&local_68);
  if (lVar4 != 0) {
    *(int *)(lVar4 + 8) = *(int *)(lVar4 + 8) + 1;
  }
  lVar5 = param_1[0x10];
  if ((lVar5 != 0) && (iVar1 = *(int *)(lVar5 + 8) + -1, *(int *)(lVar5 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  param_1[0x10] = lVar4;
  if ((local_68 != 0) &&
     (iVar1 = *(int *)(local_68 + 8) + -1, *(int *)(local_68 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  if (local_49 < '\0') {
    operator_delete((void *)CONCAT26(local_60._6_2_,local_60._0_6_));
    lVar4 = FUN_1025d9f3c(param_1[0x10]);
  }
  else {
    lVar4 = FUN_1025d9f3c(param_1[0x10]);
  }
  if (lVar4 != 0) {
    lVar5 = *(long *)(lVar4 + 8);
    lVar4 = *(long *)(lVar4 + 0x10);
    if (lVar5 == lVar4) {
LAB_103179af4:
      if (lVar5 != lVar4) goto LAB_103179bac;
    }
    else {
      do {
        if ((*(long **)(lVar5 + 0x18) == param_1) &&
           (*(long **)(lVar5 + 0x28) == param_1 && *(code **)(lVar5 + 0x20) == thunk_FUN_10317bcf0))
        goto LAB_103179af4;
        lVar5 = lVar5 + 0x30;
      } while (lVar5 != lVar4);
    }
  }
  lVar4 = FUN_1025d9f3c(param_1[0x10]);
  FUN_101458fc8(local_60,param_1);
  builtin_strncpy(local_60,"\x10%Y\x06\x01",6);
  local_60[6] = '\0';
  local_60[7] = '\0';
  local_40 = thunk_FUN_10317bcf0;
  puVar6 = *(undefined8 **)(lVar4 + 0x10);
  plStack_38 = param_1;
  if (puVar6 < *(undefined8 **)(lVar4 + 0x18)) {
    puVar8 = puVar6 + 2;
    *puVar8 = 0;
    puVar6[1] = 0;
    puVar6[3] = local_48;
    if (local_48 != 0) {
      lVar5 = *(long *)(local_48 + 0x10);
      puVar9 = puVar6;
      if (lVar5 != 0) {
        puVar8 = (undefined8 *)(lVar5 + 8);
        puVar9 = (undefined8 *)*puVar8;
        puVar6[2] = lVar5;
        puVar9[2] = puVar6;
      }
      puVar6[1] = puVar9;
      *puVar8 = puVar6;
      *(undefined8 **)(local_48 + 0x10) = puVar6;
    }
    *puVar6 = &DAT_106592510;
    puVar6[5] = param_1;
    puVar6[4] = thunk_FUN_10317bcf0;
    puVar6 = puVar6 + 6;
  }
  else {
    puVar6 = (undefined8 *)FUN_10027a5c8(lVar4 + 8,local_60);
  }
  *(undefined8 **)(lVar4 + 0x10) = puVar6;
  FUN_101459068(local_60);
LAB_103179bac:
  FUN_103179e68(param_1);
  FUN_1011cb734(local_60);
  FUN_10317ad9c(param_1,local_60,0,0);
  piVar2 = (int *)CONCAT26(local_60._6_2_,local_60._0_6_);
  if ((piVar2 != (int *)0x0) && (iVar1 = *piVar2, *piVar2 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((*(byte *)(param_1 + 0xc) & 1) == 0) {
    *(undefined1 *)(param_1 + 0xc) = 1;
    FUN_1017cde1c(param_1 + 4,1);
    return;
  }
  return;
}

