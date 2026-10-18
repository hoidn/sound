// 0x3b320 _RWDEFSetAudioInfo | undefined _RWDEFSetAudioInfo() | state=exported | chunk-00008.jsonl

void _RWDEFSetAudioInfo(long param_1)

{
  TRegister local_14 [4];
  
  AThreadManager::TRegister::TRegister(local_14,0x200600);
  FUN_0003b020(*(undefined4 *)(param_1 + 4),*(undefined4 *)(param_1 + 8));
  AThreadManager::TRegister::~TRegister(local_14);
  return;
}

