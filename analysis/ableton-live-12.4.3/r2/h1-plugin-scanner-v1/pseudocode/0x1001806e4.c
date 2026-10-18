
void FUN_1001806e4(void)

{
  int iVar1;
  size_t local_2c8;
  undefined1 auStack_2c0 [560];
  int local_90;
  undefined8 local_38;
  undefined4 local_30;
  pid_t local_2c;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_100b1c378;
  local_38 = DAT_1009ab000;
  local_30 = 1;
  local_2c = _getpid();
  local_2c8 = 0x288;
  iVar1 = _sysctl((int *)&local_38,4,auStack_2c0,&local_2c8,(void *)0x0,0);
  if (*(long *)PTR____stack_chk_guard_100b1c378 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(-1 < iVar1 && local_90 == 1);
}

