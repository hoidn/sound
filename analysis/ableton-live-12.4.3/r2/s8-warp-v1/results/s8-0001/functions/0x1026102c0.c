
bool FUN_1026102c0(long param_1)

{
  long *plVar1;
  undefined8 *puVar2;
  long lVar3;
  long *plVar4;
  long lVar5;
  
  plVar1 = (long *)___dynamic_cast(*(undefined8 *)(param_1 + 0x80),FUN_106662d78,
                                   &PTR_vtable_1067e8c00,0xfffffffffffffffe);
  plVar1 = (long *)(**(code **)(*plVar1 + 0x18))();
  puVar2 = (undefined8 *)(**(code **)(*plVar1 + 0x60))();
  lVar3 = (**(code **)*puVar2)(puVar2,plVar1);
  lVar5 = *(long *)(lVar3 + 0x20);
  if (lVar5 == 0 || lVar5 == lVar3) {
    return param_1 == 0;
  }
  plVar4 = (long *)(**(code **)(*plVar1 + 0x60))(plVar1);
  lVar3 = (**(code **)(*plVar4 + 0x20))(plVar4,plVar1,lVar5);
  return *(long *)(lVar3 + 8) == param_1;
}

