// x86 0x1031d7120 FUN_1031d7120 state=exported-with-warnings chunk=chunk-02323.jsonl code_sha256=87dd8edd2da8edf8bb79680cd6004e1db189f09cd25f02349d1fa64e896630cf

undefined8 * FUN_1031d7120(undefined8 *param_1,long param_2)

{
  int *piVar1;
  undefined8 *puVar2;
  int iVar3;
  long *plVar4;
  undefined8 *puVar5;
  void *pvVar6;
  undefined8 uVar7;
  long lVar8;
  undefined8 *puVar9;
  long lVar10;
  ulong uVar11;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined4 local_88;
  undefined4 uStack_84;
  undefined4 uStack_80;
  undefined4 uStack_7c;
  ushort local_78;
  void *local_70;
  void *local_68;
  undefined8 *local_58;
  long local_50;
  void *local_48;
  undefined8 *local_40;
  undefined8 *local_38;
  
  local_38 = param_1;
  plVar4 = (long *)(**(code **)(**(long **)(param_2 + 0x28) + 0x58))
                             (*(long **)(param_2 + 0x28),*(undefined8 *)(param_2 + 0x20));
  puVar5 = (undefined8 *)FUN_1012bdaa0(0x28);
  lVar8 = *(long *)(param_2 + 0x28);
  local_50 = param_2;
  FUN_1012715b0(puVar5);
  *puVar5 = &PTR_FUN_106e01d58;
  puVar5[3] = plVar4;
  puVar5[4] = lVar8;
  if (lVar8 != 0) {
    *(int *)(lVar8 + 8) = *(int *)(lVar8 + 8) + 1;
  }
  *(int *)(puVar5 + 1) = *(int *)(puVar5 + 1) + 1;
  *local_38 = 0;
  local_38[1] = 0;
  local_38[2] = 0;
  lVar8 = 0;
  lVar10 = 0;
  puVar9 = local_38;
  local_58 = puVar5;
  local_40 = puVar5;
  while( true ) {
    iVar3 = 0;
    if (plVar4 != (long *)0x0) {
      iVar3 = (int)plVar4[1];
    }
    if (iVar3 <= lVar10) break;
    FUN_1031d7420(&local_98,*plVar4 + lVar8);
    if (*(int *)(local_50 + 0x30) == 1) {
      local_78 = local_78 & 0xff00;
    }
    puVar2 = (undefined8 *)puVar9[1];
    if (puVar2 < (undefined8 *)puVar9[2]) {
      *(ushort *)(puVar2 + 4) = local_78;
      *(undefined4 *)(puVar2 + 2) = local_88;
      *(undefined4 *)((long)puVar2 + 0x14) = uStack_84;
      *(undefined4 *)(puVar2 + 3) = uStack_80;
      *(undefined4 *)((long)puVar2 + 0x1c) = uStack_7c;
      *puVar2 = local_98;
      puVar2[1] = uStack_90;
      puVar2[5] = 0;
      puVar2[6] = 0;
      puVar2[7] = 0;
      local_48 = local_70;
      uVar11 = (long)local_68 - (long)local_70;
      if (uVar11 != 0) {
        if ((long)uVar11 < 0) {
                    /* WARNING: Subroutine does not return */
          FUN_10317e620(puVar2 + 5);
        }
        pvVar6 = operator_new(uVar11);
        puVar2[5] = pvVar6;
        puVar2[6] = pvVar6;
        puVar2[7] = (long)pvVar6 + uVar11;
        _memcpy(pvVar6,local_48,uVar11);
        puVar2[6] = (long)pvVar6 + uVar11;
        puVar9 = local_38;
      }
      puVar9[1] = puVar2 + 8;
      puVar5 = local_40;
    }
    else {
      uVar7 = FUN_1031c19f0(puVar9,&local_98);
      puVar9[1] = uVar7;
    }
    if (local_70 != (void *)0x0) {
      local_68 = local_70;
      operator_delete(local_70);
    }
    lVar10 = lVar10 + 1;
    plVar4 = (long *)puVar5[3];
    lVar8 = lVar8 + 0x20;
  }
  piVar1 = (int *)(puVar5 + 1);
  *piVar1 = *piVar1 + -1;
  if (*piVar1 == 0) {
    FUN_1012716c0(puVar5);
  }
  return puVar9;
}

