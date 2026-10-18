// x86 0x101554650 FUN_101554650 state=exported chunk=chunk-00827.jsonl code_sha256=f5033fee1369c722e21fb84fdf36b70fe548003cecb028e35f23d0bb73e82e7c

void FUN_101554650(long param_1,char param_2)

{
  if (*(char *)(param_1 + 0x60) != param_2) {
    *(char *)(param_1 + 0x60) = param_2;
  }
  return;
}

