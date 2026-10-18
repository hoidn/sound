// 0x1012946e8 FUN_1012946e8 exported  sig: undefined FUN_1012946e8()

bool FUN_1012946e8(uint *param_1,uint *param_2)

{
  return (*param_2 & (*param_1 ^ 0xffffffff)) == 0;
}


