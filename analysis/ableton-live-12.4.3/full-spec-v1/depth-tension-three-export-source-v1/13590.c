
void _SetParameterA(long *param_1)

{
  if (param_1 == (long *)0x0) {
    if ((DAT_000605e0 & 1) == 0) {
      _fwrite("SetParameterA called with nullptr.\n",0x23,1,*(FILE **)PTR____stderrp_0005c098);
      DAT_000605e0 = 1;
      return;
    }
  }
  else {
    (**(code **)(*param_1 + 0x38))();
  }
  return;
}

