// 0x100265ac4 FUN_100265ac4 state=exported body_bytes=416 warnings=0 chunk=chunk-00107.jsonl

long FUN_100265ac4(long param_1,uint param_2)

{
  undefined *puVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  
  puVar2 = (undefined8 *)FUN_100231c2c(param_1,param_2 & 1);
  *puVar2 = &PTR_thunk_FUN_10028d0a4_100d92710;
  puVar2[0xd] = &PTR_FUN_100d927b8;
  puVar2[0xe] = puVar2;
  puVar2[0xf] = &PTR_FUN_100d927f0;
  puVar2[0x10] = puVar2;
  FUN_10025b600(puVar2 + 0x11,param_1);
  FUN_1002bb284(param_1 + 0x98,param_1);
  FUN_100441b14(param_1 + 0xa8,param_1);
  *(undefined8 *)(param_1 + 0xb8) = &PTR_FUN_100d92660;
  FUN_100478f78(param_1 + 0xc0,param_1);
  *(undefined ***)(param_1 + 0xc0) = &PTR_thunk_FUN_100479018_100d93ad8;
  FUN_10043f0a4(param_1 + 0xe0,param_1);
  FUN_100443304(param_1 + 0xf8,param_1);
  FUN_100465704(param_1 + 0x108,param_1);
  FUN_1002ae4fc(param_1 + 0x118,param_1);
  FUN_100440438(param_1 + 0x128,param_1);
  FUN_10044b280(param_1 + 0x138,param_1);
  puVar1 = PTR_CallMemberFunc<&(TFileDatabase::MapFileTypeToFileKind(int)const)>_100d60d60;
  *(undefined2 *)(param_1 + 0x148) = 0;
  *(undefined **)(param_1 + 0x150) = puVar1;
  *(long *)(param_1 + 0x158) = param_1;
  *(byte *)(param_1 + 0x160) = (byte)(param_2 >> 1) & 1;
  *(byte *)(param_1 + 0x161) = (byte)(param_2 >> 2) & 1;
  *(undefined8 *)(param_1 + 0x168) = 0;
  *(undefined8 *)(param_1 + 0x170) = 0;
  *(undefined8 *)(param_1 + 400) = 0;
  *(undefined8 *)(param_1 + 0x1b0) = 0;
  uVar3 = FUN_100234750(param_1);
  uVar3 = FUN_100234758(uVar3,puVar2 + 0xd);
  uVar3 = FUN_100234758(uVar3,puVar2 + 0xf);
  uVar3 = FUN_100234758(uVar3,param_1 + 0x88);
  uVar3 = FUN_100234758(uVar3,param_1 + 0x108);
  uVar3 = FUN_100234758(uVar3,param_1 + 0x98);
  uVar3 = FUN_100234758(uVar3,param_1 + 0xa8);
  uVar3 = FUN_100234758(uVar3,param_1 + 0xf8);
  uVar3 = FUN_100234758(uVar3,(undefined8 *)(param_1 + 0xb8));
  uVar3 = FUN_100234758(uVar3,param_1 + 0xe0);
  uVar3 = FUN_100234758(uVar3,param_1 + 0x118);
  uVar3 = FUN_100234758(uVar3,param_1 + 0x128);
  FUN_100234758(uVar3,param_1 + 0x138);
  return param_1;
}

