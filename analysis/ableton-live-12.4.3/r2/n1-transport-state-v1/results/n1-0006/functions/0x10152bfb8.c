
void FUN_10152bfb8(TString param_1,undefined8 *param_2)

{
  int iVar1;
  ulong uVar2;
  long *plVar3;
  undefined8 *puVar4;
  int *piVar5;
  undefined8 uVar6;
  ulong extraout_x1;
  uint uVar7;
  float fVar8;
  double dVar9;
  undefined1 auVar10 [16];
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  undefined1 auStack_68 [8];
  undefined1 auStack_60 [8];
  int *local_58;
  int *local_50;
  int **local_48;
  undefined1 local_40;
  
  (**(code **)(*(long *)param_1.field0_0x0.field0_0x0 + 0x28))();
  iVar1 = FUN_10120e264();
  if (iVar1 < 0x14) {
    if (iVar1 < 0x12) {
      if (iVar1 != 0x10) {
        if (iVar1 != 0x11) {
          return;
        }
        uVar2 = FUN_1002fd908(*param_2,(long)*(int *)(param_2 + 1));
        if ((uVar2 >> 0x20 & 1) == 0) {
          uVar6 = ___cxa_allocate_exception(0x30);
          FUN_101447188(&local_48,&DAT_106e0cc01,"Unexpected value for int node: $1");
          FUN_101432520(&local_50,*param_2,*(undefined4 *)(param_2 + 1));
          FUN_1011cb734(&local_58);
          FUN_1011cb734(auStack_60);
          FUN_1011cb734(auStack_68);
          FUN_1011cb734(auStack_70);
          FUN_101242ce8(uVar6,&local_48,&local_50,&local_58,auStack_60,auStack_68,auStack_70);
                    /* WARNING: Subroutine does not return */
          ___cxa_throw(uVar6,&PTR_vtable_106661270,FUN_10124335c);
        }
        AAbstractNode::SetValue<int>((int)param_1.field0_0x0.field0_0x0);
        return;
      }
      iVar1 = *(int *)(param_2 + 1);
      if (iVar1 == 1) {
        if (*(char *)*param_2 == '1') {
LAB_10152c940:
          AAbstractNode::SetValue<bool>(param_1.field0_0x0.field0_0x0._0_1_);
          return;
        }
      }
      else if (iVar1 == 5) {
        if (*(int *)*param_2 == 0x736c6166 && (char)((int *)*param_2)[1] == 'e') goto LAB_10152c970;
      }
      else if ((iVar1 == 4) && (*(int *)*param_2 == 0x65757274)) goto LAB_10152c940;
      iVar1 = FUN_10152bf4c(param_2,"0");
      if (iVar1 == 0) {
        uVar6 = ___cxa_allocate_exception(0x30);
        FUN_101447188(&local_48,&DAT_106e0cc01,"Unexpected value for bool node: $1");
        FUN_101432520(&local_50,*param_2,*(undefined4 *)(param_2 + 1));
        FUN_1011cb734(&local_58);
        FUN_1011cb734(auStack_60);
        FUN_1011cb734(auStack_68);
        FUN_1011cb734(auStack_70);
        FUN_101242ce8(uVar6,&local_48,&local_50,&local_58,auStack_60,auStack_68,auStack_70);
                    /* WARNING: Subroutine does not return */
        ___cxa_throw(uVar6,&PTR_vtable_106661270,FUN_10124335c);
      }
LAB_10152c970:
      AAbstractNode::SetValue<bool>(param_1.field0_0x0.field0_0x0._0_1_);
      return;
    }
    if (iVar1 != 0x12) {
      if (iVar1 != 0x13) {
        return;
      }
      FUN_101432520(&local_50,*param_2,*(undefined4 *)(param_2 + 1));
      FUN_1011cb734(&local_58);
      plVar3 = (long *)FUN_10152d098(&local_50,&local_58);
      if ((*plVar3 != 0) && ((*(uint *)(*plVar3 + 4) & 0xfffffffe) == 4)) {
        FUN_101428974(plVar3,0);
        AAbstractNode::SetValue<char16_t>((wchar16)param_1.field0_0x0.field0_0x0);
        if ((local_58 != (int *)0x0) && (iVar1 = *local_58, *local_58 = iVar1 + -1, iVar1 + -1 == 0)
           ) {
          FUN_101449efc();
        }
        if (local_50 == (int *)0x0) {
          return;
        }
        iVar1 = *local_50;
        *local_50 = iVar1 + -1;
        if (iVar1 + -1 != 0) {
          return;
        }
        FUN_101449efc();
        return;
      }
      uVar6 = ___cxa_allocate_exception(0x30);
      FUN_101447188(&local_48,&DAT_106e0cc01,"Unexpected value for char node: $1");
      FUN_1011cb734(auStack_60);
      FUN_1011cb734(auStack_68);
      FUN_1011cb734(auStack_70);
      FUN_1011cb734(auStack_78);
      FUN_101242ce8(uVar6,&local_48,&local_50,auStack_60,auStack_68,auStack_70,auStack_78);
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(uVar6,&PTR_vtable_106661270,FUN_10124335c);
    }
    piVar5 = (int *)*param_2;
    if (*(int *)(param_2 + 1) == 9) {
      if ((char)*piVar5 == '#') {
        uVar7 = (uint)*(byte *)((long)piVar5 + 1);
        if (((((((((uVar7 - 0x30 & 0xff) < 10) ||
                 (uVar7 = uVar7 - 0x41,
                 uVar7 < 0x26 && (1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)) &&
                (((*(byte *)((long)piVar5 + 2) - 0x30 & 0xff) < 10 ||
                 (uVar7 = *(byte *)((long)piVar5 + 2) - 0x41,
                 uVar7 < 0x26 && (1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))) &&
               (((*(byte *)((long)piVar5 + 3) - 0x30 & 0xff) < 10 ||
                (uVar7 = *(byte *)((long)piVar5 + 3) - 0x41,
                uVar7 < 0x26 && (1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))) &&
              (((*(byte *)(piVar5 + 1) - 0x30 & 0xff) < 10 ||
               ((uVar7 = *(byte *)(piVar5 + 1) - 0x41, uVar7 < 0x26 &&
                ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))))) &&
             (((*(byte *)((long)piVar5 + 5) - 0x30 & 0xff) < 10 ||
              ((uVar7 = *(byte *)((long)piVar5 + 5) - 0x41, uVar7 < 0x26 &&
               ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))))) &&
            (((*(byte *)((long)piVar5 + 6) - 0x30 & 0xff) < 10 ||
             ((uVar7 = *(byte *)((long)piVar5 + 6) - 0x41, uVar7 < 0x26 &&
              ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))))) &&
           ((((*(byte *)((long)piVar5 + 7) - 0x30 & 0xff) < 10 ||
             ((uVar7 = *(byte *)((long)piVar5 + 7) - 0x41, uVar7 < 0x26 &&
              ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))) &&
            (((*(byte *)(piVar5 + 2) - 0x30 & 0xff) < 10 ||
             ((uVar7 = *(byte *)(piVar5 + 2) - 0x41, uVar7 < 0x26 &&
              ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))))))) {
          local_48 = &local_50;
          local_40 = 1;
          FUN_10152cff8(&local_48,(byte *)((long)piVar5 + 1),8);
          uVar7 = ((uint)local_50 & 0xff00ff00) >> 8 | ((uint)local_50 & 0xff00ff) << 8;
          fVar8 = (float)(uVar7 >> 0x10 | uVar7 << 0x10);
          local_50 = (int *)CONCAT44(local_50._4_4_,fVar8);
          goto LAB_10152c538;
        }
      }
    }
    else if ((*(int *)(param_2 + 1) == 7) &&
            (*piVar5 == 0x61766e49 && *(int *)((long)piVar5 + 3) == 0x64696c61)) {
      AAbstractNode::SetValue<float>(3.4028235e+38);
      return;
    }
    dVar9 = _strtod((char *)piVar5,(char **)&local_50);
    if (local_50 == (int *)*param_2) {
      uVar6 = ___cxa_allocate_exception(0x30);
      FUN_101447188(&local_48,&DAT_106e0cc01,"Unexpected value for float node: $1");
      FUN_101432520(&local_58,*param_2,*(undefined4 *)(param_2 + 1));
      FUN_1011cb734(auStack_60);
      FUN_1011cb734(auStack_68);
      FUN_1011cb734(auStack_70);
      FUN_1011cb734(auStack_78);
      FUN_101242ce8(uVar6,&local_48,&local_58,auStack_60,auStack_68,auStack_70,auStack_78);
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(uVar6,&PTR_vtable_106661270,FUN_10124335c);
    }
    fVar8 = (float)dVar9;
LAB_10152c538:
    AAbstractNode::SetValue<float>(fVar8);
    return;
  }
  if (0x17 < iVar1) {
    if (iVar1 != 0x18) {
      if (iVar1 == 0x19) {
        FUN_101432520(&local_48,*param_2,*(undefined4 *)(param_2 + 1));
        FUN_1011cb734(&local_50);
        FUN_10152d098(&local_48,&local_50);
        auVar10 = FUN_1012908d8();
        AAbstractNode::SetValue<TIdentifier>
                  (param_1.field0_0x0.field0_0x0,auVar10._0_8_,auVar10._8_8_ & 0xff);
        if ((local_50 != (int *)0x0) && (iVar1 = *local_50, *local_50 = iVar1 + -1, iVar1 + -1 == 0)
           ) {
          FUN_101449efc();
        }
        if ((local_48 != (int **)0x0) &&
           (iVar1 = *(int *)local_48, *(int *)local_48 = iVar1 + -1, iVar1 + -1 == 0)) {
          FUN_101449efc();
        }
      }
      return;
    }
    FUN_101533e14(*param_2,(long)*(int *)(param_2 + 1));
    if ((extraout_x1 & 1) == 0) {
      uVar6 = ___cxa_allocate_exception(0x30);
      FUN_101447188(&local_48,&DAT_106e0cc01,"Unexpected value for int64 node: $1");
      FUN_101432520(&local_50,*param_2,*(undefined4 *)(param_2 + 1));
      FUN_1011cb734(&local_58);
      FUN_1011cb734(auStack_60);
      FUN_1011cb734(auStack_68);
      FUN_1011cb734(auStack_70);
      FUN_101242ce8(uVar6,&local_48,&local_50,&local_58,auStack_60,auStack_68,auStack_70);
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(uVar6,&PTR_vtable_106661270,FUN_10124335c);
    }
    AAbstractNode::SetValue<long_long>((longlong)param_1.field0_0x0.field0_0x0);
    return;
  }
  if (iVar1 == 0x14) {
    FUN_101432520(&local_48,*param_2,*(undefined4 *)(param_2 + 1));
    FUN_1011cb734(&local_50);
    puVar4 = (undefined8 *)FUN_10152d098(&local_48,&local_50);
    piVar5 = (int *)*puVar4;
    if (piVar5 != (int *)0x0) {
      *piVar5 = *piVar5 + 1;
    }
    AAbstractNode::SetValue<TString>(param_1);
    if ((piVar5 != (int *)0x0) && (iVar1 = *piVar5, *piVar5 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
    if ((local_50 != (int *)0x0) && (iVar1 = *local_50, *local_50 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
    if (local_48 == (int **)0x0) {
      return;
    }
    iVar1 = *(int *)local_48;
    *(int *)local_48 = iVar1 + -1;
    if (iVar1 + -1 != 0) {
      return;
    }
    FUN_101449efc();
    return;
  }
  if (iVar1 != 0x17) {
    return;
  }
  piVar5 = (int *)*param_2;
  if (*(int *)(param_2 + 1) == 0x11) {
    if ((char)*piVar5 == '#') {
      uVar7 = (uint)*(byte *)((long)piVar5 + 1);
      if ((((((((uVar7 - 0x30 & 0xff) < 10) ||
              (uVar7 = uVar7 - 0x41,
              uVar7 < 0x26 && (1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)) &&
             (((*(byte *)((long)piVar5 + 2) - 0x30 & 0xff) < 10 ||
              (uVar7 = *(byte *)((long)piVar5 + 2) - 0x41,
              uVar7 < 0x26 && (1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))) &&
            (((*(byte *)((long)piVar5 + 3) - 0x30 & 0xff) < 10 ||
             ((uVar7 = *(byte *)((long)piVar5 + 3) - 0x41, uVar7 < 0x26 &&
              ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))))) &&
           (((((*(byte *)(piVar5 + 1) - 0x30 & 0xff) < 10 ||
              ((uVar7 = *(byte *)(piVar5 + 1) - 0x41, uVar7 < 0x26 &&
               ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))) &&
             (((*(byte *)((long)piVar5 + 5) - 0x30 & 0xff) < 10 ||
              ((uVar7 = *(byte *)((long)piVar5 + 5) - 0x41, uVar7 < 0x26 &&
               ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))))) &&
            (((((*(byte *)((long)piVar5 + 6) - 0x30 & 0xff) < 10 ||
               ((uVar7 = *(byte *)((long)piVar5 + 6) - 0x41, uVar7 < 0x26 &&
                ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))) &&
              (((*(byte *)((long)piVar5 + 7) - 0x30 & 0xff) < 10 ||
               ((uVar7 = *(byte *)((long)piVar5 + 7) - 0x41, uVar7 < 0x26 &&
                ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))))) &&
             (((*(byte *)(piVar5 + 2) - 0x30 & 0xff) < 10 ||
              ((uVar7 = *(byte *)(piVar5 + 2) - 0x41, uVar7 < 0x26 &&
               ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))))))))) &&
          (((((*(byte *)((long)piVar5 + 9) - 0x30 & 0xff) < 10 ||
             ((uVar7 = *(byte *)((long)piVar5 + 9) - 0x41, uVar7 < 0x26 &&
              ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))) &&
            ((((*(byte *)((long)piVar5 + 10) - 0x30 & 0xff) < 10 ||
              ((uVar7 = *(byte *)((long)piVar5 + 10) - 0x41, uVar7 < 0x26 &&
               ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))) &&
             (((*(byte *)((long)piVar5 + 0xb) - 0x30 & 0xff) < 10 ||
              ((uVar7 = *(byte *)((long)piVar5 + 0xb) - 0x41, uVar7 < 0x26 &&
               ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))))))) &&
           ((((*(byte *)(piVar5 + 3) - 0x30 & 0xff) < 10 ||
             ((uVar7 = *(byte *)(piVar5 + 3) - 0x41, uVar7 < 0x26 &&
              ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))) &&
            (((*(byte *)((long)piVar5 + 0xd) - 0x30 & 0xff) < 10 ||
             ((uVar7 = *(byte *)((long)piVar5 + 0xd) - 0x41, uVar7 < 0x26 &&
              ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))))))))) &&
         (((((*(byte *)((long)piVar5 + 0xe) - 0x30 & 0xff) < 10 ||
            ((uVar7 = *(byte *)((long)piVar5 + 0xe) - 0x41, uVar7 < 0x26 &&
             ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))) &&
           (((*(byte *)((long)piVar5 + 0xf) - 0x30 & 0xff) < 10 ||
            ((uVar7 = *(byte *)((long)piVar5 + 0xf) - 0x41, uVar7 < 0x26 &&
             ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))))) &&
          (((*(byte *)(piVar5 + 4) - 0x30 & 0xff) < 10 ||
           ((uVar7 = *(byte *)(piVar5 + 4) - 0x41, uVar7 < 0x26 &&
            ((1L << ((ulong)uVar7 & 0x3f) & 0x3f0000003fU) != 0)))))))) {
        local_48 = &local_50;
        local_40 = 1;
        FUN_10152cff8(&local_48,(byte *)((long)piVar5 + 1),0x10);
        uVar2 = ((ulong)local_50 & 0xff00ff00ff00ff00) >> 8 |
                ((ulong)local_50 & 0xff00ff00ff00ff) << 8;
        uVar2 = (uVar2 & 0xffff0000ffff0000) >> 0x10 | (uVar2 & 0xffff0000ffff) << 0x10;
        piVar5 = (int *)(uVar2 >> 0x20 | uVar2 << 0x20);
        local_50 = piVar5;
        goto LAB_10152c8ec;
      }
    }
  }
  else if ((*(int *)(param_2 + 1) == 7) &&
          (*piVar5 == 0x61766e49 && *(int *)((long)piVar5 + 3) == 0x64696c61)) {
    AAbstractNode::SetValue<double>(1.79769313486232e+308);
    return;
  }
  piVar5 = (int *)_strtod((char *)piVar5,(char **)&local_50);
  if (local_50 == (int *)*param_2) {
    uVar6 = ___cxa_allocate_exception(0x30);
    FUN_101447188(&local_48,&DAT_106e0cc01,"Unexpected value for double node: $1");
    FUN_101432520(&local_58,*param_2,*(undefined4 *)(param_2 + 1));
    FUN_1011cb734(auStack_60);
    FUN_1011cb734(auStack_68);
    FUN_1011cb734(auStack_70);
    FUN_1011cb734(auStack_78);
    FUN_101242ce8(uVar6,&local_48,&local_58,auStack_60,auStack_68,auStack_70,auStack_78);
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar6,&PTR_vtable_106661270,FUN_10124335c);
  }
LAB_10152c8ec:
  AAbstractNode::SetValue<double>((double)piVar5);
  return;
}

