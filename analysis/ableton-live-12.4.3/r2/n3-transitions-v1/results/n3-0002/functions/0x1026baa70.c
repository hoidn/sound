
void FUN_1026baa70(undefined8 param_1)

{
  long lVar1;
  long lVar2;
  undefined8 uVar3;
  undefined8 local_50;
  undefined8 local_48;
  undefined1 local_3a;
  undefined1 local_39;
  undefined8 local_38;
  undefined8 uStack_30;
  undefined1 local_25;
  undefined4 local_24;
  
  FUN_101a9c9cc(param_1,&local_24);
  lVar1 = FUN_10150b5e8(local_24);
  if (((lVar1 != 0) && (*(long *)(lVar1 + 0x78) != 0)) &&
     (lVar2 = (**(code **)(**(long **)(lVar1 + 8) + 0x198))(), lVar2 != 0)) {
    uVar3 = FUN_101a9c98c(param_1,&local_25);
    uVar3 = FUN_101a9ca3c(uVar3,&uStack_30);
    uVar3 = FUN_101a9ca3c(uVar3,&local_38);
    uVar3 = FUN_101a9c98c(uVar3,&local_39);
    uVar3 = FUN_101a9c98c(uVar3,&local_3a);
    FUN_101a9c9e8(uVar3,&local_48);
    local_50 = local_48;
    uVar3 = FUN_102688d2c(*(undefined8 *)(lVar1 + 0x78));
    FUN_10276c538(uStack_30,local_38,uVar3,local_25,local_39,local_3a,&local_50);
  }
  return;
}

