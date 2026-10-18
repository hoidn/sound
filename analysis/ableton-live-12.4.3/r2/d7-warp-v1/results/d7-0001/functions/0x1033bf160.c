
void FUN_1033bf160(double param_1,long *param_2)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  ulong uVar4;
  logic_error *this;
  double dVar5;
  
  uVar2 = (**(code **)(*param_2 + 0x170))();
  uVar3 = FUN_1027afddc();
  iVar1 = FUN_10147fd68(uVar2,uVar3);
  if (iVar1 == 0) {
    this = (logic_error *)___cxa_allocate_exception(0x10);
    std::logic_error::logic_error(this,"Conversion is only available for audio clips");
  }
  else {
    uVar4 = (**(code **)(*param_2 + 0x300))(param_2);
    if ((uVar4 & 1) != 0) {
      dVar5 = (double)FUN_1027b7514(param_2);
                    /* WARNING: Could not recover jumptable at 0x0001033bf1d8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(*param_2 + 0x4b8))(param_1 / dVar5,param_2,1);
      return;
    }
    this = (logic_error *)___cxa_allocate_exception(0x10);
    std::logic_error::logic_error(this,"Cannot convert sample to beat time for unwarped clips.");
  }
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(this,PTR_typeinfo_1064f86a8,PTR__logic_error_1064f8540);
}

