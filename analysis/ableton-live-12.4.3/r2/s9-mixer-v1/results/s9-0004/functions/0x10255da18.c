
void FUN_10255da18(float param_1,long *param_2)

{
  float fVar1;
  undefined4 uVar2;
  float fVar3;
  float fVar4;
  
  if (param_1 <= 0.0) {
    fVar1 = -6.9500003;
  }
  else {
    fVar1 = (float)_log10f();
    fVar1 = (fVar1 * 20.0 + 1.0) * 0.05;
  }
  uVar2 = ___exp10f(fVar1);
  fVar3 = (float)(**(code **)(*param_2 + 0x28))(uVar2,0,0x3f800000,param_2);
  fVar1 = 1.0;
  if (fVar3 <= 1.0) {
    fVar1 = fVar3;
  }
  fVar4 = 0.0;
  if (0.0 <= fVar3) {
    fVar4 = fVar1;
  }
                    /* WARNING: Could not recover jumptable at 0x00010255dabc. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(*param_2 + 0x30))(fVar4,0,0x3f800000,param_2);
  return;
}

