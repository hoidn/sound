// x86 0x101ae06b0 FUN_101ae06b0 state=exported chunk=chunk-01177.jsonl code_sha256=1abca7476adcacce29a1db1662935ae3f2732916aae0a519f97c7d2f7a3b0c10

void FUN_101ae06b0(long param_1)

{
  undefined8 uVar1;
  
  if (*(undefined **)(param_1 + 8) != &DAT_1073e8050) {
    FUN_101ac4760(param_1);
    uVar1 = FUN_101ad6490();
    FUN_101ad4ef0(uVar1,*(undefined8 *)(param_1 + 8),*(undefined4 *)(param_1 + 0x10),
                  *(undefined4 *)(param_1 + 0x14),*(undefined4 *)(param_1 + 0x18));
  }
  *(undefined8 *)(param_1 + 8) = 0;
  return;
}

