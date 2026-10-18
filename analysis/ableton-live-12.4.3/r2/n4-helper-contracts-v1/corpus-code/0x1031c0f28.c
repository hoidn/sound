// 0x1031c0f28 FUN_1031c0f28 exported-with-warnings  sig: undefined FUN_1031c0f28()

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1031c0f28(undefined8 *param_1)

{
  undefined8 *puVar1;
  int iVar2;
  undefined8 uVar3;
  int *local_80;
  int *local_78;
  undefined8 local_70;
  long lStack_68;
  char *local_60;
  undefined8 uStack_58;
  long lStack_50;
  void *local_48;
  ulong local_40;
  byte local_31;
  int local_30 [2];
  undefined8 local_28;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  local_30[0] = 0;
  local_28 = std::system_category();
  FUN_103e9e3d8(&local_48,0,local_30);
  if (local_30[0] == 0) {
    if (-1 < (char)local_31) {
      local_40 = (ulong)local_31;
    }
    if (local_40 != 0) {
      local_78 = operator_new(0x20);
      uVar3 = s_Library_Audio_Plug_Ins_VST3_105be7c71._0_8_;
      *(ulong *)(local_78 + 2) =
           CONCAT53(s_Library_Audio_Plug_Ins_VST3_105be7c71._11_5_,
                    s_Library_Audio_Plug_Ins_VST3_105be7c71._8_3_);
      *(undefined8 *)local_78 = uVar3;
      uVar3 = CONCAT35(s_Library_Audio_Plug_Ins_VST3_105be7c71._16_3_,
                       s_Library_Audio_Plug_Ins_VST3_105be7c71._11_5_);
      *(undefined8 *)((long)local_78 + 0x13) = s_Library_Audio_Plug_Ins_VST3_105be7c71._19_8_;
      *(undefined8 *)((long)local_78 + 0xb) = uVar3;
      *(undefined1 *)((long)local_78 + 0x1b) = 0;
      lStack_68 = _UNK_1055cdf88;
      local_70 = _DAT_1055cdf80;
      FUN_100241e54(&local_60,&local_48,&local_78);
      FUN_101427680(&local_80,"user");
      puVar1 = (undefined8 *)param_1[1];
      if (puVar1 < (undefined8 *)param_1[2]) {
        puVar1[2] = lStack_50;
        puVar1[3] = local_80;
        puVar1[1] = uStack_58;
        *puVar1 = local_60;
        uStack_58 = 0;
        lStack_50 = 0;
        local_60 = (char *)0x0;
        param_1[1] = puVar1 + 4;
      }
      else {
        uVar3 = FUN_1031c342c(param_1,&local_60,&local_80);
        param_1[1] = uVar3;
        if ((local_80 != (int *)0x0) && (iVar2 = *local_80, *local_80 = iVar2 + -1, iVar2 + -1 == 0)
           ) {
          FUN_101449efc();
        }
      }
      if (lStack_50 < 0) {
        operator_delete(local_60);
      }
      if (lStack_68 < 0) {
        operator_delete(local_78);
      }
    }
  }
  local_60 = operator_new(0x20);
  uVar3 = s__Library_Audio_Plug_Ins_VST3_105be7c92._0_8_;
  *(ulong *)(local_60 + 8) =
       CONCAT44(s__Library_Audio_Plug_Ins_VST3_105be7c92._12_4_,
                s__Library_Audio_Plug_Ins_VST3_105be7c92._8_4_);
  *(undefined8 *)local_60 = uVar3;
  uVar3 = CONCAT44(s__Library_Audio_Plug_Ins_VST3_105be7c92._16_4_,
                   s__Library_Audio_Plug_Ins_VST3_105be7c92._12_4_);
  *(undefined8 *)(local_60 + 0x14) = s__Library_Audio_Plug_Ins_VST3_105be7c92._20_8_;
  *(undefined8 *)(local_60 + 0xc) = uVar3;
  local_60[0x1c] = '\0';
  lStack_50 = _UNK_1055d3958;
  uStack_58 = _DAT_1055d3950;
  FUN_101427680(&local_78,"local");
  puVar1 = (undefined8 *)param_1[1];
  if (puVar1 < (undefined8 *)param_1[2]) {
    puVar1[2] = lStack_50;
    puVar1[1] = uStack_58;
    *puVar1 = local_60;
    uStack_58 = 0;
    lStack_50 = 0;
    local_60 = (char *)0x0;
    puVar1[3] = local_78;
    param_1[1] = puVar1 + 4;
  }
  else {
    uVar3 = FUN_1031c342c(param_1,&local_60,&local_78);
    param_1[1] = uVar3;
    if ((local_78 != (int *)0x0) && (iVar2 = *local_78, *local_78 = iVar2 + -1, iVar2 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  if (lStack_50 < 0) {
    operator_delete(local_60);
  }
  if ((char)local_31 < '\0') {
    operator_delete(local_48);
    return;
  }
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0] = (char)s_Library_Audio_Plug_Ins_VST3_105be7c71._0_8_;
  s_Library_Audio_Plug_Ins_VST3_105be7c71[1] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._0_8_,1);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[2] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._0_8_,2);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[3] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._0_8_,3);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[4] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._0_8_,4);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[5] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._0_8_,5);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[6] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._0_8_,6);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[7] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._0_8_,7);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[8] = (char)s_Library_Audio_Plug_Ins_VST3_105be7c71._8_3_;
  s_Library_Audio_Plug_Ins_VST3_105be7c71[9] =
       SUB31(s_Library_Audio_Plug_Ins_VST3_105be7c71._8_3_,1);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[10] =
       SUB31(s_Library_Audio_Plug_Ins_VST3_105be7c71._8_3_,2);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0xb] =
       (char)s_Library_Audio_Plug_Ins_VST3_105be7c71._11_5_;
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0xc] =
       SUB51(s_Library_Audio_Plug_Ins_VST3_105be7c71._11_5_,1);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0xd] =
       SUB51(s_Library_Audio_Plug_Ins_VST3_105be7c71._11_5_,2);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0xe] =
       SUB51(s_Library_Audio_Plug_Ins_VST3_105be7c71._11_5_,3);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0xf] =
       SUB51(s_Library_Audio_Plug_Ins_VST3_105be7c71._11_5_,4);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0x10] =
       (char)s_Library_Audio_Plug_Ins_VST3_105be7c71._16_3_;
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0x11] =
       SUB31(s_Library_Audio_Plug_Ins_VST3_105be7c71._16_3_,1);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0x12] =
       SUB31(s_Library_Audio_Plug_Ins_VST3_105be7c71._16_3_,2);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0x13] =
       (char)s_Library_Audio_Plug_Ins_VST3_105be7c71._19_8_;
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0x14] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._19_8_,1);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0x15] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._19_8_,2);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0x16] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._19_8_,3);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0x17] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._19_8_,4);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0x18] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._19_8_,5);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0x19] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._19_8_,6);
  s_Library_Audio_Plug_Ins_VST3_105be7c71[0x1a] =
       SUB81(s_Library_Audio_Plug_Ins_VST3_105be7c71._19_8_,7);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0] = (char)s__Library_Audio_Plug_Ins_VST3_105be7c92._0_8_
  ;
  s__Library_Audio_Plug_Ins_VST3_105be7c92[1] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._0_8_,1);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[2] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._0_8_,2);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[3] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._0_8_,3);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[4] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._0_8_,4);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[5] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._0_8_,5);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[6] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._0_8_,6);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[7] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._0_8_,7);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[8] = (char)s__Library_Audio_Plug_Ins_VST3_105be7c92._8_4_
  ;
  s__Library_Audio_Plug_Ins_VST3_105be7c92[9] =
       SUB41(s__Library_Audio_Plug_Ins_VST3_105be7c92._8_4_,1);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[10] =
       SUB41(s__Library_Audio_Plug_Ins_VST3_105be7c92._8_4_,2);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0xb] =
       SUB41(s__Library_Audio_Plug_Ins_VST3_105be7c92._8_4_,3);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0xc] =
       (char)s__Library_Audio_Plug_Ins_VST3_105be7c92._12_4_;
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0xd] =
       SUB41(s__Library_Audio_Plug_Ins_VST3_105be7c92._12_4_,1);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0xe] =
       SUB41(s__Library_Audio_Plug_Ins_VST3_105be7c92._12_4_,2);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0xf] =
       SUB41(s__Library_Audio_Plug_Ins_VST3_105be7c92._12_4_,3);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0x10] =
       (char)s__Library_Audio_Plug_Ins_VST3_105be7c92._16_4_;
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0x11] =
       SUB41(s__Library_Audio_Plug_Ins_VST3_105be7c92._16_4_,1);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0x12] =
       SUB41(s__Library_Audio_Plug_Ins_VST3_105be7c92._16_4_,2);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0x13] =
       SUB41(s__Library_Audio_Plug_Ins_VST3_105be7c92._16_4_,3);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0x14] =
       (char)s__Library_Audio_Plug_Ins_VST3_105be7c92._20_8_;
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0x15] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._20_8_,1);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0x16] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._20_8_,2);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0x17] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._20_8_,3);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0x18] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._20_8_,4);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0x19] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._20_8_,5);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0x1a] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._20_8_,6);
  s__Library_Audio_Plug_Ins_VST3_105be7c92[0x1b] =
       SUB81(s__Library_Audio_Plug_Ins_VST3_105be7c92._20_8_,7);
  return;
}


