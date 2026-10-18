// 0x10023344c FUN_10023344c state=exported body_bytes=472 warnings=0 chunk=chunk-00096.jsonl

undefined8 FUN_10023344c(long param_1,int param_2,int param_3,int *param_4,int *param_5)

{
  int iVar1;
  int iVar2;
  long *local_50;
  undefined8 local_48;
  
  if (param_4 != (int *)0x0) {
    *param_4 = 0;
  }
  if (param_5 != (int *)0x0) {
    *param_5 = 0;
  }
  if (*(long *)(param_1 + 0x20) == 0) {
    return 0;
  }
  iVar2 = FUN_100233910(param_1);
  if (iVar2 != 0) {
    local_48 = 0;
    (**(code **)(**(long **)(param_1 + 0x20) + 0xd0))
              (&local_50,*(long **)(param_1 + 0x20),"SELECT version, platform FROM version");
    if (local_50 != (long *)0x0) {
      iVar2 = (**(code **)(*local_50 + 0xb8))();
      if (iVar2 != 0) {
        (**(code **)(*local_50 + 0xc0))(local_50,2);
        (**(code **)(*local_50 + 0x88))(local_50,0,(long)&local_48 + 4);
        (**(code **)(*local_50 + 0x88))(local_50,1,&local_48);
        (**(code **)(*local_50 + 0x28))();
      }
      if (((local_50 != (long *)0x0) && ((**(code **)(*local_50 + 0x28))(), local_50 != (long *)0x0)
          ) && (iVar1 = (int)local_50[1] + -1, *(int *)(local_50 + 1) = iVar1, iVar1 == 0)) {
        FUN_1002abea8();
      }
      if (iVar2 != 0) {
        if (param_4 != (int *)0x0) {
          *param_4 = local_48._4_4_;
        }
        if (param_5 != (int *)0x0) {
          *param_5 = (int)local_48;
        }
        if (local_48._4_4_ < param_2) {
          return 1;
        }
        if (param_2 < local_48._4_4_) {
          return 2;
        }
        if (param_3 == 0) {
          return 0;
        }
        if ((int)local_48 == param_3) {
          return 0;
        }
        return 3;
      }
    }
  }
  return 4;
}

