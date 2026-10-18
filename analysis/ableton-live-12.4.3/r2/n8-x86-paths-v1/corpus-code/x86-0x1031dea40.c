// x86 0x1031dea40 FUN_1031dea40 state=exported chunk=chunk-02326.jsonl code_sha256=8346486c776b94d3525d05dd718d44316348b823ce991788661427e59c19ae9d

undefined8 *
FUN_1031dea40(undefined8 *param_1,long param_2,long param_3,long *param_4,undefined8 param_5)

{
  int *piVar1;
  int iVar2;
  long lVar3;
  undefined8 *puVar4;
  long lVar5;
  undefined8 uVar6;
  undefined8 *puVar7;
  long local_40;
  undefined8 *local_38;
  
  lVar5 = FUN_1012bdaa0(0x80);
  lVar3 = *param_4;
  if (lVar3 != 0) {
    *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
  }
  local_40 = lVar3;
  FUN_1031d78b0(lVar5,&local_40,param_5);
  if (lVar5 != 0) {
    *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
  }
  if (lVar3 != 0) {
    piVar1 = (int *)(lVar3 + 8);
    *piVar1 = *piVar1 + -1;
    if (*piVar1 == 0) {
      FUN_1012716c0(lVar3);
    }
  }
  local_38 = param_1;
  uVar6 = FUN_1054eace0(param_3,lVar5 + 0x20,0);
  iVar2 = *(int *)(param_3 + 4);
  puVar7 = (undefined8 *)FUN_1012bdaa0(0x48);
  FUN_1012715b0(puVar7);
  puVar4 = local_38;
  *puVar7 = &PTR_FUN_106e01c70;
  puVar7[3] = &PTR_FUN_106e01cf8;
  puVar7[4] = uVar6;
  puVar7[5] = param_2;
  if (param_2 != 0) {
    *(int *)(param_2 + 8) = *(int *)(param_2 + 8) + 1;
  }
  *(uint *)(puVar7 + 6) = (uint)(iVar2 == 0);
  *(undefined1 *)((long)puVar7 + 0x34) = 0;
  puVar7[7] = lVar5;
  if (lVar5 == 0) {
    puVar7[8] = param_5;
    *local_38 = puVar7;
    *(int *)(puVar7 + 1) = *(int *)(puVar7 + 1) + 1;
  }
  else {
    *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
    puVar7[8] = param_5;
    *local_38 = puVar7;
    *(int *)(puVar7 + 1) = *(int *)(puVar7 + 1) + 1;
    piVar1 = (int *)(lVar5 + 8);
    *piVar1 = *piVar1 + -1;
    if (*piVar1 == 0) {
      FUN_1012716c0(lVar5);
    }
  }
  return puVar4;
}

