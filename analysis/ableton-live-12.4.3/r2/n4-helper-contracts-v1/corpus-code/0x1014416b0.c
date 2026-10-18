// 0x1014416b0 FUN_1014416b0 exported  sig: undefined FUN_1014416b0()

undefined8 FUN_1014416b0(undefined8 param_1,undefined8 param_2)

{
  int iVar1;
  uint uVar2;
  ulong uVar3;
  undefined8 uVar4;
  int *local_48;
  undefined1 local_40 [16];
  
  local_40 = FUN_1011aeb80();
  if ((local_40._8_8_ & 1) == 0) {
    return param_2;
  }
  FUN_1011abfa4(local_40);
  FUN_101427680(&local_48);
  uVar3 = FUN_1014289f4(&local_48,"Normal");
  if ((uVar3 & 1) != 0) {
    uVar4 = 0;
    uVar2 = 0;
    goto joined_r0x00010144177c;
  }
  uVar3 = FUN_1014289f4(&local_48,"BelowNormal1");
  if ((uVar3 & 1) == 0) {
    uVar3 = FUN_1014289f4(&local_48,"BelowNormal2");
    if ((uVar3 & 1) != 0) {
      uVar2 = 0;
      uVar4 = 2;
      goto joined_r0x00010144177c;
    }
    uVar3 = FUN_1014289f4(&local_48,"BelowNormal3");
    if ((uVar3 & 1) == 0) {
      uVar2 = FUN_1014289f4(&local_48,"Idle");
      uVar2 = uVar2 ^ 1;
      uVar4 = 4;
      goto joined_r0x00010144177c;
    }
    uVar4 = 3;
  }
  else {
    uVar4 = 1;
  }
  uVar2 = 0;
joined_r0x00010144177c:
  if ((local_48 != (int *)0x0) && (iVar1 = *local_48, *local_48 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((uVar2 & 1) == 0) {
    param_2 = uVar4;
  }
  return param_2;
}


