// 0x10017eabc FUN_10017eabc state=exported-with-warnings role=open Push MIDI output (client port name Ableton Internal Output)
// source chunk chunk-00065.jsonl; code_sha256=608ce691214cee23bb25ae67c2396366910da176e61fe1ad3ca41f4b8c0a1803

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_10017eabc(undefined8 param_1,int *param_2)

{
  int iVar1;
  undefined8 uVar2;
  runtime_error *this;
  ulong extraout_x1;
  char *local_48;
  undefined8 local_40;
  long lStack_38;
  
  iVar1 = FUN_1002867e0();
  if ((extraout_x1 >> 0x20 & 1) == 0) {
    this = (runtime_error *)___cxa_allocate_exception(0x10);
    std::runtime_error::runtime_error(this,"No Push hardware found");
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(this,PTR_typeinfo_101b8c318,PTR__runtime_error_101b8c1f0);
  }
  if (*param_2 != iVar1) {
    uVar2 = std::chrono::system_clock::now();
    FUN_1003324b0(&local_48,3,uVar2);
    iVar1 = FUN_10032ece8(&local_48);
    if (iVar1 != 0) {
      FUN_10032bea8(&local_48,"Unexpected Push hardware type found");
    }
    thunk_FUN_10032ba14(&local_48);
  }
  local_48 = operator_new(0x19);
  uVar2 = s_Ableton_Internal_Output_101837600._0_8_;
  lStack_38 = _UNK_1015703c8;
  local_40 = _DAT_1015703c0;
  *(ulong *)(local_48 + 8) =
       CONCAT17(s_Ableton_Internal_Output_101837600[0xf],s_Ableton_Internal_Output_101837600._8_7_);
  *(undefined8 *)local_48 = uVar2;
  *(ulong *)(local_48 + 0xf) =
       CONCAT71(s_Ableton_Internal_Output_101837600._16_7_,s_Ableton_Internal_Output_101837600[0xf])
  ;
  local_48[0x17] = '\0';
  thunk_FUN_1001cbfec(param_1,extraout_x1,&local_48);
  if (-1 < lStack_38) {
    return;
  }
  operator_delete(local_48);
  return;
}

