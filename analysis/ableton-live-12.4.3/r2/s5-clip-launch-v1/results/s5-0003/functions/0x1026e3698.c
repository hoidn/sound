
undefined8 FUN_1026e3698(long param_1)

{
  long lVar1;
  long lVar2;
  float fVar3;
  float fVar4;
  
  lVar2 = *(long *)(param_1 + 0x30);
  lVar1 = (**(code **)(**(long **)(lVar2 + 8) + 0x1d0))();
  fVar3 = (float)(**(code **)(**(long **)(lVar1 + 0x78) + 0x210))();
  lVar1 = (**(code **)(**(long **)(lVar2 + 8) + 0x1d0))();
  fVar4 = (float)(**(code **)(**(long **)(lVar1 + 0x90) + 0x210))();
  return CONCAT44((int)fVar4,(int)fVar3);
}

