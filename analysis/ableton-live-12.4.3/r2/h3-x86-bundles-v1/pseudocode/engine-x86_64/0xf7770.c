// 0xf7770 FUN_000f7770 | undefined FUN_000f7770() | state=exported-with-warnings | chunk-00050.jsonl

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_000f7770(void)

{
  TInitThreadManager::TInitThreadManager((TInitThreadManager *)&DAT_017fbb80);
  OSharedMemory::TEnsureExit::TEnsureExit((TEnsureExit *)&DAT_017fbb81);
  ___cxa_atexit(OSharedMemory::TEnsureExit::~TEnsureExit,&DAT_017fbb81,0);
  _DAT_017fbb98 = 0xffffffff;
  _DAT_017fbba0 = "OAudioMemoryAllocator.AddPool";
  OMutex::OMutex((OMutex *)&DAT_017fbbb0,"/ableton.live.omessage-factory");
  ___cxa_atexit(OMutex::~OMutex,&DAT_017fbbb0,0);
  _DAT_017fbbb8 = 0xffffffff;
  _DAT_017fbbc0 = "OMessageTimeCallbackProcessor.MessageTimeProcess";
  _DAT_017fbbc8 = 0xffffffff;
  _DAT_017fbbd0 = "OMessageTimeCallbackProcessor.ScheduleEvent";
  return;
}

