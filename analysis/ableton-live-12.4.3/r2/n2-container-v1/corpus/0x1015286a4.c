
long FUN_1015286a4(long param_1)

{
  int iVar1;
  undefined8 *puVar2;
  long lVar3;
  long *plVar4;
  undefined8 local_48;
  
  puVar2 = (undefined8 *)FUN_10145f064();
  *puVar2 = &PTR_thunk_FUN_101533af8_106676ee0;
  FUN_1011cb734(puVar2 + 6);
  FUN_1011cb734(param_1 + 0x38);
  FUN_1011cb734(param_1 + 0x48);
  FUN_1011cb734(param_1 + 0x50);
  *(undefined8 *)(param_1 + 0x70) = 0;
  *(undefined8 *)(param_1 + 0x68) = 0;
  *(undefined1 *)(param_1 + 0x61) = 1;
  *(undefined8 *)(param_1 + 0x80) = 0;
  *(undefined8 *)(param_1 + 0x78) = 0;
  *(undefined8 *)(param_1 + 0x90) = 0;
  *(undefined8 *)(param_1 + 0x88) = 0;
  *(undefined8 *)(param_1 + 0xa0) = 0;
  *(undefined8 *)(param_1 + 0xa8) = 0;
  *(undefined8 *)(param_1 + 0xb0) = 0;
  FUN_1011cb734(param_1 + 0xc0);
  plVar4 = (long *)(param_1 + 0xd0);
  *plVar4 = 0;
  *(undefined1 *)(param_1 + 200) = 0;
  FUN_10129ece8(&local_48);
  lVar3 = *plVar4;
  if (lVar3 != 0) {
    iVar1 = *(int *)(lVar3 + 8) + -1;
    *(int *)(lVar3 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined8 *)(param_1 + 0xd0) = local_48;
  FUN_10145f25c(param_1,3,1);
  FUN_10145f25c(param_1,4,1);
  FUN_10145f25c(param_1,0,0);
  FUN_10145f25c(param_1,5,0);
  FUN_10145f25c(param_1,6,0);
  FUN_10145f25c(param_1,1,0);
  FUN_10145f25c(param_1,2,0);
  *(undefined2 *)(param_1 + 0x28) = 0;
  *(undefined1 *)(param_1 + 0x98) = 0;
  *(undefined1 *)(param_1 + 0xb8) = 0;
  *(undefined4 *)(param_1 + 0xbc) = 0;
  *(undefined4 *)(param_1 + 0x40) = 0;
  *(undefined1 *)(param_1 + 0x60) = 0;
  (**(code **)(**(long **)(param_1 + 0xd0) + 0xa8))(*(long **)(param_1 + 0xd0),0x4000);
  (**(code **)(*(long *)*plVar4 + 0x68))((long *)*plVar4,1);
  return param_1;
}

