
void FUN_1027c1c7c(long *param_1,undefined8 param_2)

{
  int iVar1;
  uint uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  long *plVar5;
  ulong uVar6;
  long lVar7;
  float fVar8;
  float fVar9;
  int *local_38;
  
  FUN_102441a30();
  iVar1 = FUN_10156da34(param_1[0xcb]);
  if (iVar1 == 0) {
    lVar7 = param_1[0xcb];
    uVar2 = (**(code **)(*param_1 + 0x300))(param_1);
    FUN_10155e55c(lVar7,uVar2 ^ 1);
    FUN_1027b3928(param_1);
    FUN_101427680(&local_38,"AfterRead");
    if (local_38 != (int *)0x0) {
      iVar1 = *local_38;
      *local_38 = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_101449efc();
      }
    }
    uVar3 = FUN_10243afa0(param_1);
    uVar4 = (**(code **)(*param_1 + 0x300))(param_1);
    FUN_10256d5ac(uVar3,uVar4,1);
    FUN_10279b15c(param_1[0xbe],param_1 + 0x8c);
    FUN_102440ff0(param_1,0);
    FUN_10283b098(param_1[0xb4],param_1[0xbe]);
    lVar7 = param_1[0xb4];
    plVar5 = (long *)FUN_102876f14(param_1[0xbe]);
    (**(code **)(*plVar5 + 0x1b0))();
    FUN_10283adb8(lVar7);
    FUN_102440ff0(param_1,1);
    fVar8 = (float)(**(code **)(*(long *)param_1[0xef] + 0x210))();
    fVar9 = (float)(**(code **)(*(long *)param_1[0xf2] + 0x210))();
    fVar8 = (float)_powf(0x3f879c7d,fVar8 + fVar9 * 0.01);
    param_1[199] = (long)(double)fVar8;
    uVar3 = FUN_101505400();
    plVar5 = (long *)FUN_102876f14(param_1[0xbe]);
    iVar1 = (**(code **)(*plVar5 + 0x210))();
    if ((iVar1 != 0) && (uVar6 = FUN_101509d40(uVar3), (uVar6 & 1) == 0)) {
      FUN_101506558(uVar3,2);
    }
    return;
  }
  FUN_101488e64(param_2,"Empty warp marker array.");
                    /* WARNING: Subroutine does not return */
  FUN_10017b398();
}

