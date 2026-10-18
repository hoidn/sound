// x86 0x10393ebc0 FUN_10393ebc0 state=exported-with-warnings chunk=chunk-02767.jsonl code_sha256=b512cb4f893daf922307113948eb70046eba77b61c7d388c1504b9102ca88cd6

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_10393ebc0(undefined8 param_1,double param_2,long *param_3,undefined4 param_4)

{
  int *piVar1;
  long lVar2;
  long lVar3;
  double dVar4;
  undefined1 auVar5 [16];
  undefined1 auVar6 [16];
  long *local_98;
  long *local_90;
  long local_80;
  undefined4 local_78;
  long local_70;
  long local_68;
  long local_60;
  undefined4 local_58;
  uint local_50;
  undefined8 local_48;
  double local_40;
  double local_38;
  double local_30;
  double local_28;
  
  lVar3 = (**(code **)(*param_3 + 0x7e0))(param_3,1);
  FUN_1027bd850(&local_98,lVar3,0,0);
  lVar2 = *local_98;
  dVar4 = (double)FUN_102810200(lVar2);
  local_30 = DAT_105b3ce00;
  local_28 = DAT_105b3ce00;
  if ((dVar4 != DAT_105b3ce00) || (NAN(dVar4) || NAN(DAT_105b3ce00))) {
    if (((param_2 != DAT_105b3ce00) || (NAN(param_2) || NAN(DAT_105b3ce00))) &&
       ((param_2 - dVar4 != 0.0 || (NAN(param_2 - dVar4))))) {
      if (dVar4 < DAT_105b35848) {
        if ((dVar4 != DAT_105b9e6f0) || (NAN(dVar4) || NAN(DAT_105b9e6f0))) {
          if ((dVar4 != DAT_105b42d18) || (NAN(dVar4) || NAN(DAT_105b42d18))) {
            auVar5._0_8_ = (double)((ulong)(DAT_105b3eac0 *
                                            *(double *)(&DAT_105b3eb20 + (ulong)(0.0 <= dVar4) * 8)
                                            * DAT_105a57808 + dVar4) & _DAT_105b35690) *
                           DAT_105b3eac8;
            auVar5._8_8_ = 0;
            auVar5 = roundsd(ZEXT816(0),auVar5,9);
            dVar4 = (auVar5._0_8_ / DAT_105b3eac8) *
                    *(double *)(&DAT_105b3eb20 + (ulong)(0.0 <= dVar4) * 8);
          }
        }
      }
      local_30 = dVar4;
      local_28 = param_2;
      if (param_2 < DAT_105b35848) {
        if ((param_2 != DAT_105b9e6f0) || (NAN(param_2) || NAN(DAT_105b9e6f0))) {
          if ((param_2 != DAT_105b42d18) || (NAN(param_2) || NAN(DAT_105b42d18))) {
            auVar6._0_8_ = (double)((ulong)(DAT_105b3eac0 *
                                            *(double *)
                                             (&DAT_105b3eb20 + (ulong)(0.0 <= param_2) * 8) *
                                            DAT_105a57808 + param_2) & _DAT_105b35690) *
                           DAT_105b3eac8;
            auVar6._8_8_ = 0;
            auVar5 = roundsd(auVar6,auVar6,9);
            local_28 = (auVar5._0_8_ / DAT_105b3eac8) *
                       *(double *)(&DAT_105b3eb20 + (ulong)(0.0 <= param_2) * 8);
          }
        }
      }
    }
  }
  if (lVar3 != 0) {
    *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
  }
  if (lVar2 != 0) {
    *(int *)(lVar2 + 8) = *(int *)(lVar2 + 8) + 1;
  }
  local_70 = lVar3;
  local_68 = lVar2;
  FUN_102514eb0(&local_80,0,0xffffffff);
  local_60 = local_80;
  if (local_80 == 0) {
    local_58 = local_78;
    local_50 = 0;
    local_48 = 0x7fefffffffffffff;
    local_40 = local_30;
    local_38 = local_28;
  }
  else {
    *(int *)(local_80 + 8) = *(int *)(local_80 + 8) + 1;
    local_58 = local_78;
    local_50 = 0;
    local_48 = 0x7fefffffffffffff;
    local_40 = local_30;
    local_38 = local_28;
    piVar1 = (int *)(local_80 + 8);
    *piVar1 = *piVar1 + -1;
    if (*piVar1 == 0) {
      FUN_1012716c0();
    }
  }
  FUN_103171b40(&local_70,param_4,DAT_107527df8);
  if ((ulong)local_50 != 0xffffffff) {
    (*(code *)(&PTR_FUN_106f57230)[local_50])(&local_80,&local_60);
  }
  local_50 = 0xffffffff;
  if (local_68 != 0) {
    piVar1 = (int *)(local_68 + 8);
    *piVar1 = *piVar1 + -1;
    if (*piVar1 == 0) {
      FUN_1012716c0();
    }
  }
  if (local_70 != 0) {
    piVar1 = (int *)(local_70 + 8);
    *piVar1 = *piVar1 + -1;
    if (*piVar1 == 0) {
      FUN_1012716c0();
    }
  }
  if (local_98 != (long *)0x0) {
    local_90 = local_98;
    operator_delete(local_98);
  }
  return;
}

