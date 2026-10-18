
void FUN_1030cb434(long param_1,long param_2,int param_3)

{
  uint uVar1;
  byte bVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  byte bVar6;
  byte bVar7;
  byte bVar8;
  byte bVar9;
  byte bVar10;
  byte bVar11;
  byte bVar12;
  byte bVar13;
  byte bVar14;
  byte bVar15;
  byte bVar16;
  byte bVar17;
  byte bVar18;
  byte bVar19;
  void *pvVar20;
  undefined8 *puVar21;
  long lVar22;
  undefined8 local_70;
  uint local_68;
  char local_64;
  
  if (param_3 == 0) {
    puVar21 = *(undefined8 **)(param_2 + 8);
    if (puVar21 < *(undefined8 **)(param_2 + 0x10)) {
      *puVar21 = *(undefined8 *)(param_1 + 0x48);
      puVar21[1] = 0;
      puVar21[2] = 0x8000000000000000;
      puVar21[3] = 0x7f7fffff7f7fffff;
      *(undefined1 *)(puVar21 + 4) = 0;
      puVar21[5] = 0;
      *(undefined4 *)(puVar21 + 6) = 0;
      *(undefined1 *)((long)puVar21 + 0x34) = 0;
      puVar21 = puVar21 + 7;
    }
    else {
      puVar21 = (undefined8 *)FUN_1030ed054(param_2,param_1 + 0x40);
    }
    *(undefined8 **)(param_2 + 8) = puVar21;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar21) goto LAB_1030cb8bc;
  }
  else {
    local_70 = (undefined4 *)0x0;
    local_68 = 0;
    local_64 = '\0';
    bVar2 = (&DAT_1068c5398)[param_3];
    bVar3 = (&DAT_1068c53c0)[param_3];
    bVar4 = (&DAT_1068c53e8)[param_3];
    bVar5 = (&DAT_1068c5410)[param_3];
    bVar6 = (&DAT_1068c5438)[param_3];
    bVar7 = (&DAT_1068c5460)[param_3];
    bVar8 = (&DAT_1068c5488)[param_3];
    bVar9 = (&DAT_1068c54b0)[param_3];
    bVar10 = (&DAT_1068c54d8)[param_3];
    bVar11 = (&DAT_1068c5500)[param_3];
    bVar12 = (&DAT_1068c5528)[param_3];
    bVar13 = (&DAT_1068c5550)[param_3];
    bVar14 = (&DAT_1068c5578)[param_3];
    bVar15 = (&DAT_1068c55a0)[param_3];
    bVar16 = (&DAT_1068c55c8)[param_3];
    bVar17 = (&DAT_1068c55f0)[param_3];
    bVar18 = (&DAT_1068c5618)[param_3];
    bVar19 = (&DAT_1068c5640)[param_3];
    uVar1 = (bVar8 ^ 1) +
            (uint)(byte)((bVar3 ^ 1) + (bVar2 ^ 1) + (bVar4 ^ 1) + (bVar5 ^ 1) +
                        (bVar6 ^ 1) + (bVar7 ^ 1)) +
            (bVar9 ^ 1) + (bVar10 ^ 1) + (bVar11 ^ 1) + (bVar12 ^ 1) + (bVar13 ^ 1) + (bVar14 ^ 1) +
            (bVar15 ^ 1) + (bVar16 ^ 1) + (bVar17 ^ 1) + (bVar18 ^ 1) + (bVar19 ^ 1);
    if (uVar1 == 0) {
      if ((bVar2 & 1) == 0) goto LAB_1030cb618;
LAB_1030cb5c4:
      lVar22 = 0;
      uVar1 = local_68;
    }
    else {
      local_70 = operator_new__((ulong)uVar1 << 2);
      local_64 = '\x01';
      local_68 = uVar1;
      if ((bVar2 & 1) != 0) goto LAB_1030cb5c4;
LAB_1030cb618:
      *local_70 = 0;
      lVar22 = 1;
      uVar1 = local_68;
    }
    if ((bVar3 & 1) == 0) {
      local_70[lVar22] = 1;
      lVar22 = lVar22 + 1;
    }
    local_68 = uVar1;
    if ((bVar4 & 1) == 0) {
      local_70[lVar22] = 2;
      lVar22 = lVar22 + 1;
      if ((bVar5 & 1) == 0) goto LAB_1030cb718;
LAB_1030cb638:
      if ((bVar6 & 1) != 0) goto LAB_1030cb63c;
LAB_1030cb728:
      local_70[lVar22] = 4;
      lVar22 = lVar22 + 1;
      if ((bVar7 & 1) == 0) goto LAB_1030cb738;
LAB_1030cb640:
      if ((bVar8 & 1) != 0) goto LAB_1030cb644;
LAB_1030cb748:
      local_70[lVar22] = 6;
      lVar22 = lVar22 + 1;
      if ((bVar9 & 1) == 0) goto LAB_1030cb758;
LAB_1030cb648:
      if ((bVar10 & 1) != 0) goto LAB_1030cb650;
LAB_1030cb76c:
      local_70[lVar22] = 8;
      lVar22 = lVar22 + 1;
      if ((bVar11 & 1) == 0) goto LAB_1030cb77c;
LAB_1030cb654:
      if ((bVar12 & 1) != 0) goto LAB_1030cb658;
LAB_1030cb78c:
      local_70[lVar22] = 10;
      lVar22 = lVar22 + 1;
      if ((bVar13 & 1) == 0) goto LAB_1030cb79c;
LAB_1030cb65c:
      if ((bVar14 & 1) != 0) goto LAB_1030cb660;
LAB_1030cb7ac:
      local_70[lVar22] = 0xc;
      lVar22 = lVar22 + 1;
      if ((bVar15 & 1) == 0) goto LAB_1030cb7bc;
LAB_1030cb664:
      if ((bVar16 & 1) != 0) goto LAB_1030cb668;
LAB_1030cb7cc:
      local_70[lVar22] = 0xe;
      lVar22 = lVar22 + 1;
      if ((bVar17 & 1) == 0) goto LAB_1030cb7dc;
LAB_1030cb66c:
      if ((bVar18 & 1) != 0) goto LAB_1030cb670;
LAB_1030cb7ec:
      local_70[lVar22] = 0x10;
      lVar22 = lVar22 + 1;
      if ((bVar19 & 1) == 0) goto LAB_1030cb7fc;
LAB_1030cb674:
      puVar21 = *(undefined8 **)(param_2 + 8);
      if (puVar21 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030cb680;
LAB_1030cb810:
      puVar21 = (undefined8 *)FUN_1030ed468(param_2,param_1 + 0x40,&local_70);
      *(undefined8 **)(param_2 + 8) = puVar21;
    }
    else {
      if ((bVar5 & 1) != 0) goto LAB_1030cb638;
LAB_1030cb718:
      local_70[lVar22] = 3;
      lVar22 = lVar22 + 1;
      if ((bVar6 & 1) == 0) goto LAB_1030cb728;
LAB_1030cb63c:
      if ((bVar7 & 1) != 0) goto LAB_1030cb640;
LAB_1030cb738:
      local_70[lVar22] = 5;
      lVar22 = lVar22 + 1;
      if ((bVar8 & 1) == 0) goto LAB_1030cb748;
LAB_1030cb644:
      if ((bVar9 & 1) != 0) goto LAB_1030cb648;
LAB_1030cb758:
      local_70[lVar22] = 7;
      lVar22 = lVar22 + 1;
      if ((bVar10 & 1) == 0) goto LAB_1030cb76c;
LAB_1030cb650:
      if ((bVar11 & 1) != 0) goto LAB_1030cb654;
LAB_1030cb77c:
      local_70[lVar22] = 9;
      lVar22 = lVar22 + 1;
      if ((bVar12 & 1) == 0) goto LAB_1030cb78c;
LAB_1030cb658:
      if ((bVar13 & 1) != 0) goto LAB_1030cb65c;
LAB_1030cb79c:
      local_70[lVar22] = 0xb;
      lVar22 = lVar22 + 1;
      if ((bVar14 & 1) == 0) goto LAB_1030cb7ac;
LAB_1030cb660:
      if ((bVar15 & 1) != 0) goto LAB_1030cb664;
LAB_1030cb7bc:
      local_70[lVar22] = 0xd;
      lVar22 = lVar22 + 1;
      if ((bVar16 & 1) == 0) goto LAB_1030cb7cc;
LAB_1030cb668:
      if ((bVar17 & 1) != 0) goto LAB_1030cb66c;
LAB_1030cb7dc:
      local_70[lVar22] = 0xf;
      lVar22 = lVar22 + 1;
      if ((bVar18 & 1) == 0) goto LAB_1030cb7ec;
LAB_1030cb670:
      if ((bVar19 & 1) != 0) goto LAB_1030cb674;
LAB_1030cb7fc:
      local_70[lVar22] = 0x11;
      puVar21 = *(undefined8 **)(param_2 + 8);
      if (*(undefined8 **)(param_2 + 0x10) <= puVar21) goto LAB_1030cb810;
LAB_1030cb680:
      *puVar21 = *(undefined8 *)(param_1 + 0x48);
      puVar21[1] = 0;
      puVar21[2] = DAT_1055d1ed0;
      puVar21[3] = 0x7f7fffff7f7fffff;
      *(undefined1 *)(puVar21 + 4) = 0;
      puVar21[5] = 0;
      *(undefined4 *)(puVar21 + 6) = 0;
      *(undefined1 *)((long)puVar21 + 0x34) = 0;
      if (uVar1 != 0) {
        pvVar20 = operator_new__((ulong)uVar1 << 2);
        lVar22 = 0;
        puVar21[5] = pvVar20;
        *(uint *)(puVar21 + 6) = uVar1;
        *(undefined1 *)((long)puVar21 + 0x34) = 1;
        do {
          *(undefined4 *)((long)pvVar20 + lVar22 * 4) = local_70[lVar22];
          lVar22 = lVar22 + 1;
        } while (lVar22 < *(int *)(puVar21 + 6));
      }
      puVar21 = puVar21 + 7;
      *(undefined8 **)(param_2 + 8) = puVar21;
      *(undefined8 **)(param_2 + 8) = puVar21;
    }
    if ((local_70 != (undefined4 *)0x0) && (local_64 == '\x01')) {
      FUN_101a24778(local_70,(long)(int)local_68 << 2);
      puVar21 = *(undefined8 **)(param_2 + 8);
    }
    if (*(undefined8 **)(param_2 + 0x10) <= puVar21) {
LAB_1030cb8bc:
      local_70 = (undefined4 *)CONCAT44(local_70._4_4_,8);
      puVar21 = (undefined8 *)FUN_1030ed63c(param_2,param_1 + 0x58,&local_70);
      goto LAB_1030cb8cc;
    }
  }
  *puVar21 = *(undefined8 *)(param_1 + 0x60);
  puVar21[1] = 0;
  puVar21[2] = DAT_10584d6d0;
  puVar21[3] = 0x7f7fffff7f7fffff;
  *(undefined1 *)(puVar21 + 4) = 0;
  puVar21[5] = 0;
  *(undefined4 *)(puVar21 + 6) = 0;
  *(undefined1 *)((long)puVar21 + 0x34) = 0;
  puVar21 = puVar21 + 7;
LAB_1030cb8cc:
  *(undefined8 **)(param_2 + 8) = puVar21;
  return;
}

