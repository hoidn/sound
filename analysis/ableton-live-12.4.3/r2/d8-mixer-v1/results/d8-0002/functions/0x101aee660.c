
/* __invoke(void*, void*) */

void detail::TMemberFuncTypes<void(OConvertLevelRampEventProcessor::*)(void*)>::
     SProcessorFunc<&OConvertLevelRampEventProcessor::OnIn>()::{lambda(void*,void*)#1}::__invoke
               (void *param_1,void *param_2)

{
  float fVar1;
  float fVar2;
  
  fVar1 = (float)FUN_101ac3bac(*(undefined4 *)param_2,*(undefined4 *)((long)param_1 + 8));
  fVar2 = 0.0;
  if (0.00032 < fVar1) {
    fVar2 = fVar1;
  }
  *(float *)((long)param_1 + 0xc) = fVar2;
  *(undefined4 *)((long)param_1 + 0x10) = *(undefined4 *)((long)param_2 + 4);
                    /* WARNING: Could not recover jumptable at 0x000101aee6b8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)((long)param_1 + 0x18))
            (*(undefined8 *)((long)param_1 + 0x20),(float *)((long)param_1 + 0xc));
  return;
}

