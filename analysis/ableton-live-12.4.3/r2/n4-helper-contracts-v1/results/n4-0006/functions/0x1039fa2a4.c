
void FUN_1039fa2a4(void)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  undefined8 in_x7;
  long lVar3;
  long *plVar4;
  long **pplVar5;
  long ***ppplVar6;
  char *local_268;
  long *local_260;
  undefined1 local_251;
  char *local_250;
  long *local_248;
  undefined1 local_239;
  char *local_238;
  undefined8 uStack_230;
  char *local_228;
  undefined8 uStack_220;
  char *local_218;
  undefined8 uStack_210;
  char *local_208;
  undefined8 uStack_200;
  char *local_1f8;
  undefined8 uStack_1f0;
  char *local_1e8;
  undefined8 uStack_1e0;
  char *local_1d8;
  undefined8 uStack_1d0;
  char *local_1c8;
  undefined8 uStack_1c0;
  char *local_1b8;
  undefined8 uStack_1b0;
  long *local_1a8;
  undefined8 uStack_1a0;
  char *local_198;
  undefined8 uStack_190;
  char *local_188;
  undefined8 uStack_180;
  char *local_178;
  undefined8 uStack_170;
  long *local_168;
  long *plStack_160;
  char *local_158;
  long *plStack_150;
  char *local_148;
  long *plStack_140;
  char *local_138;
  long *plStack_130;
  undefined8 local_128;
  long *local_120;
  long *local_118;
  code *local_110;
  undefined8 uStack_108;
  undefined8 local_100;
  long **local_f8;
  long **local_f0;
  long **local_e8;
  long **local_e0;
  char *pcStack_d8;
  long *local_d0;
  char *local_c8;
  long *local_c0;
  undefined8 uStack_b8;
  long *local_b0;
  undefined8 uStack_a8;
  long *local_a0;
  long **local_98;
  undefined1 *puStack_90;
  undefined1 *local_88;
  undefined1 *puStack_80;
  undefined8 local_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined1 auStack_50 [8];
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_1064f8818;
  FUN_103b51c40();
  FUN_103b50844();
  FUN_103b368ec();
  FUN_103be8e38();
  FUN_103b6d044();
  FUN_100e57820(PTR_convert_106510ab0,"17TFunctionProxyPtrI17ATimeToMidiModuleE",
                PTR_get_pytype_impl_10650f418);
  FUN_100e57820(PTR_convert_106510aa8,"17TFunctionProxyPtrI17ANoteRepeatModuleE",
                PTR_get_pytype_impl_10650f410);
  FUN_100e57820(PTR_convert_106510ab8,"17TFunctionProxyPtrI19AFullVelocityModuleE",
                PTR_get_pytype_impl_10650f420);
  FUN_100e57820(PTR_convert_106510ac0,"17TFunctionProxyPtrI21AVelocityLevelsModuleE",
                PTR_get_pytype_impl_10650f428);
  pplVar5 = (long **)((ulong)PTR_s_22APythonPreferenceEntry_1067e4e90 & 0x7fffffffffffffff);
  local_f8 = pplVar5;
  FUN_100e5b814(&local_1a8,"Preferences",1,&local_f8,0);
  FUN_100e57b04(PTR_convertible_1065112d8,PTR_construct_1065112e0,
                "N5boost10shared_ptrI22APythonPreferenceEntryEE",PTR_get_pytype_106512918);
  FUN_100e57b04(PTR_convertible_1065112e8,PTR_construct_1065112f0,
                "NSt3__110shared_ptrI22APythonPreferenceEntryEE",PTR_get_pytype_106512918);
  FUN_100e68898(pplVar5,PTR_execute_1065107b0);
  FUN_100e5c64c(&local_1a8);
  local_98 = (long **)FUN_1025ec99c;
  puStack_90 = (undefined1 *)0x0;
  local_168 = (long *)0x0;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f8 = &local_168;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a11e88(&local_1a8,0,"set_serializer",FUN_1025ec99c,0,&local_f8);
  local_98 = (long **)FUN_1025ec980;
  puStack_90 = (undefined1 *)0x0;
  local_168 = (long *)0x0;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f8 = &local_168;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a121d8(&local_1a8,0,"__bytes__",FUN_1025ec980,0,&local_f8);
  lVar3 = *local_1a8;
  *local_1a8 = lVar3 + -1;
  if (lVar3 + -1 == 0) {
    FUN_101032fbc();
  }
  pplVar5 = (long **)((ulong)PTR_s_17TMidiRemoteScript_1067d9648 & 0x7fffffffffffffff);
  local_f8 = pplVar5;
  FUN_100e5b814(&local_118,"MidiRemoteScript",1,&local_f8,0);
  FUN_100e57b04(PTR_convertible_106511078,PTR_construct_106511080,
                "N5boost10shared_ptrI17TMidiRemoteScriptEE",PTR_get_pytype_106512880);
  FUN_100e57b04(PTR_convertible_106511088,PTR_construct_106511090,
                "NSt3__110shared_ptrI17TMidiRemoteScriptEE",PTR_get_pytype_106512880);
  FUN_100e68898(pplVar5,PTR_execute_106510720);
  FUN_100e5c64c(&local_118);
  local_98 = (long **)FUN_1039fb2d0;
  local_168 = (long *)0x0;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f8 = &local_168;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a128ac(&local_118,0,"song",FUN_1039fb2d0,&local_f8);
  local_98 = (long **)thunk_FUN_10259babc;
  local_168 = (long *)0x0;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f8 = &local_168;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a12c40(&local_118,0,"handle",thunk_FUN_10259babc,&local_f8);
  local_98 = (long **)FUN_1039fb31c;
  local_168 = (long *)0x0;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f8 = &local_168;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a12f10(&local_118,0,"send_midi",FUN_1039fb31c,&local_f8);
  local_98 = (long **)thunk_FUN_10259ba50;
  local_168 = (long *)0x0;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f8 = &local_168;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a13314(&local_118,0,"toggle_lock",thunk_FUN_10259ba50,&local_f8);
  local_98 = (long **)FUN_1039fb76c;
  local_168 = (long *)0x0;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f8 = &local_168;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a13314(&local_118,0,"update_locks",FUN_1039fb76c,&local_f8);
  local_98 = (long **)FUN_1039fb780;
  local_168 = (long *)0x0;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f8 = &local_168;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a13580(&local_118,0,"log_message",FUN_1039fb780,&local_f8);
  local_98 = (long **)FUN_1039fb7f8;
  local_168 = (long *)0x0;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f8 = &local_168;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a13580(&local_118,0,"show_message",FUN_1039fb7f8,&local_f8);
  local_98 = (long **)thunk_FUN_102599ba4;
  local_168 = (long *)0x0;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f8 = &local_168;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a139ac(&local_118,0,"set_cc_translation",thunk_FUN_102599ba4,&local_f8);
  local_98 = (long **)FUN_1039fb998;
  local_168 = (long *)0x0;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f8 = &local_168;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a12f10(&local_118,0,"set_pad_translation",FUN_1039fb998,&local_f8);
  local_98 = (long **)thunk_FUN_10259b34c;
  local_168 = (long *)0x0;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f8 = &local_168;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a139ac(&local_118,0,"set_note_translation",thunk_FUN_10259b34c,&local_f8);
  local_208 = s_track_offset_105c186dc;
  uStack_200 = 0;
  local_218 = "scene_offset";
  uStack_210 = 0;
  local_1f8 = s_track_offset_105c186dc;
  uStack_1f0 = 0;
  local_1e8 = "scene_offset";
  uStack_1e0 = 0;
  local_228 = "width";
  uStack_220 = 0;
  local_1d8 = s_track_offset_105c186dc;
  uStack_1d0 = 0;
  local_1c8 = "scene_offset";
  uStack_1c0 = 0;
  local_1b8 = "width";
  uStack_1b0 = 0;
  local_238 = "height";
  uStack_230 = 0;
  local_1a8 = (long *)s_track_offset_105c186dc;
  uStack_1a0 = 0;
  local_198 = "scene_offset";
  uStack_190 = 0;
  local_188 = "width";
  uStack_180 = 0;
  local_178 = "height";
  uStack_170 = 0;
  local_239 = 0;
  local_250 = "include_return_tracks";
  local_248 = (long *)0x0;
  puVar1 = (undefined8 *)FUN_1039fc268(&local_250,&local_239);
  local_168 = (long *)s_track_offset_105c186dc;
  plStack_160 = (long *)0x0;
  local_158 = "scene_offset";
  plStack_150 = (long *)0x0;
  local_148 = "width";
  plStack_140 = (long *)0x0;
  local_138 = "height";
  plStack_130 = (long *)0x0;
  local_128 = *puVar1;
  local_120 = (long *)puVar1[1];
  if (local_120 != (long *)0x0) {
    *local_120 = *local_120 + 1;
  }
  local_251 = 0;
  local_268 = "include_rack_chains";
  local_260 = (long *)0x0;
  puVar1 = (undefined8 *)FUN_1039fc268(&local_268,&local_251);
  local_f8 = (long **)local_168;
  if (plStack_160 != (long *)0x0) {
    *plStack_160 = *plStack_160 + 1;
  }
  local_f0 = (long **)plStack_160;
  local_e8 = (long **)local_158;
  if (plStack_150 != (long *)0x0) {
    *plStack_150 = *plStack_150 + 1;
  }
  local_e0 = (long **)plStack_150;
  pcStack_d8 = local_148;
  if (plStack_140 != (long *)0x0) {
    *plStack_140 = *plStack_140 + 1;
  }
  local_d0 = plStack_140;
  local_c8 = local_138;
  if (plStack_130 != (long *)0x0) {
    *plStack_130 = *plStack_130 + 1;
  }
  local_c0 = plStack_130;
  uStack_b8 = local_128;
  if (local_120 != (long *)0x0) {
    *local_120 = *local_120 + 1;
  }
  local_b0 = local_120;
  uStack_a8 = *puVar1;
  local_a0 = (long *)puVar1[1];
  if (local_a0 != (long *)0x0) {
    *local_a0 = *local_a0 + 1;
  }
  local_110 = thunk_FUN_10259b1f0;
  local_98 = (long **)&local_f8;
  local_60 = 0;
  uStack_58 = 0;
  local_68 = 0;
  puStack_90 = auStack_50;
  local_88 = auStack_50;
  puStack_80 = auStack_50;
  FUN_103a1401c(&local_118,0,"set_session_highlight",thunk_FUN_10259b1f0,&local_98);
  local_110 = FUN_1039fc3e0;
  local_100 = (long *)0x0;
  local_60 = 0;
  uStack_58 = 0;
  local_68 = 0;
  local_98 = (long **)&local_100;
  puStack_90 = auStack_50;
  local_88 = auStack_50;
  puStack_80 = auStack_50;
  FUN_103a12c40(&local_118,0,"instance_identifier",FUN_1039fc3e0,&local_98);
  local_110 = thunk_FUN_102598bac;
  local_100 = (long *)0x0;
  local_60 = 0;
  uStack_58 = 0;
  local_68 = 0;
  local_98 = (long **)&local_100;
  puStack_90 = auStack_50;
  local_88 = auStack_50;
  puStack_80 = auStack_50;
  FUN_103a13314(&local_118,0,"request_rebuild_midi_map",thunk_FUN_102598bac,&local_98);
  local_110 = FUN_1039fc3f0;
  local_100 = (long *)0x0;
  local_60 = 0;
  uStack_58 = 0;
  local_68 = 0;
  local_98 = (long **)&local_100;
  puStack_90 = auStack_50;
  local_88 = auStack_50;
  puStack_80 = auStack_50;
  FUN_103a14808(&local_118,0,"preferences",FUN_1039fc3f0,&local_98);
  local_110 = thunk_FUN_10259b710;
  local_100 = (long *)0x0;
  local_60 = 0;
  uStack_58 = 0;
  local_68 = 0;
  local_98 = (long **)&local_100;
  puStack_90 = auStack_50;
  local_88 = auStack_50;
  puStack_80 = auStack_50;
  FUN_103a13314(&local_118,0,"reset_input_history",thunk_FUN_10259b710,&local_98);
  local_110 = thunk_FUN_10259b7d0;
  local_100 = (long *)0x0;
  local_98 = (long **)&local_100;
  local_60 = 0;
  uStack_58 = 0;
  local_68 = 0;
  puStack_90 = auStack_50;
  local_88 = auStack_50;
  puStack_80 = auStack_50;
  FUN_103a14d08(&local_118,0,"set_sync_sysex_macos",thunk_FUN_10259b7d0,&local_98);
  local_110 = thunk_FUN_10259b5d4;
  local_98 = (long **)0x105c1879c;
  local_60 = 0;
  uStack_58 = 0;
  local_68 = 0;
  puStack_90 = auStack_50;
  local_88 = auStack_50;
  puStack_80 = auStack_50;
  FUN_103a150a0(&local_118,0,"set_controlled_track",thunk_FUN_10259b5d4,&local_98);
  local_110 = thunk_FUN_10259b194;
  local_98 = (long **)0x105c1879c;
  local_60 = 0;
  uStack_58 = 0;
  local_68 = 0;
  puStack_90 = auStack_50;
  local_88 = auStack_50;
  puStack_80 = auStack_50;
  FUN_103a1550c(&local_118,0,"release_controlled_track",thunk_FUN_10259b194,&local_98);
  local_110 = FUN_1039fc484;
  local_98 = (long **)0x105c1879c;
  local_60 = 0;
  uStack_58 = 0;
  local_68 = 0;
  puStack_90 = auStack_50;
  local_88 = auStack_50;
  puStack_80 = auStack_50;
  FUN_103a155f4(&local_118,0,"set_feedback_channels",FUN_1039fc484,&local_98);
  local_110 = FUN_10259b6c0;
  uStack_108 = 0;
  local_98 = (long **)0x105c1879c;
  local_60 = 0;
  uStack_58 = 0;
  local_68 = 0;
  puStack_90 = auStack_50;
  local_88 = auStack_50;
  puStack_80 = auStack_50;
  FUN_103a15984(&local_118,0,"set_feedback_velocity",FUN_10259b6c0,0,&local_98);
  uVar2 = FUN_1039fc84c(&local_118,"playhead",FUN_1039fc930,
                        "Disclaimer: The API functions/properties used for Push will be changed or removed and may not be available in the future."
                       );
  uVar2 = FUN_1039fc944(uVar2,"note_repeat",FUN_1039fca28,
                        "Disclaimer: The API functions/properties used for Push will be changed or removed and may not be available in the future."
                       );
  uVar2 = FUN_1039fca3c(uVar2,"full_velocity",FUN_1039fcb20,
                        "Disclaimer: The API functions/properties used for Push will be changed or removed and may not be available in the future."
                       );
  uVar2 = FUN_1039fcb34(uVar2,"velocity_levels",FUN_1039fcc18,
                        "Disclaimer: The API functions/properties used for Push will be changed or removed and may not be available in the future."
                       );
  local_110 = (code *)PTR_eq_106537158;
  local_100 = (long *)0x0;
  local_60 = 0;
  uStack_58 = 0;
  local_68 = 0;
  local_98 = (long **)&local_100;
  puStack_90 = auStack_50;
  local_88 = auStack_50;
  puStack_80 = auStack_50;
  FUN_103a16934(uVar2,0,"__eq__",PTR_eq_106537158,&local_98);
  local_110 = (code *)PTR_ne_106537160;
  local_100 = (long *)0x0;
  local_60 = 0;
  uStack_58 = 0;
  local_68 = 0;
  local_98 = (long **)&local_100;
  puStack_90 = auStack_50;
  local_88 = auStack_50;
  puStack_80 = auStack_50;
  FUN_103a16934(uVar2,0,"__ne__",PTR_ne_106537160,&local_98);
  local_110 = (code *)PTR_bool__106537168;
  local_100 = (long *)0x0;
  puStack_90 = auStack_50;
  local_98 = (long **)&local_100;
  local_60 = 0;
  uStack_58 = 0;
  local_68 = 0;
  local_88 = puStack_90;
  puStack_80 = puStack_90;
  FUN_103a16ec8(uVar2,0,"__bool__",PTR_bool__106537168,&local_98);
  FUN_103a06f2c(&local_f8);
  if (local_260 != (long *)0x0) {
    lVar3 = *local_260;
    *local_260 = lVar3 + -1;
    if (lVar3 + -1 == 0) {
      FUN_101032fbc();
    }
  }
  FUN_103a06ff8(&local_168);
  if (local_248 != (long *)0x0) {
    lVar3 = *local_248;
    *local_248 = lVar3 + -1;
    if (lVar3 + -1 == 0) {
      FUN_101032fbc();
    }
  }
  lVar3 = *local_118;
  *local_118 = lVar3 + -1;
  if (lVar3 + -1 == 0) {
    FUN_101032fbc();
  }
  FUN_103a172c4(&local_1a8,"PushMidiRemoteScript",0);
  local_98 = (long **)FUN_1025e3080;
  puStack_90 = (undefined1 *)0x0;
  local_168 = (long *)0x0;
  local_f0 = &local_b0;
  local_f8 = &local_168;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  ppplVar6 = &local_98;
  local_e8 = local_f0;
  local_e0 = local_f0;
  FUN_103a17758(&local_1a8,0,"set_firmware_version",FUN_1025e3080,0,&local_f8);
  lVar3 = *local_1a8;
  *local_1a8 = lVar3 + -1;
  if (lVar3 + -1 == 0) {
    FUN_101032fbc();
  }
  uVar2 = FUN_100e5d644(&local_f8,"Push2ProcessState",PTR_to_python_10650faa0,
                        PTR_convertible_from_python_10650fa90,PTR_construct_10650fa98,
                        "N16TProcessObserver5StateE","The state the external process is in.",in_x7,
                        ppplVar6);
  FUN_100e5df2c(uVar2,"initialized",0);
  FUN_100e5df2c(&local_f8,"launching",1);
  FUN_100e5df2c(&local_f8,"running",2);
  FUN_100e5df2c(&local_f8,"connected",3);
  FUN_100e5df2c(&local_f8,"died",4);
  FUN_100e5df2c(&local_f8,"terminated",5);
  FUN_100e5df2c(&local_f8,"killed",6);
  FUN_100e5df2c(&local_f8,"wait_for_termination",7);
  FUN_100e5df2c(&local_f8,"defunct_process_wait_for_termination",8);
  FUN_100e5df2c(&local_f8,"defunct_process_terminated",9);
  FUN_100e5df2c(&local_f8,"defunct_process_killed",10);
  plVar4 = *local_f8;
  *local_f8 = (long *)((long)plVar4 + -1);
  if ((long *)((long)plVar4 + -1) == (long *)0x0) {
    FUN_101032fbc();
  }
  FUN_103a17c44(&local_168,"Push2MidiRemoteScript",0);
  uVar2 = FUN_1039fce1c(&local_168,"real_time_mapper",FUN_1025e0360,0,
                        "Disclaimer: The API functions/properties used for Push and Push 2 will be changed or removed and may not be available in the future."
                       );
  local_98 = (long **)FUN_1025e0580;
  puStack_90 = (undefined1 *)0x0;
  local_f8 = (long **)0x105c189c1;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a18378(uVar2,0,"process_connected",FUN_1025e0580,0,&local_f8);
  local_98 = (long **)FUN_1025dee98;
  puStack_90 = (undefined1 *)0x0;
  local_f8 = (long **)0x105c189c1;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_f0 = &local_b0;
  local_e8 = &local_b0;
  local_e0 = &local_b0;
  FUN_103a18648(uVar2,0,"launch_external_process",FUN_1025dee98,0,&local_f8);
  local_98 = (long **)FUN_1025e0398;
  puStack_90 = (undefined1 *)0x0;
  local_f0 = &local_b0;
  local_f8 = (long **)0x105c189c1;
  local_c0 = (long *)0x0;
  uStack_b8 = 0;
  local_c8 = (char *)0x0;
  local_e8 = local_f0;
  local_e0 = local_f0;
  FUN_103a188a4(uVar2,0,"send_model_update",FUN_1025e0398,0,&local_f8);
  lVar3 = *local_168;
  *local_168 = lVar3 + -1;
  if (lVar3 + -1 == 0) {
    FUN_101032fbc();
  }
  FUN_100e57820(PTR_convert_106510bc8,"8TWeakPtrI22APythonPreferenceEntryE",
                PTR_get_pytype_impl_10650f530);
  FUN_100e57820(PTR_convert_106510b50,"8TWeakPtrI17TMidiRemoteScriptE",PTR_get_pytype_impl_10650f4b8
               );
  FUN_100e57820(PTR_convert_106510bb8,"8TWeakPtrI21TPushMidiRemoteScriptE",
                PTR_get_pytype_impl_10650f520);
  FUN_100e57820(PTR_convert_106510bd0,"8TWeakPtrI22TPush2MidiRemoteScriptE",
                PTR_get_pytype_impl_10650f538);
  FUN_100e57820(PTR_convert_106510ba0,"8TWeakPtrI21IPythonRealTimeMapperE",
                PTR_get_pytype_impl_10650f508);
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

