// 0x102966800 FUN_102966800 exported  sig: undefined FUN_102966800()

void FUN_102966800(long param_1)

{
  int iVar1;
  long lVar2;
  long local_30 [2];
  
  local_30[0] = 0;
  local_30[1] = 0;
  *(undefined8 *)(param_1 + 0x58) = 0;
  lVar2 = *(long *)(param_1 + 0x50);
  if (lVar2 != 0) {
    iVar1 = *(int *)(lVar2 + 8) + -1;
    *(int *)(lVar2 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined8 *)(param_1 + 0x50) = 0;
  lVar2 = *(long *)(param_1 + 0x48);
  if (lVar2 != 0) {
    iVar1 = *(int *)(lVar2 + 8) + -1;
    *(int *)(lVar2 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined8 *)(param_1 + 0x48) = 0;
  *(undefined1 *)(param_1 + 0x60) = 0;
  *(undefined4 *)(param_1 + 100) = 0;
  local_30[0] = 0;
  local_30[1] = 0;
  FUN_1029655e4(*(undefined8 *)(param_1 + 0x40),local_30,0);
  if (local_30[0] != 0) {
    iVar1 = *(int *)(local_30[0] + 8) + -1;
    *(int *)(local_30[0] + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  if (*(char *)(param_1 + 0x38) != '\0') {
    *(undefined1 *)(param_1 + 0x38) = 0;
    FUN_1017cde1c(param_1 + 0x18,0);
  }
  return;
}


