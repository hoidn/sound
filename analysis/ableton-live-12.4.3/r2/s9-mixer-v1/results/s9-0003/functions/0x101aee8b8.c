
/* OCrossFadeHelper::CrossfadeToLevelNormalDip(float) */

float OCrossFadeHelper::CrossfadeToLevelNormalDip(float param_1)

{
  float fVar1;
  float fVar2;
  float fVar3;
  
  fVar1 = 1.0;
  if ((-0.95 <= param_1) && (fVar1 = 0.0, param_1 <= 0.95)) {
    fVar3 = param_1 / 0.95;
    fVar1 = (float)_cosf((fVar3 + 1.0) * 0.7853982);
    fVar2 = (float)_cosf(fVar3 * 1.5707964);
    fVar1 = fVar1 + fVar2 * -0.20710677;
    if (0.55 <= fVar3) {
      fVar2 = (float)_cosf(((fVar3 + -0.55) / 0.45) * 3.1415927);
      fVar1 = fVar1 * (fVar2 + 1.0) * 0.5;
    }
  }
  return fVar1;
}

