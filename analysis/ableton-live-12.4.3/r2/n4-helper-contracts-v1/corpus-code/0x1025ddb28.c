// 0x1025ddb28 FUN_1025ddb28 exported  sig: undefined FUN_1025ddb28()

undefined8 FUN_1025ddb28(long param_1,undefined8 param_2,undefined8 param_3)

{
  int iVar1;
  long *plVar2;
  undefined8 uVar3;
  long lVar4;
  long lVar5;
  
  lVar4 = *(long *)(param_1 + 0x10);
  if (*(long *)(lVar4 + 0x48) != 0) {
    lVar5 = *(long *)(lVar4 + 0x38);
    plVar2 = *(long **)(lVar5 + 0x18);
    if ((((plVar2 != (long *)0x0) && (iVar1 = (**(code **)(*plVar2 + 0x20))(), iVar1 != 0)) &&
        (iVar1 = (**(code **)(**(long **)(lVar5 + 0x18) + 0x38))(), iVar1 != 0)) &&
       (**(int **)(*(long *)(lVar4 + 0x38) + 0x28) == 3)) {
      uVar3 = FUN_1025da178(*(long *)(lVar4 + 0x38) + 0x10,param_2,param_3);
      return uVar3;
    }
  }
  return 1;
}


