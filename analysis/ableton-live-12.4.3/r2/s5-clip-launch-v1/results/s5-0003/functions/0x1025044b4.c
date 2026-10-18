
/* WARNING: Type propagation algorithm not settling */

void FUN_1025044b4(long param_1)

{
  float fVar1;
  float fVar2;
  float local_3c;
  float local_38 [2];
  
  fVar1 = (float)(**(code **)(**(long **)(param_1 + 0xf0) + 0x210))();
  fVar2 = (float)(**(code **)(**(long **)(param_1 + 0x108) + 0x210))();
  if ((fVar1 == 0.0) && (fVar2 == 0.0)) {
    local_38[1] = 100.0;
    (**(code **)(**(long **)(param_1 + 0xf0) + 0x280))(*(long **)(param_1 + 0xf0),local_38 + 1);
    FUN_101564698(*(undefined8 *)(param_1 + 0x120),0);
    return;
  }
  fVar1 = (float)(int)(fVar1 / ((fVar1 + fVar2) / 100.0));
  local_38[0] = fVar1;
  (**(code **)(**(long **)(param_1 + 0xf0) + 0x280))(*(long **)(param_1 + 0xf0),local_38);
  local_3c = 100.0 - fVar1;
  (**(code **)(**(long **)(param_1 + 0x108) + 0x280))(*(long **)(param_1 + 0x108),&local_3c);
  return;
}

