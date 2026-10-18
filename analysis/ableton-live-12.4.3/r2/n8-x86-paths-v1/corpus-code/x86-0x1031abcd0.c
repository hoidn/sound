// x86 0x1031abcd0 FUN_1031abcd0 state=exported chunk=chunk-02319.jsonl code_sha256=bf4d066ecf3a146175b3e2d8c8dbd421440cf3945d3f69fd1bad0b0ba47bb6fa

undefined8 * FUN_1031abcd0(undefined8 *param_1,long param_2)

{
  double dVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  int iVar4;
  ulong uVar5;
  long lVar6;
  float fVar7;
  float fVar8;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined2 local_88;
  void *local_80;
  void *pvStack_78;
  undefined8 local_70;
  void *local_68;
  void *pvStack_60;
  undefined8 local_58;
  void *local_48;
  void *pvStack_40;
  undefined8 local_38;
  
  local_48 = (void *)0x0;
  pvStack_40 = (void *)0x0;
  local_38 = 0;
  std::mutex::lock();
  if (&local_48 != (void **)(param_2 + 0x108)) {
    FUN_1031ac340(&local_48,*(long *)(param_2 + 0x108),*(long *)(param_2 + 0x110),
                  (*(long *)(param_2 + 0x110) - *(long *)(param_2 + 0x108) >> 4) *
                  -0x5555555555555555);
  }
  std::mutex::unlock();
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  local_68 = (void *)0x0;
  pvStack_60 = (void *)0x0;
  local_58 = 0;
  if (pvStack_40 != local_48) {
    lVar6 = 0x28;
    uVar5 = 0;
    do {
      iVar4 = (int)*(double *)((long)local_48 + lVar6 + -8);
      if (0x7e < iVar4) {
        iVar4 = 0x7f;
      }
      if (iVar4 < 1) {
        iVar4 = 0;
      }
      fVar8 = (float)(*(double *)((long)local_48 + lVar6 + -0x20) * DAT_105bcba70);
      fVar7 = DAT_105b8419c;
      if (fVar8 <= DAT_105b8419c) {
        fVar7 = fVar8;
      }
      dVar1 = *(double *)((long)local_48 + lVar6 + -0x28);
      FUN_103172b40(SUB84(dVar1,0),SUB84(*(double *)((long)local_48 + lVar6 + -0x18) + dVar1,0),
                    -(uint)(fVar8 < DAT_105a781c0) & (uint)DAT_105a781c0 |
                    ~-(uint)(fVar8 < DAT_105a781c0) & (uint)fVar7,DAT_105ddb7a8,&local_a8,iVar4,
                    *(undefined1 *)((long)local_48 + lVar6),&local_68);
      puVar2 = (undefined8 *)param_1[1];
      if (puVar2 < (undefined8 *)param_1[2]) {
        *(undefined2 *)(puVar2 + 4) = local_88;
        puVar2[2] = local_98;
        puVar2[3] = uStack_90;
        *puVar2 = local_a8;
        puVar2[1] = uStack_a0;
        puVar2[5] = 0;
        puVar2[6] = 0;
        puVar2[7] = 0;
        puVar2[5] = local_80;
        puVar2[6] = pvStack_78;
        puVar2[7] = local_70;
        param_1[1] = puVar2 + 8;
      }
      else {
        uVar3 = FUN_1031ac4a0(param_1,&local_a8);
        param_1[1] = uVar3;
        if (local_80 != (void *)0x0) {
          pvStack_78 = local_80;
          operator_delete(local_80);
        }
      }
      uVar5 = uVar5 + 1;
      lVar6 = lVar6 + 0x30;
    } while (uVar5 < (ulong)(((long)pvStack_40 - (long)local_48 >> 4) * -0x5555555555555555));
    if (local_68 != (void *)0x0) {
      pvStack_60 = local_68;
      operator_delete(local_68);
    }
  }
  if (local_48 != (void *)0x0) {
    pvStack_40 = local_48;
    operator_delete(local_48);
  }
  return param_1;
}

