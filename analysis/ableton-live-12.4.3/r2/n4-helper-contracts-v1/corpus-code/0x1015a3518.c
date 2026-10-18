// 0x1015a3518 FUN_1015a3518 exported  sig: undefined FUN_1015a3518()

void FUN_1015a3518(long param_1,undefined8 param_2,undefined8 param_3)

{
  void *local_38;
  void *local_30;
  
  FUN_1015a2b6c(&local_38,param_2,param_3);
  (**(code **)(**(long **)(param_1 + 8) + 0x20))(*(long **)(param_1 + 8),&local_38,1);
  if (local_38 != (void *)0x0) {
    local_30 = local_38;
    operator_delete(local_38);
  }
  return;
}


