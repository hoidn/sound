// x86 0x101a6f520 FUN_101a6f520 state=exported chunk=chunk-01151.jsonl code_sha256=595a5221cd9cad941890286219b5cd4b704f5df60907012d23489f161e2ab277

void FUN_101a6f520(long param_1,char param_2)

{
  long lVar1;
  int iVar2;
  int iVar3;
  undefined8 uVar4;
  long local_48;
  undefined8 local_40;
  
  if (*(char *)(param_1 + 0x60) != param_2) {
    if (*(int *)(param_1 + 8) != -1) {
      FUN_101ae0120(&local_48,&DAT_1073e7c80,0x10100,0x100500,0);
      FUN_101ac3f80(local_40,*(undefined4 *)(param_1 + 8));
      FUN_101ac3f40(local_40,param_2);
      (**(code **)(local_48 + 0x10))(&local_48);
      FUN_101ae0670(&local_48);
    }
    *(char *)(param_1 + 0x60) = param_2;
    lVar1 = *(long *)(param_1 + 0x10);
    if (lVar1 != 0) {
      iVar2 = FUN_101a64430(lVar1);
      iVar3 = FUN_101a64420(lVar1);
      if (iVar3 <= iVar2) {
        do {
          uVar4 = FUN_101a643d0(lVar1,iVar3);
          FUN_101a78eb0(uVar4,param_2);
          iVar3 = iVar3 + 1;
        } while (iVar2 + 1 != iVar3);
      }
    }
  }
  return;
}

