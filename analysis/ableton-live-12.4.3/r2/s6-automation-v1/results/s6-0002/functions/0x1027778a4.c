
bool FUN_1027778a4(undefined1 param_1 [16],double param_2,double param_3,double param_4,
                  long *param_5)

{
  bool bVar1;
  bool bVar2;
  double dVar3;
  
  dVar3 = (double)(**(code **)(*param_5 + 0x218))();
  bVar1 = false;
  if ((dVar3 == 0.5) && (bVar1 = false, !NAN(param_2))) {
    bVar1 = param_2 == 0.5;
  }
  bVar2 = false;
  if ((bVar1) && (bVar2 = false, !NAN(param_3))) {
    bVar2 = param_3 == 0.5;
  }
  if (!bVar2) {
    return true;
  }
  return param_4 != 0.5;
}

