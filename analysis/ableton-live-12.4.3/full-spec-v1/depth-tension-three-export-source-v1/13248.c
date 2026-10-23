
undefined8
_CalcA(undefined8 param_1,undefined8 param_2,float *param_3,float *param_4,undefined8 param_5,
      undefined8 param_6,int *param_7,uint *param_8)

{
  bool bVar1;
  bool bVar2;
  bool bVar3;
  bool bVar4;
  bool bVar5;
  int iVar6;
  long *plVar7;
  undefined8 uVar8;
  long lVar9;
  float fVar10;
  float fVar11;
  undefined1 auVar12 [16];
  undefined1 local_40d8 [8];
  undefined8 local_40d0;
  undefined8 uStack_40c8;
  undefined1 local_40b9;
  undefined1 auStack_40b8 [16432];
  float *local_88;
  float *pfStack_80;
  float *local_78;
  float *local_70;
  long local_68;
  
  auVar12 = (*(code *)PTR____chkstk_darwin_0005c080)();
  lVar9 = auVar12._8_8_;
  plVar7 = auVar12._0_8_;
  local_68 = *(long *)PTR____stack_chk_guard_0005c090;
  if (plVar7 == (long *)0x0) {
    if ((DAT_000605e3 & 1) == 0) {
      _fwrite("CalcA called with nullptr.\n",0x1b,1,*(FILE **)PTR____stderrp_0005c098);
      uVar8 = 0;
      DAT_000605e3 = 1;
    }
    else {
      uVar8 = 0;
    }
  }
  else {
    FUN_000162ec(auStack_40b8,0x400);
    local_40b9 = 0;
    FUN_0001577c(param_5,param_6,auStack_40b8,&local_40b9);
    if (DAT_00060318 == 1) {
      local_70 = (float *)0x0;
      uVar8 = 0;
      local_78 = (float *)0x0;
    }
    else {
      local_70 = param_4;
      if (DAT_000603d8 != '\0') {
        local_70 = param_3;
      }
      uVar8 = 2;
      local_78 = param_3;
    }
    pfStack_80 = param_4;
    if (DAT_000603d8 != '\0') {
      pfStack_80 = param_3;
    }
    local_40d8[0] = *param_7 != 0;
    uStack_40c8 = *(undefined8 *)(param_7 + 4);
    local_40d0 = *(undefined8 *)(param_7 + 2);
    local_88 = param_3;
    (**(code **)(*plVar7 + 0x60))
              (plVar7,auStack_40b8,0,&local_78,&local_88,lVar9,uVar8,2,local_40d8);
    if (param_8 != (uint *)0x0) {
      iVar6 = (**(code **)(*plVar7 + 0x68))(plVar7,0x14,0,0);
      *param_8 = (uint)(iVar6 == 0);
    }
    if (DAT_00060328 == '\0') {
      uVar8 = 0;
    }
    else if (lVar9 < 1) {
      uVar8 = 0;
    }
    else {
      uVar8 = 0;
      do {
        fVar10 = *param_3;
        if (fVar10 < -0.7) {
LAB_000133fc:
          uVar8 = 1;
        }
        else {
          fVar11 = *param_4;
          bVar1 = false;
          bVar3 = false;
          bVar4 = false;
          if (fVar11 <= 0.7) {
            bVar1 = false;
            bVar3 = false;
            bVar4 = true;
            if (!NAN(fVar10)) {
              bVar1 = fVar10 < 0.7;
              bVar3 = fVar10 == 0.7;
              bVar4 = false;
            }
          }
          bVar2 = true;
          bVar5 = false;
          if (bVar3 || bVar1 != bVar4) {
            bVar2 = false;
            bVar5 = true;
            if (!NAN(fVar11)) {
              bVar2 = fVar11 < -0.7;
              bVar5 = false;
            }
          }
          if (bVar2 != bVar5) goto LAB_000133fc;
        }
        *param_3 = fVar10 * 4.0;
        *param_4 = *param_4 * 4.0;
        lVar9 = lVar9 + -1;
        param_4 = param_4 + 1;
        param_3 = param_3 + 1;
      } while (lVar9 != 0);
    }
    FUN_000163a0(auStack_40b8);
  }
  if (*(long *)PTR____stack_chk_guard_0005c090 == local_68) {
    return uVar8;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

