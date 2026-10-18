// 0x1008f000c FUN_1008f000c exported  sig: undefined FUN_1008f000c()

void FUN_1008f000c(undefined8 param_1)

{
  void *local_50 [2];
  char local_39;
  void *local_38 [2];
  char local_21;
  
  FUN_1008fcae4(local_50);
  FUN_103e96bc4(local_38,local_50);
  if (local_39 < '\0') {
    operator_delete(local_50[0]);
  }
  FUN_1008f00c0(local_38,"../..");
  FUN_103e952d0(param_1,local_38);
  if (-1 < local_21) {
    return;
  }
  operator_delete(local_38[0]);
  return;
}


