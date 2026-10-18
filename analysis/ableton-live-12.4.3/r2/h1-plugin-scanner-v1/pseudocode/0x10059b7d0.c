
void FUN_10059b7d0(char *param_1,uint param_2)

{
  ulong uVar1;
  void *pvVar2;
  size_t sVar3;
  undefined8 uVar4;
  char *pcVar5;
  ulong uVar6;
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
  long lStack_100;
  ulong local_f8;
  uint local_f0;
  undefined **local_e8 [6];
  undefined8 local_b8;
  undefined8 local_60;
  undefined4 local_58;
  
  if (param_2 == 0) {
    param_1[0x17] = '\v';
    param_1[7] = ' ';
    param_1[8] = 'c';
    param_1[9] = 'p';
    param_1[10] = 'u';
    *(undefined8 *)param_1 = s_unknown_cpu_100a48771._0_8_;
    param_1[0xb] = '\0';
    return;
  }
  local_b8 = 0;
  local_160 = 0;
  local_158 = &PTR_FUN_100b43858;
  local_e8[0] = &PTR__istream_100b43998;
  local_168 = &PTR__istream_100b43970;
  std::ios_base::init(local_e8);
  local_58 = 0xffffffff;
  local_60 = 0;
  local_e8[0] = &PTR_FUN_100b43880;
  local_168 = &PTR_FUN_100b43830;
  local_158 = &PTR_FUN_100b43858;
  std::streambuf::streambuf((streambuf *)local_150);
  local_150[0] = &PTR_FUN_100b43a20;
  uStack_108 = 0;
  local_110 = (void *)0x0;
  local_f8 = 0;
  lStack_100 = 0;
  local_f0 = 0x18;
  if ((param_2 & 1) == 0) {
    pcVar5 = "";
  }
  else {
    uVar4 = FUN_10013e5bc(&local_158,"",0);
    FUN_10013e5bc(uVar4,"x86_64",6);
    pcVar5 = "|";
  }
  if ((param_2 >> 1 & 1) != 0) {
    sVar3 = _strlen(pcVar5);
    uVar4 = FUN_10013e5bc(&local_158,pcVar5,sVar3);
    FUN_10013e5bc(uVar4,"arm64",5);
  }
  if ((local_f0 >> 4 & 1) == 0) {
    if ((local_f0 >> 3 & 1) == 0) {
      uVar6 = 0;
      param_1[0x17] = '\0';
      goto LAB_10059b9a8;
    }
    uVar6 = local_130 - (long)local_140;
    pvVar2 = local_140;
  }
  else {
    if (local_f8 < local_120) {
      local_f8 = local_120;
    }
    uVar6 = local_f8 - (long)local_128;
    pvVar2 = local_128;
  }
  if (0x7ffffffffffffff7 < uVar6) {
                    /* WARNING: Subroutine does not return */
    FUN_100134f2c(param_1);
  }
  if (uVar6 < 0x17) {
    param_1[0x17] = (char)uVar6;
    pcVar5 = param_1;
    if (uVar6 == 0) goto LAB_10059b9a8;
  }
  else {
    uVar1 = 0x19;
    if ((uVar6 | 7) != 0x17) {
      uVar1 = (uVar6 | 7) + 1;
    }
    pcVar5 = operator_new(uVar1);
    *(ulong *)(param_1 + 8) = uVar6;
    *(ulong *)(param_1 + 0x10) = uVar1 | 0x8000000000000000;
    *(char **)param_1 = pcVar5;
  }
  _memmove(pcVar5,pvVar2,uVar6);
  param_1 = pcVar5;
LAB_10059b9a8:
  param_1[uVar6] = '\0';
  local_168 = &PTR_FUN_100b43830;
  local_e8[0] = &PTR_FUN_100b43880;
  local_158 = &PTR_FUN_100b43858;
  local_150[0] = &PTR_FUN_100b43a20;
  if (lStack_100 < 0) {
    operator_delete(local_110);
  }
  std::streambuf::~streambuf((streambuf *)local_150);
  std::iostream::~iostream((iostream *)&local_168);
  std::ios::~ios((ios *)local_e8);
  return;
}

