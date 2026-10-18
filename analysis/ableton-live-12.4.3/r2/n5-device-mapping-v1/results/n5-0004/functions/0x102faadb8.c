
/* __invoke(void*, float) */

void detail::TMemberFuncTypes<void(OThirdPartyIntegerMappingProcessor::*)(float)>::
     SProcessorFunc<&OThirdPartyIntegerMappingProcessor::OnValue>()::{lambda(void*,float)#1}::
     __invoke(void *param_1,float param_2)

{
  *(float *)((long)param_1 + 0xc) =
       (float)*(int *)(*(long *)((long)param_1 + 0x28) + (long)(int)param_2 * 4);
                    /* WARNING: Could not recover jumptable at 0x000102faadd8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)((long)param_1 + 0x10))(*(undefined8 *)((long)param_1 + 0x18),(long)param_1 + 8);
  return;
}

