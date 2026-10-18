
void FUN_102f998c4(long param_1,undefined8 *param_2)

{
  ulong uVar1;
  undefined8 *puVar2;
  int iVar3;
  long lVar4;
  undefined8 uVar5;
  
  uVar5 = *(undefined8 *)PTR__kCFAllocatorDefault_1064f8088;
  uVar1 = param_2[1];
  puVar2 = (undefined8 *)*param_2;
  if (-1 < (char)*(byte *)((long)param_2 + 0x17)) {
    uVar1 = (ulong)*(byte *)((long)param_2 + 0x17);
    puVar2 = param_2;
  }
  lVar4 = _CFURLCreateFromFileSystemRepresentation(uVar5,puVar2,uVar1,1);
  if (lVar4 != 0) {
    _CFAutorelease();
    lVar4 = _CFBundleCreate(uVar5,lVar4);
    *(long *)(param_1 + 0x48) = lVar4;
    if ((((lVar4 != 0) && (iVar3 = _CFBundleIsExecutableLoaded(), iVar3 == 0)) &&
        (iVar3 = _CFBundleLoadExecutable(*(undefined8 *)(param_1 + 0x48)), iVar3 == 0)) &&
       (FUN_102fbe248(param_1), *(long *)(param_1 + 0x48) != 0)) {
      _CFRelease();
      *(undefined8 *)(param_1 + 0x48) = 0;
    }
  }
  if (*(long *)(param_1 + 0x48) != 0) {
    uVar5 = _CFBundleGetFunctionPointerForName(*(long *)(param_1 + 0x48),&cf_GetPlugInfoU);
    FUN_102fbe49c(param_1,uVar5);
    uVar5 = _CFBundleGetFunctionPointerForName(*(undefined8 *)(param_1 + 0x48),&cf_CreateInstanceU);
    *(undefined8 *)(param_1 + 0x18) = uVar5;
    uVar5 = _CFBundleGetFunctionPointerForName(*(undefined8 *)(param_1 + 0x48),&cf_DestroyInstanceU)
    ;
    *(undefined8 *)(param_1 + 0x20) = uVar5;
    uVar5 = _CFBundleGetFunctionPointerForName(*(undefined8 *)(param_1 + 0x48),&cf_SetSampleRateU);
    *(undefined8 *)(param_1 + 0x28) = uVar5;
    uVar5 = _CFBundleGetFunctionPointerForName(*(undefined8 *)(param_1 + 0x48),&cf_CalcA);
    *(undefined8 *)(param_1 + 0x30) = uVar5;
    uVar5 = _CFBundleGetFunctionPointerForName(*(undefined8 *)(param_1 + 0x48),&cf_SetParameterA);
    *(undefined8 *)(param_1 + 0x38) = uVar5;
    uVar5 = _CFBundleGetFunctionPointerForName(*(undefined8 *)(param_1 + 0x48),&cf_ResetA);
    *(undefined8 *)(param_1 + 0x40) = uVar5;
  }
  return;
}

