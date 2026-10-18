
long FUN_1024f4b08(long param_1)

{
  int iVar1;
  undefined8 *puVar2;
  long lVar3;
  long *plVar4;
  long *plVar5;
  long *plVar6;
  long *plVar7;
  undefined8 local_58;
  
  puVar2 = (undefined8 *)FUN_102348a34();
  *puVar2 = &PTR_thunk_FUN_102500218_1067c74e8;
  plVar4 = puVar2 + 0x10;
  *plVar4 = 0;
  FUN_102776cec(&local_58);
  lVar3 = *plVar4;
  if ((lVar3 != 0) && (iVar1 = *(int *)(lVar3 + 8) + -1, *(int *)(lVar3 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined8 *)(param_1 + 0x80) = local_58;
  plVar5 = (long *)(param_1 + 0x88);
  *plVar5 = 0;
  FUN_102776cec(&local_58);
  lVar3 = *plVar5;
  if ((lVar3 != 0) && (iVar1 = *(int *)(lVar3 + 8) + -1, *(int *)(lVar3 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined8 *)(param_1 + 0x88) = local_58;
  plVar6 = (long *)(param_1 + 0x90);
  *plVar6 = 0;
  FUN_1024f44b8(&local_58);
  lVar3 = *plVar6;
  if ((lVar3 != 0) && (iVar1 = *(int *)(lVar3 + 8) + -1, *(int *)(lVar3 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined8 *)(param_1 + 0x90) = local_58;
  plVar7 = (long *)(param_1 + 0x98);
  *plVar7 = 0;
  FUN_1023485f4(&local_58);
  lVar3 = *plVar7;
  if ((lVar3 != 0) && (iVar1 = *(int *)(lVar3 + 8) + -1, *(int *)(lVar3 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  *(undefined8 *)(param_1 + 0x98) = local_58;
  *(undefined8 *)(param_1 + 0xa0) = 0;
  *(undefined1 *)(param_1 + 0xa8) = 0;
  FUN_101486414(param_1);
  if ((DAT_10700a8f8 & 1) == 0) {
    FUN_105421974();
  }
  if ((DAT_10700a900 & 1) == 0) {
    FUN_1054219ac();
  }
  if ((DAT_10700a908 & 1) == 0) {
    FUN_1054219e4();
  }
  if ((DAT_10700a910 & 1) == 0) {
    FUN_105421a1c();
  }
  FUN_102776f10(*plVar4,&DAT_10700a998,0x80000000);
  FUN_102776f10(*plVar5,&DAT_10700a9a8,0x80000000);
  lVar3 = *plVar6;
  if ((DAT_10700a8f0 & 1) == 0) {
    FUN_105421a54(lVar3);
  }
  FUN_1023298f8(lVar3,&DAT_10700a9b8);
  FUN_1023486d0(*plVar7,&DAT_10700a9c8);
  FUN_1023490d0(param_1,*(undefined8 *)(param_1 + 0x80));
  FUN_1023490d0(param_1,*(undefined8 *)(param_1 + 0x88));
  FUN_1023490d0(param_1,*(undefined8 *)(param_1 + 0x90));
  FUN_1023495d0(param_1,*(undefined8 *)(param_1 + 0x98));
  return param_1;
}

