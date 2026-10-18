
/* __invoke(void*, void*) */

void detail::TMemberFuncTypes<void(OThirdPartyDeviceProcessor::*)(void*)>::
     SProcessorFunc<&OThirdPartyDeviceProcessor::OnParameter>()::{lambda(void*,void*)#1}::__invoke
               (void *param_1,void *param_2)

{
  int *piVar1;
  undefined4 *puVar2;
  uint uVar3;
  undefined4 uVar4;
  
  if (*(long *)((long)param_1 + 0x28) != 0) {
    piVar1 = (int *)((long)param_1 + 0x1096c);
    uVar3 = *(uint *)param_2;
    if ((uVar3 < 0x100) && (*piVar1 < 0x100)) {
      uVar4 = *(undefined4 *)((long)param_2 + 4);
      puVar2 = (undefined4 *)((long)param_1 + (ulong)uVar3 * 8 + 0x1006c);
      if ((*(byte *)(puVar2 + 1) & 1) == 0) {
        *(char *)((long)param_1 + (long)*piVar1 + 0x1086c) = (char)uVar3;
        *piVar1 = *piVar1 + 1;
      }
      *puVar2 = uVar4;
      *(undefined1 *)(puVar2 + 1) = 1;
    }
    *(undefined1 *)((long)param_1 + 0x11295) = 1;
  }
  return;
}

