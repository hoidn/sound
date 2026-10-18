
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_101485240(long *param_1,long param_2,ulong param_3,ulong param_4)

{
  byte bVar1;
  undefined8 *puVar2;
  bool bVar3;
  int iVar4;
  uint uVar5;
  long lVar6;
  wchar16 *pwVar7;
  undefined8 uVar8;
  int *piVar9;
  undefined8 *puVar10;
  undefined8 uVar11;
  undefined8 *puVar12;
  int *local_a0;
  int *local_98;
  int *local_90;
  int *local_88;
  int *local_80;
  long local_78;
  wchar16 *local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined1 local_50 [16];
  
  lVar6 = (**(code **)(*param_1 + 0x170))();
  bVar1 = *(byte *)(lVar6 + 0xbe);
  if (bVar1 == 1) {
    FUN_1015154fc();
    iVar4 = FUN_1015147cc();
    if (iVar4 == -0x80000000) {
      local_70 = L"ACompound::SaveXmlStream";
      uStack_68 = 0x18;
                    /* WARNING: Subroutine does not return */
      FUN_10124210c(&local_70);
    }
  }
  if ((int)param_3 == -1) {
    uStack_68 = _UNK_105815b24;
    local_70 = _DAT_105815b1c;
    uStack_58 = _UNK_105815b34;
    uStack_60 = _DAT_105815b2c;
    local_50 = FUN_1011aeb80(&local_70);
    if ((local_50._8_8_ & 1) == 0) {
      param_3 = 6;
    }
    else {
      uVar5 = FUN_1011ac014(local_50,1,6);
      if (8 < (int)uVar5) {
        uVar5 = 9;
      }
      param_3 = (ulong)(uVar5 & ((int)uVar5 >> 0x1f ^ 0xffffffffU));
    }
  }
  FUN_1014338b0(param_2,0x100000,param_3);
  FUN_100258fe8(&DAT_106f4f750,DAT_106f4f758);
  DAT_106f4f750 = &DAT_106f4f758;
  DAT_106f4f760 = 0;
  DAT_106f4f758 = 0;
  (**(code **)(*param_1 + 0x168))(param_1);
  FUN_101485a6c();
  local_50._0_8_ = 0;
  pwVar7 = (wchar16 *)FUN_1012d9850(0x60);
  FUN_1015209e4();
  if (pwVar7 != (wchar16 *)0x0) {
    *(int *)(pwVar7 + 4) = *(int *)(pwVar7 + 4) + 1;
  }
  local_70 = pwVar7;
  if ((local_50._0_8_ != 0) &&
     (iVar4 = *(int *)(local_50._0_8_ + 8) + -1, *(int *)(local_50._0_8_ + 8) = iVar4, iVar4 == 0))
  {
    FUN_10128eea0();
  }
  if (param_2 != 0) {
    *(int *)(param_2 + 8) = *(int *)(param_2 + 8) + 1;
  }
  local_78 = param_2;
  local_50._0_8_ = pwVar7;
  FUN_101517044(pwVar7,&local_78);
  if ((local_78 != 0) &&
     (iVar4 = *(int *)(local_78 + 8) + -1, *(int *)(local_78 + 8) = iVar4, iVar4 == 0)) {
    FUN_10128eea0();
  }
  if ((param_4 & 1) == 0) {
    (**(code **)(*param_1 + 0x108))(param_1,param_2);
  }
  FUN_101515508(&local_80);
  FUN_1015170a8(local_50._0_8_);
  uVar11 = local_50._0_8_;
  FUN_101427680(&local_70,"Ableton");
  FUN_1015170e0(uVar11,&local_70);
  if ((local_70 != (wchar16 *)0x0) &&
     (iVar4 = *(int *)local_70, *(int *)local_70 = iVar4 + -1, iVar4 + -1 == 0)) {
    FUN_101449efc();
  }
  uVar11 = local_50._0_8_;
  if (bVar1 != 0) {
    FUN_1015227f8(local_50._0_8_,"MajorVersion",0x22);
    FUN_101520b2c(uVar11,5);
    FUN_101522920(uVar11,0x22);
    FUN_101517404(local_50._0_8_,"MinorVersion",&local_80);
    FUN_1015154fc();
    iVar4 = FUN_1015147cc();
    uVar11 = local_50._0_8_;
    if (0 < iVar4) {
      FUN_1015154fc();
      uVar8 = FUN_1015147cc();
      FUN_1015227f8(uVar11,"SchemaChangeCount",0x22);
      FUN_101520b2c(uVar11,uVar8);
      FUN_101522920(uVar11,0x22);
    }
    uVar11 = local_50._0_8_;
    FUN_101427680(&local_88,"Ableton ");
    FUN_1011c4690();
    FUN_101427680(&local_70);
    uVar8 = FUN_10142da5c(&local_88,&local_70);
    if ((local_70 != (wchar16 *)0x0) &&
       (iVar4 = *(int *)local_70, *(int *)local_70 = iVar4 + -1, iVar4 + -1 == 0)) {
      FUN_101449efc();
    }
    FUN_101517404(uVar11,"Creator",uVar8);
    if ((local_88 != (int *)0x0) && (iVar4 = *local_88, *local_88 = iVar4 + -1, iVar4 + -1 == 0)) {
      FUN_101449efc();
    }
    uVar11 = local_50._0_8_;
    FUN_1011c45d8();
    FUN_101427680(&local_70);
    FUN_101517404(uVar11,"Revision",&local_70);
    if ((local_70 != (wchar16 *)0x0) &&
       (iVar4 = *(int *)local_70, *(int *)local_70 = iVar4 + -1, iVar4 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  FUN_101520ae0(local_50._0_8_,bVar1);
  FUN_101520af0(local_50._0_8_,bVar1 ^ 1);
  uVar11 = local_50._0_8_;
  lVar6 = (**(code **)(*param_1 + 0x170))(param_1);
  piVar9 = *(int **)(lVar6 + 0x10);
  if (piVar9 != (int *)0x0) {
    uVar5 = piVar9[1];
    if (*piVar9 == 0) {
      FUN_101449efc();
    }
    if ((uVar5 & 0xfffffffe) == 2) {
      (**(code **)(*param_1 + 0x168))(param_1);
      puVar10 = (undefined8 *)FUN_10120e26c();
      local_70 = (wchar16 *)*puVar10;
      goto joined_r0x0001014855ec;
    }
  }
  lVar6 = (**(code **)(*param_1 + 0x170))(param_1);
  local_70 = *(wchar16 **)(lVar6 + 0x10);
joined_r0x0001014855ec:
  if (local_70 != (wchar16 *)0x0) {
    *(int *)local_70 = *(int *)local_70 + 1;
  }
  FUN_1015170e0(uVar11,&local_70);
  if ((local_70 != (wchar16 *)0x0) &&
     (iVar4 = *(int *)local_70, *(int *)local_70 = iVar4 + -1, iVar4 + -1 == 0)) {
    FUN_101449efc();
  }
  (**(code **)(*param_1 + 0x138))(param_1,local_50._0_8_);
  FUN_10151752c(local_50._0_8_);
  FUN_10151752c(local_50._0_8_);
  FUN_101517610(local_50._0_8_);
  FUN_1014339e4(param_2);
  if ((bVar1 != 0) && (DAT_106f4f760 != 0)) {
    uVar11 = std::chrono::system_clock::now();
    FUN_103f3ffec(&local_70,4,uVar11);
    iVar4 = FUN_103f3c8b8(&local_70);
    if (iVar4 != 0) {
      FUN_103f39a78(&local_70,"Schema: *** Schema error! ***");
    }
    thunk_FUN_103f395e4(&local_70);
    puVar10 = DAT_106f4f750;
    if (DAT_106f4f750 != &DAT_106f4f758) {
      do {
        uVar11 = std::chrono::system_clock::now();
        FUN_103f3ffec(&local_70,4,uVar11);
        iVar4 = FUN_103f3c8b8(&local_70);
        if (iVar4 != 0) {
          uVar11 = FUN_103f39a78(&local_70,"Schema: ");
          FUN_101432ff0(uVar11,puVar10 + 4);
        }
        thunk_FUN_103f395e4(&local_70);
        puVar2 = (undefined8 *)puVar10[1];
        if ((undefined8 *)puVar10[1] == (undefined8 *)0x0) {
          do {
            puVar12 = (undefined8 *)puVar10[2];
            bVar3 = (undefined8 *)*puVar12 != puVar10;
            puVar10 = puVar12;
          } while (bVar3);
        }
        else {
          do {
            puVar12 = puVar2;
            puVar2 = (undefined8 *)*puVar12;
          } while ((undefined8 *)*puVar12 != (undefined8 *)0x0);
        }
        puVar10 = puVar12;
      } while (puVar12 != &DAT_106f4f758);
    }
    FUN_100258fe8(&DAT_106f4f750,DAT_106f4f758);
    DAT_106f4f750 = &DAT_106f4f758;
    DAT_106f4f760 = 0;
    DAT_106f4f758 = 0;
    FUN_1011cb734(&local_70);
    FUN_1011cb734(&local_88);
    FUN_1011cb734(&local_90);
    FUN_1011cb734(&local_98);
    FUN_1011cb734(&local_a0);
    FUN_101241d1c(&DAT_106f4f738,&local_70,&local_88,&local_90,&local_98,&local_a0);
    if ((local_a0 != (int *)0x0) && (iVar4 = *local_a0, *local_a0 = iVar4 + -1, iVar4 + -1 == 0)) {
      FUN_101449efc();
    }
    if ((local_98 != (int *)0x0) && (iVar4 = *local_98, *local_98 = iVar4 + -1, iVar4 + -1 == 0)) {
      FUN_101449efc();
    }
    if ((local_90 != (int *)0x0) && (iVar4 = *local_90, *local_90 = iVar4 + -1, iVar4 + -1 == 0)) {
      FUN_101449efc();
    }
    if ((local_88 != (int *)0x0) && (iVar4 = *local_88, *local_88 = iVar4 + -1, iVar4 + -1 == 0)) {
      FUN_101449efc();
    }
    if ((local_70 != (wchar16 *)0x0) &&
       (iVar4 = *(int *)local_70, *(int *)local_70 = iVar4 + -1, iVar4 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  if ((local_80 != (int *)0x0) && (iVar4 = *local_80, *local_80 = iVar4 + -1, iVar4 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((((wchar16 *)local_50._0_8_ != (wchar16 *)0x0) &&
      ((**(code **)(*(long *)local_50._0_8_ + 0x18))(), (wchar16 *)local_50._0_8_ != (wchar16 *)0x0)
      ) && (iVar4 = *(int *)(local_50._0_8_ + 8), *(int *)(local_50._0_8_ + 8) = iVar4 + -1,
           iVar4 + -1 == 0)) {
    FUN_10128eea0();
  }
  return;
}

