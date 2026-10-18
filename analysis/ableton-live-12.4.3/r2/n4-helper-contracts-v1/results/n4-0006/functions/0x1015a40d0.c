
void FUN_1015a40d0(long param_1)

{
  int iVar1;
  undefined8 uVar2;
  void *local_38;
  void *local_30;
  
  FUN_100e170d0(&local_38,0);
  iVar1 = (**(code **)(**(long **)(param_1 + 0x20) + 0x20))(*(long **)(param_1 + 0x20),&local_38,0);
  if (local_38 != (void *)0x0) {
    local_30 = local_38;
    operator_delete(local_38);
  }
  if (iVar1 != 0) {
    uVar2 = std::chrono::system_clock::now();
    FUN_103f3ffec(&local_38,4,uVar2);
    iVar1 = FUN_103f3c8b8(&local_38);
    if (iVar1 != 0) {
      FUN_103f39a78(&local_38,"IPC: Failed to send sync signal to other site.");
    }
    thunk_FUN_103f395e4(&local_38);
  }
  return;
}

