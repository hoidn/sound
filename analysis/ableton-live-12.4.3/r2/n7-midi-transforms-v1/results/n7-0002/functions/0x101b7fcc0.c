
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_101b7fcc0(long param_1)

{
  int iVar1;
  float fVar2;
  float fVar3;
  float local_50;
  float fStack_4c;
  undefined8 local_48;
  undefined4 local_40;
  undefined4 uStack_3c;
  undefined1 local_38;
  undefined4 local_34;
  
  if ((*(byte *)(param_1 + 0x44) & 1) == 0) {
    fVar2 = 3.4028235e+38;
    if (*(float *)(param_1 + 0x3c) != 3.4028235e+38) {
      fVar2 = 3.4028235e+38;
      if (*(float *)(param_1 + 0x40) != 3.4028235e+38) {
        fVar2 = (float)((int)*(float *)(param_1 + 0x40) | (int)*(float *)(param_1 + 0x3c) << 7) /
                _DAT_10584a8b4;
      }
    }
  }
  else {
    fVar2 = 3.4028235e+38;
  }
  fVar3 = (float)((int)*(float *)(param_1 + 0x38) | (int)*(float *)(param_1 + 0x34) << 7) /
          _DAT_10584a8b4;
  iVar1 = FUN_1011c0ee8(0x100500);
  local_40 = 0;
  if (iVar1 == 0) {
    local_40 = 4;
  }
  uStack_3c = 2;
  local_38 = 1;
  local_34 = 1;
  local_48 = 0x3f80000000000000;
  local_50 = fVar3;
  fStack_4c = fVar2;
  FUN_101b7fde4(*(undefined8 *)(*(long *)(param_1 + 8) + 0xa0),param_1 + 0x10,&local_50,&local_40);
  *(undefined8 *)(param_1 + 0x3c) = 0x7f7fffff7f7fffff;
  *(undefined8 *)(param_1 + 0x34) = 0x7f7fffff7f7fffff;
  return;
}

