// 0x100180a80 FUN_100180a80 state=exported-with-warnings role=ipc:// + temp_directory_path + channel name
// source chunk chunk-00065.jsonl; code_sha256=09ac35656c0a39808006e9712edb254f165ef1e96b7672270f280e8b8a709c98

void FUN_100180a80(undefined8 *param_1,undefined8 *param_2,int param_3)

{
  ulong uVar1;
  undefined8 ***pppuVar2;
  void *pvVar3;
  undefined8 *puVar4;
  ulong uVar5;
  undefined8 **local_198;
  ulong uStack_190;
  byte bStack_181;
  undefined8 **local_180;
  ulong uStack_178;
  undefined8 local_170;
  undefined **local_168;
  undefined8 local_160;
  undefined **local_158;
  undefined **local_150 [2];
  void *local_140;
  long local_130;
  void *local_128;
  ulong local_120;
  void *local_110;
  undefined8 uStack_108;
  long local_100;
  ulong uStack_f8;
  uint local_f0;
  undefined **local_e8 [6];
  undefined8 local_b8;
  undefined8 local_60;
  undefined4 local_58;
  
  local_b8 = 0;
  local_160 = 0;
  local_158 = &PTR_FUN_101bcf1d0;
  local_e8[0] = &PTR__istream_101bcf310;
  local_168 = &PTR__istream_101bcf2e8;
  std::ios_base::init(local_e8);
  local_58 = 0xffffffff;
  local_60 = 0;
  local_e8[0] = &PTR_FUN_101bcf1f8;
  local_168 = &PTR_FUN_101bcf1a8;
  local_158 = &PTR_FUN_101bcf1d0;
  std::streambuf::streambuf((streambuf *)local_150);
  local_150[0] = &PTR_FUN_101bcf398;
  uStack_108 = 0;
  local_110 = (void *)0x0;
  uStack_f8 = 0;
  local_100 = 0;
  local_f0 = 0x18;
  if (param_3 == 1) {
    FUN_100181e9c(&local_158,"inproc://",9);
  }
  else if (param_3 == 0) {
    FUN_100181e9c(&local_158,"ipc://",6);
    thunk_FUN_10031ce0c(&local_198);
    if ((char)bStack_181 < '\0') {
      FUN_10018127c(&local_180,local_198,uStack_190);
    }
    else {
      uStack_178 = uStack_190;
      local_180 = local_198;
      local_170 = (ulong)bStack_181 << 0x38;
    }
    uVar5 = uStack_178;
    pppuVar2 = (undefined8 ***)local_180;
    if (-1 < local_170) {
      uVar5 = (ulong)local_170._7_1_;
      pppuVar2 = &local_180;
    }
    FUN_100181e9c(&local_158,pppuVar2,uVar5);
    if ((char)local_170._7_1_ < '\0') {
      operator_delete(local_180);
    }
    if ((char)bStack_181 < '\0') {
      operator_delete(local_198);
    }
  }
  uVar5 = param_2[1];
  puVar4 = (undefined8 *)*param_2;
  if (-1 < (char)*(byte *)((long)param_2 + 0x17)) {
    uVar5 = (ulong)*(byte *)((long)param_2 + 0x17);
    puVar4 = param_2;
  }
  FUN_100181e9c(&local_158,puVar4,uVar5);
  if ((local_f0 >> 4 & 1) == 0) {
    if ((local_f0 >> 3 & 1) == 0) {
      uVar5 = 0;
      *(undefined1 *)((long)param_1 + 0x17) = 0;
      goto LAB_100180c80;
    }
    uVar5 = local_130 - (long)local_140;
    pvVar3 = local_140;
  }
  else {
    if (uStack_f8 < local_120) {
      uStack_f8 = local_120;
    }
    uVar5 = uStack_f8 - (long)local_128;
    pvVar3 = local_128;
  }
  if (0x7ffffffffffffff7 < uVar5) {
                    /* WARNING: Subroutine does not return */
    FUN_100181308(param_1);
  }
  if (uVar5 < 0x17) {
    *(char *)((long)param_1 + 0x17) = (char)uVar5;
    puVar4 = param_1;
    if (uVar5 == 0) goto LAB_100180c80;
  }
  else {
    uVar1 = 0x19;
    if ((uVar5 | 7) != 0x17) {
      uVar1 = (uVar5 | 7) + 1;
    }
    puVar4 = operator_new(uVar1);
    param_1[1] = uVar5;
    param_1[2] = uVar1 | 0x8000000000000000;
    *param_1 = puVar4;
  }
  _memmove(puVar4,pvVar3,uVar5);
  param_1 = puVar4;
LAB_100180c80:
  *(undefined1 *)((long)param_1 + uVar5) = 0;
  local_168 = &PTR_FUN_101bcf1a8;
  local_e8[0] = &PTR_FUN_101bcf1f8;
  local_158 = &PTR_FUN_101bcf1d0;
  local_150[0] = &PTR_FUN_101bcf398;
  if (local_100 < 0) {
    operator_delete(local_110);
  }
  std::streambuf::~streambuf((streambuf *)local_150);
  std::iostream::~iostream((iostream *)&local_168);
  std::ios::~ios((ios *)local_e8);
  return;
}

