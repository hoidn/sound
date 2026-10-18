// 0x1013e5b58 FUN_1013e5b58 state=exported-with-warnings role=libusb device enumeration, VID/PID/class match, claim interface 0
// source chunk chunk-00890.jsonl; code_sha256=de0ed784d16239f3a8d1c58fbfa14365067a2ed87b86227ce226cae79aefad29

/* WARNING: Removing unreachable block (ram,0x0001013e5f1c) */
/* WARNING: Removing unreachable block (ram,0x0001013e5f48) */
/* WARNING: Removing unreachable block (ram,0x0001013e629c) */
/* WARNING: Removing unreachable block (ram,0x0001013e5ba8) */
/* WARNING: Removing unreachable block (ram,0x0001013e5fb8) */
/* WARNING: Removing unreachable block (ram,0x0001013e5fd4) */
/* WARNING: Removing unreachable block (ram,0x0001013e5e8c) */
/* WARNING: Removing unreachable block (ram,0x0001013e6028) */
/* WARNING: Removing unreachable block (ram,0x0001013e637c) */
/* WARNING: Removing unreachable block (ram,0x0001013e62ac) */
/* WARNING: Removing unreachable block (ram,0x0001013e6280) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: stack */

void FUN_1013e5b58(long *param_1,undefined4 *param_2,int param_3)

