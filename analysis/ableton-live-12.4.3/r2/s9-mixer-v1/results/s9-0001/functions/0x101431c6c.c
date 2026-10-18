
void FUN_101431c6c(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  size_t sVar1;
  char *pcVar2;
  short *psVar3;
  char *pcVar4;
  short *psVar5;
  ulong uVar7;
  short *psVar8;
  long lVar9;
  undefined8 *puVar10;
  int iVar11;
  undefined8 uVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  undefined8 uVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  undefined8 uVar18;
  undefined8 uVar19;
  char cStack_ad;
  short local_ac [16];
  undefined8 auStack_8c [8];
  long local_48;
  short *psVar6;
  
  local_48 = *(long *)PTR____stack_chk_guard_1064f8818;
  iVar11 = (int)((ulong)param_3 >> 0x20);
  ___exp10((double)iVar11);
  FUN_1011bfe14(local_ac,100,"%*.*f");
  if ((int)param_3 < iVar11) {
    sVar1 = _strlen((char *)local_ac);
    pcVar2 = _strchr((char *)local_ac,0x2e);
    for (pcVar4 = &cStack_ad + sVar1; (pcVar2 + (int)param_3 < pcVar4 && (*pcVar4 == '0'));
        pcVar4 = pcVar4 + -1) {
      *pcVar4 = '\0';
    }
    if (pcVar2[1] == '\0') {
      *pcVar2 = '\0';
    }
  }
  sVar1 = _strlen((char *)local_ac);
  FUN_1011cb734(param_1);
  iVar11 = (int)sVar1;
  psVar3 = (short *)FUN_101449848(param_1,iVar11 * 2 + 2);
  if (iVar11 != 0) {
    uVar7 = (ulong)iVar11;
    psVar6 = local_ac;
    if ((0x3f < uVar7) &&
       (((short *)((long)local_ac + uVar7) <= psVar3 ||
        ((short *)((long)psVar3 + ((long)(sVar1 << 0x20) >> 0x1f)) <= psVar6)))) {
      lVar9 = uVar7 - (sVar1 & 0x3f);
      psVar6 = (short *)((long)local_ac + lVar9);
      psVar5 = psVar3 + lVar9;
      psVar3 = psVar3 + 0x20;
      puVar10 = auStack_8c;
      do {
        uVar13 = puVar10[-3];
        uVar12 = puVar10[-4];
        uVar15 = puVar10[-1];
        uVar14 = puVar10[-2];
        uVar17 = puVar10[1];
        uVar16 = *puVar10;
        uVar19 = puVar10[3];
        uVar18 = puVar10[2];
        *(ulong *)(psVar3 + -0x1c) =
             CONCAT26((short)(char)((ulong)uVar12 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar12 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar12 >> 0x28),
                                        (short)(char)((ulong)uVar12 >> 0x20))));
        *(ulong *)(psVar3 + -0x20) =
             CONCAT26((short)(char)((ulong)uVar12 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar12 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar12 >> 8),(short)(char)uVar12)));
        *(ulong *)(psVar3 + -0x14) =
             CONCAT26((short)(char)((ulong)uVar13 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar13 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar13 >> 0x28),
                                        (short)(char)((ulong)uVar13 >> 0x20))));
        *(ulong *)(psVar3 + -0x18) =
             CONCAT26((short)(char)((ulong)uVar13 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar13 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar13 >> 8),(short)(char)uVar13)));
        *(ulong *)(psVar3 + -0xc) =
             CONCAT26((short)(char)((ulong)uVar14 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar14 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar14 >> 0x28),
                                        (short)(char)((ulong)uVar14 >> 0x20))));
        *(ulong *)(psVar3 + -0x10) =
             CONCAT26((short)(char)((ulong)uVar14 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar14 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar14 >> 8),(short)(char)uVar14)));
        *(ulong *)(psVar3 + -4) =
             CONCAT26((short)(char)((ulong)uVar15 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar15 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar15 >> 0x28),
                                        (short)(char)((ulong)uVar15 >> 0x20))));
        *(ulong *)(psVar3 + -8) =
             CONCAT26((short)(char)((ulong)uVar15 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar15 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar15 >> 8),(short)(char)uVar15)));
        *(ulong *)(psVar3 + 4) =
             CONCAT26((short)(char)((ulong)uVar16 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar16 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar16 >> 0x28),
                                        (short)(char)((ulong)uVar16 >> 0x20))));
        *(ulong *)psVar3 =
             CONCAT26((short)(char)((ulong)uVar16 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar16 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar16 >> 8),(short)(char)uVar16)));
        *(ulong *)(psVar3 + 0xc) =
             CONCAT26((short)(char)((ulong)uVar17 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar17 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar17 >> 0x28),
                                        (short)(char)((ulong)uVar17 >> 0x20))));
        *(ulong *)(psVar3 + 8) =
             CONCAT26((short)(char)((ulong)uVar17 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar17 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar17 >> 8),(short)(char)uVar17)));
        *(ulong *)(psVar3 + 0x14) =
             CONCAT26((short)(char)((ulong)uVar18 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar18 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar18 >> 0x28),
                                        (short)(char)((ulong)uVar18 >> 0x20))));
        *(ulong *)(psVar3 + 0x10) =
             CONCAT26((short)(char)((ulong)uVar18 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar18 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar18 >> 8),(short)(char)uVar18)));
        *(ulong *)(psVar3 + 0x1c) =
             CONCAT26((short)(char)((ulong)uVar19 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar19 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar19 >> 0x28),
                                        (short)(char)((ulong)uVar19 >> 0x20))));
        *(ulong *)(psVar3 + 0x18) =
             CONCAT26((short)(char)((ulong)uVar19 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar19 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar19 >> 8),(short)(char)uVar19)));
        psVar3 = psVar3 + 0x40;
        lVar9 = lVar9 + -0x40;
        puVar10 = puVar10 + 8;
      } while (lVar9 != 0);
      psVar3 = psVar5;
      if ((sVar1 & 0x3f) == 0) goto LAB_101431e20;
    }
    do {
      psVar5 = (short *)((long)psVar6 + 1);
      psVar8 = psVar3 + 1;
      *psVar3 = (short)(char)*psVar6;
      psVar6 = psVar5;
      psVar3 = psVar8;
    } while (psVar5 != (short *)((long)local_ac + uVar7));
  }
LAB_101431e20:
  *psVar3 = 0;
  if (*(long *)PTR____stack_chk_guard_1064f8818 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}

