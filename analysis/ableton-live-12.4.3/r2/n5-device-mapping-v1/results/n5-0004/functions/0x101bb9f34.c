
/* __invoke(void*, float) */

void detail::TMemberFuncTypes<void(OConvertQuantingIntProcessor::*)(float)>::
     SProcessorFunc<&OConvertQuantingIntProcessor::OnIn>()::{lambda(void*,float)#1}::__invoke
               (void *param_1,float param_2)

{
  bool bVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  
  fVar2 = *(float *)((long)param_1 + 0x28);
  fVar3 = *(float *)((long)param_1 + 0x2c);
  fVar4 = *(float *)((long)param_1 + 0x30);
  fVar5 = *(float *)((long)param_1 + 0x34);
  bVar1 = false;
  if ((fVar2 == fVar4) && (bVar1 = false, !NAN(fVar3) && !NAN(fVar5))) {
    bVar1 = fVar3 == fVar5;
  }
  if (!bVar1) {
    fVar2 = (param_2 - fVar2) / (fVar3 - fVar2);
    param_2 = (fVar4 - fVar4 * fVar2) + fVar5 * fVar2;
  }
  fVar2 = (float)(int)((double)(long)(param_2 * 32768.0) * 3.0517578125e-05);
  if (*(float *)((long)param_1 + 8) != fVar2) {
    *(float *)((long)param_1 + 8) = fVar2;
                    /* WARNING: Could not recover jumptable at 0x000101bb9fa8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)((long)param_1 + 0x10))(*(undefined8 *)((long)param_1 + 0x18));
    return;
  }
  return;
}

