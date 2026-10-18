
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */
/* SUseEngineCodeGeneration() */

undefined4 SUseEngineCodeGeneration(void)

{
  undefined4 uVar1;
  byte extraout_DL;
  undefined8 local_48;
  undefined8 uStack_40;
  undefined8 local_38;
  undefined8 uStack_30;
  undefined8 local_20;
  byte local_18;
  
  local_38 = _DAT_015be51c;
  uStack_30 = _UNK_015be524;
  local_48 = _DAT_015be50c;
  uStack_40 = _UNK_015be514;
  uVar1 = ableton::system::runningOnNativeArch();
  local_20 = ADebugOptions::GetOption((TDebugOptionHash *)&local_48);
  if ((extraout_DL & 1) != 0) {
    local_18 = extraout_DL;
    uVar1 = TDebugOption::Parameter((TDebugOption *)&local_20,1,SUB41(uVar1,0));
  }
  return uVar1;
}

