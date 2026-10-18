
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

long FUN_103171b40(undefined8 *param_1,ulong param_2,long param_3)

{
  int *piVar1;
  void *pvVar2;
  undefined1 auVar3 [16];
  undefined1 auVar4 [16];
  undefined1 auVar5 [16];
  undefined1 auVar6 [16];
  undefined1 auVar7 [16];
  undefined1 auVar8 [16];
  undefined1 auVar9 [16];
  undefined1 auVar10 [16];
  void *pvVar11;
  void *pvVar12;
  char cVar13;
  byte bVar14;
  int iVar15;
  undefined4 uVar16;
  undefined4 uVar17;
  uint uVar18;
  undefined8 uVar19;
  undefined8 uVar20;
  long *plVar21;
  long lVar22;
  long *plVar23;
  ulong uVar24;
  undefined8 *extraout_XMM0_Qa;
  undefined8 *puVar25;
  double extraout_XMM0_Qa_00;
  double dVar26;
  undefined8 *extraout_XMM0_Qa_01;
  double extraout_XMM0_Qa_03;
  undefined8 extraout_XMM0_Qb;
  undefined8 extraout_XMM0_Qb_00;
  undefined1 auVar27 [16];
  double extraout_XMM0_Qa_02;
  undefined8 extraout_XMM0_Qb_01;
  undefined1 auVar28 [16];
  undefined1 auVar29 [16];
  undefined1 auVar30 [16];
  undefined1 auVar31 [16];
  undefined1 auVar32 [16];
  undefined8 *local_160 [6];
  ulong local_130;
  void *local_128;
  void *local_120;
  undefined8 *local_110;
  undefined8 local_108;
  undefined8 uStack_100;
  undefined8 *local_f8;
  undefined8 uStack_f0;
  int *local_e0;
  undefined8 local_d8;
  undefined4 local_d0;
  undefined8 *local_c8;
  undefined8 uStack_c0;
  long *local_b8;
  int local_ac;
  long local_a8;
  long *local_a0;
  undefined1 local_98 [16];
  undefined8 uStack_88;
  long *local_78;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_106a33b20;
  plVar21 = (long *)param_1[1];
  local_130 = param_2;
  if (plVar21 == (long *)0x0) {
    local_b8 = (long *)0x0;
  }
  else {
    uVar19 = (**(code **)(*plVar21 + 0x170))(plVar21);
    uVar20 = FUN_1028e9790();
    cVar13 = FUN_1014765e0(uVar19,uVar20);
    local_b8 = (long *)0x0;
    if (cVar13 != '\0') {
      local_b8 = plVar21;
    }
  }
  local_160[0] = param_1;
  if ((int)(param_2 >> 0x20) == -1) {
                    /* WARNING: Subroutine does not return */
    FUN_1002c71d0();
  }
  local_98._0_8_ = local_160;
  local_ac = (*(code *)(&PTR_FUN_106dff8d0)[param_2 >> 0x20])(local_98,&local_130);
  uVar19 = FUN_101749200();
  FUN_101749260(uVar19,1);
  local_110 = &local_108;
  local_108 = 0;
  uStack_100 = 0;
  puVar25 = param_1 + 6;
  FUN_1031712f0(&local_128,local_b8,local_ac,puVar25,&local_110);
  FUN_1031728b0(&local_a8,&local_128,local_b8,local_ac);
  if (param_3 != 0) {
    FUN_102635aa0(param_3,local_b8,local_a8);
  }
  FUN_101547c30(local_160,*param_1);
  if (local_ac == 2) {
    local_98._0_8_ = DAT_1075566d0;
    local_98._8_8_ = _DAT_1075566d8;
    uStack_88 = uRam00000001075566e0;
    if (DAT_1075566d0 != (int *)0x0) {
      *DAT_1075566d0 = *DAT_1075566d0 + 1;
      local_98._8_8_ = _DAT_1075566d8;
      uStack_88 = uRam00000001075566e0;
    }
  }
  else if (local_ac == 1) {
    local_98._0_8_ = DAT_1075566b8;
    local_98._8_8_ = _DAT_1075566c0;
    uStack_88 = uRam00000001075566c8;
    if (DAT_1075566b8 != (int *)0x0) {
      *DAT_1075566b8 = *DAT_1075566b8 + 1;
      local_98._8_8_ = _DAT_1075566c0;
      uStack_88 = uRam00000001075566c8;
    }
  }
  else {
    local_98._0_8_ = DAT_1075566e8;
    local_98._8_8_ = _DAT_1075566f0;
    uStack_88 = uRam00000001075566f8;
    if (DAT_1075566e8 != (int *)0x0) {
      *DAT_1075566e8 = *DAT_1075566e8 + 1;
      local_98._8_8_ = _DAT_1075566f0;
      uStack_88 = uRam00000001075566f8;
    }
  }
  FUN_1011a7c70(&local_d8);
  FUN_1011a7c70(&local_a0);
  FUN_1011a7c70(&local_e0);
  FUN_101547ee0(local_160,local_98,&local_d8,&local_a0,&local_e0);
  if ((local_e0 != (int *)0x0) && (*local_e0 = *local_e0 + -1, *local_e0 == 0)) {
    FUN_101442b40();
  }
  if ((local_a0 != (long *)0x0) && (*(int *)local_a0 = (int)*local_a0 + -1, (int)*local_a0 == 0)) {
    FUN_101442b40();
  }
  if ((local_d8 != (long *)0x0) && (*(int *)local_d8 = (int)*local_d8 + -1, (int)*local_d8 == 0)) {
    FUN_101442b40();
  }
  if (((int *)local_98._0_8_ != (int *)0x0) &&
     (*(int *)local_98._0_8_ = *(int *)local_98._0_8_ + -1, *(int *)local_98._0_8_ == 0)) {
    FUN_101442b40();
  }
  local_c8 = puVar25;
  if ((ulong)*(uint *)(param_1 + 4) == 0xffffffff) {
                    /* WARNING: Subroutine does not return */
    FUN_1002c71d0();
  }
  puVar25 = param_1 + 2;
  local_98._0_8_ = &local_e0;
  (*(code *)(&PTR_FUN_106dff8e0)[*(uint *)(param_1 + 4)])(&local_d8,local_98,puVar25);
  plVar21 = local_d8;
  if (local_d8 == (long *)0x0) {
LAB_103171e4d:
    local_a0 = (long *)0x0;
  }
  else {
    plVar23 = local_d8 + 1;
    *(int *)plVar23 = (int)*plVar23 + -1;
    if ((int)*plVar23 == 0) {
      FUN_1012716c0(local_d8);
    }
    uVar19 = (**(code **)(*plVar21 + 0x170))(plVar21);
    uVar20 = FUN_102a6d070();
    cVar13 = FUN_1014765e0(uVar19,uVar20);
    if (cVar13 == '\0') goto LAB_103171e4d;
    local_a0 = plVar21;
    *(int *)(plVar21 + 1) = (int)plVar21[1] + 1;
  }
  cVar13 = FUN_101479c50(param_1[1]);
  if (cVar13 == '\0') {
    bVar14 = 0;
  }
  else {
    bVar14 = FUN_10255d8d0(param_1[1]);
    bVar14 = bVar14 ^ 1;
  }
  if (local_a0 == (long *)0x0) {
    local_d8._4_4_ = (undefined4)((ulong)local_d8 >> 0x20);
    plVar21 = (long *)(**(code **)(*local_b8 + 0x238))(local_b8,0);
    if (plVar21 == (long *)0x0) {
LAB_103171ef5:
      iVar15 = FUN_1027a5480(*param_1);
      iVar15 = iVar15 + -1;
    }
    else {
      uVar19 = (**(code **)(*plVar21 + 0x170))(plVar21);
      uVar20 = FUN_102918600();
      cVar13 = FUN_1014765e0(uVar19,uVar20);
      if ((cVar13 == '\0') || (lVar22 = (**(code **)(*plVar21 + 0x3a0))(plVar21), lVar22 == 0))
      goto LAB_103171ef5;
      iVar15 = (**(code **)(*plVar21 + 0x370))(plVar21);
    }
    local_d8 = (long *)CONCAT44(local_d8._4_4_,iVar15);
    uVar16 = FUN_101533580(*param_1);
    uVar19 = *param_1;
    local_f8 = puVar25;
    local_78 = operator_new(0x30);
    *local_78 = (long)&PTR_FUN_106dffd48;
    local_78[1] = (long)&local_a0;
    local_78[2] = (long)param_1;
    local_78[3] = (long)&local_d8;
    local_78[4] = (long)&local_b8;
    local_78[5] = (long)&local_ac;
    FUN_101544f70(uVar16,uVar19,local_98);
    if (local_78 == (long *)local_98) {
      lVar22 = 0x20;
LAB_103171fc3:
      (**(code **)(*local_78 + lVar22))();
      if (bVar14 != 0) goto LAB_103171fa3;
LAB_103171fdc:
      plVar21 = local_a0;
      puVar25 = local_f8;
      uVar19 = FUN_1027bf840(*param_1,local_a0);
      FUN_102515260(plVar21,uVar19,1);
    }
    else {
      lVar22 = 0x28;
      if (local_78 != (long *)0x0) goto LAB_103171fc3;
      if (bVar14 == 0) goto LAB_103171fdc;
LAB_103171fa3:
      plVar21 = local_a0;
      puVar25 = local_f8;
      uVar16 = FUN_10255da50(local_b8);
      FUN_10283ffc0(plVar21,uVar16);
    }
    FUN_1025168f0(local_a0);
  }
  if (*(int *)(param_1 + 4) == 1) {
    uVar19 = (**(code **)(*local_a0 + 0x318))(local_a0,*(undefined4 *)(param_1 + 3));
    FUN_10257b7e0(uVar19,local_a8);
  }
  else {
    if (*(int *)(param_1 + 4) != 0) {
                    /* WARNING: Subroutine does not return */
      FUN_1002c71d0();
    }
    plVar21 = (long *)*puVar25;
    if (plVar21 != (long *)0x0) {
      *(int *)(plVar21 + 1) = (int)plVar21[1] + 1;
    }
    uVar16 = *(undefined4 *)(param_1 + 3);
    puVar25 = (undefined8 *)param_1[5];
    uStack_f0 = 0;
    local_d8 = plVar21;
    local_d0 = uVar16;
    if (((double)puVar25 == DAT_105b3ce00) && (!NAN((double)puVar25) && !NAN(DAT_105b3ce00))) {
      uVar17 = FUN_1025637a0(local_b8);
      auVar31._4_4_ = -(uint)((double)extraout_XMM0_Qa == _UNK_105b3eb18);
      auVar31._0_4_ = -(uint)((double)extraout_XMM0_Qa == _DAT_105b3eb10);
      auVar31._8_4_ = -(uint)(_DAT_105b3eb00 == (double)extraout_XMM0_Qa);
      auVar31._12_4_ = -(uint)(_UNK_105b3eb08 == (double)extraout_XMM0_Qa);
      iVar15 = movmskps(uVar17,auVar31);
      puVar25 = extraout_XMM0_Qa;
      uStack_f0 = extraout_XMM0_Qb;
      if (iVar15 == 0) {
        auVar29._0_8_ =
             (double)((ulong)(DAT_105b3eac0 *
                              *(double *)
                               (&DAT_105b3eb20 + (ulong)(0.0 <= (double)extraout_XMM0_Qa) * 8) *
                              DAT_105a57808 + (double)extraout_XMM0_Qa) & _DAT_105b35690) *
             DAT_105b3eac8;
        auVar29._8_8_ = 0;
        auVar31 = roundsd(ZEXT816(0),auVar29,9);
        uStack_f0 = auVar31._8_8_;
        puVar25 = (undefined8 *)
                  ((auVar31._0_8_ / DAT_105b3eac8) *
                  *(double *)(&DAT_105b3eb20 + (ulong)(0.0 <= (double)extraout_XMM0_Qa) * 8));
      }
    }
    local_f8 = puVar25;
    uVar19 = FUN_10283d2d0(local_a0);
    uVar19 = FUN_102784a50(uVar19);
    uVar19 = FUN_102813a50(uVar19,0xffffffff);
    FUN_102533de0(local_98,uVar19);
    lVar22 = local_a8;
    uVar17 = FUN_102558c70(local_a8);
    dVar26 = extraout_XMM0_Qa_00 + (double)local_f8;
    auVar10._4_4_ = -(uint)(dVar26 == _UNK_105b3eb18);
    auVar10._0_4_ = -(uint)(dVar26 == _DAT_105b3eb10);
    auVar10._8_4_ = -(uint)(_DAT_105b3eb00 == dVar26);
    auVar10._12_4_ = -(uint)(_UNK_105b3eb08 == dVar26);
    iVar15 = movmskps(uVar17,auVar10);
    if (iVar15 == 0) {
      auVar6._8_8_ = 0;
      auVar6._0_8_ = (double)((ulong)(DAT_105b3eac0 *
                                      *(double *)(&DAT_105b3eb20 + (ulong)(0.0 <= dVar26) * 8) *
                                      DAT_105a57808 + dVar26) & _DAT_105b35690) * DAT_105b3eac8;
      auVar31 = roundsd(ZEXT816(0),auVar6,9);
      dVar26 = (auVar31._0_8_ / DAT_105b3eac8) *
               *(double *)(&DAT_105b3eb20 + (ulong)(0.0 <= dVar26) * 8);
    }
    FUN_102558fd0(local_f8,dVar26,lVar22);
    if (plVar21 == (long *)0x0) {
      plVar23 = local_a0 + 0xb;
      if (local_a0 == (long *)0x0) {
        plVar23 = (long *)0x0;
      }
    }
    else {
      plVar23 = (long *)FUN_102892510(plVar21,uVar16);
    }
    FUN_102558b50(local_a8,plVar23);
    FUN_102533e60(local_98);
    if (plVar21 != (long *)0x0) {
      plVar23 = plVar21 + 1;
      *(int *)plVar23 = (int)*plVar23 + -1;
      if ((int)*plVar23 == 0) {
        FUN_1012716c0(plVar21);
      }
    }
  }
  plVar21 = local_a0;
  lVar22 = local_a8;
  if (bVar14 == 0) {
    uVar19 = FUN_1027bf8c0(*param_1);
    FUN_102516930(lVar22,plVar21,uVar19,0);
  }
  lVar22 = local_a8;
  if ((double)param_1[6] == DAT_105b3ce00) {
    if (((double)param_1[7] == DAT_105b3ce00) && (!NAN((double)param_1[7]) && !NAN(DAT_105b3ce00)))
    goto LAB_103172633;
  }
  cVar13 = (**(code **)(*(long *)param_1[1] + 0x300))();
  if (cVar13 == '\0') {
    uVar19 = FUN_1025595c0(lVar22);
    uVar16 = FUN_102693450(uVar19);
    auVar32._4_4_ = -(uint)(extraout_XMM0_Qa_03 == _UNK_105b3eb18);
    auVar32._0_4_ = -(uint)(extraout_XMM0_Qa_03 == _DAT_105b3eb10);
    auVar32._8_4_ = -(uint)(_DAT_105b3eb00 == extraout_XMM0_Qa_03);
    auVar32._12_4_ = -(uint)(_UNK_105b3eb08 == extraout_XMM0_Qa_03);
    uVar18 = movmskps(uVar16,auVar32);
    uVar24 = (ulong)uVar18;
    local_98._8_8_ = extraout_XMM0_Qa_03;
    if (uVar18 == 0) {
      uVar24 = (ulong)(0.0 <= extraout_XMM0_Qa_03);
      auVar3._8_8_ = 0;
      auVar3._0_8_ = (double)((ulong)(DAT_105b3eac0 * *(double *)(&DAT_105b3eb20 + uVar24 * 8) *
                                      DAT_105a57808 + extraout_XMM0_Qa_03) & _DAT_105b35690) *
                     DAT_105b3eac8;
      auVar31 = roundsd(ZEXT816(0),auVar3,9);
      local_98._8_8_ = (auVar31._0_8_ / DAT_105b3eac8) * *(double *)(&DAT_105b3eb20 + uVar24 * 8);
    }
    local_98._0_8_ = (double)param_1[6] + (double)local_98._8_8_;
    local_98._8_8_ = (double)local_98._8_8_ + (double)param_1[7];
    auVar4._4_4_ = -(uint)((double)local_98._0_8_ == _UNK_105b3eb18);
    auVar4._0_4_ = -(uint)((double)local_98._0_8_ == _DAT_105b3eb10);
    auVar4._8_4_ = -(uint)(_DAT_105b3eb00 == (double)local_98._0_8_);
    auVar4._12_4_ = -(uint)(_UNK_105b3eb08 == (double)local_98._0_8_);
    uVar18 = movmskps((int)uVar24,auVar4);
    uVar24 = (ulong)uVar18;
    if (uVar18 == 0) {
      uVar24 = (ulong)(0.0 <= (double)local_98._0_8_);
      auVar8._8_8_ = 0;
      auVar8._0_8_ = (double)((ulong)(DAT_105b3eac0 * *(double *)(&DAT_105b3eb20 + uVar24 * 8) *
                                      DAT_105a57808 + (double)local_98._0_8_) & _DAT_105b35690) *
                     DAT_105b3eac8;
      auVar31 = roundsd(ZEXT816(0),auVar8,9);
      local_98._0_8_ = (auVar31._0_8_ / DAT_105b3eac8) * *(double *)(&DAT_105b3eb20 + uVar24 * 8);
    }
    auVar5._4_4_ = -(uint)((double)local_98._8_8_ == _UNK_105b3eb18);
    auVar5._0_4_ = -(uint)((double)local_98._8_8_ == _DAT_105b3eb10);
    auVar5._8_4_ = -(uint)(_DAT_105b3eb00 == (double)local_98._8_8_);
    auVar5._12_4_ = -(uint)(_UNK_105b3eb08 == (double)local_98._8_8_);
    iVar15 = movmskps((int)uVar24,auVar5);
    if (iVar15 == 0) {
      auVar9._8_8_ = 0;
      auVar9._0_8_ = (double)((ulong)(DAT_105b3eac0 *
                                      *(double *)
                                       (&DAT_105b3eb20 + (ulong)(0.0 <= (double)local_98._8_8_) * 8)
                                      * DAT_105a57808 + (double)local_98._8_8_) & _DAT_105b35690) *
                     DAT_105b3eac8;
      auVar31 = roundsd(ZEXT816(0),auVar9,9);
      local_98._8_8_ =
           (auVar31._0_8_ / DAT_105b3eac8) *
           *(double *)(&DAT_105b3eb20 + (ulong)(0.0 <= (double)local_98._8_8_) * 8);
    }
    FUN_1031bc770(lVar22,local_98);
  }
  else {
    FUN_1031bc770(lVar22,local_c8);
    uVar19 = FUN_1027b6140(*param_1);
    bVar14 = FUN_10280fec0(uVar19);
    if ((bVar14 & *(int *)(param_1 + 4) == 0) == 1) {
      uVar19 = FUN_1027b6140(*param_1);
      local_c8 = (undefined8 *)FUN_10280fcc0(uVar19);
      dVar26 = (double)FUN_102558290(param_1[1]);
      if (dVar26 < (double)local_c8) {
        uVar19 = FUN_1027b6140(*param_1);
        local_c8 = (undefined8 *)FUN_10280fcc0(uVar19);
        dVar26 = (double)FUN_102558290(lVar22);
        if (((double)local_c8 != dVar26) || (NAN((double)local_c8) || NAN(dVar26))) {
          uVar19 = FUN_1027b6140(*param_1);
          uVar16 = FUN_10280fcc0(uVar19);
          auVar27._4_4_ = -(uint)((double)extraout_XMM0_Qa_01 == _UNK_105b3eb18);
          auVar27._0_4_ = -(uint)((double)extraout_XMM0_Qa_01 == _DAT_105b3eb10);
          auVar27._8_4_ = -(uint)(_DAT_105b3eb00 == (double)extraout_XMM0_Qa_01);
          auVar27._12_4_ = -(uint)(_UNK_105b3eb08 == (double)extraout_XMM0_Qa_01);
          iVar15 = movmskps(uVar16,auVar27);
          local_c8 = extraout_XMM0_Qa_01;
          uStack_c0 = extraout_XMM0_Qb_00;
          if (iVar15 == 0) {
            auVar30._0_8_ =
                 (double)((ulong)(DAT_105b3eac0 *
                                  *(double *)
                                   (&DAT_105b3eb20 + (ulong)(0.0 <= (double)extraout_XMM0_Qa_01) * 8
                                   ) * DAT_105a57808 + (double)extraout_XMM0_Qa_01) & _DAT_105b35690
                         ) * DAT_105b3eac8;
            auVar30._8_8_ = 0;
            auVar31 = roundsd(auVar30,auVar30,9);
            uStack_c0 = auVar31._8_8_;
            local_c8 = (undefined8 *)
                       ((auVar31._0_8_ / DAT_105b3eac8) *
                       *(double *)(&DAT_105b3eb20 + (ulong)(0.0 <= (double)extraout_XMM0_Qa_01) * 8)
                       );
          }
          uVar19 = FUN_1027b6140(*param_1);
          local_f8 = (undefined8 *)FUN_10280fcc0(uVar19);
          uStack_f0 = extraout_XMM0_Qb_01;
          uVar16 = FUN_102558c70(lVar22);
          dVar26 = (double)local_f8 + extraout_XMM0_Qa_02;
          auVar28._4_4_ = -(uint)(dVar26 == _UNK_105b3eb18);
          auVar28._0_4_ = -(uint)(dVar26 == _DAT_105b3eb10);
          auVar28._8_4_ = -(uint)(_DAT_105b3eb00 == dVar26);
          auVar28._12_4_ = -(uint)(_UNK_105b3eb08 == dVar26);
          iVar15 = movmskps(uVar16,auVar28);
          if (iVar15 == 0) {
            auVar7._8_8_ = 0;
            auVar7._0_8_ = (double)((ulong)(DAT_105b3eac0 *
                                            *(double *)(&DAT_105b3eb20 + (ulong)(0.0 <= dVar26) * 8)
                                            * DAT_105a57808 + dVar26) & _DAT_105b35690) *
                           DAT_105b3eac8;
            auVar31 = roundsd(ZEXT816(0),auVar7,9);
            dVar26 = (auVar31._0_8_ / DAT_105b3eac8) *
                     *(double *)(&DAT_105b3eb20 + (ulong)(0.0 <= dVar26) * 8);
          }
          FUN_102558fd0(local_c8,dVar26,lVar22);
        }
      }
    }
  }
LAB_103172633:
  uVar19 = FUN_10255cf50(local_a8);
  uVar20 = FUN_1025595c0(local_a8);
  local_98 = FUN_102694170(uVar20);
  FUN_102777e00(uVar19,local_98);
  FUN_101548040(local_160);
  FUN_10316c140(&local_110);
  lVar22 = local_a8;
  if (local_a0 != (long *)0x0) {
    plVar21 = local_a0 + 1;
    *(int *)plVar21 = (int)*plVar21 + -1;
    if ((int)*plVar21 == 0) {
      FUN_1012716c0();
    }
  }
  FUN_101547e90(local_160);
  if (local_a8 != 0) {
    piVar1 = (int *)(local_a8 + 8);
    *piVar1 = *piVar1 + -1;
    if (*piVar1 == 0) {
      FUN_1012716c0();
    }
  }
  pvVar12 = local_128;
  pvVar11 = local_120;
  if (local_128 != (void *)0x0) {
    for (; pvVar11 != pvVar12; pvVar11 = (void *)((long)pvVar11 + -0x40)) {
      pvVar2 = *(void **)((long)pvVar11 + -0x18);
      if (pvVar2 != (void *)0x0) {
        *(void **)((long)pvVar11 + -0x10) = pvVar2;
        operator_delete(pvVar2);
      }
    }
    local_120 = pvVar12;
    operator_delete(local_128);
  }
  FUN_1002e01d0(&local_110,local_108);
  if (*(long *)PTR____stack_chk_guard_106a33b20 == local_38) {
    return lVar22;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

