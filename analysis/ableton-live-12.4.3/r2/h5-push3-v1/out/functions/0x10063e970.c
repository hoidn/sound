// 0x10063e970 FUN_10063e970 state=exported-with-warnings role={}-files-{}.db
// source chunk chunk-00225.jsonl; code_sha256=95c83dffef2899c3b2e0f60909b693353f8c58a74562f632abfa470a3b81c20b

void FUN_10063e970(undefined8 param_1,undefined8 param_2,undefined4 param_3,undefined8 ****param_4)

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
  FUN_1002e72a4(&local_98,"{}-files-{}.db",0xe,0x1d,&local_60);
  pppuVar4 = (undefined8 ***)(long)local_81;
  if ((long)pppuVar4 < 0) {
    if ((undefined8 ***)0x7ffffffffffffff7 < local_90) {
                    /* WARNING: Subroutine does not return */
      FUN_100181308(&local_60);
    }
    pppuVar4 = (undefined8 ***)local_90;
    ppppuVar5 = (undefined8 ****)local_98;
    if ((undefined8 ***)0x16 < local_90) goto LAB_10063ea0c;
LAB_10063e9e0:
    local_50 = CONCAT17((char)local_90,(undefined7)local_50);
    ppppuVar3 = &local_60;
    pppuVar4 = (undefined8 ***)local_90;
    if ((undefined8 ***)local_90 == (undefined8 ***)0x0) goto LAB_10063ea44;
  }
  else {
    local_90 = pppuVar4;
    ppppuVar5 = &local_98;
    if (pppuVar4 < (undefined8 ***)0x17) goto LAB_10063e9e0;
LAB_10063ea0c:
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
LAB_10063ea44:
  *(undefined1 *)((long)ppppuVar3 + (long)local_90) = 0;
  ppuStack_78 = ppuStack_58;
  local_80 = local_60;
  local_70 = local_50;
  FUN_1001a63f8(param_1,param_2,&local_80);
  if ((long)local_70 < 0) {
    operator_delete(local_80);
  }
  if (local_81 < '\0') {
    operator_delete(local_98);
    return;
  }
  return;
}

