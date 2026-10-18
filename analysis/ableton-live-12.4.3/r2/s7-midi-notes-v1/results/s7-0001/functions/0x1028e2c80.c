
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1028e2c80(long param_1)

{
  bool bVar1;
  float fVar2;
  float fVar3;
  double dVar4;
  ulong uVar5;
  float fVar6;
  int iVar7;
  int iVar8;
  
  dVar4 = *(double *)(param_1 + 0x38);
  bVar1 = true;
  if ((0.0 <= dVar4) && (bVar1 = false, !NAN(dVar4))) {
    bVar1 = dVar4 == 1.79769313486232e+308;
  }
  if (bVar1) {
    *(undefined8 *)(param_1 + 0x38) = 0;
  }
  fVar2 = *(float *)(param_1 + 0x40);
  fVar6 = 127.0;
  if (fVar2 <= 127.0) {
    fVar6 = fVar2;
  }
  fVar3 = 1.0;
  if (1.0 <= fVar2) {
    fVar3 = fVar6;
  }
  *(float *)(param_1 + 0x40) = fVar3;
  uVar5 = *(ulong *)(param_1 + 0x48);
  iVar7 = -(uint)((float)uVar5 < 0.0);
  fVar6 = (float)(uVar5 >> 0x20);
  iVar8 = -(uint)(fVar6 < 0.0);
  uVar5 = uVar5 ^ (uVar5 ^ _DAT_105896fa8) &
                  CONCAT44(-(uint)((float)(_DAT_105896fa8 >> 0x20) < fVar6),
                           -(uint)((float)_DAT_105896fa8 < (float)uVar5));
  *(ulong *)(param_1 + 0x48) =
       CONCAT17((byte)(uVar5 >> 0x38) & ~(byte)((uint)iVar8 >> 0x18),
                CONCAT16((byte)(uVar5 >> 0x30) & ~(byte)((uint)iVar8 >> 0x10),
                         CONCAT15((byte)(uVar5 >> 0x28) & ~(byte)((uint)iVar8 >> 8),
                                  CONCAT14((byte)(uVar5 >> 0x20) & ~(byte)iVar8,
                                           CONCAT13((byte)(uVar5 >> 0x18) &
                                                    ~(byte)((uint)iVar7 >> 0x18),
                                                    CONCAT12((byte)(uVar5 >> 0x10) &
                                                             ~(byte)((uint)iVar7 >> 0x10),
                                                             CONCAT11((byte)(uVar5 >> 8) &
                                                                      ~(byte)((uint)iVar7 >> 8),
                                                                      (byte)uVar5 & ~(byte)iVar7))))
                                 )));
  return;
}

