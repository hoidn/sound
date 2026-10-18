// 0x10073559c FUN_10073559c state=exported-with-warnings body_bytes=344 warnings=1 chunk=chunk-00293.jsonl

void FUN_10073559c(undefined8 param_1,undefined8 param_2,undefined4 param_3,undefined8 ****param_4)

{
  ulong uVar1;
  char cVar2;
  undefined8 ****ppppuVar3;
  undefined8 ***pppuVar4;
  undefined8 ****ppppuVar5;
  undefined8 ***local_98;
  undefined8 **local_90;
  char local_81;
  undefined8 ***local_80;
  undefined8 **ppuStack_78;
  ulong local_70;
  undefined8 ***local_60;
  undefined8 **ppuStack_58;
  undefined8 local_50;
  
  cVar2 = *(char *)((long)param_4 + 0x17);
  local_60 = *param_4;
  if (-1 < (long)cVar2) {
    local_60 = param_4;
  }
  ppuStack_58 = param_4[1];
  if (-1 < cVar2) {
    ppuStack_58 = (undefined8 ***)(long)cVar2;
  }
  local_50 = CONCAT44(local_50._4_4_,param_3);
  FUN_100762008(&local_98,"{}-files-{}.db",0xe,0x1d,&local_60);
  pppuVar4 = (undefined8 ***)(long)local_81;
  if ((long)pppuVar4 < 0) {
    if ((undefined8 ***)0x7ffffffffffffff7 < local_90) {
                    /* WARNING: Subroutine does not return */
      FUN_100147bd8(&local_60);
    }
    pppuVar4 = (undefined8 ***)local_90;
    ppppuVar5 = (undefined8 ****)local_98;
    if ((undefined8 ***)0x16 < local_90) goto LAB_100735638;
LAB_10073560c:
    local_50 = CONCAT17((char)local_90,(undefined7)local_50);
    ppppuVar3 = &local_60;
    pppuVar4 = (undefined8 ***)local_90;
    if ((undefined8 ***)local_90 == (undefined8 ***)0x0) goto LAB_100735670;
  }
  else {
    local_90 = pppuVar4;
    ppppuVar5 = &local_98;
    if (pppuVar4 < (undefined8 ***)0x17) goto LAB_10073560c;
LAB_100735638:
    uVar1 = 0x19;
    if (((ulong)pppuVar4 | 7) != 0x17) {
      uVar1 = ((ulong)pppuVar4 | 7) + 1;
    }
    ppppuVar3 = operator_new(uVar1);
    local_50 = uVar1 | 0x8000000000000000;
    local_60 = ppppuVar3;
    ppuStack_58 = pppuVar4;
  }
  _memmove(ppppuVar3,ppppuVar5,(size_t)pppuVar4);
  local_90 = pppuVar4;
LAB_100735670:
  *(undefined1 *)((long)ppppuVar3 + (long)local_90) = 0;
  ppuStack_78 = ppuStack_58;
  local_80 = local_60;
  local_70 = local_50;
  FUN_10014bdb8(param_1,param_2,&local_80);
  if ((long)local_70 < 0) {
    operator_delete(local_80);
  }
  if (local_81 < '\0') {
    operator_delete(local_98);
    return;
  }
  return;
}

