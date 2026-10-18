
/* OReWireMemoryInitializer::Open() */

byte __thiscall OReWireMemoryInitializer::Open(OReWireMemoryInitializer *this)

{
  undefined4 *puVar1;
  OReWireMemoryInitializer OVar2;
  undefined4 *puVar3;
  bool bVar4;
  
  OVar2 = *this;
  if (OVar2 == (OReWireMemoryInitializer)0x0) {
    puVar3 = operator_new(0x10);
    *puVar3 = 0xffffffff;
    *(char **)(puVar3 + 2) = "RootUnit.SetSampleRateReWireHost";
    puVar1 = DAT_017bbef8;
    bVar4 = DAT_017bbef8 != (undefined4 *)0x0;
    DAT_017bbef8 = puVar3;
    if (bVar4) {
      operator_delete(puVar1);
    }
    OVar2 = (OReWireMemoryInitializer)OObject::SInit<true>(true);
    *this = OVar2;
    if ((bool)OVar2) {
      OceanEngineInitO();
      OceanSongInitO();
      OceanProcessorInitO();
      OceanMidiInitO();
      OceanMidiSyncInitO();
      OceanSampleInitO();
      OceanPluginInitO();
      OProcessorManager::SCommitRegistryO();
      _atexit(SClose);
      OVar2 = *this;
    }
    else {
      OVar2 = (OReWireMemoryInitializer)0x0;
    }
  }
  return (byte)OVar2 & 1;
}

