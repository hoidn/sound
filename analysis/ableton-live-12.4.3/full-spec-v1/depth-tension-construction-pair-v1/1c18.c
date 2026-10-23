
void FUN_00001c18(long param_1)

{
  long *plVar1;
  
  if ((param_1 != 0) &&
     (plVar1 = (long *)___dynamic_cast(param_1,&PTR_vtable_0005d6b8,&PTR_vtable_0005d630,0),
     plVar1 != (long *)0x0)) {
    FUN_000161cc();
    if ((long *)plVar1[1] != (long *)0x0) {
      (**(code **)(*(long *)plVar1[1] + 8))();
    }
                    /* WARNING: Could not recover jumptable at 0x00001c74. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 8))(plVar1);
    return;
  }
  return;
}

