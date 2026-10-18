
/* WARNING: Removing unreachable block (ram,0x0001005ac3b0) */
/* WARNING: Removing unreachable block (ram,0x0001005ac240) */
/* WARNING: Removing unreachable block (ram,0x0001005ac254) */
/* WARNING: Removing unreachable block (ram,0x0001005ac260) */
/* WARNING: Removing unreachable block (ram,0x0001005ac244) */
/* WARNING: Removing unreachable block (ram,0x0001005ac3c0) */
/* WARNING: Removing unreachable block (ram,0x0001005ac388) */

void FUN_1005aba10(long *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                  long *param_5,long *param_6)

{
  char *pcVar1;
  bool bVar2;
  long *plVar3;
  int iVar4;
  undefined8 uVar5;
  ulong uVar6;
  undefined8 *puVar7;
  undefined4 *puVar8;
  ulong uVar9;
  undefined4 *puVar10;
  undefined4 uVar11;
  undefined1 auVar12 [16];
  int *local_1c0;
  int *local_1b8;
  undefined1 local_1b0 [16];
  int *local_1a0;
  void *local_198 [2];
  char local_181;
  int *local_180;
  long *local_178;
  int *local_170;
  int *local_168;
  undefined1 local_160 [15];
  char local_151;
  undefined8 *local_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined1 local_c0 [24];
  undefined1 local_a8 [24];
  int local_90 [2];
  undefined8 local_88;
  undefined1 local_80;
  undefined7 uStack_7f;
  undefined4 *local_78;
  undefined1 local_69;
  
  local_90[0] = 0;
  local_88 = std::system_category();
  FUN_100674264(local_a8,param_3,local_90);
  if (local_90[0] == 0) {
    local_151 = '\b';
    local_168 = (int *)&DAT_6e61637367756c70;
    local_160[0] = 0;
    uVar5 = std::chrono::system_clock::now();
    FUN_1006a284c(&local_80,2,&local_168,uVar5);
    if (local_151 < '\0') {
      operator_delete(local_168);
    }
    iVar4 = FUN_10069f1d8(&local_80);
    if (iVar4 != 0) {
      uVar5 = FUN_10069c398(&local_80,"VST2: check plugin at path: ");
      uVar5 = FUN_10013300c(uVar5,local_a8);
      uVar5 = FUN_10069c398(uVar5," [");
      uVar5 = FUN_10013300c(uVar5,param_4);
      FUN_10069c398(uVar5,"]");
    }
    thunk_FUN_10069bf04(&local_80);
    (**(code **)(*param_5 + 0x18))(local_c0,param_5,local_a8,local_90);
    if (local_90[0] != 0) {
      local_151 = '\b';
      local_168 = (int *)&DAT_6e61637367756c70;
      local_160[0] = 0;
      uVar5 = std::chrono::system_clock::now();
      FUN_1006a284c(&local_80,3,&local_168,uVar5);
      if (local_151 < '\0') {
        operator_delete(local_168);
      }
      iVar4 = FUN_10069f1d8(&local_80);
      if (iVar4 != 0) {
        uVar5 = FUN_10069c398(&local_80,"VST2: couldn\'t determine plugin\'s fingerprint: ");
        FUN_1005ac678(uVar5,local_90);
      }
      thunk_FUN_10069bf04(&local_80);
    }
    auVar12 = (**(code **)(*param_1 + 0x18))(param_1,local_a8,2,2,param_2,local_c0,param_4);
    uVar6 = auVar12._0_8_;
    local_d0 = 0;
    uStack_c8 = 0;
    local_d8 = &local_d0;
    if ((uVar6 >> 0x20 & 1) != 0) {
      local_151 = '\b';
      local_168 = (int *)&DAT_6e61637367756c70;
      local_160[0] = 0;
      uVar5 = std::chrono::system_clock::now();
      FUN_1006a284c(&local_80,2,&local_168,uVar5);
      if (local_151 < '\0') {
        operator_delete(local_168);
      }
      iVar4 = FUN_10069f1d8(&local_80);
      uVar9 = auVar12._8_8_ & 0xfffffffb;
      if (iVar4 != 0) {
        uVar5 = FUN_10069c398(&local_80,"VST2: plugin already scanned. ");
        pcVar1 = "Rescan";
        if (uVar9 == 0) {
          pcVar1 = "Retry";
        }
        FUN_10069c398(uVar5,pcVar1);
      }
      thunk_FUN_10069bf04(&local_80);
      (**(code **)(*param_1 + 0x20))(&local_80,param_1,uVar6,local_c0,uVar9 != 0);
      puVar8 = local_78;
      puVar10 = (undefined4 *)CONCAT71(uStack_7f,local_80);
      if (puVar10 != local_78) {
        do {
          local_168 = *(int **)(puVar10 + 0x1a);
          if (local_168 != (int *)0x0) {
            *local_168 = *local_168 + 1;
          }
          FUN_1005d4ef4(local_160,puVar10);
          FUN_1005e6af4(&local_d8,&local_168,&local_168);
          FUN_1005cede0(local_160);
          if ((local_168 != (int *)0x0) &&
             (iVar4 = *local_168, *local_168 = iVar4 + -1, iVar4 + -1 == 0)) {
            FUN_100454b40();
          }
          puVar10 = puVar10 + 0x22;
        } while (puVar10 != puVar8);
        puVar10 = (undefined4 *)CONCAT71(uStack_7f,local_80);
      }
      if (puVar10 != (undefined4 *)0x0) {
        puVar8 = puVar10;
        if (local_78 != puVar10) {
          do {
            local_78 = (undefined4 *)FUN_1005cede0(local_78 + -0x22);
          } while (local_78 != puVar10);
          puVar8 = (undefined4 *)CONCAT71(uStack_7f,local_80);
        }
        local_78 = puVar10;
        operator_delete(puVar8);
      }
    }
    FUN_10067c300(&local_168,local_a8);
    local_80 = 0;
    local_69 = 0;
    FUN_1006c45e4(&local_168,&local_80);
    FUN_1001b0cb8(&local_170,&local_168);
    if (local_151 < '\0') {
      operator_delete(local_168);
    }
    FUN_1001b4e9c(&local_168);
    (**(code **)(*param_6 + 0x20))(param_6,&local_170,&local_168);
    if ((local_168 != (int *)0x0) && (iVar4 = *local_168, *local_168 = iVar4 + -1, iVar4 + -1 == 0))
    {
      FUN_100454b40();
    }
    (**(code **)(*param_5 + 0x10))(&local_178,param_5,local_a8);
    if (local_178 == (long *)0x0) {
      local_151 = '\b';
      local_168 = (int *)&DAT_6e61637367756c70;
      local_160[0] = 0;
      uVar5 = std::chrono::system_clock::now();
      FUN_1006a284c(&local_80,2,&local_168,uVar5);
      if (local_151 < '\0') {
        operator_delete(local_168);
      }
      iVar4 = FUN_10069f1d8(&local_80);
      if (iVar4 != 0) {
        FUN_10069c398(&local_80,"VST2: not a plugin");
      }
      thunk_FUN_10069bf04(&local_80);
      (**(code **)(*param_1 + 0x40))(param_1,uVar6,3);
    }
    else {
      (**(code **)(*local_178 + 0x20))(&local_80);
      puVar8 = local_78;
      puVar10 = (undefined4 *)CONCAT71(uStack_7f,local_80);
      if (puVar10 != local_78) {
        do {
          FUN_10043ce2c(&local_180,puVar10 + 2);
          uVar11 = 1;
          if (*(char *)(puVar10 + 0xe) == '\0') {
            uVar11 = 2;
          }
          FUN_1005aab3c(local_198,*puVar10,uVar11,puVar10 + 2);
          FUN_10068a0f8(&local_168,local_198);
          auVar12 = FUN_100688208(&local_168);
          local_1b0 = auVar12;
          FUN_10043cb54(&local_1a0,local_1b0);
          if (local_151 < '\0') {
            operator_delete(local_168);
          }
          puVar7 = (undefined8 *)FUN_1005e6d94(&local_d8,&local_1a0);
          if (&local_d0 == puVar7) {
            bVar2 = false;
LAB_1005abeb0:
            FUN_10043ce2c(local_1b0,puVar10 + 8);
            (**(code **)(*local_178 + 0x10))(&local_168);
            FUN_10043ce2c(&local_1b8,&local_168);
            (**(code **)(*param_6 + 0x20))(param_6,&local_1b8,&local_180);
            if ((local_1b8 != (int *)0x0) &&
               (iVar4 = *local_1b8, *local_1b8 = iVar4 + -1, iVar4 + -1 == 0)) {
              FUN_100454b40();
            }
            if (local_151 < '\0') {
              operator_delete(local_168);
            }
            local_151 = '\b';
            local_168 = (int *)&DAT_6e61637367756c70;
            local_160[0] = 0;
            uVar5 = std::chrono::system_clock::now();
            FUN_1006a284c(&local_1b8,2,&local_168,uVar5);
            if (local_151 < '\0') {
              operator_delete(local_168);
            }
            iVar4 = FUN_10069f1d8(&local_1b8);
            if (iVar4 == 0) {
LAB_1005ac07c:
              thunk_FUN_10069bf04(&local_1b8);
              if (bVar2) goto LAB_1005ac088;
LAB_1005ac0a4:
              uVar9 = (**(code **)(*param_1 + 0x28))(param_1,uVar6,&local_180);
            }
            else {
              uVar5 = FUN_10069c398(&local_1b8,"VST2: found");
              pcVar1 = " [retry]";
              if (!bVar2) {
                pcVar1 = "";
              }
              uVar5 = FUN_10069c398(uVar5,pcVar1);
              uVar5 = FUN_10069c398(uVar5,": ");
              uVar5 = FUN_10043d2b0(uVar5,&local_180);
              uVar5 = FUN_10069c398(uVar5,"\n");
              uVar5 = FUN_10069c398(uVar5,"   vendor: ");
              uVar5 = FUN_10043d2b0(uVar5,local_1b0);
              uVar5 = FUN_10069c398(uVar5,"\n");
              uVar5 = FUN_10069c398(uVar5,"   device-class-id: ");
              FUN_100689c1c(&local_168,local_198,1);
              uVar5 = FUN_10069d278(uVar5,&local_168);
              uVar5 = FUN_10069c398(uVar5,"\n");
              uVar5 = FUN_10069c398(uVar5,"   version: ");
              uVar5 = FUN_10069e0d0(uVar5,puVar10[0x10]);
              uVar5 = FUN_10069c398(uVar5,"\n");
              uVar5 = FUN_10069c398(uVar5,"   sdkVersion: ");
              uVar5 = FUN_10069e0d0(uVar5,puVar10[0x11]);
              uVar5 = FUN_10069c398(uVar5,"\n");
              uVar5 = FUN_10069c398(uVar5,"   path: ");
              uVar5 = FUN_10013300c(uVar5,local_a8);
              uVar5 = FUN_10069c398(uVar5,"\n");
              uVar5 = FUN_10069c398(uVar5,"   fp: ");
              FUN_10069d278(uVar5,local_c0);
              if (-1 < local_151) goto LAB_1005ac07c;
              operator_delete(local_168);
              thunk_FUN_10069bf04(&local_1b8);
              if (!bVar2) goto LAB_1005ac0a4;
LAB_1005ac088:
              uVar9 = (ulong)*(uint *)(puVar7 + 5);
            }
            uVar5 = (**(code **)(*local_178 + 0x18))();
            FUN_10043acd0(&local_168,puVar10[0x10]);
            FUN_10043acd0(&local_1b8,puVar10[0x11]);
            FUN_1001b4e9c(&local_1c0);
            (**(code **)(*param_1 + 0x30))
                      (param_1,uVar9,&local_1a0,&local_180,local_1b0,&local_168,&local_1b8,uVar5,
                       &local_1c0);
            if ((local_1c0 != (int *)0x0) &&
               (iVar4 = *local_1c0, *local_1c0 = iVar4 + -1, iVar4 + -1 == 0)) {
              FUN_100454b40();
            }
            if ((local_1b8 != (int *)0x0) &&
               (iVar4 = *local_1b8, *local_1b8 = iVar4 + -1, iVar4 + -1 == 0)) {
              FUN_100454b40();
            }
            if ((local_168 != (int *)0x0) &&
               (iVar4 = *local_168, *local_168 = iVar4 + -1, iVar4 + -1 == 0)) {
              FUN_100454b40();
            }
            (**(code **)(*param_1 + 0x70))(param_1,uVar9,1);
            if (((int *)local_1b0._0_8_ != (int *)0x0) &&
               (iVar4 = *(int *)local_1b0._0_8_, *(int *)local_1b0._0_8_ = iVar4 + -1,
               iVar4 + -1 == 0)) {
              FUN_100454b40();
            }
          }
          else {
            if (*(int *)(puVar7 + 0x13) == 0) {
              bVar2 = true;
              goto LAB_1005abeb0;
            }
            bVar2 = true;
            if (*(int *)(puVar7 + 0x13) == 4) goto LAB_1005abeb0;
          }
          if ((local_1a0 != (int *)0x0) &&
             (iVar4 = *local_1a0, *local_1a0 = iVar4 + -1, iVar4 + -1 == 0)) {
            FUN_100454b40();
          }
          if (local_181 < '\0') {
            operator_delete(local_198[0]);
          }
          if ((local_180 != (int *)0x0) &&
             (iVar4 = *local_180, *local_180 = iVar4 + -1, iVar4 + -1 == 0)) {
            FUN_100454b40();
          }
          puVar10 = puVar10 + 0x12;
        } while (puVar10 != puVar8);
        puVar10 = (undefined4 *)CONCAT71(uStack_7f,local_80);
      }
      if (puVar10 != (undefined4 *)0x0) {
        puVar8 = puVar10;
        if (local_78 != puVar10) {
          do {
            local_78 = local_78 + -0x12;
          } while (local_78 != puVar10);
          puVar8 = (undefined4 *)CONCAT71(uStack_7f,local_80);
        }
        local_78 = puVar10;
        operator_delete(puVar8);
      }
      (**(code **)(*param_1 + 0x38))(param_1,uVar6);
      (**(code **)(*param_6 + 0x18))(param_6);
    }
    plVar3 = local_178;
    local_178 = (long *)0x0;
    if (plVar3 != (long *)0x0) {
      (**(code **)(*plVar3 + 8))();
    }
    if ((local_170 != (int *)0x0) && (iVar4 = *local_170, *local_170 = iVar4 + -1, iVar4 + -1 == 0))
    {
      FUN_100454b40();
    }
    FUN_1005e6a84(&local_d8,local_d0);
  }
  return;
}

