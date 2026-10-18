
void FUN_1005e91fc(long *param_1,undefined8 param_2,undefined8 param_3,long *param_4,long *param_5)

{
  int *piVar1;
  size_t sVar2;
  char *pcVar3;
  bool bVar4;
  int *piVar5;
  void *pvVar6;
  int *piVar7;
  void *pvVar8;
  int iVar9;
  undefined8 uVar10;
  ulong uVar11;
  void *pvVar12;
  undefined8 *puVar13;
  undefined4 uVar14;
  ulong uVar15;
  undefined1 auVar16 [16];
  undefined8 *local_340;
  int *local_338 [2];
  char local_321;
  undefined1 local_320 [16];
  char local_309;
  int *local_308;
  int *local_300;
  void *local_2f8 [2];
  char local_2e1;
  int *local_2e0;
  int *local_2d8;
  undefined8 *local_2d0;
  undefined8 local_2c8;
  undefined8 uStack_2c0;
  void *local_2b8 [2];
  char local_2a1;
  void *local_2a0 [2];
  char local_289;
  int local_288 [2];
  undefined8 local_280;
  undefined1 auStack_278 [8];
  int *local_270;
  int *local_268;
  char local_259;
  int *local_258;
  ulong local_250;
  undefined8 local_248;
  void *local_90;
  void *local_88;
  char local_78;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_100b1c378;
  FUN_100184120(auStack_278);
  local_288[0] = 0;
  local_280 = std::system_category();
  FUN_100674264(local_2a0,param_3,local_288);
  if (local_288[0] == 0) {
    local_248._7_1_ = '\b';
    local_258 = (int *)&DAT_6e61637367756c70;
    local_250 = local_250 & 0xffffffffffffff00;
    uVar10 = std::chrono::system_clock::now();
    FUN_1006a284c(&local_270,2,&local_258,uVar10);
    if (local_248._7_1_ < '\0') {
      operator_delete(local_258);
    }
    iVar9 = FUN_10069f1d8(&local_270);
    if (iVar9 != 0) {
      uVar10 = FUN_10069c398(&local_270,"VST3: check plugin at path: ");
      FUN_10013300c(uVar10,local_2a0);
    }
    thunk_FUN_10069bf04(&local_270);
    (**(code **)(*param_4 + 0x18))(local_2b8,param_4,local_2a0,local_288);
    if (local_288[0] != 0) {
      uVar10 = std::chrono::system_clock::now();
      FUN_1006a290c(&local_258,3,uVar10);
      iVar9 = FUN_10069f1d8(&local_258);
      if (iVar9 != 0) {
        uVar10 = FUN_10069c398(&local_258,"VST3: couldn\'t determine plugin\'s fingerprint: ");
        FUN_1005ac678(uVar10,local_288);
      }
      thunk_FUN_10069bf04(&local_258);
    }
    uVar10 = FUN_1005aa7cc();
    local_258 = (int *)0x0;
    local_250 = 0;
    local_248 = 0;
    auVar16 = (**(code **)(*param_1 + 0x18))
                        (param_1,local_2a0,3,uVar10,param_2,local_2b8,&local_258);
    uVar11 = auVar16._0_8_;
    if (local_248 < 0) {
      operator_delete(local_258);
    }
    uStack_2c0 = 0;
    local_2c8 = 0;
    local_2d0 = &local_2c8;
    if ((uVar11 >> 0x20 & 1) != 0) {
      local_340 = &local_2c8;
      uStack_2c0 = 0;
      local_2c8 = 0;
      local_248 = CONCAT17(8,(undefined7)local_248);
      local_258 = (int *)&DAT_6e61637367756c70;
      local_250 = local_250 & 0xffffffffffffff00;
      local_2d0 = local_340;
      uVar10 = std::chrono::system_clock::now();
      FUN_1006a284c(&local_270,2,&local_258,uVar10);
      if (local_248 < 0) {
        operator_delete(local_258);
      }
      iVar9 = FUN_10069f1d8(&local_270);
      uVar15 = auVar16._8_8_ & 0xfffffffb;
      if (iVar9 != 0) {
        uVar10 = FUN_10069c398(&local_270,"VST3: plugin already scanned. ");
        pcVar3 = "Rescan";
        if (uVar15 == 0) {
          pcVar3 = "Retry";
        }
        FUN_10069c398(uVar10,pcVar3);
      }
      thunk_FUN_10069bf04(&local_270);
      (**(code **)(*param_1 + 0x20))(&local_270,param_1,uVar11,local_2b8,uVar15 != 0);
      piVar7 = local_268;
      piVar5 = local_270;
      for (piVar1 = local_270; local_270 = piVar5, piVar1 != piVar7; piVar1 = piVar1 + 0x22) {
        local_258 = *(int **)(piVar1 + 0x1a);
        if (local_258 != (int *)0x0) {
          *local_258 = *local_258 + 1;
        }
        FUN_1005d4ef4(&local_250,piVar1);
        FUN_1005e6af4(&local_2d0,&local_258,&local_258);
        FUN_1005cede0(&local_250);
        if ((local_258 != (int *)0x0) &&
           (iVar9 = *local_258, *local_258 = iVar9 + -1, iVar9 + -1 == 0)) {
          FUN_100454b40();
        }
        piVar5 = local_270;
      }
      if (piVar5 != (int *)0x0) {
        while (local_268 != piVar5) {
          local_268 = (int *)FUN_1005cede0(local_268 + -0x22);
        }
        local_268 = piVar5;
        operator_delete(local_270);
      }
    }
    local_340 = &local_2c8;
    FUN_10067c300(&local_258,local_2a0);
    local_270 = (int *)((ulong)local_270 & 0xffffffffffffff00);
    local_259 = '\0';
    FUN_1006c45e4(&local_258,&local_270);
    FUN_1001b0cb8(&local_2d8,&local_258);
    if (local_259 < '\0') {
      operator_delete(local_270);
    }
    if (local_248 < 0) {
      operator_delete(local_258);
    }
    FUN_1001b4e9c(&local_258);
    (**(code **)(*param_5 + 0x20))(param_5,&local_2d8,&local_258);
    if ((local_258 != (int *)0x0) && (iVar9 = *local_258, *local_258 = iVar9 + -1, iVar9 + -1 == 0))
    {
      FUN_100454b40();
    }
    (**(code **)(*param_4 + 0x10))(&local_258,param_4,local_2a0);
    pvVar8 = local_88;
    pvVar6 = local_90;
    if (local_78 == '\x01') {
      for (; pvVar6 != pvVar8; pvVar6 = (void *)((long)pvVar6 + 0xd0)) {
        uVar15 = (ulong)*(char *)((long)pvVar6 + 0x37);
        if ((long)uVar15 < 0) {
          pvVar12 = *(void **)((long)pvVar6 + 0x20);
          uVar15 = *(ulong *)((long)pvVar6 + 0x28);
        }
        else {
          pvVar12 = (void *)((long)pvVar6 + 0x20);
        }
        sVar2 = uVar15;
        if (0x11 < uVar15) {
          sVar2 = 0x12;
        }
        iVar9 = _memcmp(pvVar12,"Audio Module Class",sVar2);
        if (uVar15 == 0x12 && iVar9 == 0) {
          FUN_10043ce2c(&local_2e0,(long)pvVar6 + 0x38);
          iVar9 = FUN_100145768((long)pvVar6 + 0x98);
          uVar14 = 1;
          if (iVar9 == 0) {
            uVar14 = 2;
          }
          FUN_1005ada44(local_2f8,pvVar6,uVar14,(long)pvVar6 + 0x38);
          FUN_10068a0f8(&local_270,local_2f8);
          auVar16 = FUN_100688208(&local_270);
          local_320 = auVar16;
          FUN_10043cb54(&local_300,local_320);
          if (local_259 < '\0') {
            operator_delete(local_270);
          }
          puVar13 = (undefined8 *)FUN_1005e6d94(&local_2d0,&local_300);
          if (local_340 == puVar13) {
            bVar4 = false;
LAB_1005e96d8:
            (**(code **)(*param_5 + 0x20))(param_5,&local_2d8,&local_2e0);
            local_259 = '\b';
            local_270 = (int *)&DAT_6e61637367756c70;
            local_268 = (int *)((ulong)local_268 & 0xffffffffffffff00);
            uVar10 = std::chrono::system_clock::now();
            FUN_1006a284c(&local_308,2,&local_270,uVar10);
            if (local_259 < '\0') {
              operator_delete(local_270);
            }
            iVar9 = FUN_10069f1d8(&local_308);
            if (iVar9 == 0) {
LAB_1005e98f4:
              thunk_FUN_10069bf04(&local_308);
              if (bVar4) goto LAB_1005e9900;
LAB_1005e993c:
              uVar15 = (**(code **)(*param_1 + 0x28))(param_1,uVar11,&local_2e0);
            }
            else {
              uVar10 = FUN_10069c398(&local_308,"VST3: found");
              pcVar3 = " [retry]";
              if (!bVar4) {
                pcVar3 = "";
              }
              uVar10 = FUN_10069c398(uVar10,pcVar3);
              uVar10 = FUN_10069c398(uVar10,": ");
              uVar10 = FUN_10043d2b0(uVar10,&local_2e0);
              uVar10 = FUN_10069c398(uVar10,"\n");
              uVar10 = FUN_10069c398(uVar10,"   vendor: ");
              uVar10 = FUN_10069d278(uVar10,(long)pvVar6 + 0x50);
              uVar10 = FUN_10069c398(uVar10,"\n");
              uVar10 = FUN_10069c398(uVar10,"   url: ");
              FUN_100141db8(&local_270,&local_258);
              uVar10 = FUN_10069d278(uVar10,&local_270);
              uVar10 = FUN_10069c398(uVar10,"\n");
              uVar10 = FUN_10069c398(uVar10,"   email: ");
              FUN_100141e78(local_320,&local_258);
              uVar10 = FUN_10069d278(uVar10,local_320);
              uVar10 = FUN_10069c398(uVar10,"\n");
              uVar10 = FUN_10069c398(uVar10,"   device-class-id: ");
              FUN_100689c1c(local_338,local_2f8,1);
              uVar10 = FUN_10069d278(uVar10,local_338);
              uVar10 = FUN_10069c398(uVar10,"\n");
              uVar10 = FUN_10069c398(uVar10,"   cardinality: ");
              uVar10 = FUN_10069e0d0(uVar10,*(undefined4 *)((long)pvVar6 + 0x18));
              uVar10 = FUN_10069c398(uVar10,"\n");
              uVar10 = FUN_10069c398(uVar10,"   version: ");
              uVar10 = FUN_10069d278(uVar10,(long)pvVar6 + 0x68);
              uVar10 = FUN_10069c398(uVar10,"\n");
              uVar10 = FUN_10069c398(uVar10,"   sdkVersion: ");
              uVar10 = FUN_10069d278(uVar10,(long)pvVar6 + 0x80);
              uVar10 = FUN_10069c398(uVar10,"\n");
              uVar10 = FUN_10069c398(uVar10,"   subCategories: ");
              uVar10 = FUN_10069d278(uVar10,(long)pvVar6 + 0xb0);
              uVar10 = FUN_10069c398(uVar10,"\n");
              uVar10 = FUN_10069c398(uVar10,"   path: ");
              uVar10 = FUN_10013300c(uVar10,local_2a0);
              uVar10 = FUN_10069c398(uVar10,"\n");
              uVar10 = FUN_10069c398(uVar10,"   fp: ");
              FUN_10069d278(uVar10,local_2b8);
              if (local_321 < '\0') {
                operator_delete(local_338[0]);
              }
              if (local_309 < '\0') {
                operator_delete((void *)local_320._0_8_);
              }
              if (-1 < local_259) goto LAB_1005e98f4;
              operator_delete(local_270);
              thunk_FUN_10069bf04(&local_308);
              if (!bVar4) goto LAB_1005e993c;
LAB_1005e9900:
              uVar15 = (ulong)*(uint *)(puVar13 + 5);
            }
            FUN_10043ce2c(&local_270,(long)pvVar6 + 0x50);
            FUN_10043ce2c(local_320,(long)pvVar6 + 0x68);
            FUN_10043ce2c(local_338,(long)pvVar6 + 0x80);
            FUN_10043ce2c(&local_308,(long)pvVar6 + 0xb0);
            (**(code **)(*param_1 + 0x30))
                      (param_1,uVar15,&local_300,&local_2e0,&local_270,local_320,local_338,1,
                       &local_308);
            if ((local_308 != (int *)0x0) &&
               (iVar9 = *local_308, *local_308 = iVar9 + -1, iVar9 + -1 == 0)) {
              FUN_100454b40();
            }
            if ((local_338[0] != (int *)0x0) &&
               (iVar9 = *local_338[0], *local_338[0] = iVar9 + -1, iVar9 + -1 == 0)) {
              FUN_100454b40();
            }
            if (((int *)local_320._0_8_ != (int *)0x0) &&
               (iVar9 = *(int *)local_320._0_8_, *(int *)local_320._0_8_ = iVar9 + -1,
               iVar9 + -1 == 0)) {
              FUN_100454b40();
            }
            if ((local_270 != (int *)0x0) &&
               (iVar9 = *local_270, *local_270 = iVar9 + -1, iVar9 + -1 == 0)) {
              FUN_100454b40();
            }
            (**(code **)(*param_1 + 0x70))(param_1,uVar15,1);
          }
          else {
            if (*(int *)(puVar13 + 0x13) == 0) {
              bVar4 = true;
              goto LAB_1005e96d8;
            }
            bVar4 = true;
            if (*(int *)(puVar13 + 0x13) == 4) goto LAB_1005e96d8;
          }
          if ((local_300 != (int *)0x0) &&
             (iVar9 = *local_300, *local_300 = iVar9 + -1, iVar9 + -1 == 0)) {
            FUN_100454b40();
          }
          if (local_2e1 < '\0') {
            operator_delete(local_2f8[0]);
          }
          if ((local_2e0 != (int *)0x0) &&
             (iVar9 = *local_2e0, *local_2e0 = iVar9 + -1, iVar9 + -1 == 0)) {
            FUN_100454b40();
          }
        }
      }
      (**(code **)(*param_1 + 0x38))(param_1,uVar11);
      (**(code **)(*param_5 + 0x18))(param_5);
    }
    else {
      local_259 = '\b';
      local_270 = (int *)&DAT_6e61637367756c70;
      local_268 = (int *)((ulong)local_268 & 0xffffffffffffff00);
      uVar10 = std::chrono::system_clock::now();
      FUN_1006a284c(local_2f8,2,&local_270,uVar10);
      if (local_259 < '\0') {
        operator_delete(local_270);
      }
      iVar9 = FUN_10069f1d8(local_2f8);
      if (iVar9 != 0) {
        FUN_10069c398(local_2f8,"VST3: not a plugin");
      }
      thunk_FUN_10069bf04(local_2f8);
      (**(code **)(*param_1 + 0x40))(param_1,uVar11,3);
    }
    pvVar6 = local_90;
    if ((local_78 == '\x01') && (local_90 != (void *)0x0)) {
      while (local_88 != pvVar6) {
        local_88 = (void *)FUN_100145124((long)local_88 + -0xd0);
      }
      local_88 = pvVar6;
      operator_delete(local_90);
    }
    if ((local_2d8 != (int *)0x0) && (iVar9 = *local_2d8, *local_2d8 = iVar9 + -1, iVar9 + -1 == 0))
    {
      FUN_100454b40();
    }
    FUN_1005e6a84(&local_2d0,local_2c8);
    if (local_2a1 < '\0') {
      operator_delete(local_2b8[0]);
    }
  }
  if (local_289 < '\0') {
    operator_delete(local_2a0[0]);
  }
  FUN_100184174(auStack_278);
  if (*(long *)PTR____stack_chk_guard_100b1c378 != local_70) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}

