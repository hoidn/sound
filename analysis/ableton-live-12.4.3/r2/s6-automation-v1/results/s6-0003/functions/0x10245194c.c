
void FUN_10245194c(long param_1,undefined8 param_2,undefined8 param_3)

{
  long *plVar1;
  long lVar2;
  
  lVar2 = *(long *)(param_1 + 0x30);
  FUN_101487c3c(*(undefined8 *)(lVar2 + 8));
  plVar1 = *(long **)(lVar2 + 0x30);
                    /* WARNING: Could not recover jumptable at 0x000102451980. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(*plVar1 + 0x1e8))(plVar1,param_3);
  return;
}