{
  undefined8 *****pppppuVar1;
  undefined8 uVar2;
  long lVar3;
  undefined8 *****pppppuVar4;
  ulong uVar5;
  undefined8 *****pppppuVar6;
  ulong uVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  void *pvVar10;
  code *pcVar11;
  int iVar12;
  int iVar13;
  long lVar14;
  undefined8 uVar15;
  undefined8 uVar16;
  long *plVar17;
  ulong uVar18;
  undefined8 *puVar19;
  duration *pdVar20;
  ulong uVar21;
  long lVar22;
  size_t sVar23;
  long *plVar24;
  long *plVar25;
  long lVar26;
  undefined8 ****local_1a0 [2];
  char local_189;
  undefined8 ****local_188 [2];
  char local_171;
  undefined8 ****local_170 [2];
  char local_159;
  char *local_158;
  undefined8 local_150;
  long lStack_148;
  void *local_140;
  undefined8 uStack_138;
  long local_130;
  void *local_120;
  long lStack_118;
  long local_110;
  long *local_100;
  undefined8 uStack_f8;
  undefined8 local_f0;
  undefined1 local_e8 [23];
  undefined1 local_d1;
  undefined4 local_d0 [2];
  undefined8 ****local_c8;
  ulong uStack_c0;
  undefined8 local_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  ulong local_a0;
  ulong local_98;
  long *local_90;
  long *plStack_88;
  long *local_80;
  
  *param_1 = 0;
  local_d1 = 0;
  local_e8[0] = 0;
  FUN_1013f1400(local_d0,0,local_e8);
  if (((DAT_101e32298 & 1) == 0) && (iVar13 = ___cxa_guard_acquire(&DAT_101e32298), iVar13 != 0)) {
    FUN_1013e7b44();
    ___cxa_atexit(FUN_1013e7bf0,&DAT_101e32290,0x100000000);
    ___cxa_guard_release(&DAT_101e32298);
  }
  uVar7 = _UNK_101577398;
  pppppuVar6 = _DAT_101577390;
  uVar5 = _UNK_1015771d8;
  pppppuVar4 = _DAT_1015771d0;
  lVar3 = _UNK_101574818;
  uVar2 = _DAT_101574810;
  iVar13 = 0;
  do {
    lVar14 = _libusb_get_device_list(0,&local_100);
    if (lVar14 < 0) {
      local_b0 = operator_new(0x20);
      uVar15 = s_could_not_get_usb_device_list_1018feda0._0_8_;
      local_a0 = uVar5;
      uStack_a8 = pppppuVar4;
      *(ulong *)(local_b0 + 8) =
           CONCAT35(s_could_not_get_usb_device_list_1018feda0._13_3_,
                    s_could_not_get_usb_device_list_1018feda0._8_5_);
      *(undefined8 *)local_b0 = uVar15;
      uVar15 = CONCAT53(s_could_not_get_usb_device_list_1018feda0._16_5_,
                        s_could_not_get_usb_device_list_1018feda0._13_3_);
      *(undefined8 *)(local_b0 + 0x15) = s_could_not_get_usb_device_list_1018feda0._21_8_;
      *(undefined8 *)(local_b0 + 0xd) = uVar15;
      local_b0[0x1d] = '\0';
      FUN_1013f137c(local_d0,0xffffff9e,lVar14,&local_b0);
      lVar14 = *param_1;
      *param_1 = 0;
    }
    else {
      local_120 = (void *)0x0;
      local_90 = (long *)0x0;
      plStack_88 = (long *)0x0;
      local_80 = (long *)0x0;
      lVar14 = *local_100;
      if (lVar14 == 0) {
LAB_1013e5e68:
        plVar24 = local_90;
        local_a0 = local_a0 & 0xffffffffffffff;
        local_b0 = (char *)((ulong)local_b0 & 0xffffffffffffff00);
        FUN_1013f137c(local_d0,0xffffff9e,0,&local_b0);
      }
      else {
        plVar25 = (long *)0x0;
        lVar22 = 8;
        do {
          uVar15 = _libusb_get_device_descriptor(lVar14,&local_b0);
          if ((int)uVar15 < 0) {
            uVar16 = std::chrono::system_clock::now();
            FUN_1003324b0(&local_140,4,uVar16);
            iVar12 = FUN_10032ece8(&local_140);
            if (iVar12 != 0) {
              uVar16 = FUN_10032bea8(&local_140,"Could not get USB device descriptor, error: ");
              uVar15 = _libusb_error_name(uVar15);
              FUN_10032bea8(uVar16,uVar15);
            }
            thunk_FUN_10032ba14(&local_140);
          }
          else if ((short)uStack_a8 == 0x2982) {
            if ((local_b0._4_1_ == '\0') && (uStack_a8._2_2_ == 0x1967)) {
              uVar15 = 0x41;
            }
            else {
              if ((local_b0._4_1_ != -0x11) || (uStack_a8._2_2_ != 0x1969)) goto LAB_1013e5c60;
              uVar15 = 0x42;
            }
            uVar16 = std::chrono::system_clock::now();
            FUN_1003324b0(&local_140,2,uVar16);
            iVar12 = FUN_10032ece8(&local_140);
            if (iVar12 != 0) {
              uVar16 = FUN_10032bea8(&local_140,"Found Push USB device (rev ");
              uVar15 = FUN_10032df1c(uVar16,uVar15);
              FUN_10032bea8(uVar15,")");
            }
            thunk_FUN_10032ba14(&local_140);
            plVar24 = local_90;
            if ((((param_3 == 0) && (local_b0._4_1_ == '\0')) && (uStack_a8._2_2_ == 0x1967)) ||
               (((param_3 == 1 && (local_b0._4_1_ == -0x11)) && (uStack_a8._2_2_ == 0x1969)))) {
              if (plVar25 < local_80) {
                *plVar25 = lVar14;
              }
              else {
                sVar23 = (long)plVar25 - (long)local_90;
                lVar26 = (long)sVar23 >> 3;
                uVar18 = lVar26 + 1;
                if (uVar18 >> 0x3d != 0) {
                  FUN_1013e7c1c(&local_90);
                    /* WARNING: Does not return */
                  pcVar11 = (code *)SoftwareBreakpoint(1,0x1013e63b8);
                  (*pcVar11)();
                }
                uVar21 = (long)local_80 - (long)local_90 >> 2;
                if (uVar21 <= uVar18) {
                  uVar21 = uVar18;
                }
                if (0x7ffffffffffffff7 < (ulong)((long)local_80 - (long)local_90)) {
                  uVar21 = 0x1fffffffffffffff;
                }
                if (uVar21 == 0) {
                  plVar17 = (long *)0x0;
                }
                else {
                  if (uVar21 >> 0x3d != 0) {
                    /* WARNING: Subroutine does not return */
                    FUN_10017f504();
                  }
                  plVar17 = operator_new(uVar21 << 3);
                }
                plVar25 = plVar17 + lVar26;
                *plVar25 = lVar14;
                _memcpy(plVar17,plVar24,sVar23);
                local_90 = plVar17;
                local_80 = plVar17 + uVar21;
                if (plVar24 != (long *)0x0) {
                  operator_delete(plVar24);
                }
              }
              plVar25 = plVar25 + 1;
              plStack_88 = plVar25;
            }
          }
LAB_1013e5c60:
          plVar24 = local_90;
          lVar14 = *(long *)((long)local_100 + lVar22);
          lVar22 = lVar22 + 8;
        } while (lVar14 != 0);
        plVar17 = local_90;
        if (local_90 == plVar25) goto LAB_1013e5e68;
        do {
          uVar15 = _libusb_open(*plVar17,&local_120);
          if ((int)uVar15 < 0) {
            local_a0 = local_a0 & 0xffffffffffffff;
            local_b0 = (char *)((ulong)local_b0 & 0xffffffffffffff00);
            FUN_1013f137c(local_d0,0xffffff9f,uVar15,&local_b0);
          }
          else {
            uVar15 = _libusb_claim_interface(local_120,0);
            if (-1 < (int)uVar15) {
              uVar15 = std::chrono::system_clock::now();
              FUN_1003324b0(&local_b0,2,uVar15);
              iVar12 = FUN_10032ece8(&local_b0);
              if (iVar12 != 0) {
                FUN_10032bea8(&local_b0,"Push display USB device opened");
              }
              thunk_FUN_10032ba14(&local_b0);
              FUN_1013f1168(&local_b0);
              local_d0[0] = (undefined4)local_b0;
              uStack_c0 = local_a0;
              local_c8 = uStack_a8;
              local_b8 = local_98;
              break;
            }
            local_b0 = operator_new(0x30);
            uVar9 = s_could_not_claim_the_device_with_i_1018fee07._16_8_;
            uVar8 = s_could_not_claim_the_device_with_i_1018fee07._0_8_;
            local_a0 = uVar7;
            uStack_a8 = pppppuVar6;
            uVar16 = CONCAT53(s_could_not_claim_the_device_with_i_1018fee07._27_5_,
                              s_could_not_claim_the_device_with_i_1018fee07._24_3_);
            *(undefined8 *)(local_b0 + 8) = s_could_not_claim_the_device_with_i_1018fee07._8_8_;
            *(undefined8 *)local_b0 = uVar8;
            *(undefined8 *)(local_b0 + 0x18) = uVar16;
            *(undefined8 *)(local_b0 + 0x10) = uVar9;
            uVar16 = CONCAT35(s_could_not_claim_the_device_with_i_1018fee07._32_3_,
                              s_could_not_claim_the_device_with_i_1018fee07._27_5_);
            *(undefined8 *)(local_b0 + 0x23) = s_could_not_claim_the_device_with_i_1018fee07._35_8_;
            *(undefined8 *)(local_b0 + 0x1b) = uVar16;
            local_b0[0x2b] = '\0';
            FUN_1013f137c(local_d0,0xffffff9f,uVar15,&local_b0);
            _libusb_close(local_120);
            local_120 = (void *)0x0;
          }
          plVar17 = plVar17 + 1;
        } while (plVar17 != plVar25);
      }
      _libusb_free_device_list(local_100,1);
      pvVar10 = local_120;
      if (plVar24 != (long *)0x0) {
        plStack_88 = plVar24;
        operator_delete(plVar24);
      }
      lVar14 = *param_1;
      *param_1 = (long)pvVar10;
    }
    if (lVar14 != 0) {
      FUN_1013e6640();
    }
    uVar18 = FUN_1013f18c0(local_d0);
    if ((uVar18 & 1) != 0) break;
    local_158 = operator_new(0x28);
    lStack_148 = lVar3;
    local_150 = uVar2;
    local_158[0x20] = ':';
    uVar8 = s_could_not_open_usb_device__error_1018fed44._24_8_;
    uVar16 = s_could_not_open_usb_device__error_1018fed44._16_8_;
    uVar15 = s_could_not_open_usb_device__error_1018fed44._0_8_;
    local_158[0x21] = ' ';
    *(undefined8 *)(local_158 + 8) = s_could_not_open_usb_device__error_1018fed44._8_8_;
    *(undefined8 *)local_158 = uVar15;
    *(undefined8 *)(local_158 + 0x18) = uVar8;
    *(undefined8 *)(local_158 + 0x10) = uVar16;
    local_158[0x22] = '\0';
    FUN_1013f14ec(local_170,local_d0);
    pppppuVar1 = (undefined8 *****)local_170[0];
    if (-1 < local_159) {
      pppppuVar1 = local_170;
    }
    puVar19 = (undefined8 *)std::string::append((char *)&local_158,(ulong)pppppuVar1);
    uStack_138 = puVar19[1];
    local_140 = (void *)*puVar19;
    local_130 = puVar19[2];
    puVar19[1] = 0;
    puVar19[2] = 0;
    *puVar19 = 0;
    plVar25 = (long *)std::string::append((char *)&local_140,0x1018fed67);
    lStack_118 = plVar25[1];
    local_120 = (void *)*plVar25;
    local_110 = plVar25[2];
    plVar25[1] = 0;
    plVar25[2] = 0;
    *plVar25 = 0;
    iVar13 = iVar13 + 1;
    std::to_string(iVar13);
    pppppuVar1 = (undefined8 *****)local_188[0];
    if (-1 < local_171) {
      pppppuVar1 = local_188;
    }
    puVar19 = (undefined8 *)std::string::append((char *)&local_120,(ulong)pppppuVar1);
    uStack_f8 = puVar19[1];
    local_100 = (long *)*puVar19;
    local_f0 = puVar19[2];
    puVar19[1] = 0;
    puVar19[2] = 0;
    *puVar19 = 0;
    puVar19 = (undefined8 *)std::string::append((char *)&local_100,0x1018fed72);
    plStack_88 = (long *)puVar19[1];
    local_90 = (long *)*puVar19;
    local_80 = (long *)puVar19[2];
    puVar19[1] = 0;
    puVar19[2] = 0;
    *puVar19 = 0;
    std::to_string(1000);
    pppppuVar1 = (undefined8 *****)local_1a0[0];
    if (-1 < local_189) {
      pppppuVar1 = local_1a0;
    }
    puVar19 = (undefined8 *)std::string::append((char *)&local_90,(ulong)pppppuVar1);
    uStack_a8 = (undefined8 *****)puVar19[1];
    local_b0 = (char *)*puVar19;
    local_a0 = puVar19[2];
    puVar19[1] = 0;
    puVar19[2] = 0;
    *puVar19 = 0;
    if (local_189 < '\0') {
      operator_delete(local_1a0[0]);
    }
    if (local_171 < '\0') {
      operator_delete(local_188[0]);
      if (-1 < local_110) goto LAB_1013e621c;
LAB_1013e62cc:
      operator_delete(local_120);
      if (-1 < local_130) goto LAB_1013e6224;
LAB_1013e62dc:
      operator_delete(local_140);
      if (-1 < local_159) goto LAB_1013e622c;
LAB_1013e62ec:
      operator_delete(local_170[0]);
    }
    else {
      if (local_110 < 0) goto LAB_1013e62cc;
LAB_1013e621c:
      if (local_130 < 0) goto LAB_1013e62dc;
LAB_1013e6224:
      if (local_159 < '\0') goto LAB_1013e62ec;
LAB_1013e622c:
    }
    if (lStack_148 < 0) {
      operator_delete(local_158);
    }
    uVar15 = std::chrono::system_clock::now();
    FUN_1003324b0(&local_90,4,uVar15);
    iVar12 = FUN_10032ece8(&local_90);
    if (iVar12 != 0) {
      FUN_10032cd88(&local_90,&local_b0);
    }
    pdVar20 = (duration *)thunk_FUN_10032ba14(&local_90);
    local_90 = (long *)&DAT_3b9aca00;
    std::this_thread::sleep_for(pdVar20);
  } while (iVar13 != 0x14);
  if (param_2 != (undefined4 *)0x0) {
    plVar25 = (long *)(param_2 + 2);
    *param_2 = local_d0[0];
    if (local_d0 != param_2) {
      if (*(char *)((long)param_2 + 0x1f) < '\0') {
        if (-1 < (long)local_b8) {
          uStack_c0 = local_b8 >> 0x38;
          local_c8 = &local_c8;
        }
        FUN_1001b9f50(plVar25,local_c8,uStack_c0);
      }
      else if ((long)local_b8 < 0) {
        FUN_10018e284(plVar25,local_c8,uStack_c0);
      }
      else {
        *(ulong *)(param_2 + 4) = uStack_c0;
        *plVar25 = (long)local_c8;
        *(ulong *)(param_2 + 6) = local_b8;
      }
    }
  }
  return;
}

