
float FUN_101b7c344(float param_1,float param_2,float param_3,float param_4,float param_5,
                   undefined8 param_6,int param_7)

{
  float fVar1;
  float fVar2;
  long local_60;
  undefined8 local_58;
  
  fVar2 = param_2;
  if (param_3 <= param_2) {
    fVar2 = param_3;
  }
  fVar1 = 16384.0;
  if (param_7 == 0) {
    fVar1 = 128.0;
  }
  fVar1 = ((param_5 - param_4) + (param_5 - param_4)) / fVar1;
  if (fVar2 - fVar1 <= param_1) {
    fVar2 = param_2;
    if (param_2 < param_3) {
      fVar2 = param_3;
    }
    if (param_1 <= fVar2 + fVar1) {
      param_1 = param_2;
    }
  }
  FUN_101ab7348(&local_60,&DAT_106fba1a8,0x10100,0x100500,0);
  FUN_101a9c534(local_58,param_6);
  FUN_101a9c57c(param_4,local_58);
  FUN_101a9c57c(param_5,local_58);
  FUN_101a9c57c(param_2,local_58);
  FUN_101a9c57c(param_1,local_58);
  (**(code **)(local_60 + 0x10))(&local_60);
  FUN_101ab786c(&local_60);
  return param_1;
}

