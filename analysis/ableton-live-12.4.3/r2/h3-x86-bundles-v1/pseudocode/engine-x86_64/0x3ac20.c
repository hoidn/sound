// 0x3ac20 _RWDEFGetDeviceNameAndVersion | undefined _RWDEFGetDeviceNameAndVersion() | state=exported-with-warnings | chunk-00007.jsonl

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void _RWDEFGetDeviceNameAndVersion(undefined4 *param_1,char *param_2)

{
  char cVar1;
  OEngineReWireData *this;
  char *pcVar2;
  byte extraout_DL;
  undefined8 local_48;
  undefined8 uStack_40;
  undefined8 local_38;
  undefined8 uStack_30;
  TRegister local_1c [4];
  
  AThreadManager::TRegister::TRegister(local_1c,0x200600);
  *param_1 = 1000000;
  if (DAT_017bbf00 == '\0') {
    ADebugOptions::SInit();
    cVar1 = NTests::SInitialized();
    if (cVar1 == '\0') {
      NTests::SDisable();
    }
    local_38 = _DAT_015bb578;
    uStack_30 = _UNK_015bb580;
    local_48 = _DAT_015bb568;
    uStack_40 = _UNK_015bb570;
    ADebugOptions::GetOption((TDebugOptionHash *)&local_48);
    DAT_01793574 = ~extraout_DL & 1;
    DAT_017bbf00 = '\x01';
  }
  this = (OEngineReWireData *)OEngineReWireData::SInstance();
  pcVar2 = (char *)OEngineReWireData::ReWireDeviceName(this);
  _strncpy(param_2,pcVar2,0x1f);
  AThreadManager::TRegister::~TRegister(local_1c);
  return;
}

