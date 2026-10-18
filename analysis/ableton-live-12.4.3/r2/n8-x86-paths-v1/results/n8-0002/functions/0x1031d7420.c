
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_1031d7420(undefined8 param_1,float *param_2)

{
  ulong uVar1;
  double dVar2;
  double dVar3;
  undefined8 uVar4;
  void *pvVar5;
  void *pvVar6;
  undefined8 *puVar7;
  long lVar8;
  ulong uVar9;
  undefined8 *puVar10;
  size_t sVar11;
  long lVar12;
  undefined4 extraout_XMM0_Dc;
  undefined4 extraout_XMM0_Dd;
  undefined1 auVar13 [16];
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  double local_70;
  void *local_68;
  undefined4 uStack_60;
  undefined4 uStack_5c;
  float *local_50;
  void *local_48;
  undefined8 *puStack_40;
  undefined8 *local_38;
  
  local_48 = (void *)0x0;
  puStack_40 = (undefined8 *)0x0;
  local_38 = (undefined8 *)0x0;
  local_78 = param_1;
  if (0 < (int)param_2[6]) {
    lVar12 = 0;
    local_50 = param_2;
    do {
      FUN_103172c00(SUB84((double)*(float *)(*(long *)(local_50 + 4) + lVar12 * 8),0),
                    SUB84((double)(*(float *)(*(long *)(local_50 + 4) + 4 + lVar12 * 8) -
                                  local_50[2]),0),&local_88);
      if (puStack_40 < local_38) {
        *puStack_40 = local_88;
        puStack_40[1] = uStack_80;
        puVar7 = puStack_40 + 2;
      }
      else {
        sVar11 = (long)puStack_40 - (long)local_48;
        lVar8 = (long)sVar11 >> 4;
        uVar1 = lVar8 + 1;
        if (0xfffffffffffffff < uVar1) {
                    /* WARNING: Subroutine does not return */
          FUN_10317e620(&local_48);
        }
        uVar9 = (long)local_38 - (long)local_48 >> 3;
        if (uVar9 <= uVar1) {
          uVar9 = uVar1;
        }
        if (0x7fffffffffffffef < (ulong)((long)local_38 - (long)local_48)) {
          uVar9 = 0xfffffffffffffff;
        }
        local_68 = local_48;
        if (uVar9 == 0) {
          pvVar6 = (void *)0x0;
        }
        else {
          if (0xfffffffffffffff < uVar9) {
                    /* WARNING: Subroutine does not return */
            FUN_1002c4a90();
          }
          pvVar6 = operator_new(uVar9 << 4);
        }
        pvVar5 = local_68;
        lVar8 = lVar8 * 0x10;
        puVar10 = (undefined8 *)(uVar9 * 0x10 + (long)pvVar6);
        puVar7 = (undefined8 *)((long)pvVar6 + lVar8);
        *puVar7 = local_88;
        puVar7[1] = uStack_80;
        puVar7 = (undefined8 *)((long)pvVar6 + lVar8 + 0x10);
        _memcpy(pvVar6,local_68,sVar11);
        local_48 = pvVar6;
        local_38 = puVar10;
        if (pvVar5 != (void *)0x0) {
          puStack_40 = puVar7;
          operator_delete(pvVar5);
        }
      }
      lVar12 = lVar12 + 1;
      param_2 = local_50;
      puStack_40 = puVar7;
    } while (lVar12 < (int)local_50[6]);
  }
  local_68 = (void *)FUN_103173c30(SUB84((double)param_2[2],0));
  local_70 = (double)param_2[7];
  dVar3 = (double)local_68 / DAT_105bcba70;
  uStack_60 = extraout_XMM0_Dc;
  uStack_5c = extraout_XMM0_Dd;
  dVar2 = (double)_fma(SUB84(dVar3,0) ^ _DAT_105a57810,(int)DAT_105a57808,DAT_105a57808);
  dVar2 = (dVar2 + dVar3) * local_70;
  dVar2 = (double)_fma(SUB84(dVar2,0),SUB84(DAT_105bcba70,0),DAT_105a577f0 - dVar2);
  uVar4 = local_78;
  auVar13._8_8_ = _UNK_105a57818 & CONCAT44(uStack_5c,uStack_60) | _UNK_105b500f8;
  auVar13._0_8_ =
       (double)(CONCAT44(_UNK_105a57814,_DAT_105a57810) & (ulong)local_68 | _DAT_105b500f0) +
       (double)local_68;
  auVar13 = roundsd(auVar13,auVar13,0xb);
  FUN_103172b40(SUB84((double)*param_2,0),SUB84((double)param_2[1],0),(float)dVar2,
                (double)param_2[2],local_78,(int)auVar13._0_8_,0,&local_48);
  if (local_48 != (void *)0x0) {
    puStack_40 = local_48;
    operator_delete(local_48);
  }
  return uVar4;
}

