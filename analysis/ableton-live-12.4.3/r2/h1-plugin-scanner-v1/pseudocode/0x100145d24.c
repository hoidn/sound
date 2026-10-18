
void FUN_100145d24(undefined8 *param_1,undefined8 *param_2,undefined8 param_3,undefined4 param_4,
                  undefined1 (*param_5) [16])

{
  ulong uVar1;
  char cVar2;
  undefined8 *puVar3;
  int iVar4;
  undefined4 uVar5;
  int iVar6;
  undefined8 *puVar7;
  long lVar8;
  undefined8 uVar9;
  long lVar10;
  long *plVar11;
  long *plVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  undefined1 auVar15 [16];
  void *local_c0;
  long lStack_b8;
  undefined8 local_b0;
  void *local_a8 [2];
  char local_91;
  void *local_90;
  long lStack_88;
  long local_80;
  void *local_78;
  long lStack_70;
  undefined7 local_68;
  char cStack_61;
  
  puVar7 = operator_new(0x60);
  plVar12 = puVar7 + 1;
  puVar7[2] = 0;
  *plVar12 = 0;
  puVar7[4] = 0;
  puVar7[3] = 0;
  puVar7[6] = 0;
  puVar7[5] = 0;
  puVar7[8] = 0;
  puVar7[7] = 0;
  *(undefined1 *)(puVar7 + 9) = 0;
  *puVar7 = &PTR_FUN_100b44818;
  plVar11 = puVar7 + 10;
  *plVar11 = 0;
  *(undefined4 *)(puVar7 + 0xb) = 0xffffffff;
  uVar14 = *(undefined8 *)PTR__kCFAllocatorDefault_100b1c030;
  uVar1 = param_2[1];
  puVar3 = (undefined8 *)*param_2;
  if (-1 < (char)*(byte *)((long)param_2 + 0x17)) {
    uVar1 = (ulong)*(byte *)((long)param_2 + 0x17);
    puVar3 = param_2;
  }
  lVar8 = _CFURLCreateFromFileSystemRepresentation(uVar14,puVar3,uVar1,1);
  if (lVar8 == 0) {
    uVar14 = std::generic_category();
    auVar15._8_8_ = uVar14;
    auVar15._0_8_ = 2;
  }
  else {
    _CFAutorelease(lVar8);
    uVar9 = FUN_10075325c(lVar8);
    iVar4 = (int)uVar9;
    if (iVar4 != -0x105f6 && iVar4 != 0) {
      uVar13 = std::chrono::system_clock::now();
      FUN_1006a290c(&local_90,4,uVar13);
      iVar6 = FUN_10069f1d8(&local_90);
      if (iVar6 != 0) {
        uVar13 = FUN_10069c398(&local_90,"VST2: Code signature verification failed for ");
        uVar13 = FUN_10013300c(uVar13,param_2);
        uVar13 = FUN_10069c398(uVar13," with error ");
        uVar13 = FUN_10069e0d0(uVar13,uVar9);
        uVar13 = FUN_10069c398(uVar13," (");
        lVar10 = _SecCopyErrorMessageString(uVar9,0);
        if (lVar10 != 0) {
          _CFAutorelease(lVar10);
        }
        FUN_1007535f4(&local_78,lVar10);
        uVar9 = FUN_10069d278(uVar13,&local_78);
        FUN_10069c398(uVar9,")");
        if (cStack_61 < '\0') {
          operator_delete(local_78);
        }
      }
      thunk_FUN_10069bf04(&local_90);
      auVar15 = FUN_10014088c(4);
      *param_5 = auVar15;
      if (iVar4 != -0x105f6) goto LAB_100146120;
    }
    lVar8 = _CFBundleCreate(uVar14,lVar8);
    if (lVar8 != 0) {
      _CFRetain(lVar8);
    }
    lVar10 = *plVar11;
    *plVar11 = lVar8;
    if (lVar10 != 0) {
      _CFRelease();
      lVar8 = *plVar11;
    }
    if (lVar8 != 0) {
      uVar9 = _CurResFile();
      uVar5 = _CFBundleOpenBundleResourceMap(*plVar11);
      *(undefined4 *)(puVar7 + 0xb) = uVar5;
      uVar13 = puVar7[10];
      lVar8 = _CFStringCreateWithCString(uVar14,"main_macho",0x600);
      if (lVar8 != 0) {
        _CFAutorelease(lVar8);
      }
      lVar8 = _CFBundleGetFunctionPointerForName(uVar13,lVar8);
      if (lVar8 == 0) {
        auVar15 = FUN_10014088c(1);
        *param_5 = auVar15;
        *plVar12 = 0;
        if (auVar15._0_4_ != 0) {
          lVar10 = *plVar11;
          lVar8 = _CFStringCreateWithCString(uVar14,"VSTPluginMain",0x600);
          if (lVar8 != 0) {
            _CFAutorelease(lVar8);
          }
          lVar8 = _CFBundleGetFunctionPointerForName(lVar10,lVar8);
          if (lVar8 != 0) goto LAB_100145e80;
          auVar15 = FUN_10014088c(1);
          *param_5 = auVar15;
          *plVar12 = 0;
          if (auVar15._0_4_ != 0) {
            auVar15 = FUN_10014088c(2);
            *param_5 = auVar15;
            _UseResFile(uVar9);
            goto LAB_100146120;
          }
        }
      }
      else {
LAB_100145e80:
        *(undefined4 *)*param_5 = 0;
        uVar14 = std::system_category();
        *(undefined8 *)(*param_5 + 8) = uVar14;
        *plVar12 = lVar8;
      }
      _UseResFile(uVar9);
      lVar8 = _CFBundleGetInfoDictionary(*plVar11);
      if (lVar8 == 0) {
LAB_10014605c:
        FUN_10067c300(local_a8,param_2);
        FUN_1006c548c(&local_78,local_a8);
        if (cStack_61 < '\0') {
          FUN_100135b64(&local_90,local_78,lStack_70);
          if (cStack_61 < '\0') {
            operator_delete(local_78);
          }
        }
        else {
          lStack_88 = lStack_70;
          local_90 = local_78;
          local_80 = CONCAT17(cStack_61,local_68);
        }
        if (local_80 < 0) {
          FUN_100135b64(&local_c0,local_90,lStack_88);
          if (local_80 < 0) {
            operator_delete(local_90);
          }
        }
        else {
          lStack_b8 = lStack_88;
          local_c0 = local_90;
          local_b0 = local_80;
        }
        if (-1 < local_91) goto LAB_1001460ec;
        operator_delete(local_a8[0]);
        cVar2 = *(char *)((long)puVar7 + 0x2f);
      }
      else {
        lVar8 = _CFDictionaryGetValue(lVar8,&cf_CFBundleName);
        if (lVar8 != 0) {
          _CFAutorelease();
        }
        FUN_1007535f4(&local_c0,lVar8);
        if (local_b0 < 0) {
          if (lStack_b8 == 0) {
            operator_delete(local_c0);
            goto LAB_10014605c;
          }
        }
        else if (local_b0._7_1_ == '\0') goto LAB_10014605c;
LAB_1001460ec:
        cVar2 = *(char *)((long)puVar7 + 0x2f);
      }
      if (cVar2 < '\0') {
        operator_delete((void *)puVar7[3]);
      }
      puVar7[4] = lStack_b8;
      puVar7[3] = local_c0;
      puVar7[5] = local_b0;
      FUN_100140e2c(puVar7,param_3,param_4,param_5);
      goto LAB_100146120;
    }
    auVar15 = FUN_10014088c(5);
  }
  *param_5 = auVar15;
LAB_100146120:
  *param_1 = puVar7;
  return;
}

