
void FUN_1033bfa68(undefined8 param_1,long *param_2)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  ulong uVar4;
  long lVar5;
  logic_error *this;
  runtime_error *this_00;
  
  uVar2 = (**(code **)(*param_2 + 0x170))();
  uVar3 = FUN_1027afddc();
  uVar4 = FUN_10147fd68(uVar2,uVar3);
  if ((uVar4 & 1) == 0) {
    this = (logic_error *)___cxa_allocate_exception(0x10);
    std::logic_error::logic_error(this,"Warping is only available for audio clips");
  }
  else {
    lVar5 = FUN_1027c79d0(param_1,param_2,0);
    if (lVar5 != 0) {
      iVar1 = FUN_1026102c0();
      if (iVar1 == 0) {
        FUN_1027c6eec(param_2,lVar5);
        return;
      }
      this_00 = (runtime_error *)___cxa_allocate_exception(0x10);
      std::runtime_error::runtime_error(this_00,"The shadow marker can\'t be deleted.");
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(this_00,PTR_typeinfo_1064f86b0,PTR__runtime_error_1064f8560);
    }
    this = (logic_error *)___cxa_allocate_exception(0x10);
    std::logic_error::logic_error(this,"The specified warp marker doesn\'t exist");
  }
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(this,PTR_typeinfo_1064f86a8,PTR__logic_error_1064f8540);
}

