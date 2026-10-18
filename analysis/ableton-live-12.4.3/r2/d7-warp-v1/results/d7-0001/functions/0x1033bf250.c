
undefined1  [16] FUN_1033bf250(undefined8 param_1,long *param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  ulong uVar3;
  logic_error *this;
  double dVar4;
  double dVar5;
  undefined1 auVar6 [16];
  
  uVar1 = (**(code **)(*param_2 + 0x170))();
  uVar2 = FUN_1027afddc();
  uVar3 = FUN_10147fd68(uVar1,uVar2);
  if ((uVar3 & 1) == 0) {
    this = (logic_error *)___cxa_allocate_exception(0x10);
    std::logic_error::logic_error(this,"Conversion is only available for audio clips");
  }
  else {
    uVar3 = (**(code **)(*param_2 + 0x300))(param_2);
    if ((uVar3 & 1) != 0) {
      dVar4 = (double)(**(code **)(*param_2 + 0x4c0))(param_1,param_2,1);
      dVar5 = (double)FUN_1027b7514(param_2);
      auVar6._0_8_ = dVar5 * dVar4;
      auVar6._8_8_ = 0;
      return auVar6;
    }
    this = (logic_error *)___cxa_allocate_exception(0x10);
    std::logic_error::logic_error(this,"Cannot convert beat to sample time for unwarped clips.");
  }
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(this,PTR_typeinfo_1064f86a8,PTR__logic_error_1064f8540);
}

