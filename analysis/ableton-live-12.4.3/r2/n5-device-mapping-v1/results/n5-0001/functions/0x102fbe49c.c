
void FUN_102fbe49c(long param_1,code *param_2)

{
  int iVar1;
  int local_34;
  undefined8 local_30;
  undefined8 local_28;
  
  if (param_2 != (code *)0x0) {
    iVar1 = (*param_2)(1,&local_28,8);
    if (iVar1 != 0) {
      *(undefined8 *)(param_1 + 0x70) = local_28;
    }
    iVar1 = (*param_2)(2,&local_28,8);
    if (iVar1 != 0) {
      *(undefined8 *)(param_1 + 0x78) = local_28;
    }
    iVar1 = (*param_2)(3,&local_28,8);
    if (iVar1 != 0) {
      *(int *)(param_1 + 0x80) = (int)local_28;
    }
    iVar1 = (*param_2)(5,&local_30,8);
    if (iVar1 != 0) {
      *(undefined8 *)(param_1 + 0x88) = local_30;
    }
    iVar1 = (*param_2)(4,&local_34,4);
    if (iVar1 != 0) {
      *(uint *)(param_1 + 0x84) = (uint)(local_34 != 0);
    }
    iVar1 = (*param_2)(6,&local_34,4);
    if (iVar1 != 0) {
      *(uint *)(param_1 + 0x90) = (uint)(local_34 != 0);
    }
  }
  return;
}

