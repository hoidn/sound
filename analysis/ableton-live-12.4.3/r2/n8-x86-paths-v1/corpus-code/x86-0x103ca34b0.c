// x86 0x103ca34b0 FUN_103ca34b0 state=exported-with-warnings chunk=chunk-02985.jsonl code_sha256=22cf837f4382b86968c2377012bbb777b8865bfa05d690f267bbd802ab3aad1d

void FUN_103ca34b0(void)

{
  code *local_f8;
  char *local_f0;
  undefined8 local_e8;
  char *local_e0;
  undefined8 local_d8;
  code *local_d0;
  undefined8 local_c8;
  char *local_c0;
  long *local_b8;
  char *local_b0;
  long *local_a8;
  char *local_a0;
  long *local_98;
  char *local_90;
  undefined8 local_88;
  long *local_80;
  char **local_78;
  undefined1 *local_70;
  undefined1 *local_68;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40;
  undefined1 local_38 [8];
  long local_30;
  
  local_30 = *(long *)PTR____stack_chk_guard_106a33b20;
  FUN_100e22260(&local_80,"AudioToMidiType",PTR_to_python_106a4ad98,
                PTR_convertible_from_python_106a4ad88,PTR_construct_106a4ad90,
                PTR_typeinfo_name_106a79870,0);
  FUN_100e22a40(&local_80,"harmony_to_midi",0);
  FUN_100e22a40(&local_80,"melody_to_midi",1);
  FUN_100e22a40(&local_80,"drums_to_midi",2);
  *local_80 = *local_80 + -1;
  if (*local_80 == 0) {
    FUN_100ff8900();
  }
  local_e8 = 0;
  local_f0 = "song";
  local_88 = 0;
  local_90 = "track_index";
  local_c0 = "song";
  local_b8 = (long *)0x0;
  local_b0 = "track_index";
  local_a8 = (long *)0x0;
  local_d0 = FUN_103ca3c10;
  local_80 = (long *)0x10618509d;
  local_50 = 0;
  uStack_48 = 0;
  local_40 = 0;
  local_78 = &local_c0;
  local_70 = local_38;
  local_68 = local_38;
  FUN_103caaa80("move_devices_on_track_to_new_drum_rack_pad",&local_d0,&local_80);
  if ((local_a8 != (long *)0x0) && (*local_a8 = *local_a8 + -1, *local_a8 == 0)) {
    FUN_100ff8900();
  }
  if ((local_b8 != (long *)0x0) && (*local_b8 = *local_b8 + -1, *local_b8 == 0)) {
    FUN_100ff8900();
  }
  local_e8 = 0;
  local_f0 = "song";
  local_88 = 0;
  local_90 = "audio_clip";
  local_c0 = "song";
  local_b8 = (long *)0x0;
  local_b0 = "audio_clip";
  local_a8 = (long *)0x0;
  local_d0 = FUN_103ca3ca0;
  local_80 = (long *)0x1061851e1;
  local_50 = 0;
  uStack_48 = 0;
  local_40 = 0;
  local_78 = &local_c0;
  local_70 = local_38;
  local_68 = local_38;
  FUN_103caaf70("create_midi_track_with_simpler",&local_d0,&local_80);
  if ((local_a8 != (long *)0x0) && (*local_a8 = *local_a8 + -1, *local_a8 == 0)) {
    FUN_100ff8900();
  }
  if ((local_b8 != (long *)0x0) && (*local_b8 = *local_b8 + -1, *local_b8 == 0)) {
    FUN_100ff8900();
  }
  local_e8 = 0;
  local_f0 = "song";
  local_88 = 0;
  local_90 = "drum_pad";
  local_c0 = "song";
  local_b8 = (long *)0x0;
  local_b0 = "drum_pad";
  local_a8 = (long *)0x0;
  local_d0 = FUN_103ca3cd0;
  local_80 = (long *)0x106185258;
  local_50 = 0;
  uStack_48 = 0;
  local_40 = 0;
  local_78 = &local_c0;
  local_70 = local_38;
  local_68 = local_38;
  FUN_103cab360("create_midi_track_from_drum_pad",&local_d0,&local_80);
  if ((local_a8 != (long *)0x0) && (*local_a8 = *local_a8 + -1, *local_a8 == 0)) {
    FUN_100ff8900();
  }
  if ((local_b8 != (long *)0x0) && (*local_b8 = *local_b8 + -1, *local_b8 == 0)) {
    FUN_100ff8900();
  }
  local_e8 = 0;
  local_f0 = "song";
  local_88 = 0;
  local_90 = "simpler";
  local_c0 = "song";
  local_b8 = (long *)0x0;
  local_b0 = "simpler";
  local_a8 = (long *)0x0;
  local_d0 = FUN_103ca3d00;
  local_80 = (long *)0x1061852c8;
  local_50 = 0;
  uStack_48 = 0;
  local_40 = 0;
  local_78 = &local_c0;
  local_70 = local_38;
  local_68 = local_38;
  FUN_103cab7d0("sliced_simpler_to_drum_rack",&local_d0,&local_80);
  if ((local_a8 != (long *)0x0) && (*local_a8 = *local_a8 + -1, *local_a8 == 0)) {
    FUN_100ff8900();
  }
  if ((local_b8 != (long *)0x0) && (*local_b8 = *local_b8 + -1, *local_b8 == 0)) {
    FUN_100ff8900();
  }
  local_e8 = 0;
  local_f0 = "song";
  local_88 = 0;
  local_90 = "audio_clip";
  local_c0 = "song";
  local_b8 = (long *)0x0;
  local_b0 = "audio_clip";
  local_a8 = (long *)0x0;
  local_d0 = FUN_103ca3d20;
  local_80 = (long *)0x106185370;
  local_50 = 0;
  uStack_48 = 0;
  local_40 = 0;
  local_78 = &local_c0;
  local_70 = local_38;
  local_68 = local_38;
  FUN_103cabc40("create_drum_rack_from_audio_clip",&local_d0,&local_80);
  if ((local_a8 != (long *)0x0) && (*local_a8 = *local_a8 + -1, *local_a8 == 0)) {
    FUN_100ff8900();
  }
  if ((local_b8 != (long *)0x0) && (*local_b8 = *local_b8 + -1, *local_b8 == 0)) {
    FUN_100ff8900();
  }
  local_e8 = 0;
  local_f0 = "song";
  local_88 = 0;
  local_90 = "audio_clip";
  local_c0 = "song";
  local_b8 = (long *)0x0;
  local_b0 = "audio_clip";
  local_a8 = (long *)0x0;
  local_d0 = FUN_103ca3d50;
  local_80 = (long *)0x1061853eb;
  local_50 = 0;
  uStack_48 = 0;
  local_40 = 0;
  local_78 = &local_c0;
  local_70 = local_38;
  local_68 = local_38;
  FUN_103cabd20("is_convertible_to_midi",&local_d0,&local_80);
  if ((local_a8 != (long *)0x0) && (*local_a8 = *local_a8 + -1, *local_a8 == 0)) {
    FUN_100ff8900();
  }
  if ((local_b8 != (long *)0x0) && (*local_b8 = *local_b8 + -1, *local_b8 == 0)) {
    FUN_100ff8900();
  }
  local_88 = 0;
  local_90 = "song";
  local_c8 = 0;
  local_d0 = (code *)0x10618522d;
  local_f0 = "song";
  local_e8 = 0;
  local_e0 = "audio_clip";
  local_d8 = 0;
  local_c0 = "song";
  local_b8 = (long *)0x0;
  local_b0 = "audio_clip";
  local_a8 = (long *)0x0;
  local_a0 = "audio_to_midi_type";
  local_98 = (long *)0x0;
  local_f8 = FUN_103ca3d70;
  local_80 = (long *)0x10618545f;
  local_50 = 0;
  uStack_48 = 0;
  local_40 = 0;
  local_78 = &local_c0;
  local_70 = local_38;
  local_68 = local_38;
  FUN_103cac190("audio_to_midi_clip",&local_f8,&local_80);
  if ((local_98 != (long *)0x0) && (*local_98 = *local_98 + -1, *local_98 == 0)) {
    FUN_100ff8900();
  }
  if ((local_a8 != (long *)0x0) && (*local_a8 = *local_a8 + -1, *local_a8 == 0)) {
    FUN_100ff8900();
  }
  if ((local_b8 != (long *)0x0) && (*local_b8 = *local_b8 + -1, *local_b8 == 0)) {
    FUN_100ff8900();
  }
  if (*(long *)PTR____stack_chk_guard_106a33b20 == local_30) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

