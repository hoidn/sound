// 0x1013ec734 FUN_1013ec734 state=exported role=display frame cycle (header then 0x50000-byte payload)
// source chunk chunk-00891.jsonl; code_sha256=7f19c518ef65807bc352a3d73737c4b229cbae8e43cf265319d79b079dbe259a

void FUN_1013ec734(undefined4 *param_1,undefined8 *param_2)

{
  int iVar1;
  long lVar2;
  undefined8 local_70;
  void *local_68;
  undefined8 uStack_60;
  long local_58;
  undefined4 local_50 [2];
  void *local_48;
  undefined8 uStack_40;
  long local_38;
  
  FUN_1013f1168(local_50);
  if (*(int *)(param_2 + 2) != 4) {
    lVar2 = (*(code *)**(undefined8 **)*param_2)();
    param_2[1] = lVar2;
    if (lVar2 != 0) {
      FUN_1013f038c(&local_70,param_2 + 7);
      local_50[0] = (undefined4)local_70;
      if (local_38 < 0) {
        operator_delete(local_48);
      }
      uStack_40 = uStack_60;
      local_48 = local_68;
      local_38 = local_58;
      iVar1 = FUN_1013f18d0(local_50);
      if (iVar1 == 0) {
        local_70 = param_2[1];
        local_68 = (void *)0x50000;
        FUN_1013f053c(param_2 + 0x10,&local_70);
        FUN_1013f038c(param_1,param_2 + 0x10);
        if (-1 < local_38) {
          return;
        }
        operator_delete(local_48);
        return;
      }
      *param_1 = local_50[0];
      *(undefined8 *)(param_1 + 4) = uStack_40;
      *(void **)(param_1 + 2) = local_48;
      *(long *)(param_1 + 6) = local_38;
      return;
    }
    if ((*(int *)(param_2 + 2) == 4) || (*(int *)(param_2 + 2) == 1)) {
      *(undefined4 *)(param_2 + 2) = 2;
    }
  }
  *param_1 = local_50[0];
  *(undefined8 *)(param_1 + 4) = uStack_40;
  *(void **)(param_1 + 2) = local_48;
  *(long *)(param_1 + 6) = local_38;
  return;
}

