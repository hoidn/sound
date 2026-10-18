
bool _RWDEFIsPanelAppLaunched(void)

{
  long lVar1;
  TRegister local_14 [4];
  
  AThreadManager::TRegister::TRegister(local_14,0x200600);
  lVar1 = OSharedMemory::SStaticPointer(0);
  AThreadManager::TRegister::~TRegister(local_14);
  return lVar1 != 0;
}

