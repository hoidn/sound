
undefined8 FUN_10245efa0(undefined8 param_1,long param_2,undefined8 param_3)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar3;
  long lVar4;
  long *plVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  long local_88;
  undefined8 local_80;
  undefined8 local_68;
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 uStack_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  
  if ((param_2 != 0) && (lVar4 = FUN_10273b950(param_2), lVar4 != 0)) {
    plVar5 = (long *)FUN_10273b950(param_2);
    uVar6 = FUN_101a9419c();
    FUN_10243f868(plVar5);
    FUN_10250416c(&local_68);
    FUN_10243f868(plVar5);
    FUN_102504310();
    iVar3 = FUN_1015645a0();
    uVar2 = uStack_58;
    uVar1 = local_5c;
    if (iVar3 == 0) {
      uVar1 = 0;
      uVar2 = 0;
    }
    FUN_101ab7348(&local_88,&DAT_10700a240,0x100500,0x200600,0);
    FUN_101a9c618(local_80,uVar6);
    FUN_101a9c534(local_80,param_3);
    iVar3 = (**(code **)(*plVar5 + 0x300))(plVar5);
    if (iVar3 == 0) {
      uVar7 = 0;
    }
    else {
      uVar7 = FUN_1015645a0(plVar5[0xd]);
    }
    FUN_101a9c504(local_80,uVar7);
    FUN_101a9c594(local_68,local_80);
    FUN_101a9c534(local_80,local_60);
    FUN_101a9c534(local_80,uVar1);
    FUN_101a9c534(local_80,uVar2);
    FUN_101a9c57c(local_54,local_80);
    FUN_101a9c57c(local_50,local_80);
    FUN_101a9c534(local_80,local_4c);
    FUN_101a9c534(local_80,local_48);
    uVar7 = FUN_10243f7f8(plVar5);
    FUN_101a9c534(local_80,uVar7);
    FUN_102442998(plVar5,0);
    FUN_101a9c594(local_80);
    (**(code **)(local_88 + 0x10))(&local_88);
    FUN_101ab786c(&local_88);
    return uVar6;
  }
  return 0;
}

