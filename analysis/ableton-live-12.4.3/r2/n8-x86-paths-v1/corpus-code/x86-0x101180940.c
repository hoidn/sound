// x86 0x101180940 FUN_101180940 state=exported-with-warnings chunk=chunk-00673.jsonl code_sha256=a36e7dc35ac8431a28dbd5e46e497b971eaa183dc1e618f8ac0137cc068acd21

undefined1 FUN_101180940(undefined8 param_1,undefined8 param_2)

{
  int iVar1;
  pid_t pVar2;
  size_t sVar3;
  int *piVar4;
  undefined1 uVar5;
  uint local_434;
  FILE *local_430;
  undefined1 local_428 [1032];
  long local_20;
  
  local_20 = *(long *)PTR____stack_chk_guard_106a33b20;
  if (DAT_1073a0d68 == 0) {
    iVar1 = _AuthorizationCreate(0,0,0,&DAT_1073a0d68);
    uVar5 = 1;
    if (iVar1 != 0) goto LAB_101180a5c;
  }
  local_430 = (FILE *)0x0;
  iVar1 = _AuthorizationExecuteWithPrivileges(DAT_1073a0d68,param_1,0,param_2,&local_430);
  if (iVar1 == -0xea66) {
    uVar5 = 2;
  }
  else {
    if (iVar1 == 0) {
      sVar3 = _fread(local_428,1,0x400,local_430);
      if (0 < (int)sVar3) {
        do {
          local_428[(uint)sVar3 & 0x7fffffff] = 0;
          sVar3 = _fread(local_428,1,0x400,local_430);
        } while (0 < (int)sVar3);
      }
      _fclose(local_430);
      do {
        pVar2 = _wait((int *)&local_434);
        if (pVar2 != -1) {
          uVar5 = 1;
          if ((0 < pVar2) && ((local_434 & 0x7f) == 0)) {
            uVar5 = (local_434 & 0xff00) != 0;
          }
          goto LAB_101180a5c;
        }
        piVar4 = ___error();
      } while (*piVar4 == 4);
    }
    uVar5 = 1;
  }
LAB_101180a5c:
  if (*(long *)PTR____stack_chk_guard_106a33b20 != local_20) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar5;
}

