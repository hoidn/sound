
void FUN_101431584(undefined8 param_1,double param_2)

{
  uint uVar1;
  char *pcVar2;
  size_t sVar3;
  short *psVar4;
  short *psVar5;
  ulong uVar7;
  short *psVar8;
  long lVar9;
  undefined8 *puVar10;
  uint uVar11;
  int iVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  undefined8 uVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  undefined8 uVar18;
  undefined8 uVar19;
  undefined8 uVar20;
  short local_430 [16];
  undefined8 auStack_410 [121];
  long local_48;
  short *psVar6;
  
  local_48 = *(long *)PTR____stack_chk_guard_1064f8818;
  if (param_2 != 0.0) {
    _log10(ABS(param_2));
  }
  uVar1 = FUN_1011bfe14(local_430,1000,"%.*lf");
  pcVar2 = _strchr((char *)local_430,0x2e);
  if (pcVar2 != (char *)0x0) {
    pcVar2 = (char *)((long)local_430 + (ulong)uVar1);
    do {
      uVar11 = uVar1;
      pcVar2 = pcVar2 + -1;
      uVar1 = uVar11;
      if ((int)uVar11 < 1) goto LAB_101431648;
      uVar1 = uVar11 - 1;
    } while (*pcVar2 == '0');
    if (*pcVar2 != '.') {
      uVar1 = uVar11;
    }
  }
LAB_101431648:
  *(undefined1 *)((long)local_430 + (long)(int)uVar1) = 0;
  sVar3 = _strlen((char *)local_430);
  FUN_1011cb734(param_1);
  iVar12 = (int)sVar3;
  psVar4 = (short *)FUN_101449848(param_1,iVar12 * 2 + 2);
  if (iVar12 != 0) {
    uVar7 = (ulong)iVar12;
    psVar6 = local_430;
    if ((0x3f < uVar7) &&
       (((short *)((long)local_430 + uVar7) <= psVar4 ||
        ((short *)((long)psVar4 + ((long)(sVar3 << 0x20) >> 0x1f)) <= psVar6)))) {
      lVar9 = uVar7 - (sVar3 & 0x3f);
      psVar6 = (short *)((long)local_430 + lVar9);
      psVar5 = psVar4 + lVar9;
      psVar4 = psVar4 + 0x20;
      puVar10 = auStack_410;
      do {
        uVar14 = puVar10[-3];
        uVar13 = puVar10[-4];
        uVar16 = puVar10[-1];
        uVar15 = puVar10[-2];
        uVar18 = puVar10[1];
        uVar17 = *puVar10;
        uVar20 = puVar10[3];
        uVar19 = puVar10[2];
        *(ulong *)(psVar4 + -0x1c) =
             CONCAT26((short)(char)((ulong)uVar13 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar13 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar13 >> 0x28),
                                        (short)(char)((ulong)uVar13 >> 0x20))));
        *(ulong *)(psVar4 + -0x20) =
             CONCAT26((short)(char)((ulong)uVar13 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar13 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar13 >> 8),(short)(char)uVar13)));
        *(ulong *)(psVar4 + -0x14) =
             CONCAT26((short)(char)((ulong)uVar14 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar14 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar14 >> 0x28),
                                        (short)(char)((ulong)uVar14 >> 0x20))));
        *(ulong *)(psVar4 + -0x18) =
             CONCAT26((short)(char)((ulong)uVar14 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar14 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar14 >> 8),(short)(char)uVar14)));
        *(ulong *)(psVar4 + -0xc) =
             CONCAT26((short)(char)((ulong)uVar15 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar15 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar15 >> 0x28),
                                        (short)(char)((ulong)uVar15 >> 0x20))));
        *(ulong *)(psVar4 + -0x10) =
             CONCAT26((short)(char)((ulong)uVar15 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar15 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar15 >> 8),(short)(char)uVar15)));
        *(ulong *)(psVar4 + -4) =
             CONCAT26((short)(char)((ulong)uVar16 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar16 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar16 >> 0x28),
                                        (short)(char)((ulong)uVar16 >> 0x20))));
        *(ulong *)(psVar4 + -8) =
             CONCAT26((short)(char)((ulong)uVar16 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar16 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar16 >> 8),(short)(char)uVar16)));
        *(ulong *)(psVar4 + 4) =
             CONCAT26((short)(char)((ulong)uVar17 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar17 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar17 >> 0x28),
                                        (short)(char)((ulong)uVar17 >> 0x20))));
        *(ulong *)psVar4 =
             CONCAT26((short)(char)((ulong)uVar17 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar17 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar17 >> 8),(short)(char)uVar17)));
        *(ulong *)(psVar4 + 0xc) =
             CONCAT26((short)(char)((ulong)uVar18 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar18 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar18 >> 0x28),
                                        (short)(char)((ulong)uVar18 >> 0x20))));
        *(ulong *)(psVar4 + 8) =
             CONCAT26((short)(char)((ulong)uVar18 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar18 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar18 >> 8),(short)(char)uVar18)));
        *(ulong *)(psVar4 + 0x14) =
             CONCAT26((short)(char)((ulong)uVar19 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar19 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar19 >> 0x28),
                                        (short)(char)((ulong)uVar19 >> 0x20))));
        *(ulong *)(psVar4 + 0x10) =
             CONCAT26((short)(char)((ulong)uVar19 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar19 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar19 >> 8),(short)(char)uVar19)));
        *(ulong *)(psVar4 + 0x1c) =
             CONCAT26((short)(char)((ulong)uVar20 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar20 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar20 >> 0x28),
                                        (short)(char)((ulong)uVar20 >> 0x20))));
        *(ulong *)(psVar4 + 0x18) =
             CONCAT26((short)(char)((ulong)uVar20 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar20 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar20 >> 8),(short)(char)uVar20)));
        psVar4 = psVar4 + 0x40;
        lVar9 = lVar9 + -0x40;
        puVar10 = puVar10 + 8;
      } while (lVar9 != 0);
      psVar4 = psVar5;
      if ((sVar3 & 0x3f) == 0) goto LAB_101431734;
    }
    do {
      psVar5 = (short *)((long)psVar6 + 1);
      psVar8 = psVar4 + 1;
      *psVar4 = (short)(char)*psVar6;
      psVar6 = psVar5;
      psVar4 = psVar8;
    } while (psVar5 != (short *)((long)local_430 + uVar7));
  }
LAB_101431734:
  *psVar4 = 0;
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

