
void FUN_1033bfb94(undefined8 param_1,undefined8 param_2,long *param_3)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  ulong uVar4;
  long lVar5;
  logic_error *this;
  runtime_error *this_00;
  long *local_48;
  long *local_40;
  long *plStack_38;
  
  uVar2 = (**(code **)(*param_3 + 0x170))();
  uVar3 = FUN_1027afddc();
  uVar4 = FUN_10147fd68(uVar2,uVar3);
  if ((uVar4 & 1) == 0) {
    this = (logic_error *)___cxa_allocate_exception(0x10);
    std::logic_error::logic_error(this,"Warping is only available for audio clips");
  }
  else {
    lVar5 = FUN_1027c79d0(param_1,param_3,0);
    if (lVar5 != 0) {
      iVar1 = FUN_1026102c0();
      if (iVar1 == 0) {
        local_48 = operator_new(8);
        local_40 = local_48 + 1;
        *local_48 = lVar5;
        plStack_38 = local_40;
        FUN_1027b83bc(param_2,param_3,&local_48);
        if (local_48 != (long *)0x0) {
          local_40 = local_48;
          operator_delete(local_48);
        }
        return;
      }
      this_00 = (runtime_error *)___cxa_allocate_exception(0x10);
      std::runtime_error::runtime_error(this_00,"The shadow marker can\'t be moved.");
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(this_00,PTR_typeinfo_1064f86b0,PTR__runtime_error_1064f8560);
    }
    this = (logic_error *)___cxa_allocate_exception(0x10);
    std::logic_error::logic_error(this,"The specified warp marker doesn\'t exist");
  }
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(this,PTR_typeinfo_1064f86a8,PTR__logic_error_1064f8540);
}

