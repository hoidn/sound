// 0x10017ff30 FUN_10017ff30 state=exported-with-warnings role=send sync byte to parent
// source chunk chunk-00065.jsonl; code_sha256=863feaff0abf66e4f10eb5e38385806e227a3b754396c87c5c6bd61682cb9d50

void FUN_10017ff30(long *param_1)

{
  int iVar1;
  undefined8 uVar2;
  long *plVar3;
  long lVar4;
  void *local_38;
  void *local_30;
  
  lVar4 = *param_1;
  plVar3 = *(long **)(lVar4 + 0xe0);
  FUN_1006677a8(&local_38,0);
  iVar1 = (**(code **)(*plVar3 + 0x18))(plVar3,&local_38,0);
  if (local_38 != (void *)0x0) {
    local_30 = local_38;
    operator_delete(local_38);
  }
  if (iVar1 != 0) {
    uVar2 = std::chrono::system_clock::now();
    FUN_1003324b0(&local_38,4,uVar2);
    iVar1 = FUN_10032ece8(&local_38);
    if (iVar1 != 0) {
      FUN_10032bea8(&local_38,"Failed to send sync signal to parent process. Shutting down.");
    }
    thunk_FUN_10032ba14(&local_38);
    plVar3 = *(long **)(lVar4 + 0xd8);
    if (plVar3 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_10018001c();
    }
    (**(code **)(*plVar3 + 0x30))();
  }
  return;
}

