// 0x1002ad94c FUN_1002ad94c state=exported-with-warnings role=service discovery multicast endpoint
// source chunk chunk-00120.jsonl; code_sha256=44f174794644cfa8205051661effb734bee7f512ed00191930ef0fe74f247c7c

void FUN_1002ad94c(undefined1 *param_1,undefined8 param_2,int *param_3)

{
  code *pcVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined4 local_4c;
  undefined4 uStack_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined8 local_3c;
  undefined8 uStack_34;
  undefined4 local_2c;
  undefined **local_28;
  
  if (*param_3 == 1) {
    FUN_1002ae444(&local_44,param_3[6]);
  }
  else {
    FUN_1002aea64(&local_44,"224.76.78.75");
    local_4c = 0;
    uStack_48 = 0;
    if (local_44 == 0) {
      puVar2 = &local_40;
      local_3c = 0;
      uStack_34 = 0;
      puVar3 = &uStack_48;
      local_44._1_1_ = 2;
    }
    else {
      if (local_44 != 1) {
        std::bad_cast::bad_cast((bad_cast *)&local_28);
        local_28 = &PTR__bad_cast_101bd9400;
        FUN_1002ae5d8();
                    /* WARNING: Does not return */
        pcVar1 = (code *)SoftwareBreakpoint(1,0x1002ada44);
        (*pcVar1)();
      }
      puVar2 = &local_2c;
      puVar3 = &local_4c;
      local_44._1_1_ = 0x1e;
    }
    local_44._0_1_ = 0;
    *puVar3 = *puVar2;
    local_44._2_2_ = 0xad51;
    local_40 = uStack_48;
    local_2c = local_4c;
  }
  *param_1 = (undefined1)local_44;
  param_1[1] = local_44._1_1_;
  *(undefined2 *)(param_1 + 2) = local_44._2_2_;
  *(undefined4 *)(param_1 + 4) = local_40;
  *(undefined8 *)(param_1 + 0x10) = uStack_34;
  *(undefined8 *)(param_1 + 8) = local_3c;
  *(undefined4 *)(param_1 + 0x18) = local_2c;
  param_1[0x1c] = 1;
  return;
}

