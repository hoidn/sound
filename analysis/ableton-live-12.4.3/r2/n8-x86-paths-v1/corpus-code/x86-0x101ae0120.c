// x86 0x101ae0120 FUN_101ae0120 state=exported-with-warnings chunk=chunk-01177.jsonl code_sha256=8a502ef1237a270248ec108fb77774c19360819c5ad9f0708345beab3566ac3c

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_101ae0120(undefined8 *param_1,int *param_2,undefined4 param_3,undefined4 param_4,
                  undefined4 param_5)

{
  int iVar1;
  undefined8 uVar2;
  long lVar3;
  
  param_1[1] = 0;
  *param_1 = &PTR_FUN_106c98f18;
  *(undefined4 *)(param_1 + 2) = param_3;
  *(undefined4 *)((long)param_1 + 0x14) = param_4;
  *(undefined4 *)(param_1 + 3) = 0xffffffff;
  *(undefined4 *)((long)param_1 + 0x1c) = param_5;
  uVar2 = FUN_101ad6490();
  lVar3 = FUN_101ad4c90(uVar2,param_2,*(undefined4 *)(param_1 + 2),
                        *(undefined4 *)((long)param_1 + 0x14),*(undefined4 *)(param_1 + 3));
  param_1[1] = lVar3;
  if (lVar3 != 0) {
    return;
  }
  iVar1 = *param_2;
  if (iVar1 == -1) {
    iVar1 = FUN_101ac3d40(*(undefined8 *)(param_2 + 2));
    *param_2 = iVar1;
  }
  _DAT_1073e8050 = (undefined2)iVar1;
  _DAT_1073e8052 = 0;
  param_1[1] = &DAT_1073e8050;
  return;
}

