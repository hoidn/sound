// 0x3b3e0 _RWDEFDriveAudio | undefined _RWDEFDriveAudio() | state=exported-with-warnings | chunk-00008.jsonl

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void _RWDEFDriveAudio(long param_1,double param_2)

{
  int iVar1;
  uint uVar2;
  bool bVar3;
  uint uVar4;
  char cVar5;
  int iVar6;
  OEngine *this;
  OReWireMidiInMainProcessor *pOVar7;
  long lVar8;
  undefined2 *puVar9;
  OEngine *this_00;
  ulong uVar10;
  float fVar11;
  double dVar12;
  undefined8 local_98;
  OEngine *local_90;
  uint local_88 [8];
  double local_68;
  TRegister local_5c [4];
  long local_58;
  double local_50;
  uint local_48 [4];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_01727258;
  local_58 = param_1;
  if ((DAT_017bc708 == (OEngine *)0x0) ||
     (this = (OEngine *)OSharedMemory::SStaticPointer(1), this == (OEngine *)0x0)) {
    this_00 = (OEngine *)0x0;
    iVar6 = *(int *)(param_1 + 0x1c);
    if (iVar6 == DAT_017bc710) goto LAB_0003b457;
LAB_0003b4b4:
    lVar8 = param_1 + 0x1c;
    local_50 = (double)((long)param_2 + 0x1c);
    uVar10 = 0;
    local_90 = this_00;
    local_68 = param_2;
    do {
      while ((cVar5 = _ReWireIsBitInBitFieldSet(lVar8,uVar10 & 0xffff), cVar5 == '\0' ||
             (*(long *)(param_1 + 0x3c + uVar10 * 8) == 0))) {
        (&DAT_017bbf08)[uVar10] = 0;
        _ReWireClearBitInBitField(&DAT_017bc710,uVar10 & 0xffff);
        uVar10 = uVar10 + 1;
        if (uVar10 == 0x40) goto LAB_0003b547;
      }
      (&DAT_017bbf08)[uVar10] = 1;
      _ReWireSetBitInBitField(local_50,uVar10 & 0xffff);
      param_1 = local_58;
      _ReWireSetBitInBitField(&DAT_017bc710,uVar10 & 0xffff);
      uVar10 = uVar10 + 1;
    } while (uVar10 != 0x40);
LAB_0003b547:
    bVar3 = false;
    this_00 = local_90;
    param_2 = local_68;
  }
  else {
    cVar5 = OEngine::CheckForDecoupled(this);
    this_00 = (OEngine *)0x0;
    if (cVar5 == '\0') {
      this_00 = this;
    }
    iVar6 = *(int *)(param_1 + 0x1c);
    if (iVar6 != DAT_017bc710) goto LAB_0003b4b4;
LAB_0003b457:
    iVar1 = *(int *)(param_1 + 0x20);
    if (iVar1 != DAT_017bc714) goto LAB_0003b4b4;
    *(int *)((long)param_2 + 0x1c) = iVar6;
    *(int *)((long)param_2 + 0x20) = iVar1;
    bVar3 = true;
  }
  if (this_00 == (OEngine *)0x0) {
    if (*(long *)PTR____stack_chk_guard_01727258 == local_38) {
      OToBufferProcessor::SClearBuffers
                ((TChannelState *)&DAT_017bbf04,(float **)(param_1 + 0x3c),0,
                 *(int *)(param_1 + 0x840));
      return;
    }
    goto LAB_0003ba8f;
  }
  AThreadManager::TRegister::TRegister(local_5c);
  uVar4 = MXCSR;
  local_88[0] = MXCSR;
  MXCSR = MXCSR | 0x8040;
  local_48[0] = MXCSR;
  if (!bVar3) {
    OEngine::SetChannelState(this_00,(TChannelState *)&DAT_017bbf04);
  }
  _fegetenv(local_48);
  iVar6 = *(int *)(local_58 + 0x844);
  local_50 = (double)*(int *)(local_58 + 0x83c) / DAT_015bb428;
  if (iVar6 == 2) {
    dVar12 = (double)OEngine::BeatTime(this_00);
    if ((local_50 != dVar12) || (NAN(local_50) || NAN(dVar12))) {
      OEngine::SetBeatTime(this_00,local_50);
    }
    cVar5 = OEngine::Playing(this_00);
    if (cVar5 == '\0') {
LAB_0003b6ac:
      OEngine::SetPlaying(this_00,true,false);
    }
  }
  else if (iVar6 == 1) {
    cVar5 = OEngine::Playing(this_00);
    dVar12 = (double)OEngine::BeatTime(this_00);
    if (cVar5 == '\0') {
      if ((local_50 != dVar12) || (NAN(local_50) || NAN(dVar12))) {
        OEngine::SetBeatTime(this_00,local_50);
      }
      goto LAB_0003b6ac;
    }
    if (_DAT_015bb430 < (double)((ulong)(local_50 - dVar12) & _DAT_015bad30)) {
      OEngine::SetBeatTime(this_00,local_50);
      OEngine::SetSyncInActivity(this_00);
    }
  }
  else if (iVar6 == 0) {
    cVar5 = OEngine::Playing(this_00);
    if (cVar5 != '\0') {
      OEngine::SetPlaying(this_00,false,false);
    }
    dVar12 = (double)OEngine::BeatTime(this_00);
    if ((local_50 != dVar12) || (NAN(local_50) || NAN(dVar12))) {
      OEngine::SetBeatTime(this_00,local_50);
    }
  }
  uVar2 = *(uint *)(local_58 + 0x84c);
  iVar6 = OEngine::SignatureNumerator(this_00);
  if (((ulong)uVar2 != (long)iVar6) ||
     (uVar2 = *(uint *)(local_58 + 0x850), iVar6 = OEngine::SignatureDenominator(this_00),
     (ulong)uVar2 != (long)iVar6)) {
    local_98 = *(undefined8 *)(local_58 + 0x84c);
    TTimeSignatureChange::TTimeSignatureChange
              ((TTimeSignatureChange *)local_88,(TTimeSignature *)&local_98,0.0,1);
    OEngine::SetTimeSignature(this_00,(TTimeSignatureChange *)local_88);
  }
  local_50 = (double)CONCAT44(local_50._4_4_,(float)*(uint *)(local_58 + 0x848) / DAT_015bb460);
  fVar11 = (float)OEngine::AudioTempo(this_00);
  if ((local_50._0_4_ != fVar11) || (NAN(local_50._0_4_) || NAN(fVar11))) {
    OEngine::SetTempo(this_00,local_50._0_4_,local_50._0_4_);
  }
  iVar6 = *(int *)(local_58 + 0x85c);
  local_50 = (double)*(int *)(local_58 + 0x854) / DAT_015bb428;
  local_68 = (double)(*(int *)(local_58 + 0x858) - *(int *)(local_58 + 0x854)) / DAT_015bb428;
  cVar5 = OEngine::LoopOn(this_00);
  if ((iVar6 != 0) == (bool)cVar5) {
    dVar12 = (double)OEngine::LoopStart(this_00);
    if ((local_50 != dVar12) || (NAN(local_50) || NAN(dVar12))) goto LAB_0003b7dd;
    dVar12 = (double)OEngine::LoopLength(this_00);
    if ((local_68 != dVar12) || (NAN(local_68) || NAN(dVar12))) goto LAB_0003b7dd;
  }
  else {
LAB_0003b7dd:
    OEngine::SetLoopOn(this_00,iVar6 != 0);
    OEngine::SetLoopStart(this_00,local_50);
    OEngine::SetLoopLength(this_00,local_68);
  }
  _fesetenv(local_48);
  pOVar7 = (OReWireMidiInMainProcessor *)OEngine::ReWireMidiInMainProcessor(this_00);
  if (pOVar7 != (OReWireMidiInMainProcessor *)0x0) {
    OReWireMidiInMainProcessor::SetReWireEvents(pOVar7,(ReWireEventBuffer *)(local_58 + 4));
  }
  OEngine::DriveAudio(this_00,(float **)&DAT_017bc770,(float **)(local_58 + 0x3c),
                      *(int *)(local_58 + 0x840),(TTimeReference *)0x0);
  if (DAT_017bc718 == '\x01') {
    _ReWireConvertToRequestStopEvent
              ((ulong)*(uint *)((long)param_2 + 0xc) * 0x18 + *(long *)((long)param_2 + 0x14));
    *(int *)((long)param_2 + 0xc) = *(int *)((long)param_2 + 0xc) + 1;
    DAT_017bc718 = '\0';
  }
  if (DAT_017bc728 == '\x01') {
    lVar8 = _ReWireConvertToRequestRepositionEvent
                      ((ulong)*(uint *)((long)param_2 + 0xc) * 0x18 +
                       *(long *)((long)param_2 + 0x14));
    *(int *)(lVar8 + 4) = (int)((float)DAT_017bc720 * _DAT_015bb464 + DAT_015bab74);
    *(int *)((long)param_2 + 0xc) = *(int *)((long)param_2 + 0xc) + 1;
    DAT_017bc728 = '\0';
  }
  if (DAT_017bc719 == '\x01') {
    _ReWireConvertToRequestPlayEvent
              ((ulong)*(uint *)((long)param_2 + 0xc) * 0x18 + *(long *)((long)param_2 + 0x14));
    *(int *)((long)param_2 + 0xc) = *(int *)((long)param_2 + 0xc) + 1;
    DAT_017bc719 = '\0';
  }
  if (DAT_017bc734 == '\x01') {
    lVar8 = _ReWireConvertToRequestSignatureEvent
                      ((ulong)*(uint *)((long)param_2 + 0xc) * 0x18 +
                       *(long *)((long)param_2 + 0x14));
    *(undefined1 *)(lVar8 + 4) = DAT_017bc72c;
    *(undefined1 *)(lVar8 + 5) = DAT_017bc730;
    *(int *)((long)param_2 + 0xc) = *(int *)((long)param_2 + 0xc) + 1;
    DAT_017bc734 = '\0';
  }
  if (DAT_017bc73c == '\x01') {
    lVar8 = _ReWireConvertToRequestTempoEvent
                      ((ulong)*(uint *)((long)param_2 + 0xc) * 0x18 +
                       *(long *)((long)param_2 + 0x14));
    *(int *)(lVar8 + 4) = (int)(DAT_017bc738 * DAT_015bb460 + DAT_015bab74);
    *(int *)((long)param_2 + 0xc) = *(int *)((long)param_2 + 0xc) + 1;
    DAT_017bc73c = '\0';
  }
  if (DAT_017bc750 == '\x01') {
    lVar8 = _ReWireConvertToRequestLoopEvent
                      ((ulong)*(uint *)((long)param_2 + 0xc) * 0x18 +
                       *(long *)((long)param_2 + 0x14));
    *(undefined1 *)(lVar8 + 0xc) = DAT_017bc73d;
    *(ulong *)(lVar8 + 4) =
         CONCAT44((int)((float)(DAT_017bc748 + DAT_017bc740) * _UNK_015bb444 + DAT_015bb450._4_4_),
                  (int)((float)DAT_017bc740 * _DAT_015bb440 + (float)DAT_015bb450));
    *(int *)((long)param_2 + 0xc) = *(int *)((long)param_2 + 0xc) + 1;
    DAT_017bc750 = '\0';
  }
  if ((DAT_017bc708 != (OEngine *)0x0) &&
     (lVar8 = OEngine::ReWireMidiInMainProcessor(DAT_017bc708), lVar8 != 0)) {
    pOVar7 = (OReWireMidiInMainProcessor *)OEngine::ReWireMidiInMainProcessor(DAT_017bc708);
    cVar5 = OReWireMidiInMainProcessor::EventTargetChanged(pOVar7);
    if (cVar5 != '\0') {
      if (DAT_01793574 == '\x01') {
        puVar9 = (undefined2 *)
                 _ReWireConvertToEventTargetChangedEvent
                           ((ulong)*(uint *)((long)param_2 + 0xc) * 0x18 +
                            *(long *)((long)param_2 + 0x14));
        *puVar9 = 0x65;
        *(undefined8 *)(puVar9 + 1) = 0;
        *(undefined8 *)(puVar9 + 5) = 0;
        *(undefined8 *)(puVar9 + 8) = 0;
        *(int *)((long)param_2 + 0xc) = *(int *)((long)param_2 + 0xc) + 1;
      }
      pOVar7 = (OReWireMidiInMainProcessor *)OEngine::ReWireMidiInMainProcessor(DAT_017bc708);
      OReWireMidiInMainProcessor::ClearEventTargetChanged(pOVar7);
    }
  }
  local_88[0] = MXCSR;
  MXCSR = (uVar4 | 0xffff7fbf) & MXCSR;
  local_48[0] = MXCSR;
  AThreadManager::TRegister::~TRegister(local_5c);
  if (*(long *)PTR____stack_chk_guard_01727258 == local_38) {
    return;
  }
LAB_0003ba8f:
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

