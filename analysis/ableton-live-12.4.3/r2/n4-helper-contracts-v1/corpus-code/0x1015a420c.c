// 0x1015a420c FUN_1015a420c exported  sig: undefined FUN_1015a420c()

void FUN_1015a420c(long param_1)

{
  void *local_38;
  void *local_30;
  
  FUN_100e170d0(&local_38,3);
  (**(code **)(**(long **)(param_1 + 0x20) + 0x20))(*(long **)(param_1 + 0x20),&local_38,1);
  if (local_38 != (void *)0x0) {
    local_30 = local_38;
    operator_delete(local_38);
  }
  return;
}


