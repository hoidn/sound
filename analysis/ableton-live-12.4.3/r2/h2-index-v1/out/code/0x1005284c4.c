// 0x1005284c4 FUN_1005284c4 state=exported body_bytes=496 warnings=0 chunk=chunk-00204.jsonl

long FUN_1005284c4(long param_1,long param_2,undefined8 param_3)

{
  ulong uVar1;
  uint uVar2;
  uint uVar3;
  int iVar4;
  undefined8 *puVar5;
  long lVar6;
  long lVar7;
  long *plVar8;
  undefined1 auStack_58 [8];
  
  puVar5 = (undefined8 *)FUN_1002abda0();
  *puVar5 = &PTR_thunk_FUN_100539314_100da6c58;
  FUN_10022be94(puVar5 + 3);
  *(long *)(param_1 + 0x28) = 0;
  plVar8 = (long *)(param_1 + 0x30);
  *plVar8 = 0;
  uVar2 = FUN_100716cfc(param_2);
  uVar1 = *(ulong *)(param_2 + 8);
  if (-1 < (char)*(byte *)(param_2 + 0x17)) {
    uVar1 = (ulong)*(byte *)(param_2 + 0x17);
  }
  if (uVar1 != 0) {
    (**(code **)(**(long **)(param_1 + 0x20) + 0x30))(*(long **)(param_1 + 0x20),param_2);
    (**(code **)(**(long **)(param_1 + 0x20) + 8))(*(long **)(param_1 + 0x20),3);
    (**(code **)(**(long **)(param_1 + 0x20) + 0x40))(*(long **)(param_1 + 0x20),param_3);
    (**(code **)(**(long **)(param_1 + 0x20) + 0x50))();
  }
  uVar3 = (**(code **)(**(long **)(param_1 + 0x20) + 0x60))();
  if ((((uint)param_3 | uVar3 ^ 0xffffffff | uVar2) & 1) == 0) {
    (**(code **)(**(long **)(param_1 + 0x20) + 0xc0))
              (*(long **)(param_1 + 0x20),
               "CREATE TABLE sample_mapping (                                                     src_type   INT NOT NULL,                                                        src_packid VARCHAR NOT NULL,                                                    src_ref    VARCHAR NOT NULL,                                                    dst_type   INT NOT NULL,                                                        dst_packid VARCHAR NOT NULL,                                                    dst_ref    VARCHAR NOT NULL                                                   );                                                                              CREATE UNIQUE INDEX sample_mapping_KEY                                            ON SAMPLE_MAPPING (src_type, src_packid, src_ref);                            CREATE TABLE pack_names (                                                         packid     VARCHAR PRIMARY KEY,                                                 packname   VARCHAR NOT NULL                                                   );                                                                              "
              );
  }
  iVar4 = (**(code **)(**(long **)(param_1 + 0x20) + 0x60))();
  if (iVar4 != 0) {
    (**(code **)(**(long **)(param_1 + 0x20) + 0xd0))
              (auStack_58,*(long **)(param_1 + 0x20),
               "SELECT dst_type, dst_packid, dst_ref                                              FROM sample_mapping                                                            WHERE src_type=:src_type                                                          AND src_packid=:src_packid                                                      AND src_ref=:src_ref                                                         "
              );
    lVar6 = FUN_100231760(auStack_58);
    if (lVar6 != 0) {
      *(int *)(lVar6 + 8) = *(int *)(lVar6 + 8) + 1;
    }
    lVar7 = *(long *)(param_1 + 0x28);
    if (lVar7 != 0) {
      iVar4 = *(int *)(lVar7 + 8) + -1;
      *(int *)(lVar7 + 8) = iVar4;
      if (iVar4 == 0) {
        FUN_1002abea8();
      }
    }
    *(long *)(param_1 + 0x28) = lVar6;
    FUN_10022d2b4(auStack_58);
    (**(code **)(**(long **)(param_1 + 0x20) + 0xd0))
              (auStack_58,*(long **)(param_1 + 0x20),
               "SELECT packname FROM pack_names WHERE packid=:packid");
    lVar6 = FUN_100231760(auStack_58);
    if (lVar6 != 0) {
      *(int *)(lVar6 + 8) = *(int *)(lVar6 + 8) + 1;
    }
    lVar7 = *plVar8;
    if (lVar7 != 0) {
      iVar4 = *(int *)(lVar7 + 8) + -1;
      *(int *)(lVar7 + 8) = iVar4;
      if (iVar4 == 0) {
        FUN_1002abea8();
      }
    }
    *plVar8 = lVar6;
    FUN_10022d2b4(auStack_58);
  }
  return param_1;
}

