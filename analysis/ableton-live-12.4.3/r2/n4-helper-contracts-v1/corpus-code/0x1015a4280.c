// 0x1015a4280 FUN_1015a4280 exported  sig: undefined FUN_1015a4280()

void FUN_1015a4280(long param_1)

{
  void *local_38;
  void *local_30;
  
  FUN_100e170d0(&local_38,2);
  (**(code **)(**(long **)(param_1 + 0x20) + 0x20))(*(long **)(param_1 + 0x20),&local_38,1);
  if (local_38 != (void *)0x0) {
    local_30 = local_38;
    operator_delete(local_38);
  }
  return;
}


