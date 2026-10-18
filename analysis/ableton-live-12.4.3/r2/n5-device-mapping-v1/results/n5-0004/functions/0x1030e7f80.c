
void FUN_1030e7f80(void)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  undefined4 local_30 [2];
  int *local_28;
  
  FUN_10147e8c8(&DAT_106e79358);
  puVar3 = (undefined4 *)FUN_1026ee86c();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026ee89c();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x248,L"mpPolyphony",0xb,&DAT_1062a3ca0,0,
                local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x260,L"mpPitchBendRange",0x10,&DAT_1062a3ca0,0
                ,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x278,L"mpPerNotePitchBendRange",0x17,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x290,L"mpVolume",8,&DAT_1062a3ca0,0,local_30,
                uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x2a8,L"mpKeyboardTranspose",0x13,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x2c0,L"mpKeyboardFineTune",0x12,&DAT_1062a3ca0
                ,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x2d8,L"mpKeyboardStretch",0x11,&DAT_1062a3ca0,
                0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x2f0,L"mpMalletStiffness",0x11,&DAT_1062a3ca0,
                0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x308,L"mpMalletStiffnessKeyboard",0x19,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,800,L"mpMalletStiffnessVelocity",0x19,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x338,L"mpMalletForceStrength",0x15,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x350,L"mpMalletForceKeyboard",0x15,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x368,L"mpMalletForceVelocity",0x15,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x380,L"mpMalletNoisePitch",0x12,&DAT_1062a3ca0
                ,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x398,L"mpMalletNoiseDecay",0x12,&DAT_1062a3ca0
                ,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x3b0,L"mpMalletNoiseAmount",0x13,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x3c8,L"mpMalletNoiseKeyboardScaling",0x1c,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x3e0,L"mpForkReleaseTime",0x11,&DAT_1062a3ca0,
                0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x3f8,L"mpForkTineDecay",0xf,&DAT_1062a3ca0,0,
                local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x410,L"mpForkTineVolume",0x10,&DAT_1062a3ca0,0
                ,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x428,L"mpForkTineKeyboardScaling",0x19,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x440,L"mpForkTineColor",0xf,&DAT_1062a3ca0,0,
                local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x458,L"mpForkToneBarDecay",0x12,&DAT_1062a3ca0
                ,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x470,L"mpForkToneBarVolume",0x13,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x488,L"mpPickupSymmetry",0x10,&DAT_1062a3ca0,0
                ,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x4a0,L"mpPickupDistance",0x10,&DAT_1062a3ca0,0
                ,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026ee86c();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026ee89c();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x4b8,L"mpPickupModel",0xd,&DAT_1062a3ca0,0,
                local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x4d0,L"mpPickupAmpIn",0xd,&DAT_1062a3ca0,0,
                local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x4e8,L"mpPickupAmpOut",0xe,&DAT_1062a3ca0,0,
                local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x500,L"mpPickupAmpKeyboardScaling",0x1a,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x518,L"mpDamperTone",0xc,&DAT_1062a3ca0,0,
                local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x530,L"mpDamperAmount",0xe,&DAT_1062a3ca0,0,
                local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x548,L"mpDamperBalance",0xf,&DAT_1062a3ca0,0,
                local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_101568ea4();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_101568ed4();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x560,L"mpSelectedFinger",0x10,&DAT_1062a3ca0,0
                ,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_101568ea4();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_101568ed4();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x578,L"mpShowModToggle",0xf,&DAT_1062a3ca0,0,
                local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar3 = (undefined4 *)FUN_1026f01e8();
  local_30[0] = *puVar3;
  local_28 = *(int **)(puVar3 + 2);
  if (local_28 != (int *)0x0) {
    *local_28 = *local_28 + 1;
  }
  uVar2 = FUN_1026f0218();
  FUN_10147e954(&DAT_106e79358,0xffffffff,0xffffffff,0x590,L"mpDummyPerNotePitchBendRange",0x1c,
                &DAT_1062a3ca0,0,local_30,uVar2);
  if (local_28 != (int *)0x0) {
    iVar1 = *local_28;
    *local_28 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

