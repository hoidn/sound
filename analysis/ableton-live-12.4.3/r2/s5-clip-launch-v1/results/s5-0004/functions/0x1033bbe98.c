
void FUN_1033bbe98(undefined8 param_1,uint param_2)

{
  logic_error *this;
  undefined8 *puVar1;
  ulong local_80 [2];
  char local_69;
  char acStack_68 [24];
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40;
  
  if (3 < param_2) {
    this = (logic_error *)___cxa_allocate_exception(0x10);
    FUN_1002aa2a4(acStack_68,"Invalid launch mode ");
    std::to_string(param_2);
    if (-1 < local_69) {
      local_80[0] = (ulong)local_80;
    }
    puVar1 = (undefined8 *)std::string::append(acStack_68,local_80[0]);
    uStack_48 = puVar1[1];
    local_50 = *puVar1;
    local_40 = puVar1[2];
    puVar1[1] = 0;
    puVar1[2] = 0;
    *puVar1 = 0;
    std::logic_error::logic_error(this,(string *)&local_50);
    *(undefined **)this = PTR_vtable_1064f87d0 + 0x10;
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(this,PTR_typeinfo_106537588,PTR__invalid_argument_1064f8570);
  }
  FUN_10243f800();
  return;
}

