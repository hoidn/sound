
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8
FUN_102593258(undefined4 param_1,long *param_2,long *param_3,undefined8 param_4,undefined8 param_5,
             undefined8 param_6,undefined8 param_7,undefined8 param_8)

{
  int iVar1;
  ulong uVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  ulong extraout_x1;
  undefined8 uVar5;
  undefined1 auStack_c4 [12];
  undefined1 auStack_b8 [8];
  long local_b0;
  int local_a8;
  char local_a4;
  char local_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  char local_6c;
  
  FUN_1025931ac(param_4,param_5,param_6);
  uVar2 = FUN_1026f9488(param_3);
  if (((uVar2 & 1) == 0) &&
     ((iVar1 = (**(code **)(*param_2 + 0x38))(param_2), iVar1 == 0 ||
      (uVar2 = (**(code **)(*param_2 + 0x30))(param_2,param_4,param_5,0,0), (uVar2 & 1) == 0)))) {
    uStack_88 = _UNK_1058838ec;
    local_90 = _DAT_1058838e4;
    uStack_78 = _UNK_1058838fc;
    uStack_80 = _DAT_1058838f4;
    FUN_1011aeb80(&local_90);
    if ((extraout_x1 & 1) == 0) {
      uVar5 = (**(code **)(*param_3 + 0x170))(param_3);
      uVar3 = FUN_1026eb7a8();
      uVar5 = FUN_10147fd68(uVar5,uVar3);
    }
    else {
      uVar5 = 0;
    }
    (**(code **)(*param_3 + 0x350))(&local_90,0x3f800000,param_3,uVar5);
    if (local_6c == '\x01') {
      if ((int)param_6 == 5) {
        FUN_101b7d010(auStack_b8,param_7);
        local_98 = '\x01';
        FUN_1026094e0(param_2,&local_90,param_4,param_5,auStack_b8);
        if (((local_98 == '\x01') && (local_b0 != 0)) && (local_a4 == '\x01')) {
          thunk_FUN_101aa0360(local_b0,(long)local_a8);
        }
      }
      else {
        uVar5 = thunk_FUN_101a9b404(0x50);
        FUN_101b7f2d4();
        uVar3 = FUN_101b7c22c(&local_90);
        uVar3 = (**(code **)(*param_2 + 0x48))(param_2,uVar3);
        FUN_101b7f32c(param_1,uVar5,uVar3,&local_90,param_8);
        uVar3 = thunk_FUN_101a9b404(0x38);
        FUN_101b7b55c();
        puVar4 = (undefined8 *)(**(code **)(*param_2 + 0x60))(param_2,3);
        FUN_101b7b59c(uVar3,uVar5,*puVar4,1,1);
        FUN_101b7b878(auStack_c4,param_4,param_5,param_6);
        (**(code **)(*param_2 + 0x80))(param_2,auStack_c4,uVar3,&local_90,param_7);
      }
      return 1;
    }
  }
  return 0;
}

