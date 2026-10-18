
void FUN_10255d93c(undefined8 param_1,uint param_2)

{
  undefined4 uVar1;
  undefined8 *puVar2;
  
  puVar2 = (undefined8 *)FUN_101574f00();
  *puVar2 = &PTR_FUN_1067d0108;
  *(uint *)(puVar2 + 5) = param_2;
  if (param_2 < 6) {
    uVar1 = *(undefined4 *)(&DAT_105883044 + (ulong)param_2 * 4);
    *(undefined4 *)((long)puVar2 + 0x2c) = *(undefined4 *)(&DAT_10588302c + (ulong)param_2 * 4);
    *(undefined4 *)(puVar2 + 6) = uVar1;
    return;
  }
  *(undefined4 *)((long)puVar2 + 0x2c) = 0x39a5cb5f;
  *(undefined4 *)(puVar2 + 6) = 0x417d953b;
  return;
}

