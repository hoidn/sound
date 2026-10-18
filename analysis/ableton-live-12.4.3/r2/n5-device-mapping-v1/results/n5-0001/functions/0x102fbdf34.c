
void FUN_102fbdf34(undefined8 param_1)

{
  ulong uVar1;
  char *pcVar2;
  undefined8 uVar3;
  size_t sVar4;
  undefined8 ***pppuVar5;
  undefined8 **local_80;
  size_t sStack_78;
  ulong local_70;
  char *local_68;
  undefined8 uStack_60;
  undefined8 **local_58;
  size_t sStack_50;
  undefined8 local_48;
  
  local_68 = (char *)0x0;
  uVar3 = FUN_101a9cac8(param_1,&uStack_60);
  FUN_101a9caac(uVar3,&local_68);
  uVar3 = thunk_FUN_101aa0448(0x98);
  pcVar2 = local_68;
  sVar4 = _strlen(local_68);
  if (0x7ffffffffffffff7 < sVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_100234518(&local_58);
  }
  if (sVar4 < 0x17) {
    local_48 = CONCAT17((char)sVar4,(undefined7)local_48);
    pppuVar5 = &local_58;
    if (sVar4 == 0) goto LAB_102fbdfd8;
  }
  else {
    uVar1 = 0x19;
    if ((sVar4 | 7) != 0x17) {
      uVar1 = (sVar4 | 7) + 1;
    }
    pppuVar5 = operator_new(uVar1);
    local_48 = uVar1 | 0x8000000000000000;
    local_58 = pppuVar5;
    sStack_50 = sVar4;
  }
  _memcpy(pppuVar5,pcVar2,sVar4);
LAB_102fbdfd8:
  *(undefined1 *)((long)pppuVar5 + sVar4) = 0;
  sStack_78 = sStack_50;
  local_80 = local_58;
  local_70 = local_48;
  FUN_102fbe07c(uVar3,uStack_60,&local_80);
  if ((long)local_70 < 0) {
    operator_delete(local_80);
  }
  FUN_101aa0360(local_68);
  return;
}

