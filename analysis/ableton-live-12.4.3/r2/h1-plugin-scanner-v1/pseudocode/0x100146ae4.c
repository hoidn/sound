
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

bool FUN_100146ae4(long param_1,ulong *param_2,undefined8 *param_3)

{
  undefined1 uVar1;
  ulong *puVar2;
  void **ppvVar3;
  undefined8 uVar4;
  bool bVar5;
  int iVar6;
  undefined8 uVar7;
  long lVar8;
  long lVar9;
  code *pcVar10;
  code *pcVar11;
  ulong uVar12;
  undefined8 *puVar13;
  char *pcVar14;
  undefined8 uVar15;
  void *local_90;
  ulong uStack_88;
  ulong local_80;
  long local_78;
  long *local_70;
  undefined8 uStack_68;
  long local_60;
  undefined7 local_58;
  undefined1 uStack_51;
  undefined7 uStack_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_100b1c378;
  uVar15 = *(undefined8 *)PTR__kCFAllocatorDefault_100b1c030;
  uVar12 = param_2[1];
  puVar2 = (ulong *)*param_2;
  if (-1 < (char)*(byte *)((long)param_2 + 0x17)) {
    uVar12 = (ulong)*(byte *)((long)param_2 + 0x17);
    puVar2 = param_2;
  }
  uVar7 = FUN_10067ca4c(param_2);
  lVar8 = _CFURLCreateFromFileSystemRepresentation(uVar15,puVar2,uVar12,uVar7);
  if (lVar8 == 0) goto LAB_100146eac;
  _CFAutorelease();
  uVar7 = FUN_10075325c(lVar8);
  if ((int)uVar7 != -0x105f6 && (int)uVar7 != 0) {
    lVar8 = _SecCopyErrorMessageString(uVar7,0);
    if (lVar8 != 0) {
      _CFAutorelease();
    }
    FUN_1007535f4(&local_70,lVar8);
LAB_100146cec:
    if (*(char *)((long)param_3 + 0x17) < '\0') {
      operator_delete((void *)*param_3);
    }
    param_3[1] = uStack_68;
    *param_3 = local_70;
    param_3[2] = local_60;
    if (*(long *)PTR____stack_chk_guard_100b1c378 == local_48) {
      return false;
    }
    goto LAB_100146ec8;
  }
  lVar8 = _CFBundleCreate(uVar15,lVar8);
  if (lVar8 != 0) {
    _CFAutorelease(lVar8);
    _CFRetain(lVar8);
  }
  lVar9 = *(long *)(param_1 + 0x48);
  *(long *)(param_1 + 0x48) = lVar8;
  if (lVar9 != 0) {
    _CFRelease();
    lVar8 = *(long *)(param_1 + 0x48);
  }
  local_78 = 0;
  if (lVar8 == 0) {
LAB_100146d64:
    local_70 = operator_new(0x28);
    local_60 = _UNK_1009a8e28;
    uStack_68 = _DAT_1009a8e20;
    *(undefined2 *)(local_70 + 4) = 0x20;
    uVar4 = s_could_not_create_Bundle_for_path_100a10cc9._24_8_;
    uVar7 = s_could_not_create_Bundle_for_path_100a10cc9._16_8_;
    uVar15 = s_could_not_create_Bundle_for_path_100a10cc9._0_8_;
    local_70[1] = s_could_not_create_Bundle_for_path_100a10cc9._8_8_;
    *local_70 = uVar15;
    local_70[3] = uVar4;
    local_70[2] = uVar7;
    if (*(char *)((long)param_2 + 0x17) < '\0') {
      FUN_100135b64(&local_90,*param_2,param_2[1]);
    }
    else {
      uStack_88 = param_2[1];
      local_90 = (void *)*param_2;
      local_80 = param_2[2];
    }
    ppvVar3 = local_90;
    if (-1 < (long)local_80) {
      ppvVar3 = &local_90;
    }
    puVar13 = (undefined8 *)std::string::append((char *)&local_70,(ulong)ppvVar3);
    uVar15 = *puVar13;
    local_58 = (undefined7)puVar13[1];
    uStack_51 = (undefined1)*(undefined8 *)((long)puVar13 + 0xf);
    uStack_50 = (undefined7)((ulong)*(undefined8 *)((long)puVar13 + 0xf) >> 8);
    uVar1 = *(undefined1 *)((long)puVar13 + 0x17);
    puVar13[1] = 0;
    puVar13[2] = 0;
    *puVar13 = 0;
    if (*(char *)((long)param_3 + 0x17) < '\0') {
      operator_delete((void *)*param_3);
    }
    *param_3 = uVar15;
    param_3[1] = CONCAT17(uStack_51,local_58);
    *(ulong *)((long)param_3 + 0xf) = CONCAT71(uStack_50,uStack_51);
    *(undefined1 *)((long)param_3 + 0x17) = uVar1;
    if ((long)local_80 < 0) {
      operator_delete(local_90);
    }
    if (local_60 < 0) {
      operator_delete(local_70);
    }
  }
  else {
    iVar6 = _CFBundleLoadExecutableAndReturnError(lVar8,&local_78);
    if (iVar6 == 0) {
      if ((local_78 == 0) || (_CFAutorelease(), local_78 == 0)) goto LAB_100146d64;
      lVar8 = _CFErrorCopyDescription();
      if (lVar8 != 0) {
        _CFAutorelease(lVar8);
        FUN_1007535f4(&local_70,lVar8);
        goto LAB_100146cec;
      }
    }
    else {
      uVar7 = *(undefined8 *)(param_1 + 0x48);
      lVar8 = _CFStringCreateWithCString(uVar15,"bundleEntry",0x600);
      if (lVar8 != 0) {
        _CFAutorelease(lVar8);
      }
      pcVar10 = (code *)_CFBundleGetFunctionPointerForName(uVar7,lVar8);
      if (pcVar10 == (code *)0x0) {
        FUN_10014088c(1);
        FUN_100141a6c(param_3,"bundle does not export the required \'bundleEntry\' function",0x3a);
      }
      else {
        uVar7 = *(undefined8 *)(param_1 + 0x48);
        lVar8 = _CFStringCreateWithCString(uVar15,"bundleExit",0x600);
        if (lVar8 != 0) {
          _CFAutorelease(lVar8);
        }
        lVar8 = _CFBundleGetFunctionPointerForName(uVar7,lVar8);
        if (lVar8 == 0) {
          FUN_10014088c(1);
          FUN_100141a6c(param_3,"bundle does not export the required \'bundleExit\' function",0x39);
        }
        else {
          uVar7 = *(undefined8 *)(param_1 + 0x48);
          lVar8 = _CFStringCreateWithCString(uVar15,"GetPluginFactory",0x600);
          if (lVar8 != 0) {
            _CFAutorelease(lVar8);
          }
          pcVar11 = (code *)_CFBundleGetFunctionPointerForName(uVar7,lVar8);
          if (pcVar11 != (code *)0x0) {
            uVar12 = (*pcVar10)(*(undefined8 *)(param_1 + 0x48));
            if ((uVar12 & 1) == 0) {
              pcVar14 = operator_new(0x20);
              uVar15 = s_calling__bundleEntry__failed_100a10dbd._0_8_;
              *(ulong *)(pcVar14 + 8) =
                   CONCAT44(s_calling__bundleEntry__failed_100a10dbd._12_4_,
                            s_calling__bundleEntry__failed_100a10dbd._8_4_);
              *(undefined8 *)pcVar14 = uVar15;
              uVar15 = CONCAT44(s_calling__bundleEntry__failed_100a10dbd._16_4_,
                                s_calling__bundleEntry__failed_100a10dbd._12_4_);
              *(undefined8 *)(pcVar14 + 0x14) = s_calling__bundleEntry__failed_100a10dbd._20_8_;
              *(undefined8 *)(pcVar14 + 0xc) = uVar15;
              pcVar14[0x1c] = '\0';
              if (*(char *)((long)param_3 + 0x17) < '\0') {
                operator_delete((void *)*param_3);
              }
              *param_3 = pcVar14;
              uVar15 = _DAT_1009a8ec0;
              param_3[2] = _UNK_1009a8ec8;
              param_3[1] = uVar15;
              if (*(long *)PTR____stack_chk_guard_100b1c378 == local_48) {
                return false;
              }
            }
            else {
              local_70 = (long *)(*pcVar11)();
              bVar5 = local_70 != (long *)0x0;
              if (local_70 == (long *)0x0) {
                pcVar14 = operator_new(0x28);
                pcVar14[0x20] = 'd';
                uVar4 = s_calling__GetPluginFactory__faile_100a10dda._24_8_;
                uVar7 = s_calling__GetPluginFactory__faile_100a10dda._16_8_;
                uVar15 = s_calling__GetPluginFactory__faile_100a10dda._0_8_;
                pcVar14[0x21] = '\0';
                *(undefined8 *)(pcVar14 + 8) = s_calling__GetPluginFactory__faile_100a10dda._8_8_;
                *(undefined8 *)pcVar14 = uVar15;
                *(undefined8 *)(pcVar14 + 0x18) = uVar4;
                *(undefined8 *)(pcVar14 + 0x10) = uVar7;
                if (*(char *)((long)param_3 + 0x17) < '\0') {
                  operator_delete((void *)*param_3);
                }
                *param_3 = pcVar14;
                uVar15 = _DAT_1009a8e20;
                param_3[2] = _UNK_1009a8e28;
                param_3[1] = uVar15;
              }
              else {
                FUN_1001440a0(&local_90,&local_70);
                if (*(long **)(param_1 + 0x10) != (long *)0x0) {
                  (**(code **)(**(long **)(param_1 + 0x10) + 0x10))();
                }
                *(void **)(param_1 + 0x10) = local_90;
              }
              if (local_70 != (long *)0x0) {
                (**(code **)(*local_70 + 0x10))();
              }
              if (*(long *)PTR____stack_chk_guard_100b1c378 == local_48) {
                return bVar5;
              }
            }
            goto LAB_100146ec8;
          }
          FUN_10014088c(1);
          FUN_100141a6c(param_3,"bundle does not export the required \'GetPluginFactory\' function",
                        0x3f);
        }
      }
    }
  }
LAB_100146eac:
  if (*(long *)PTR____stack_chk_guard_100b1c378 == local_48) {
    return false;
  }
LAB_100146ec8:
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

