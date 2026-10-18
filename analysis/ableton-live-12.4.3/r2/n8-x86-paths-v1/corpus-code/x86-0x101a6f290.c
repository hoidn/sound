// x86 0x101a6f290 FUN_101a6f290 state=exported-with-warnings chunk=chunk-01151.jsonl code_sha256=e8d87a64ef3f11a0c271716cf58da7696609b4546d57388b96488192b2611f17

void FUN_101a6f290(long param_1,int param_2,undefined1 param_3,char param_4)

{
  undefined8 *puVar1;
  long *plVar2;
  char cVar3;
  int iVar4;
  
  if (param_2 == 0) {
    if ((((*(byte *)(param_1 + 0x8e0) & 1) == 0) || ((*(byte *)(param_1 + 0x8e1) & 1) == 0)) &&
       (DAT_10750a148 != (code *)PTR__lambda___1___106a97940)) {
                    /* WARNING: Could not recover jumptable at 0x000101a6f2ff. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (*DAT_10750a148)(DAT_10750a150);
      return;
    }
    FUN_101a6f3c0(param_1,0,param_3);
    return;
  }
  if ((((*(byte *)(param_1 + 0x8e0) & 1) == 0) || ((*(byte *)(param_1 + 0x8e1) & 1) == 0)) &&
     (DAT_10750a158 != (code *)PTR__lambda___1___106a97940)) {
                    /* WARNING: Could not recover jumptable at 0x000101a6f2cd. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (*DAT_10750a158)(DAT_10750a160);
    return;
  }
  if (((param_4 != '\0') &&
      (puVar1 = *(undefined8 **)(param_1 + 0x9b0), puVar1 != (undefined8 *)0x0)) &&
     (cVar3 = (**(code **)*puVar1)(puVar1), cVar3 != '\0')) {
    return;
  }
  plVar2 = *(long **)(param_1 + 0x9b0);
  if (plVar2 != (long *)0x0) {
    (**(code **)(*plVar2 + 0x10))(plVar2);
  }
  FUN_101a6f520(*(undefined8 *)(param_1 + 0x30),1);
  if ((DAT_1073e7c60 == '\0') && (iVar4 = ___cxa_guard_acquire(&DAT_1073e7c60), iVar4 != 0)) {
    FUN_10118ff00(&DAT_1073e7c50);
    ___cxa_guard_release(&DAT_1073e7c60);
  }
  DAT_1073e7c4c = 0;
  return;
}

