// 0x12ab50 OAsyncClipFireManager::PrepareClipFire state=exported-with-warnings body=[['0x12ab50', '0x12b82c']]

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* OAsyncClipFireManager::PrepareClipFire(OClipPreload*, int, double, bool, TNoteType, bool,
   OClipFireParams const&, float, float) const */

undefined8 *
OAsyncClipFireManager::PrepareClipFire
          (double param_3,undefined4 param_2,undefined4 param_3_00,undefined8 *param_1,
          OAsyncClipFireManager *param_5,OClipPreload *param_6,ulong param_7,undefined4 param_8,
          int param_9,bool param_10,OClipFireParams *param_11)

{
  undefined8 uVar1;
  undefined1 auVar2 [16];
  undefined1 auVar3 [16];
  undefined8 uVar4;
  OClipPreload *this;
  char cVar5;
  byte bVar6;
  undefined1 uVar7;
  undefined4 uVar8;
  long lVar9;
  OScheduler *pOVar11;
  OTrack *this_00;
  OTrackRecordManager *pOVar12;
  long *plVar13;
  int iVar14;
  int iVar15;
  uint uVar16;
  OClipFireEvent *pOVar17;
  OClipFireEvent *this_01;
  int iVar18;
  bool bVar19;
  ulong uVar20;
  undefined4 uVar21;
  undefined4 in_XMM0_Dc;
  undefined4 extraout_XMM0_Dc;
  undefined4 uVar22;
  undefined4 in_XMM0_Dd;
  undefined4 extraout_XMM0_Dd;
  undefined4 uVar23;
  double dVar24;
  undefined1 auVar25 [16];
  undefined1 auVar26 [16];
  undefined1 auVar27 [16];
  undefined4 local_200;
  undefined4 local_1fc;
  double local_1f8;
  undefined1 local_1f0;
  byte local_1ef;
  char local_1ee;
  undefined8 local_1e8;
  double local_1e0;
  double local_1d8;
  undefined8 local_1d0;
  undefined8 uStack_1c8;
  undefined8 uStack_1c0;
  undefined8 local_1b8;
  uint local_1b0;
  byte local_1ac;
  undefined4 local_1a8;
  undefined4 local_1a4;
  undefined8 local_1a0;
  undefined8 uStack_198;
  undefined8 local_190;
  undefined8 uStack_188;
  undefined8 local_180;
  long lStack_178;
  OClipFireParams local_170;
  OClipLoop local_168 [24];
  undefined1 local_150;
  double dStack_140;
  undefined8 local_138;
  char local_130;
  OClipPreload *local_128;
  TStatus *local_120;
  double local_118 [3];
  undefined8 uStack_100;
  undefined8 local_f8;
  double dStack_f0;
  undefined8 local_e8;
  char local_e0;
  undefined4 local_d0;
  undefined4 local_cc;
  OClipAutomation *local_c8;
  OAsyncClipFireManager *local_c0;
  double local_b8;
  undefined4 uStack_b0;
  undefined4 uStack_ac;
  undefined8 local_a8;
  ulong uStack_a0;
  undefined4 local_8c;
  double local_88;
  double local_80;
  undefined1 local_78 [16];
  uint local_5c;
  OAsyncClipFireManager *local_58;
  double local_50;
  byte local_41;
  double local_40;
  uint local_34;
  long lVar10;
  
  local_88 = (double)CONCAT44(local_88._4_4_,param_8);
  uVar20 = param_7;
  local_d0 = param_3_00;
  local_cc = param_2;
  local_b8 = param_3;
  uStack_b0 = in_XMM0_Dc;
  uStack_ac = in_XMM0_Dd;
  local_40 = (double)OClipFireParams::StartType(param_11);
  uVar20 = uVar20 & 0xffffffffffffff00;
  if (param_9 == 1 && (int)param_7 < 0) goto LAB_0012abb1;
  local_50 = (double)CONCAT44(local_50._4_4_,(int)param_7);
  this_01 = (OClipFireEvent *)(param_5 + 0x100);
  cVar5 = OClipFireEvent::IsScheduled(this_01);
  local_128 = param_6;
  if (cVar5 != '\0') {
    uVar8 = OClipFireEvent::NeedStopGateOrToggle(this_01);
    uVar21 = uVar8;
    if (-1 < local_50._0_4_) goto LAB_0012acc2;
LAB_0012ac98:
    bVar6 = (byte)uVar21;
    bVar19 = false;
    local_34 = 0;
    local_8c = 0;
    local_a8 = (double)((ulong)local_a8 & 0xffffffff00000000);
    iVar14 = local_50._0_4_;
    goto LAB_0012ae9f;
  }
  uVar21 = 0;
  uVar8 = 0;
  if (local_50._0_4_ < 0) goto LAB_0012ac98;
LAB_0012acc2:
  local_80 = (double)CONCAT44(local_80._4_4_,uVar8);
  local_c8 = (OClipAutomation *)
             OClipTimeable::ClipAutomation
                       (*(OClipTimeable **)
                         (*(long *)(param_5 + 0x18) + 0xa0 +
                         (ulong)*(byte *)(*(long *)(param_5 + 0x18) + 0xb0) * 8),local_50._0_4_);
  if ((*(long *)(local_c8 + 0x50) == 0) || (*(int *)(local_c8 + 0x20) < 2)) {
    iVar14 = 4;
    if (local_c8[0x39] == (OClipAutomation)0x0) goto LAB_0012abb1;
  }
  else {
    iVar14 = *(int *)(*(long *)(local_c8 + 0x50) + 0x48);
    if (iVar14 == 5) goto LAB_0012abb1;
  }
  iVar15 = iVar14;
  if (SUB84(local_40,0) == 3) {
    iVar15 = 3;
  }
  bVar19 = false;
  if (SUB84(local_40,0) - 1U < 2) {
    iVar15 = 0;
  }
  iVar18 = iVar15;
  if (local_b8 != DAT_015bf380) {
    iVar18 = 0;
  }
  if (NAN(local_b8) || NAN(DAT_015bf380)) {
    iVar18 = 0;
  }
  if (iVar14 == 4) {
    iVar18 = iVar15;
  }
  pOVar17 = this_01;
  local_58 = param_5;
  cVar5 = OClipFireEvent::IsScheduled(this_01);
  if (cVar5 != '\0') {
    iVar14 = OClipFireEvent::AutomationIndex(this_01);
    bVar19 = iVar14 == local_50._0_4_;
    pOVar17 = this_01;
  }
  param_5 = local_58;
  iVar15 = *(int *)(*(long *)(local_58 + 0x18) + 0x70);
  iVar14 = local_50._0_4_;
  switch(iVar18) {
  case 0:
  case 4:
    if (param_9 == 1) goto LAB_0012abb1;
    goto LAB_0012adf6;
  case 1:
    if (param_9 == 1) {
      if (iVar15 != local_50._0_4_ && !bVar19) goto LAB_0012b73a;
      goto LAB_0012ae1a;
    }
LAB_0012adf6:
    bVar19 = false;
    local_34 = 0;
    local_a8 = (double)((ulong)local_a8._4_4_ << 0x20);
    break;
  case 2:
    if (param_9 == 1) goto LAB_0012b73a;
LAB_0012ae1a:
    local_34 = (uint)CONCAT71((int7)((ulong)pOVar17 >> 8),iVar15 == local_50._0_4_);
    local_a8 = (double)((ulong)local_a8._4_4_ << 0x20);
    break;
  case 3:
    if (param_9 == 1) {
      FUN_0012b860(param_1);
      *(int *)((long)param_1 + 4) = iVar14;
      *(int *)param_1 = SUB84(local_40,0);
      goto LAB_0012afdc;
    }
    local_a8 = (double)CONCAT44(local_a8._4_4_,(int)CONCAT71((uint7)(uint3)((uint)iVar15 >> 8),1));
    bVar19 = false;
    local_34 = 0;
    break;
  default:
    bVar19 = false;
    local_34 = 0;
    local_a8 = (double)((ulong)local_a8._4_4_ << 0x20);
  }
  pOVar12 = (OTrackRecordManager *)
            OTrack::TrackRecordManager(*(OTrack **)(*(long *)(local_58 + 0x18) + 0x20));
  pOVar11 = (OScheduler *)(**(code **)(*(long *)param_5 + 0x28))(param_5);
  lVar9 = OScheduler::CurrentStatus(pOVar11);
  uVar20 = 0;
  local_8c = OTrackRecordManager::SlotFireWillStartRecord
                       (pOVar12,local_c8,param_10,*(bool *)(lVar9 + 0xa0),(bool)param_11[0x24]);
  bVar6 = SUB81(local_80,0);
LAB_0012ae9f:
  uVar21 = (undefined4)CONCAT71((int7)(uVar20 >> 8),1);
  if (((SUB84(local_40,0) & 0xfffffffe) == 2) &&
     (*(int *)(*(long *)(param_5 + 0x18) + 0x70) != iVar14)) {
    cVar5 = OClipFireParams::AllowScrubToOtherClip(param_11);
    if (cVar5 == '\0') goto LAB_0012abb1;
    uVar21 = 0;
  }
  local_41 = (byte)local_34 | bVar6;
  if (((~bVar19 | local_41) & 1) == 0) {
    param_1[1] = 0x7fefffffffffffff;
    *(undefined2 *)(param_1 + 2) = 0;
    *(undefined1 *)((long)param_1 + 0x12) = 0;
    uVar1 = CONCAT44(_UNK_015bef04,_DAT_015bef00);
    uVar4 = CONCAT44(_UNK_015bef0c,_UNK_015bef08);
    param_1[3] = uVar1;
    param_1[4] = uVar4;
    param_1[5] = uVar1;
    param_1[6] = uVar4;
    param_1[7] = 0;
    param_1[8] = 0;
    param_1[9] = 0x7fefffffffffffff;
    *(undefined4 *)(param_1 + 10) = 0;
    *(undefined1 *)((long)param_1 + 0x54) = 0;
    param_1[0xb] = DAT_015cd3b0;
    *(undefined4 *)(param_1 + 0xc) = 0;
    param_1[0xd] = uVar1;
    param_1[0xe] = uVar4;
    param_1[0xf] = 0x7fefffffffffffff;
    *(undefined4 *)(param_1 + 0x10) = 0x80000000;
    *(undefined1 *)((long)param_1 + 0x84) = 0;
    param_1[0x11] = 0;
    *(undefined1 *)(param_1 + 0x12) = 0;
    *(int *)((long)param_1 + 4) = local_50._0_4_;
    *(undefined4 *)param_1 = 0xffffffff;
LAB_0012afdc:
    *(undefined1 *)((long)param_1 + 0x53) = 1;
    *(undefined1 *)(param_1 + 10) = 1;
    return param_1;
  }
  local_c8 = (OClipAutomation *)CONCAT44(local_c8._4_4_,uVar21);
  lVar9 = *(long *)(param_5 + 0x18);
  iVar14 = *(int *)(lVar9 + 0x70);
  lVar9 = OClipTimeable::ClipAutomation
                    (*(OClipTimeable **)(lVar9 + 0xa0 + (ulong)*(byte *)(lVar9 + 0xb0) * 8),iVar14);
  local_80 = (double)CONCAT44(local_80._4_4_,iVar14);
  if ((iVar14 < 0) || (*(int *)(lVar9 + 0x20) < 2)) {
    local_58 = (OAsyncClipFireManager *)0x0;
  }
  else {
    local_58 = *(OAsyncClipFireManager **)(*(long *)(lVar9 + 0x40) + 8);
  }
  iVar14 = local_50._0_4_;
  if ((bVar19 & bVar6) != 0) {
    iVar14 = -2;
  }
  if ((char)local_34 != '\0') {
    iVar14 = -2;
  }
  auVar27 = OClipTimeable::ClipAutomation
                      (*(OClipTimeable **)
                        (*(long *)(param_5 + 0x18) + 0xa0 +
                        (ulong)*(byte *)(*(long *)(param_5 + 0x18) + 0xb0) * 8),iVar14);
  lVar10 = auVar27._0_8_;
  local_50 = (double)CONCAT44(local_50._4_4_,iVar14);
  iVar15 = local_40._0_4_;
  if ((iVar14 < 0) || (*(int *)(lVar10 + 0x20) < 2)) {
    local_c0 = (OAsyncClipFireManager *)0x0;
  }
  else {
    local_c0 = *(OAsyncClipFireManager **)(*(long *)(lVar10 + 0x40) + 8);
  }
  if (((local_40._0_4_ == 1) && (local_c0 != local_58)) ||
     ((local_40._0_4_ != 0 && (local_c0 == (OAsyncClipFireManager *)0x0)))) {
LAB_0012abb1:
    param_1[2] = 0;
    param_1[3] = 0;
    param_1[4] = 0;
    param_1[5] = 0;
    param_1[6] = 0;
    param_1[7] = 0;
    param_1[8] = 0;
    param_1[9] = 0;
    param_1[10] = 0;
    param_1[0xb] = 0;
    param_1[0x10] = 0;
    param_1[0x11] = 0;
    param_1[0xe] = 0;
    param_1[0xf] = 0;
    param_1[0xc] = 0;
    param_1[0xd] = 0;
    param_1[0x12] = 0;
    *param_1 = 0x80000000ffffffff;
    param_1[1] = 0x7fefffffffffffff;
    *(undefined1 *)((long)param_1 + 0x11) = 0;
    uVar1 = CONCAT44(_UNK_015bef04,_DAT_015bef00);
    uVar4 = CONCAT44(_UNK_015bef0c,_UNK_015bef08);
    param_1[3] = uVar1;
    param_1[4] = uVar4;
    param_1[5] = uVar1;
    param_1[6] = uVar4;
    param_1[7] = 0;
    param_1[8] = 0;
    param_1[9] = 0x7fefffffffffffff;
    *(undefined4 *)(param_1 + 10) = 0;
    *(undefined1 *)((long)param_1 + 0x54) = 0;
    param_1[0xb] = DAT_015cd3b0;
    param_1[0xd] = uVar1;
    param_1[0xe] = uVar4;
    param_1[0xf] = 0x7fefffffffffffff;
    *(undefined4 *)(param_1 + 0x10) = 0x80000000;
    param_1[0x11] = 0;
    return param_1;
  }
  if (iVar14 == -2) {
    bVar6 = 1;
    local_5c = 0;
  }
  else {
    bVar6 = ((byte)local_8c ^ 1) & *(int *)(lVar10 + 0x20) < 2;
    local_5c = 0;
    if ((-1 < iVar14) && (1 < *(int *)(lVar10 + 0x20))) {
      local_5c = (uint)CONCAT71(auVar27._9_7_,
                                -1 < local_80._0_4_ & *(byte *)(*(long *)(lVar10 + 0x50) + 0x58) |
                                (byte)param_11[0x24]);
    }
  }
  uVar20 = -(ulong)(DAT_015bf380 == local_b8);
  local_78._8_8_ = 0;
  local_78._0_8_ = uVar20;
  uVar16 = local_34 & 0xff;
  local_34 = CONCAT31(local_34._1_3_,bVar6);
  local_88 = (double)CalcLaunchQuantization
                               (param_5,(ulong)local_88 & 0xff,(ulong)local_80 & 0xffffffff,lVar9,
                                lVar10,(ulong)local_40 & 0xffffffff,*(undefined4 *)(param_11 + 0x20)
                                ,(uint)uVar20 & 1,bVar6,uVar16);
  uVar21 = (undefined4)lVar9;
  dVar24 = local_88;
  if (iVar15 == 3) {
    dVar24 = *(double *)(param_11 + 0x10);
  }
  local_80 = 0.0;
  if ((local_5c & 1) == 0) {
    local_80 = dVar24;
  }
  if ((char)local_a8 == '\0') {
    local_80 = 0.0;
  }
  pOVar11 = (OScheduler *)(**(code **)(*(long *)param_5 + 0x28))(param_5);
  local_120 = (TStatus *)OScheduler::CurrentStatus(pOVar11);
  local_a8 = *(double *)(local_120 + 0x70);
  uStack_a0 = 0;
  auVar27._4_4_ = -(uint)(local_a8 == _UNK_015bdfd8);
  auVar27._0_4_ = -(uint)(local_a8 == _DAT_015bdfd0);
  auVar27._8_4_ = -(uint)(_DAT_015bdfc0 == local_a8);
  auVar27._12_4_ = -(uint)(_UNK_015bdfc8 == local_a8);
  iVar14 = movmskps(uVar21,auVar27);
  if (iVar14 == 0) {
    auVar3._8_8_ = 0;
    auVar3._0_8_ = (double)((ulong)(DAT_015bdfe0 *
                                    *(double *)(&DAT_015bbab0 + (ulong)(0.0 <= local_a8) * 8) *
                                    _DAT_015bad48 + local_a8) & _DAT_015bad30) * DAT_015bdfe8;
    auVar27 = roundsd(ZEXT816(0),auVar3,9);
    uStack_a0 = auVar27._8_8_;
    local_a8 = (auVar27._0_8_ / DAT_015bdfe8) *
               *(double *)(&DAT_015bbab0 + (ulong)(0.0 <= local_a8) * 8);
  }
  auVar25._0_8_ = ~local_78._0_8_ & (ulong)local_b8;
  auVar25._8_8_ = ~local_78._8_8_ & CONCAT44(uStack_ac,uStack_b0);
  auVar2._8_4_ = (int)(local_78._8_8_ & uStack_a0);
  auVar2._0_8_ = local_78._0_8_ & (ulong)local_a8;
  auVar2._12_4_ = (int)((local_78._8_8_ & uStack_a0) >> 0x20);
  auVar26 = auVar25 | auVar2;
  if (0.0 < local_88) {
    uVar1 = TTimeSignatureChange::NextQuantizationTime(auVar26._0_4_,local_120 + 0x38,1);
    auVar26._12_4_ = extraout_XMM0_Dd;
    auVar26._8_4_ = extraout_XMM0_Dc;
    auVar26._0_8_ = uVar1;
  }
  local_1ef = local_40._0_4_ != 0 & (byte)local_c8;
  local_200 = 0xffffffff;
  local_1f0 = 0;
  uStack_1c8 = 0;
  uStack_1c0 = 0;
  local_1b8 = 0x7fefffffffffffff;
  local_1ac = local_41 & 1;
  local_1fc = local_50._0_4_;
  local_1f8 = local_80;
  local_1ee = (char)local_34;
  local_1e8 = 0;
  local_1e0 = auVar26._0_8_;
  local_1d0 = 1.79769313486232e+308;
  local_1b0 = (uint)CONCAT11(local_b8 != DAT_015bf380 & param_10,param_10) << 8;
  local_1a8 = local_cc;
  local_1a4 = local_d0;
  local_170 = param_11[0x30];
  local_1a0 = *(undefined8 *)param_11;
  uStack_198 = *(undefined8 *)(param_11 + 8);
  local_190 = *(undefined8 *)(param_11 + 0x10);
  uStack_188 = *(undefined8 *)(param_11 + 0x18);
  local_180 = *(undefined8 *)(param_11 + 0x20);
  lStack_178 = *(long *)(param_11 + 0x28);
  local_1d8 = local_1e0;
  local_78 = auVar26;
  iVar14 = OClipFireParams::StartType(param_11);
  this = local_128;
  local_1a0 = CONCAT44(local_1a0._4_4_,iVar14);
  if (iVar14 == 1) {
    uStack_1c0 = uStack_198;
  }
  if ((lStack_178 != 0) &&
     (this_00 = (OTrack *)OHandleObject::SByHandle(), this_00 != (OTrack *)0x0)) {
    local_1b8 = OTrack::ClipAutomationOffset(this_00);
  }
  FUN_0012b9b0(local_168,&local_200,*(undefined8 *)(param_5 + 0x18));
  if (local_130 == '\0') goto LAB_0012b73a;
  if ((local_b8 != DAT_015bf380) || (NAN(local_b8) || NAN(DAT_015bf380))) {
LAB_0012b414:
    local_50 = (double)RequestedPredelaySongBeatForClip
                                 (param_5,(OClip *)local_58,(OClip *)local_c0,
                                  (bool)((byte)uVar20 & 1));
    if ((double)local_78._0_8_ - local_a8 < local_50) {
      local_b8 = (double)local_78._0_8_ - local_a8;
      cVar5 = SongWasPlayingBeforeCurrentSample(param_5);
      if (cVar5 == '\0') {
        uVar21 = SUB84(local_b8,0);
        uVar8 = (undefined4)((ulong)local_b8 >> 0x20);
        goto LAB_0012b494;
      }
      if ((local_88 != 0.0) || (NAN(local_88))) {
        local_78._0_8_ = (double)local_78._0_8_ + local_88;
      }
      else {
        local_50 = local_b8;
      }
    }
  }
  else {
    pOVar12 = (OTrackRecordManager *)
              OTrack::TrackRecordManager(*(OTrack **)(*(long *)(param_5 + 0x18) + 0x20));
    bVar6 = OTrackRecordManager::IsSlotRecording(pOVar12);
    if (((bVar6 | (byte)local_8c) & 1) == 0) goto LAB_0012b414;
    uVar21 = 0;
    uVar8 = 0;
LAB_0012b494:
    local_50 = (double)CONCAT44(uVar8,uVar21);
  }
  if ((dStack_140 != DAT_015bf380) || (NAN(dStack_140) || NAN(DAT_015bf380))) {
    if ((this == (OClipPreload *)0x0) || (local_40._0_4_ == 0 && (char)local_5c == '\0'))
    goto LAB_0012b657;
    local_40 = dStack_140;
    plVar13 = (long *)OClipTimeable::Sequencer
                                (*(OClipTimeable **)
                                  (*(long *)(param_5 + 0x18) + 0xa0 +
                                  (ulong)*(byte *)(*(long *)(param_5 + 0x18) + 0xb0) * 8));
    cVar5 = (**(code **)(*plVar13 + 0x18))(plVar13);
    if (cVar5 != '\0') goto LAB_0012b65c;
    OClipPreload::OClipPreload((OClipPreload *)local_118,(OClip *)local_c0,local_168,local_40);
    OClipPreload::operator=(this,(OClipPreload *)local_118);
    OClipPreload::~OClipPreload((OClipPreload *)local_118);
    cVar5 = SongWasPlayingBeforeCurrentSample(param_5);
    if (cVar5 != '\0') {
      uVar21 = local_78._0_4_;
      uVar8 = local_78._4_4_;
      uVar22 = local_78._8_4_;
      uVar23 = local_78._12_4_;
      if (((byte)local_5c & local_88 == 0.0) == 0) {
        OClipPreload::EnsureEnoughTime(this,local_78._0_8_,local_88,local_120);
        FUN_0012b920(local_118);
        if ((local_118[0] != local_78._0_8_) ||
           (uVar21 = local_78._0_4_, uVar8 = local_78._4_4_, uVar22 = local_78._8_4_,
           uVar23 = local_78._12_4_, NAN(local_118[0]) || NAN(local_78._0_8_))) {
          local_1d8 = local_118[0] - local_50;
          local_40 = local_118[0];
          local_1e0 = local_118[0];
          local_1d0 = (double)CONCAT44(_UNK_015bef04,_DAT_015bef00);
          uStack_1c8 = CONCAT44(_UNK_015bef0c,_UNK_015bef08);
          local_1b0 = local_1b0 & 0xffffff00;
          FUN_0012b9b0(local_118,&local_200,*(undefined8 *)(param_5 + 0x18));
          if (local_130 == local_e0) {
            if (local_130 == '\0') {
LAB_0012b73a:
              param_1[0x10] = 0;
              param_1[0x11] = 0;
              param_1[0xe] = 0;
              param_1[0xf] = 0;
              param_1[0xc] = 0;
              param_1[0xd] = 0;
              param_1[10] = 0;
              param_1[0xb] = 0;
              param_1[8] = 0;
              param_1[9] = 0;
              param_1[6] = 0;
              param_1[7] = 0;
              param_1[4] = 0;
              param_1[5] = 0;
              param_1[2] = 0;
              param_1[3] = 0;
              *param_1 = 0;
              param_1[1] = 0;
              param_1[0x12] = 0;
              FUN_0012b860(param_1);
              return param_1;
            }
          }
          else {
            if (local_130 != '\0') {
              local_130 = '\0';
              goto LAB_0012b73a;
            }
            local_130 = '\x01';
          }
          local_138 = local_e8;
          dStack_140 = dStack_f0;
          local_150 = (undefined1)uStack_100;
          OClipPreload::OClipPreload
                    ((OClipPreload *)local_118,(OClip *)local_c0,local_168,dStack_f0);
          OClipPreload::operator=(this,(OClipPreload *)local_118);
          OClipPreload::~OClipPreload((OClipPreload *)local_118);
          OClipPreload::AssertEnoughTime(local_40,(TStatus *)this);
          uVar21 = SUB84(local_40,0);
          uVar8 = (int)((ulong)local_40 >> 0x20);
          uVar22 = 0;
          uVar23 = 0;
        }
      }
      goto LAB_0012b6ae;
    }
  }
  else {
LAB_0012b657:
    if (this != (OClipPreload *)0x0) {
LAB_0012b65c:
      dStack_f0 = 0.0;
      local_118[0] = 0.0;
      local_118[1] = 0.0;
      local_118[2] = (double)CONCAT44(_UNK_015bef04,_DAT_015bef00);
      uStack_100 = CONCAT44(_UNK_015bef0c,_UNK_015bef08);
      local_f8 = 0x7fefffffffffffff;
      local_e8 = 0x7fefffffffffffff;
      OClipPreload::operator=(this,(OClipPreload *)local_118);
      OClipPreload::~OClipPreload((OClipPreload *)local_118);
    }
  }
  uVar21 = local_78._0_4_;
  uVar8 = local_78._4_4_;
  uVar22 = local_78._8_4_;
  uVar23 = local_78._12_4_;
LAB_0012b6ae:
  dVar24 = (double)CONCAT44(uVar8,uVar21) - local_50;
  if (dVar24 <= local_a8) {
    uVar7 = 1;
    if (local_1ee == '\0') {
      local_78._4_4_ = uVar8;
      local_78._0_4_ = uVar21;
      local_78._8_4_ = uVar22;
      local_78._12_4_ = uVar23;
      local_40 = dVar24;
      uVar7 = SongWasPlayingBeforeCurrentSample(param_5);
      uVar21 = local_78._0_4_;
      uVar8 = local_78._4_4_;
      dVar24 = local_40;
    }
  }
  else {
    uVar7 = 0;
  }
  local_1e0 = (double)CONCAT44(uVar8,uVar21);
  local_1d0 = dStack_140;
  uStack_1c8 = local_138;
  local_1b0 = CONCAT31(local_1b0._1_3_,uVar7);
  local_1d8 = dVar24;
  _memcpy(param_1,&local_200,0x98);
  return param_1;
}


