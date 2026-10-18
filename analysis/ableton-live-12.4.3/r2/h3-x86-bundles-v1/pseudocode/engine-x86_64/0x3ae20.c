// 0x3ae20 _RWDEFOpenDevice | undefined _RWDEFOpenDevice() | state=exported-with-warnings | chunk-00007.jsonl

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 _RWDEFOpenDevice(long param_1)

{
  char cVar1;
  int iVar2;
  OEngineReWireData *this;
  undefined8 uVar3;
  TRegister local_1c [4];
  
  AThreadManager::TRegister::TRegister(local_1c,0x200600);
  cVar1 = OEngineReWireData::SIsReWireDeviceEnabled();
  uVar3 = 5;
  if (cVar1 == '\0') goto LAB_0003aff7;
  if (OReWireMemoryInitializer::sInstance == '\0') {
    this = (OEngineReWireData *)OEngineReWireData::SInstance();
    iVar2 = OEngineReWireData::NumReWireOutputChannels(this);
    if (iVar2 == 0) goto LAB_0003aff7;
    cVar1 = OReWireMemoryInitializer::Open
                      ((OReWireMemoryInitializer *)&OReWireMemoryInitializer::sInstance);
    if (cVar1 == '\0') goto LAB_0003aff7;
    OEngine::SSetRequestCallbacks
              (FUN_0003be00,0,FUN_0003be10,0,FUN_0003be20,0,0x3be40,0,FUN_0003be60,0,FUN_0003be80,0)
    ;
  }
  FUN_0003b020(*(undefined4 *)(param_1 + 8),*(undefined4 *)(param_1 + 0xc));
  _DAT_017bbf04 = 1;
  _DAT_017bc308 = 0;
  uRam00000000017bc310 = 0;
  _DAT_017bc318 = 0;
  uRam00000000017bc320 = 0;
  _DAT_017bc328 = 0;
  uRam00000000017bc330 = 0;
  _DAT_017bc338 = 0;
  uRam00000000017bc340 = 0;
  _DAT_017bc348 = 0;
  uRam00000000017bc350 = 0;
  _DAT_017bc358 = 0;
  uRam00000000017bc360 = 0;
  _DAT_017bc368 = 0;
  uRam00000000017bc370 = 0;
  _DAT_017bc378 = 0;
  uRam00000000017bc380 = 0;
  _DAT_017bc388 = 0;
  uRam00000000017bc390 = 0;
  _DAT_017bc398 = 0;
  uRam00000000017bc3a0 = 0;
  _DAT_017bc3a8 = 0;
  uRam00000000017bc3b0 = 0;
  _DAT_017bc3b8 = 0;
  uRam00000000017bc3c0 = 0;
  _DAT_017bc3c8 = 0;
  uRam00000000017bc3d0 = 0;
  _DAT_017bc3d8 = 0;
  uRam00000000017bc3e0 = 0;
  _DAT_017bc3e8 = 0;
  uRam00000000017bc3f0 = 0;
  _DAT_017bc3f8 = 0;
  uRam00000000017bc400 = 0;
  _DAT_017bbf08 = 0;
  uRam00000000017bbf10 = 0;
  _DAT_017bbf18 = 0;
  uRam00000000017bbf20 = 0;
  _DAT_017bbf28 = 0;
  uRam00000000017bbf30 = 0;
  _DAT_017bbf38 = 0;
  uRam00000000017bbf40 = 0;
  _DAT_017bbf48 = 0;
  uRam00000000017bbf50 = 0;
  _DAT_017bbf58 = 0;
  uRam00000000017bbf60 = 0;
  _DAT_017bbf68 = 0;
  uRam00000000017bbf70 = 0;
  _DAT_017bbf78 = 0;
  uRam00000000017bbf80 = 0;
  _DAT_017bbf88 = 0;
  uRam00000000017bbf90 = 0;
  _DAT_017bbf98 = 0;
  uRam00000000017bbfa0 = 0;
  _DAT_017bbfa8 = 0;
  uRam00000000017bbfb0 = 0;
  _DAT_017bbfb8 = 0;
  uRam00000000017bbfc0 = 0;
  _DAT_017bbfc8 = 0;
  uRam00000000017bbfd0 = 0;
  _DAT_017bbfd8 = 0;
  uRam00000000017bbfe0 = 0;
  _DAT_017bbfe8 = 0;
  uRam00000000017bbff0 = 0;
  _DAT_017bbff8 = 0;
  uRam00000000017bc000 = 0;
  uVar3 = 1;
LAB_0003aff7:
  AThreadManager::TRegister::~TRegister(local_1c);
  return uVar3;
}

