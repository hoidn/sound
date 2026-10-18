// x86 0x101180aa0 FUN_101180aa0 state=exported chunk=chunk-00673.jsonl code_sha256=3d482590cf6a5729b82d5b3484a0763d261f5699600bac6a7656026a1cb6db04

undefined8 FUN_101180aa0(undefined8 param_1,undefined8 param_2)

{
  char cVar1;
  int iVar2;
  undefined8 uVar3;
  
  iVar2 = FUN_1011807c0();
  if (iVar2 == 0) {
    uVar3 = 0;
  }
  else {
    uVar3 = 2;
    cVar1 = FUN_101198610();
    if (cVar1 != '\0') {
      uVar3 = FUN_101180940(param_1,param_2);
      return uVar3;
    }
  }
  return uVar3;
}

