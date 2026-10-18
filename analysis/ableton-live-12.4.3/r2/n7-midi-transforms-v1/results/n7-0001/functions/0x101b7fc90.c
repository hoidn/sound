
void FUN_101b7fc90(float param_1,undefined4 param_2,long param_3)

{
  *(float *)(param_3 + 0x34) = param_1;
  *(undefined4 *)(param_3 + 0x3c) = param_2;
  if ((param_1 != 3.4028235e+38) && (*(float *)(param_3 + 0x38) != 3.4028235e+38)) {
    FUN_101b7fcc0();
    return;
  }
  return;
}

