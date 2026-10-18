
void FUN_1011c39e0(undefined8 param_1)

{
  if ((DAT_106f4dea0 & 1) == 0) {
    FUN_1054103b4();
    FUN_1011c3a54(&DAT_106f4dee8,param_1);
  }
  else {
    FUN_1011c3a54(&DAT_106f4dee8);
  }
  if ((DAT_106f4dea0 & 1) != 0) {
    return;
  }
  FUN_10541040c();
  return;
}

