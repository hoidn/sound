
void FUN_101b7fde4(long param_1,int *param_2,float *param_3,undefined8 *param_4)

{
  bool bVar1;
  bool bVar2;
  int iVar3;
  long *plVar4;
  undefined8 uVar5;
  float fVar6;
  ulong uVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  float local_80;
  float fStack_7c;
  float fStack_78;
  undefined4 uStack_74;
  undefined4 uStack_70;
  undefined8 local_68;
  
  iVar3 = FUN_1011c0ee8(0x100500);
  if (iVar3 == 0) {
    uVar5 = 0;
    if (param_1 != 0) {
      uVar5 = FUN_101a94314(param_1);
    }
    FUN_101b0d60c(uVar5,param_2[5]);
    uVar7 = FUN_101b39c8c();
    fVar10 = *param_3;
    fVar6 = (float)uVar7;
    if (fVar10 == -1.0) {
      fVar9 = (float)param_2[1];
      fVar10 = (float)param_2[2];
      fVar11 = fVar9;
      if (fVar9 <= fVar10) {
        fVar11 = fVar10;
        fVar10 = fVar9;
      }
      if (*param_2 == 2) {
        local_80 = 1.0;
        if (fVar6 != 0.0) {
          local_80 = 0.0;
        }
      }
      else if ((char)param_2[3] == '\x01') {
        local_80 = fVar6 + 1.0;
        if (fVar11 < fVar6 + 1.0) {
          local_80 = fVar10;
        }
      }
      else {
        local_80 = fVar10;
        if (fVar6 < (fVar11 - fVar10) * 0.5 + fVar10) {
          local_80 = fVar11;
        }
      }
    }
    else if ((float)param_2[7] <= 1.0) {
      if (*param_2 == 2) {
        if ((param_3[2] == 0.0) || (param_3[2] == 7.00649e-45)) {
          fVar9 = (float)param_2[1];
          fVar11 = (float)param_2[2];
          fVar6 = fVar11;
          if (fVar9 <= fVar11) {
            fVar6 = fVar9;
          }
          fVar12 = fVar11;
          if (fVar11 <= fVar9) {
            fVar12 = fVar9;
          }
          bVar1 = true;
          bVar2 = false;
          if (fVar10 <= fVar12) {
            bVar1 = false;
            bVar2 = true;
            if (!NAN(fVar10) && !NAN(fVar6)) {
              bVar1 = fVar10 < fVar6;
              bVar2 = false;
            }
          }
          bVar1 = fVar11 < fVar9 != (bVar1 == bVar2);
        }
        else {
          fVar6 = (float)FUN_101b7b96c(fVar10);
          bVar1 = 0.0 < fVar6 * param_3[3];
        }
        local_80 = 1.0;
        if (!bVar1) {
          local_80 = 0.0;
        }
      }
      else {
        fVar9 = (float)param_2[1];
        fVar11 = (float)param_2[2];
        fVar10 = fVar9;
        fVar6 = fVar11;
        if (fVar11 >= fVar9) {
          fVar10 = fVar11;
          fVar6 = fVar9;
        }
        local_80 = (float)FUN_101b76bf0(uVar7,fVar6,fVar10,param_3,(char)param_2[3],fVar11 < fVar9);
        fVar12 = param_3[2];
        if (((fVar12 == 7.00649e-45 || fVar12 == 0.0) && (*param_2 == 1)) &&
           (param_3[1] != 3.4028235e+38)) {
          local_80 = (float)FUN_101b7c508(uVar7 & 0xffffffff,local_80,param_3[1],fVar6,fVar10,
                                          param_2[6],fVar12,fVar11 < fVar9,(char)param_2[3]);
        }
      }
    }
    else {
      fVar11 = param_3[1];
      fVar6 = param_3[2];
      if (((fVar6 == 7.00649e-45) || (fVar6 == 0.0)) && ((*(byte *)(param_2 + 8) & 1) == 0)) {
        fVar9 = fVar10;
        fVar6 = fVar11;
        if (fVar11 <= fVar10) {
          fVar9 = fVar11;
          fVar6 = fVar10;
        }
        bVar1 = true;
        bVar2 = false;
        if (fVar9 <= 64.0) {
          bVar1 = false;
          bVar2 = true;
          if (!NAN(fVar6)) {
            bVar1 = fVar6 < 64.0;
            bVar2 = false;
          }
        }
        if (bVar1 == bVar2) {
          *(undefined1 *)(param_2 + 8) = 1;
          fVar11 = 64.0;
        }
        FUN_101ab7348(&local_80,&DAT_106fba1b8,0x10100,0x100500,0);
        FUN_101a9c534(CONCAT44(uStack_74,fStack_78),param_2[6]);
        FUN_101a9c504(CONCAT44(uStack_74,fStack_78),(char)param_2[8]);
        (**(code **)(CONCAT44(fStack_7c,local_80) + 0x10))(&local_80);
        FUN_101ab786c(&local_80);
        uVar7 = uVar7 & 0xffffffff;
        fVar6 = param_3[2];
      }
      fStack_78 = fVar6;
      if (((fStack_78 != 7.00649e-45) && (fStack_78 != 0.0)) ||
         (local_80 = (float)uVar7, (char)param_2[8] == '\x01')) {
        fVar9 = (float)param_2[1];
        fVar12 = (float)param_2[2];
        uStack_74 = 0x3f800000;
        fVar6 = fVar12;
        if (fVar9 <= fVar12) {
          fVar6 = fVar9;
        }
        fVar8 = fVar12;
        if (fVar12 <= fVar9) {
          fVar8 = fVar9;
        }
        local_80 = fVar10;
        fStack_7c = fVar11;
        fVar11 = (float)FUN_101b7bd1c(fVar6,fVar8,&local_80);
        fVar10 = fVar11 / (float)param_2[7];
        if (fVar12 < fVar9) {
          fVar10 = -(fVar11 / (float)param_2[7]);
        }
        fVar10 = (float)uVar7 + fVar10;
        if (fVar10 <= fVar8) {
          fVar8 = fVar10;
        }
        local_80 = fVar6;
        if (fVar6 <= fVar10) {
          local_80 = fVar8;
        }
      }
    }
    uStack_74 = (undefined4)param_4[1];
    uStack_70 = (undefined4)((ulong)param_4[1] >> 0x20);
    fStack_7c = (float)*param_4;
    fStack_78 = (float)((ulong)*param_4 >> 0x20);
    local_68 = 0;
    FUN_101b0d328(uVar5,param_2[5],param_2[6],&local_80);
  }
  else {
    FUN_101ab7348(&local_80,&DAT_106fba198,0x100500,0x10100,0);
    FUN_101a9c618(CONCAT44(uStack_74,fStack_78),param_1);
    FUN_101a9c534(CONCAT44(uStack_74,fStack_78),param_2[4]);
    FUN_101a9c534(CONCAT44(uStack_74,fStack_78),param_2[5]);
    FUN_101a9c534(CONCAT44(uStack_74,fStack_78),param_2[6]);
    FUN_101a9c57c(param_2[1],CONCAT44(uStack_74,fStack_78));
    FUN_101a9c57c(param_2[2],CONCAT44(uStack_74,fStack_78));
    FUN_101a9c57c(param_2[7],CONCAT44(uStack_74,fStack_78));
    FUN_101a9c504(CONCAT44(uStack_74,fStack_78),(char)param_2[3]);
    FUN_101a9c504(CONCAT44(uStack_74,fStack_78),*(undefined1 *)((long)param_2 + 0xd));
    FUN_101a9c534(CONCAT44(uStack_74,fStack_78),*param_2);
    FUN_101a9c504(CONCAT44(uStack_74,fStack_78),(char)param_2[8]);
    FUN_101a9c57c(*param_3,CONCAT44(uStack_74,fStack_78));
    FUN_101a9c57c(param_3[1],CONCAT44(uStack_74,fStack_78));
    FUN_101a9c534(CONCAT44(uStack_74,fStack_78),param_3[2]);
    FUN_101a9c57c(param_3[3],CONCAT44(uStack_74,fStack_78));
    plVar4 = (long *)FUN_101ac06f4(&local_80,param_4);
    (**(code **)(*plVar4 + 0x10))();
    FUN_101ab786c(&local_80);
  }
  return;
}

