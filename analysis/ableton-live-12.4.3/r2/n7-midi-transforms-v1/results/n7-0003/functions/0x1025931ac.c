
void FUN_1025931ac(uint param_1,uint param_2,int param_3)

{
  runtime_error *this;
  
  if (param_1 < 0x10) {
    if ((param_2 < 0x80) && ((param_2 < 0x60 || (param_3 != 5)))) {
      return;
    }
    this = (runtime_error *)___cxa_allocate_exception(0x10);
    std::runtime_error::runtime_error(this,"Invalid cc_no parameter.");
  }
  else {
    this = (runtime_error *)___cxa_allocate_exception(0x10);
    std::runtime_error::runtime_error(this,"Invalid channel parameter.");
  }
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(this,PTR_typeinfo_1064f86b0,PTR__runtime_error_1064f8560);
}

