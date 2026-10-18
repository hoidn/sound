// 0x3ace0 _RWDEFGetDeviceInfo | undefined _RWDEFGetDeviceInfo() | state=exported-with-warnings | chunk-00007.jsonl

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void _RWDEFGetDeviceInfo(long param_1)

{
  int iVar1;
  OEngineReWireData *this;
  byte extraout_DL;
  ushort uVar2;
  ushort uVar3;
  uint uVar4;
  undefined8 local_58;
  undefined8 uStack_50;
  undefined8 local_48;
  undefined8 uStack_40;
  TRegister local_2c [4];
  
  _RWDEFGetDeviceNameAndVersion(&DAT_0000205c + param_1,param_1 + 4);
  AThreadManager::TRegister::TRegister(local_2c,0x200600);
  this = (OEngineReWireData *)OEngineReWireData::SInstance();
  iVar1 = OEngineReWireData::NumReWireOutputChannels(this);
  *(int *)(param_1 + 0x24) = iVar1;
  if (0 < iVar1) {
    uVar3 = 0;
    do {
      _strcpy((char *)((ulong)uVar3 * 0x20 + param_1 + 0x28),
              (char *)((long)&DAT_015bb468 + (long)(int)(&DAT_015bb468)[uVar3]));
      uVar3 = uVar3 + 1;
    } while ((int)(uint)uVar3 < *(int *)(param_1 + 0x24));
  }
  _ReWireSetBitInBitField(&DAT_00002028 + param_1,0);
  _ReWireSetBitInBitField(&DAT_00002028 + param_1,1);
  local_48 = _DAT_015bb598;
  uStack_40 = _UNK_015bb5a0;
  local_58 = _DAT_015bb588;
  uStack_50 = _UNK_015bb590;
  ADebugOptions::GetOption((TDebugOptionHash *)&local_58);
  uVar3 = 1;
  if (((extraout_DL & 1) != 0) ||
     (uVar4 = (uint)(*(int *)(param_1 + 0x24) - (*(int *)(param_1 + 0x24) >> 0x1f)) >> 1,
     uVar3 = (ushort)uVar4, (uVar4 & 0xffff) != 0)) {
    uVar2 = 0;
    do {
      _ReWireSetBitInBitField(&DAT_00002048 + param_1,uVar2);
      uVar2 = uVar2 + 1;
    } while (uVar2 < uVar3);
  }
  *(undefined4 *)(&DAT_00002058 + param_1) = 0x200;
  AThreadManager::TRegister::~TRegister(local_2c);
  return;
}

