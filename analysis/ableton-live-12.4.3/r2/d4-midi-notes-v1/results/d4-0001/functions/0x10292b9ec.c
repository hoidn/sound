
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_10292b9ec(double param_1,long param_2)

{
  code *pcVar1;
  int iVar2;
  uint uVar3;
  double *pdVar4;
  long lVar5;
  undefined8 uVar6;
  ushort uVar7;
  double local_e0 [2];
  long *local_d0;
  undefined8 uStack_c8;
  long *local_c0;
  undefined **local_b8 [3];
  undefined ***local_a0;
  long alStack_98 [3];
  long *local_80;
  long alStack_78 [3];
  long *local_60;
  undefined **local_58;
  long lStack_50;
  undefined ***local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_1064f8818;
  uVar6 = *(undefined8 *)(param_2 + 0x30);
  iVar2 = FUN_10155ede4(uVar6);
  if (iVar2 == 0) goto LAB_10292bca4;
  pdVar4 = (double *)FUN_10155ee2c(uVar6,0);
  uVar3 = FUN_10155ede4(uVar6);
  if (uVar3 == 0) goto LAB_10292bca4;
  if ((int)uVar3 < 1) {
    FUN_105425050();
                    /* WARNING: Does not return */
    pcVar1 = (code *)SoftwareBreakpoint(1,0x10292bcdc);
    (*pcVar1)();
  }
  if ((0.0 < *pdVar4) && (pdVar4[(ulong)uVar3 * 6 + -6] < param_1)) goto LAB_10292bca4;
  local_c0 = (long *)0x0;
  FUN_1025c442c(&local_d0);
  if ((local_c0 != (long *)0x0) &&
     (iVar2 = *(int *)((long)local_c0 + 8) + -1, *(int *)((long)local_c0 + 8) = iVar2, iVar2 == 0))
  {
    FUN_10128eea0();
  }
  local_c0 = local_d0;
  local_58 = &PTR_FUN_10682ac40;
  local_40 = &local_58;
  local_60 = (long *)0x0;
  local_80 = (long *)0x0;
  local_b8[0] = &PTR_FUN_106827b70;
  local_a0 = local_b8;
  lStack_50 = param_2;
  FUN_1025c4708(0,local_d0,&local_58,*(undefined4 *)(param_2 + 0x48),0,alStack_78,alStack_98,
                local_b8);
  if (local_a0 == local_b8) {
    lVar5 = 0x20;
LAB_10292bb14:
    (**(code **)((long)*local_a0 + lVar5))();
  }
  else if (local_a0 != (undefined ***)0x0) {
    lVar5 = 0x28;
    goto LAB_10292bb14;
  }
  if (local_80 == alStack_98) {
    lVar5 = 0x20;
LAB_10292bb40:
    (**(code **)(*local_80 + lVar5))();
  }
  else if (local_80 != (long *)0x0) {
    lVar5 = 0x28;
    goto LAB_10292bb40;
  }
  if (local_60 == alStack_78) {
    lVar5 = 0x20;
LAB_10292bb6c:
    (**(code **)(*local_60 + lVar5))();
  }
  else if (local_60 != (long *)0x0) {
    lVar5 = 0x28;
    goto LAB_10292bb6c;
  }
  if (local_40 == &local_58) {
    lVar5 = 0x20;
LAB_10292bb98:
    (**(code **)((long)*local_40 + lVar5))();
  }
  else if (local_40 != (undefined ***)0x0) {
    lVar5 = 0x28;
    goto LAB_10292bb98;
  }
  uStack_c8 = _UNK_105847028;
  local_d0 = _DAT_105847020;
  (**(code **)(*local_c0 + 0x308))(local_c0,&local_d0,&local_d0);
  uVar7 = NEON_umaxv(CONCAT26(-(ushort)(param_1 == _UNK_1055d9698),
                              CONCAT24(-(ushort)(param_1 == _DAT_1055d9690),
                                       CONCAT22(-(ushort)(param_1 == _UNK_1055d9688),
                                                -(ushort)(param_1 == _DAT_1055d9680)))),2);
  if ((uVar7 & 1) == 0) {
    uVar7 = 0x3ff0;
    if (param_1 < 0.0) {
      uVar7 = 0xbff0;
    }
    param_1 = (double)((ulong)uVar7 << 0x30) *
              ((double)(long)(ABS(param_1 + (double)((ulong)uVar7 << 0x30) * 2.6015651015651016e-07
                                            * 0.5) * 3843840.0) / 3843840.0);
  }
  local_e0[1] = 1.7976931348623155e+308;
  local_e0[0] = param_1;
  (**(code **)(*local_c0 + 0x308))(local_c0,local_e0,local_e0);
  if (((local_c0 != (long *)0x0) && ((**(code **)(*local_c0 + 0x18))(), local_c0 != (long *)0x0)) &&
     (iVar2 = (int)local_c0[1] + -1, *(int *)(local_c0 + 1) = iVar2, iVar2 == 0)) {
    FUN_10128eea0();
  }
LAB_10292bca4:
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

