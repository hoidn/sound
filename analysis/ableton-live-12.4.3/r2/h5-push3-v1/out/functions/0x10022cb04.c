// 0x10022cb04 FUN_10022cb04 state=exported-with-warnings role=MIDI bytes + 8-byte value, send
// source chunk chunk-00096.jsonl; code_sha256=aeca51e3062b51bc2d7dd7a30b85d85a2050d5f5daeeaa7bcddfd980a166e56c

void FUN_10022cb04(undefined8 *param_1,long param_2,undefined8 param_3)

{
  ulong uVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  ulong uVar4;
  ulong uVar5;
  undefined8 *local_78;
  undefined8 *local_70;
  long local_68;
  undefined8 **ppuStack_60;
  undefined8 **local_58;
  
  local_78 = (undefined8 *)0x0;
  local_70 = (undefined8 *)0x0;
  local_68 = 0;
  local_78 = operator_new(0xb);
  local_68 = (long)local_78 + 0xb;
  ppuStack_60 = &local_78;
  local_70 = local_78;
  if (*(uint *)(param_2 + 0x18) == 0xffffffff) {
                    /* WARNING: Subroutine does not return */
    FUN_100180824();
  }
  local_58 = &ppuStack_60;
  (*(code *)(&
            PTR___dispatch_abi_ne190102_<std::__variant_detail::__visitation::__variant::__value_visitor<ableton::midi::io::getBytesFromMessage<std::variant<ableton::midi::io::NoteOn,ableton::midi::io::NoteOff,ableton::midi::io::Aftertouch,ableton::midi::io::ControlChange,ableton::midi::io::ProgramChange,ableton::midi::io::ChannelPressure,ableton::midi::io::PitchBend,ableton::midi::io::CommonMTCQuarterFrame,ableton::midi::io::CommonSongPosition,ableton::midi::io::CommonSongSelect,ableton::midi::io::CommonTuneRequest,ableton::midi::io::SysEx,ableton::midi::io::RealtimeMessage<(unsigned_char)250>,ableton::midi::io::RealtimeMessage<(unsigned_char)251>,ableton::midi::io::RealtimeMessage<(unsigned_char)252>,ableton::midi::io::RealtimeMessage<(unsigned_char)248>,ableton::midi::io::RealtimeMessage<(unsigned_char)255>>,std::back_insert_iterator<std::vector<unsigned_char,std::allocator<unsigned_char>>>>(std::variant<ableton::midi::io::NoteOn,ableton::midi::io::NoteOff,ableton::midi::io::Aftertouch,ableton::mid___::RealtimeMessage<(unsigned_char)248>,ableton::midi::io::RealtimeMessage<(unsigned_char)255>>const&>_101bd49b0
            )[*(uint *)(param_2 + 0x18)])(&local_58,param_2);
  puVar2 = local_78;
  uVar5 = (long)local_70 - (long)local_78;
  uVar1 = uVar5 + 8;
  if (uVar5 < 0xfffffffffffffff8) {
    if ((ulong)(local_68 - (long)local_70) < 8) {
      if ((long)uVar1 < 0) {
                    /* WARNING: Subroutine does not return */
        FUN_1001809dc(&local_78);
      }
      uVar4 = (local_68 - (long)local_78) * 2;
      if (uVar4 < uVar1 || uVar4 - uVar1 == 0) {
        uVar4 = uVar1;
      }
      if (0x3ffffffffffffffe < (ulong)(local_68 - (long)local_78)) {
        uVar4 = 0x7fffffffffffffff;
      }
      puVar3 = operator_new(uVar4);
      *(undefined8 *)((long)puVar3 + uVar5) = 0;
      _memcpy(puVar3,puVar2,uVar5);
      local_78 = puVar3;
      local_70 = (undefined8 *)((long)puVar3 + uVar1);
      local_68 = (long)puVar3 + uVar4;
      if (puVar2 != (undefined8 *)0x0) {
        operator_delete(puVar2);
      }
    }
    else {
      *local_70 = 0;
      local_70 = local_70 + 1;
    }
  }
  else {
    local_70 = (undefined8 *)((long)local_78 + uVar1);
  }
  *(undefined8 *)((long)local_78 + uVar5) = param_3;
  (**(code **)(*(long *)*param_1 + 0x18))((long *)*param_1,&local_78,0);
  if (local_78 != (undefined8 *)0x0) {
    local_70 = local_78;
    operator_delete(local_78);
  }
  return;
}

