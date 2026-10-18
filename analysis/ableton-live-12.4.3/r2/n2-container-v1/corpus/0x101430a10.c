
void FUN_101430a10(undefined8 param_1)

{
  uint uVar1;
  short *psVar2;
  short *psVar3;
  short *psVar5;
  ulong uVar6;
  ulong uVar7;
  undefined8 *puVar8;
  ulong uVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  undefined8 uVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  undefined8 uVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  short local_808 [16];
  undefined8 auStack_7e8 [246];
  long local_38;
  short *psVar4;
  
  local_38 = *(long *)PTR____stack_chk_guard_1064f8818;
  uVar1 = FUN_1011bfe14(local_808,2000,"%d");
  FUN_1011cb734(param_1);
  psVar2 = (short *)FUN_101449848(param_1,uVar1 * 2 + 2);
  if (uVar1 != 0) {
    uVar6 = (ulong)(int)uVar1;
    psVar4 = local_808;
    if ((0x3f < uVar1) &&
       (((short *)((long)local_808 + uVar6) <= psVar2 || (psVar2 + uVar6 <= psVar4)))) {
      uVar7 = uVar6 & 0xffffffffffffffc0;
      psVar3 = psVar2 + uVar7;
      psVar4 = (short *)((long)local_808 + uVar7);
      psVar2 = psVar2 + 0x20;
      puVar8 = auStack_7e8;
      uVar9 = uVar7;
      do {
        uVar11 = puVar8[-3];
        uVar10 = puVar8[-4];
        uVar13 = puVar8[-1];
        uVar12 = puVar8[-2];
        uVar15 = puVar8[1];
        uVar14 = *puVar8;
        uVar17 = puVar8[3];
        uVar16 = puVar8[2];
        *(ulong *)(psVar2 + -0x1c) =
             CONCAT26((short)(char)((ulong)uVar10 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar10 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar10 >> 0x28),
                                        (short)(char)((ulong)uVar10 >> 0x20))));
        *(ulong *)(psVar2 + -0x20) =
             CONCAT26((short)(char)((ulong)uVar10 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar10 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar10 >> 8),(short)(char)uVar10)));
        *(ulong *)(psVar2 + -0x14) =
             CONCAT26((short)(char)((ulong)uVar11 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar11 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar11 >> 0x28),
                                        (short)(char)((ulong)uVar11 >> 0x20))));
        *(ulong *)(psVar2 + -0x18) =
             CONCAT26((short)(char)((ulong)uVar11 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar11 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar11 >> 8),(short)(char)uVar11)));
        *(ulong *)(psVar2 + -0xc) =
             CONCAT26((short)(char)((ulong)uVar12 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar12 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar12 >> 0x28),
                                        (short)(char)((ulong)uVar12 >> 0x20))));
        *(ulong *)(psVar2 + -0x10) =
             CONCAT26((short)(char)((ulong)uVar12 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar12 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar12 >> 8),(short)(char)uVar12)));
        *(ulong *)(psVar2 + -4) =
             CONCAT26((short)(char)((ulong)uVar13 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar13 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar13 >> 0x28),
                                        (short)(char)((ulong)uVar13 >> 0x20))));
        *(ulong *)(psVar2 + -8) =
             CONCAT26((short)(char)((ulong)uVar13 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar13 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar13 >> 8),(short)(char)uVar13)));
        *(ulong *)(psVar2 + 4) =
             CONCAT26((short)(char)((ulong)uVar14 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar14 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar14 >> 0x28),
                                        (short)(char)((ulong)uVar14 >> 0x20))));
        *(ulong *)psVar2 =
             CONCAT26((short)(char)((ulong)uVar14 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar14 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar14 >> 8),(short)(char)uVar14)));
        *(ulong *)(psVar2 + 0xc) =
             CONCAT26((short)(char)((ulong)uVar15 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar15 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar15 >> 0x28),
                                        (short)(char)((ulong)uVar15 >> 0x20))));
        *(ulong *)(psVar2 + 8) =
             CONCAT26((short)(char)((ulong)uVar15 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar15 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar15 >> 8),(short)(char)uVar15)));
        *(ulong *)(psVar2 + 0x14) =
             CONCAT26((short)(char)((ulong)uVar16 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar16 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar16 >> 0x28),
                                        (short)(char)((ulong)uVar16 >> 0x20))));
        *(ulong *)(psVar2 + 0x10) =
             CONCAT26((short)(char)((ulong)uVar16 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar16 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar16 >> 8),(short)(char)uVar16)));
        *(ulong *)(psVar2 + 0x1c) =
             CONCAT26((short)(char)((ulong)uVar17 >> 0x38),
                      CONCAT24((short)(char)((ulong)uVar17 >> 0x30),
                               CONCAT22((short)(char)((ulong)uVar17 >> 0x28),
                                        (short)(char)((ulong)uVar17 >> 0x20))));
        *(ulong *)(psVar2 + 0x18) =
             CONCAT26((short)(char)((ulong)uVar17 >> 0x18),
                      CONCAT24((short)(char)((ulong)uVar17 >> 0x10),
                               CONCAT22((short)(char)((ulong)uVar17 >> 8),(short)(char)uVar17)));
        psVar2 = psVar2 + 0x40;
        uVar9 = uVar9 - 0x40;
        puVar8 = puVar8 + 8;
      } while (uVar9 != 0);
      psVar2 = psVar3;
      if (uVar7 == uVar6) goto LAB_101430b30;
    }
    do {
      psVar3 = (short *)((long)psVar4 + 1);
      psVar5 = psVar2 + 1;
      *psVar2 = (short)(char)*psVar4;
      psVar4 = psVar3;
      psVar2 = psVar5;
    } while (psVar3 != (short *)((long)local_808 + uVar6));
  }
LAB_101430b30:
  *psVar2 = 0;
  if (*(long *)PTR____stack_chk_guard_1064f8818 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}

