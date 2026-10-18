
void FUN_1025c36ec(long *param_1,undefined4 *param_2,undefined4 param_3)

{
  undefined8 *puVar1;
  int iVar2;
  long *plVar3;
  long lVar4;
  undefined8 *puVar5;
  long lVar6;
  long local_58;
  int *local_50;
  undefined4 local_48;
  
  if (((DAT_10700b6f8 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_10700b6f8), iVar2 != 0)) {
    FUN_1025d2078();
    ___cxa_atexit(FUN_1025d20f4,&DAT_10700b6f0,0x100000000);
    ___cxa_guard_release(&DAT_10700b6f8);
  }
  lVar6 = DAT_10700b6f0;
  local_50 = *(int **)(param_2 + 2);
  local_58 = CONCAT44(local_58._4_4_,*param_2);
  if (local_50 != (int *)0x0) {
    *local_50 = *local_50 + 1;
  }
  local_48 = param_3;
  plVar3 = (long *)FUN_1025d2264(lVar6 + 0x18,&local_58);
  lVar6 = *plVar3;
  if ((local_50 != (int *)0x0) && (iVar2 = *local_50, *local_50 = iVar2 + -1, iVar2 + -1 == 0)) {
    FUN_101449efc();
  }
  lVar4 = FUN_1012d9734(0x88);
  puVar5 = (undefined8 *)FUN_102348a34();
  *puVar5 = &PTR_FUN_1067dea48;
  *(undefined4 *)(puVar5 + 0x10) = 0;
  FUN_101486414();
  *(int *)(lVar4 + 8) = *(int *)(lVar4 + 8) + 1;
  local_58 = lVar4;
  FUN_101482718(lVar4);
  puVar1 = *(undefined8 **)(lVar6 + 0x20);
  for (puVar5 = *(undefined8 **)(lVar6 + 0x18); puVar5 != puVar1; puVar5 = puVar5 + 1) {
    (**(code **)(*(long *)*puVar5 + 0x28))((long *)*puVar5,local_58);
    lVar4 = local_58;
  }
  *(undefined4 *)(lVar4 + 0x80) = param_3;
  FUN_102348ce8(lVar4,lVar6 + 0x30,0,1);
  *param_1 = local_58;
  return;
}

