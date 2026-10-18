
void FUN_103ba8520(undefined8 param_1)

{
  undefined8 uVar1;
  long lVar2;
  char *pcVar3;
  code *local_138;
  code *pcStack_130;
  code *local_128;
  code *pcStack_120;
  char *local_118;
  code *pcStack_110;
  char *local_108;
  code *pcStack_100;
  char *local_f8;
  code *pcStack_f0;
  char *local_e8;
  code *pcStack_e0;
  char *local_d8;
  code *pcStack_d0;
  long *local_c8;
  code *pcStack_c0;
  code *local_b8;
  code *pcStack_b0;
  char *local_a8;
  code *pcStack_a0;
  char *local_98;
  code *pcStack_90;
  char **local_88;
  code *pcStack_80;
  undefined1 *local_78;
  undefined1 *puStack_70;
  undefined8 local_58;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined1 auStack_40 [8];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_1064f8818;
  uVar1 = FUN_103bab6d0(param_1,"clip_trigger_quantization",FUN_103bab868,FUN_103bab874,
                        "Get/Set access to the quantization settings that are used to fire\nClips in the Session."
                       );
  local_98 = "clip_trigger_quantization";
  pcStack_90 = FUN_103bab8f0;
  FUN_103bbcf10(&local_98,uVar1);
  uVar1 = FUN_103bab8fc(uVar1,"midi_recording_quantization",FUN_103baba94,FUN_103babaa0,
                        "Get/Set access to the settings that are used to quantize\nMIDI recordings."
                       );
  local_a8 = "midi_recording_quantization";
  pcStack_a0 = FUN_103babb1c;
  FUN_103bbcf10(&local_a8,uVar1);
  uVar1 = FUN_103baacbc(uVar1,"swing_amount",FUN_103babb28,FUN_103babb3c,
                        "Get/Set access to the amount of swing that is applied when adding or quantizing notes to MIDI clips"
                       );
  local_b8 = (code *)0x105c2981d;
  pcStack_b0 = FUN_103babb7c;
  FUN_103bbcf10(&local_b8,uVar1);
  uVar1 = FUN_103babb88(uVar1,"groove_pool",FUN_103babc6c,"Get the groove pool.");
  uVar1 = FUN_103ba5a60(uVar1,s_signature_numerator_105c1cbc0,FUN_103babd08,FUN_103babd20,
                        "Get/Set access to the global signature numerator of the Song.");
  local_c8 = (long *)s_signature_numerator_105c1cbc0;
  pcStack_c0 = FUN_103babdc0;
  FUN_103bbcf10(&local_c8,uVar1);
  uVar1 = FUN_103ba5a60(uVar1,"signature_denominator",FUN_103babdd8,FUN_103babdf0,
                        "Get/Set access to the global signature denominator of the Song.");
  local_d8 = "signature_denominator";
  pcStack_d0 = FUN_103babe90;
  FUN_103bbcf10(&local_d8,uVar1);
  uVar1 = FUN_103ba5efc(uVar1,"back_to_arranger",FUN_103babea8,FUN_103babec4,
                        "Get/Set if triggering a Clip in the Session, disabled the playback of\nClips in the Arranger."
                       );
  local_e8 = "back_to_arranger";
  pcStack_e0 = FUN_103babef8;
  FUN_103bbcf10(&local_e8,uVar1);
  uVar1 = FUN_103ba5efc(uVar1,"punch_in",FUN_103babf14,FUN_103babf30,
                        "Get/Set the flag that will enable recording as soon as the Song plays\nand hits the global loop start region."
                       );
  local_f8 = "punch_in";
  pcStack_f0 = FUN_103babf64;
  FUN_103bbcf10(&local_f8,uVar1);
  uVar1 = FUN_103ba5efc(uVar1,"punch_out",FUN_103babf80,FUN_103babf9c,
                        "Get/Set the flag that will disable recording as soon as the Song plays\nand hits the global loop end region."
                       );
  local_108 = "punch_out";
  pcStack_100 = FUN_103babfd0;
  FUN_103bbcf10(&local_108,uVar1);
  uVar1 = FUN_103bab214(uVar1,"loop_start",FUN_103babfec,FUN_103bac008,
                        "Get/Set the start of the global loop marker position in beats.");
  local_118 = "loop_start";
  pcStack_110 = FUN_103bac03c;
  FUN_103bbcf10(&local_118,uVar1);
  local_128 = FUN_103bac058;
  pcStack_80 = (code *)auStack_40;
  local_88 = (char **)0x105c29acf;
  local_50 = 0;
  uStack_48 = 0;
  local_58 = 0;
  local_78 = pcStack_80;
  puStack_70 = pcStack_80;
  FUN_103bcc178(uVar1,0,"get_beats_loop_start",FUN_103bac058,&local_88);
  uVar1 = FUN_103bab214(uVar1,"loop_length",FUN_103bac060,FUN_103bac07c,
                        "Get/Set the length of the global loop marker position in beats.");
  local_128 = (code *)0x105c237d6;
  pcStack_120 = FUN_103bac0b0;
  FUN_103bbcf10(&local_128,uVar1);
  pcStack_80 = (code *)auStack_40;
  local_88 = (char **)0x105c29b8d;
  local_50 = 0;
  uStack_48 = 0;
  local_58 = 0;
  local_138 = FUN_103bac0cc;
  local_78 = pcStack_80;
  puStack_70 = pcStack_80;
  FUN_103bcc260(uVar1,0,"get_beats_loop_length",FUN_103bac0cc,&local_88);
  uVar1 = FUN_103ba5efc(uVar1,"loop",FUN_103bac0d4,FUN_103bac0f0,
                        "Get/Set the looping flag that en/disables the usage of the global\nloop markers in the song."
                       );
  local_88 = (char **)0x105ab42c6;
  pcStack_80 = FUN_103bac12c;
  FUN_103bbcf10(&local_88,uVar1);
  uVar1 = FUN_103ba56dc(uVar1,"exclusive_arm",FUN_103bac148,
                        "Get if Tracks should be armed exclusively by default.");
  local_138 = (code *)0x105c29c52;
  pcStack_130 = FUN_103bac160;
  FUN_103bbcf10(&local_138,uVar1);
  uVar1 = FUN_103ba56dc(uVar1,"exclusive_solo",FUN_103bac174,
                        "Get if Tracks should be soloed exclusively by default.");
  FUN_103ba56dc(uVar1,"select_on_launch",FUN_103bac18c,
                "Get if Scenes and Clips should be selected when fired.");
  FUN_103bcc348(&local_c8,"CuePoint","Represents a \'Marker\' in the arrangement.",0);
  uVar1 = FUN_103bac1a4(&local_c8,s_time_105aa181d,FUN_103bac288,
                        "Get/Listen to the CuePoint\'s time in beats.");
  local_98 = s_time_105aa181d;
  pcStack_90 = FUN_103bac298;
  FUN_103bccb28(&local_98,uVar1);
  uVar1 = FUN_103bac2a8(uVar1,"name",FUN_103bac440,FUN_103bac470,
                        "Get/Set/Listen to the name of this CuePoint, as visible in the arranger.");
  local_a8 = "name";
  pcStack_a0 = FUN_103bac4f8;
  FUN_103bccb28(&local_a8,uVar1);
  local_b8 = FUN_103bac508;
  pcStack_80 = (code *)auStack_40;
  local_88 = (char **)0x105c29dc8;
  local_50 = 0;
  uStack_48 = 0;
  local_58 = 0;
  local_78 = pcStack_80;
  puStack_70 = pcStack_80;
  FUN_103bce17c(uVar1,0,"jump",FUN_103bac508,&local_88);
  FUN_103bac530(uVar1,"canonical_parent",FUN_103bae73c,"Get the canonical parent of the cue point.")
  ;
  lVar2 = *local_c8;
  *local_c8 = lVar2 + -1;
  if (lVar2 + -1 == 0) {
    FUN_101032fbc();
  }
  FUN_100e57820(PTR_convert_106510cc8,"8TWeakPtrI9TPyHandleI9ACuePointEE",
                PTR_get_pytype_impl_10650f630);
  FUN_100e57b58(PTR_convertible_1065139b0,PTR_construct_1065139b8,"8TWeakPtrI13TPyHandleBaseE",
                PTR_get_pytype_106512af0);
  FUN_103bceccc(&local_b8,"BeatTime",
                "Represents a Time, splitted into Bars, Beats, SubDivision and Ticks.");
  local_98 = PTR_Serialize_106537418;
  pcStack_90 = (code *)0x0;
  local_a8 = (char *)0x0;
  pcStack_80 = (code *)auStack_40;
  local_88 = &local_a8;
  local_50 = 0;
  uStack_48 = 0;
  local_58 = 0;
  local_78 = pcStack_80;
  puStack_70 = pcStack_80;
  FUN_103bcf500(&local_b8,0,"__str__",PTR_Serialize_106537418,0,&local_88);
  uVar1 = FUN_103bcf880(&local_b8,"bars",0,0,0);
  uVar1 = FUN_103bcf880(uVar1,"beats",4,4,0);
  uVar1 = FUN_103bcf880(uVar1,"sub_division",8,8,0);
  FUN_103bcf880(uVar1,"ticks",0xc,0xc,0);
  lVar2 = *(long *)local_b8;
  *(long *)local_b8 = lVar2 + -1;
  if (lVar2 + -1 == 0) {
    FUN_101032fbc();
  }
  FUN_103bcfe94(&local_b8,"SmptTime",
                "Represents a Time, split into Hours, Minutes, Seconds and Frames.\nThe frame type must be specified when calling a function that returns\na SmptTime."
               );
  local_98 = PTR_Serialize_106537420;
  pcStack_90 = (code *)0x0;
  local_a8 = (char *)0x0;
  pcStack_80 = (code *)auStack_40;
  local_88 = &local_a8;
  local_50 = 0;
  uStack_48 = 0;
  local_58 = 0;
  local_78 = pcStack_80;
  puStack_70 = pcStack_80;
  FUN_103bd06c8(&local_b8,0,"__str__",PTR_Serialize_106537420,0,&local_88);
  uVar1 = FUN_103bd0a48(&local_b8,"hours",0,0,0);
  uVar1 = FUN_103bd0a48(uVar1,"seconds",4,4,0);
  uVar1 = FUN_103bd0a48(uVar1,"minutes",8,8,0);
  FUN_103bd0a48(uVar1,"frames",0xc,0xc,0);
  lVar2 = *(long *)local_b8;
  *(long *)local_b8 = lVar2 + -1;
  if (lVar2 + -1 == 0) {
    FUN_101032fbc();
  }
  uVar1 = FUN_100e5d644(&local_88,"Quantization",PTR_to_python_10650fb00,
                        PTR_convertible_from_python_10650faf0,PTR_construct_10650faf8,
                        "N18NQuantizationTypes19TLaunchQuantizationE",0);
  FUN_100e5df2c(uVar1,"q_no_q",0);
  FUN_100e5df2c(&local_88,"q_8_bars",1);
  FUN_100e5df2c(&local_88,"q_4_bars",2);
  FUN_100e5df2c(&local_88,"q_2_bars",3);
  FUN_100e5df2c(&local_88,"q_bar",4);
  FUN_100e5df2c(&local_88,"q_half",5);
  FUN_100e5df2c(&local_88,"q_half_triplet",6);
  FUN_100e5df2c(&local_88,"q_quarter",7);
  FUN_100e5df2c(&local_88,"q_quarter_triplet",8);
  FUN_100e5df2c(&local_88,"q_eight",9);
  FUN_100e5df2c(&local_88,"q_eight_triplet",10);
  FUN_100e5df2c(&local_88,"q_sixtenth",0xb);
  FUN_100e5df2c(&local_88,"q_sixtenth_triplet",0xc);
  FUN_100e5df2c(&local_88,"q_thirtytwoth",0xd);
  pcVar3 = *local_88;
  *local_88 = pcVar3 + -1;
  if (pcVar3 + -1 == (char *)0x0) {
    FUN_101032fbc();
  }
  uVar1 = FUN_100e5d644(&local_88,"RecordingQuantization",PTR_to_python_10650fb48,
                        PTR_convertible_from_python_10650fb38,PTR_construct_10650fb40,
                        "N18NQuantizationTypes26TMidiRecordingQuantizationE",0);
  FUN_100e5df2c(uVar1,"rec_q_no_q",0);
  FUN_100e5df2c(&local_88,"rec_q_quarter",1);
  FUN_100e5df2c(&local_88,"rec_q_eight",2);
  FUN_100e5df2c(&local_88,"rec_q_eight_triplet",3);
  FUN_100e5df2c(&local_88,"rec_q_eight_eight_triplet",4);
  FUN_100e5df2c(&local_88,"rec_q_sixtenth",5);
  FUN_100e5df2c(&local_88,"rec_q_sixtenth_triplet",6);
  FUN_100e5df2c(&local_88,"rec_q_sixtenth_sixtenth_triplet",7);
  FUN_100e5df2c(&local_88,"rec_q_thirtysecond",8);
  pcVar3 = *local_88;
  *local_88 = pcVar3 + -1;
  if (pcVar3 + -1 == (char *)0x0) {
    FUN_101032fbc();
  }
  uVar1 = FUN_100e5d644(&local_88,"TimeFormat",PTR_to_python_10650fb78,
                        PTR_convertible_from_python_10650fb68,PTR_construct_10650fb70,
                        "N20NTimeConversionTypes11TTimeFormatE",0);
  FUN_100e5df2c(uVar1,"ms_time",0);
  FUN_100e5df2c(&local_88,"smpte_24",1);
  FUN_100e5df2c(&local_88,"smpte_25",2);
  FUN_100e5df2c(&local_88,"smpte_30",3);
  FUN_100e5df2c(&local_88,"smpte_30_drop",4);
  FUN_100e5df2c(&local_88,"smpte_29",5);
  pcVar3 = *local_88;
  *local_88 = pcVar3 + -1;
  if (pcVar3 + -1 == (char *)0x0) {
    FUN_101032fbc();
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

