
void FUN_101b7f354(undefined4 param_1,undefined4 param_2,long param_3,undefined8 param_4,
                  uint param_5)

{
  bool bVar1;
  long lVar2;
  undefined8 uVar3;
  code *pcVar4;
  float fVar5;
  float fVar6;
  undefined4 local_50;
  undefined4 uStack_4c;
  int local_48;
  float local_44;
  int local_40 [2];
  undefined1 local_38;
  undefined4 local_34;
  
  local_40[0] = param_5 + 2;
  if (2 < param_5) {
    local_40[0] = 0;
  }
  local_40[1] = 2;
  local_38 = 1;
  local_34 = 1;
  if ((*(char *)(param_3 + 0x44) == '\x01') && (*(float *)(param_3 + 0x3c) == 1.0)) {
    param_2 = 0x7f7fffff;
  }
  fVar6 = *(float *)(param_3 + 0x48);
  local_48 = (int)param_4;
  lVar2 = *(long *)(*(long *)(param_3 + 0x18) + 0xa0);
  if (lVar2 != 0) {
    local_50 = param_1;
    uStack_4c = param_2;
    local_44 = fVar6;
    if (((local_48 != 0) && (local_48 != 5)) && (*(char *)(param_3 + 0x2c) == '\x01')) {
      fVar5 = (float)FUN_101b7b96c(param_4);
      if (fVar5 <= 0.0) {
        fVar6 = -fVar6;
      }
      fVar6 = *(float *)(param_3 + 0x4c) + fVar6;
      fVar5 = 1.0;
      if (fVar6 < 0.0) {
        fVar5 = -1.0;
      }
      bVar1 = fVar6 * fVar5 < 1.0;
      fVar5 = fVar6 - fVar5;
      if (bVar1) {
        fVar5 = fVar6;
      }
      *(float *)(param_3 + 0x4c) = fVar5;
      if (bVar1) {
        return;
      }
    }
    pcVar4 = *(code **)(param_3 + 8);
    if (pcVar4 == (code *)PTR_TMidiControllerValue_const__TControllerOrigin_const___106551c10) {
      uVar3 = 0;
      pcVar4 = FUN_101b83974;
      *(code **)(param_3 + 8) = FUN_101b83974;
      *(undefined8 *)(param_3 + 0x10) = 0;
    }
    else {
      uVar3 = *(undefined8 *)(param_3 + 0x10);
    }
    (*pcVar4)(uVar3,lVar2,param_3 + 0x20,&local_50,local_40);
  }
  return;
}

