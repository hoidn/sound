// 0x3b120 _RWDEFIdle | undefined _RWDEFIdle() | state=exported | chunk-00008.jsonl

void _RWDEFIdle(void)

{
  int iVar1;
  long lVar2;
  void *pvVar3;
  OEngine *this;
  long local_40;
  OMessage *local_38;
  TRegister local_1c [4];
  
  AThreadManager::TRegister::TRegister();
  lVar2 = OSharedMemory::SStaticPointer(0);
  pvVar3 = (void *)OSharedMemory::SStaticPointer(2);
  if (DAT_017bc760 != (void *)0x0) {
    OQueuePool::ProcessMessages();
  }
  OSharedMemory::SIdle();
  if (DAT_017bc708 == (OEngine *)0x0) {
    if (lVar2 != 0) {
      this = (OEngine *)OEngine::SNew();
      OEngine::SetAudioActivation(this,true);
      OEngine::SetIdleActivation(this,true);
      AThreadManager::TMasquerade::TMasquerade((TMasquerade *)&local_40,0x200600,0x10100);
      OEngine::SetChannelState(this,(TChannelState *)&DAT_017bbf04);
      AThreadManager::TMasquerade::~TMasquerade((TMasquerade *)&local_40);
      OceanSampleInitThread();
      OSharedMemory::SSetStaticPointer(1,this);
      DAT_017bc708 = this;
      OSendThreadMessage::OSendThreadMessage
                ((OSendThreadMessage *)&local_40,DAT_017bbef8,0x200600,0x100500,0);
      iVar1 = OEngine::RootUnitId(DAT_017bc708);
      OMessage::operator<<(local_38,iVar1);
      OMessage::operator<<(local_38,DAT_017bc754);
      OMessage::operator<<(local_38,DAT_017bc758);
      (**(code **)(local_40 + 0x10))(&local_40);
      OSendThreadMessage::~OSendThreadMessage((OSendThreadMessage *)&local_40);
    }
  }
  else if (lVar2 == 0) {
    OceanSampleExitThread();
    OSharedMemory::SSetStaticPointer(1,(void *)0x0);
    DAT_017bc708 = (OEngine *)0x0;
  }
  if (DAT_017bc760 == (void *)0x0) {
    if (pvVar3 != (void *)0x0) {
      OQueuePool::SNew();
      DAT_017bc760 = pvVar3;
      OSharedMemory::SSetStaticPointer(3,pvVar3);
    }
  }
  else if (pvVar3 == (void *)0x0) {
    DAT_017bc760 = (void *)0x0;
    OSharedMemory::SSetStaticPointer(3,(void *)0x0);
  }
  AThreadManager::TRegister::~TRegister(local_1c);
  return;
}

