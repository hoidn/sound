// x86 0x1054224a0 FUN_1054224a0 state=exported-with-warnings chunk=chunk-03676.jsonl code_sha256=99199f67f55e29fe29e0f39d358ae2eff3c015c4dc18162d5c43d7adacf0ea2f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

ulong FUN_1054224a0(void)

{
  uint uVar1;
  ulong uVar2;
  undefined1 auVar3 [16];
  undefined1 auVar4 [16];
  undefined1 auVar5 [16];
  undefined1 auVar6 [16];
  
  if (DAT_1074e2ba0 != (code *)0x0) {
    return 6;
  }
  uVar2 = FUN_105421ae0();
  if ((int)uVar2 == 1) {
    DAT_1074e2ba0 = (code *)FUN_105421bc0("RWPOpenImp");
    DAT_1074e2bb0 = FUN_105421bc0("RWPIsCloseOKImp");
    DAT_1074e2ba8 = FUN_105421bc0("RWPCloseImp");
    DAT_1074e2bb8 = FUN_105421bc0("RWIsReWireMixerAppRunningImp");
    DAT_1074e2bc0 = FUN_105421bc0("RWPLoadDeviceImp");
    DAT_1074e2bc8 = FUN_105421bc0("RWPUnloadDeviceImp");
    DAT_1074e2bd0 = FUN_105421bc0("RWPComConnectImp");
    DAT_1074e2bd8 = FUN_105421bc0("RWPComCheckConnectionImp");
    DAT_1074e2be0 = FUN_105421bc0("RWPComDisconnectImp");
    DAT_1074e2be8 = FUN_105421bc0("RWPComDoesMessageFitImp");
    DAT_1074e2bf0 = FUN_105421bc0("RWPComSendImp");
    DAT_1074e2bf8 = FUN_105421bc0("RWPComReadImp");
    DAT_1074e2c00 = FUN_105421bc0("RWPComBytesAvailableImp");
    DAT_1074e2c08 = FUN_105421bc0("RWPRegisterReWireDeviceImp");
    _DAT_1074e2c10 = FUN_105421bc0("RWPUnregisterReWireDeviceImp");
    auVar6._0_8_ = -(ulong)(DAT_1074e2bd0 == 0);
    auVar6._8_8_ = -(ulong)(DAT_1074e2bd8 == 0);
    auVar5._0_8_ = -(ulong)(DAT_1074e2bc0 == 0);
    auVar5._8_8_ = -(ulong)(DAT_1074e2bc8 == 0);
    auVar5 = packssdw(auVar5,auVar6);
    auVar4._0_8_ = -(ulong)(DAT_1074e2ba8 == 0);
    auVar4._8_8_ = -(ulong)(DAT_1074e2bb8 == 0);
    auVar3._0_8_ = -(ulong)(DAT_1074e2ba0 == (code *)0x0);
    auVar3._8_8_ = -(ulong)(DAT_1074e2bb0 == 0);
    auVar3 = packssdw(auVar3,auVar4);
    auVar3 = packssdw(auVar3,auVar5);
    uVar2 = 0x65;
    if (((((DAT_1074e2c00 != 0 && DAT_1074e2bf8 != 0) && DAT_1074e2c08 != 0) &&
         ((DAT_1074e2be8 != 0 && DAT_1074e2be0 != 0) && DAT_1074e2bf0 != 0)) && _DAT_1074e2c10 != 0)
        && ((((((((((((((((SUB161(auVar3 >> 7,0) & 1) == 0 && (SUB161(auVar3 >> 0xf,0) & 1) == 0) &&
                        (SUB161(auVar3 >> 0x17,0) & 1) == 0) && (SUB161(auVar3 >> 0x1f,0) & 1) == 0)
                      && (SUB161(auVar3 >> 0x27,0) & 1) == 0) && (SUB161(auVar3 >> 0x2f,0) & 1) == 0
                     ) && (SUB161(auVar3 >> 0x37,0) & 1) == 0) &&
                   (SUB161(auVar3 >> 0x3f,0) & 1) == 0) && (SUB161(auVar3 >> 0x47,0) & 1) == 0) &&
                 (SUB161(auVar3 >> 0x4f,0) & 1) == 0) && (SUB161(auVar3 >> 0x57,0) & 1) == 0) &&
               (SUB161(auVar3 >> 0x5f,0) & 1) == 0) && (SUB161(auVar3 >> 0x67,0) & 1) == 0) &&
             (SUB161(auVar3 >> 0x6f,0) & 1) == 0) && (SUB161(auVar3 >> 0x77,0) & 1) == 0) &&
           -1 < auVar3[0xf])) {
      uVar1 = (*DAT_1074e2ba0)(1000000);
      uVar2 = (ulong)uVar1;
      if (uVar1 == 1) {
        return 1;
      }
    }
    DAT_1074e2ba0 = (code *)0x0;
    DAT_1074e2bb0 = 0;
    DAT_1074e2ba8 = 0;
    DAT_1074e2bb8 = 0;
    DAT_1074e2bc0 = 0;
    DAT_1074e2bc8 = 0;
    DAT_1074e2bd0 = 0;
    DAT_1074e2bd8 = 0;
    DAT_1074e2be0 = 0;
    DAT_1074e2be8 = 0;
    DAT_1074e2bf0 = 0;
    DAT_1074e2bf8 = 0;
    DAT_1074e2c00 = 0;
    DAT_1074e2c08 = 0;
    _DAT_1074e2c10 = 0;
    FUN_105421c20();
  }
  return uVar2;
}

