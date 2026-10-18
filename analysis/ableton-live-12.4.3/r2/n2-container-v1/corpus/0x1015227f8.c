
void FUN_1015227f8(long *param_1,undefined8 param_2)

{
  undefined1 auStack_35 [5];
  
  (**(code **)(*param_1 + 0x38))(param_1," ");
  (**(code **)(*param_1 + 0x38))(param_1,param_2);
  FUN_1011bfe14(auStack_35,5,"=%c");
  (**(code **)(*param_1 + 0x38))(param_1,auStack_35);
  *(undefined4 *)(param_1 + 3) = 4;
  return;
}

