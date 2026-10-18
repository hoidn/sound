
void FUN_1026ef060(void)

{
  int iVar1;
  undefined8 *in_x3;
  int *piVar2;
  
  piVar2 = (int *)*in_x3;
  if (piVar2 != (int *)0x0) {
    *piVar2 = *piVar2 + 1;
  }
  FUN_1026ef0dc();
  if (piVar2 != (int *)0x0) {
    iVar1 = *piVar2;
    *piVar2 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc(piVar2);
    }
  }
  return;
}

