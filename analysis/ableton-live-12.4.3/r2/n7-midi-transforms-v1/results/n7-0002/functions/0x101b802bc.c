
void FUN_101b802bc(float param_1,undefined4 param_2,long param_3)

{
  bool bVar1;
  
  *(float *)(param_3 + 0x38) = param_1;
  *(undefined4 *)(param_3 + 0x40) = param_2;
  bVar1 = true;
  if ((param_1 != 3.4028235e+38) && (bVar1 = false, !NAN(*(float *)(param_3 + 0x34)))) {
    bVar1 = *(float *)(param_3 + 0x34) == 3.4028235e+38;
  }
  if (bVar1) {
    return;
  }
  FUN_101b7fcc0();
  return;
}

