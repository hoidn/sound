
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* OEngineReWireData::DetermineReWireDeviceName() */

void __thiscall OEngineReWireData::DetermineReWireDeviceName(OEngineReWireData *this)

{
  void *pvVar1;
  ulong extraout_RDX;
  ulong uVar2;
  void *pvVar3;
  ulong uVar4;
  undefined8 *puVar5;
  ulong uVar6;
  char *pcVar7;
  long lVar8;
  bool bVar9;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_58;
  undefined8 uStack_50;
  undefined1 local_48 [8];
  undefined8 uStack_40;
  undefined8 *local_38;
  
  if (((byte)*this & 1) == 0) {
    if ((byte)*this >> 1 != 0) {
      return;
    }
  }
  else if (*(long *)(this + 8) != 0) {
    return;
  }
  local_58 = _DAT_015cae98;
  uStack_50 = _UNK_015caea0;
  local_68 = _DAT_015cae88;
  uStack_60 = _UNK_015cae90;
  ADebugOptions::GetOption((TDebugOptionHash *)&local_68);
  pcVar7 = "Ableton Live";
  uVar2 = (ulong)((uint)extraout_RDX & 1);
  uVar6 = uVar2 * 9 + 0x16;
  if ((extraout_RDX & 1) == 0) {
    uStack_40 = 0;
    local_38 = (undefined8 *)0x0;
    local_48._1_7_ = 0;
    local_48[0] = (char)uVar6 * '\x02';
    lVar8 = 0x16;
  }
  else {
    pcVar7 = "Ableton Live (Reason)";
    uVar4 = 0x1a;
    if ((uVar6 | 7) != 0x17) {
      uVar4 = (uVar6 | 7) + 1;
    }
    local_38 = operator_new(uVar4);
    local_48 = (undefined1  [8])(uVar4 + 1);
    lVar8 = 0x1f;
    uStack_40 = uVar6;
  }
  pvVar1 = (void *)((long)local_38 + 10);
  bVar9 = ((ulong)local_48 & 1) != 0;
  puVar5 = (undefined8 *)(local_48 + 1);
  if (bVar9) {
    puVar5 = local_38;
  }
  *puVar5 = 0x656c62617369445b;
  *(undefined2 *)(puVar5 + 1) = 0x5d64;
  pvVar3 = (void *)((long)&uStack_40 + 3);
  if (bVar9) {
    pvVar3 = pvVar1;
  }
  _memcpy(pvVar3,pcVar7,uVar2 * 9 + 0xc);
  *(undefined1 *)((long)puVar5 + lVar8) = 0;
  if (((byte)*this & 1) != 0) {
    operator_delete(*(void **)(this + 0x10));
  }
  *(undefined8 **)(this + 0x10) = local_38;
  *(undefined1 (*) [8])this = local_48;
  *(ulong *)(this + 8) = uStack_40;
  return;
}

