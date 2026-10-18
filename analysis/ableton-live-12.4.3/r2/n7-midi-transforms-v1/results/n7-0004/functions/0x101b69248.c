
void FUN_101b69248(long param_1,undefined8 param_2,int *param_3)

{
  int iVar1;
  long lVar2;
  long lVar3;
  int iVar4;
  ulong uVar5;
  long lVar6;
  
  lVar6 = *(long *)(param_1 + 0x28);
  while( true ) {
    if (lVar6 == 0) {
      return;
    }
    lVar2 = FUN_101b65da8(lVar6);
    iVar1 = FUN_101b64db8();
    iVar4 = (int)param_2;
    if (iVar1 == iVar4) break;
    lVar6 = *(long *)(lVar6 + 8);
  }
  if (lVar2 == 0) {
    return;
  }
  if (*param_3 != 6) {
    if (*param_3 == 3) {
      FUN_101b65b68(lVar2,param_3);
    }
    thunk_FUN_101b64df8(lVar2,param_3);
  }
  iVar1 = FUN_101b64dd0(lVar2);
  if (iVar1 != 0) {
    if (*(char *)(param_1 + 8) == '\x01') {
      FUN_101b69680(param_1,param_2,param_3);
      uVar5 = 1;
      lVar6 = FUN_101ab9e24(5);
      lVar6 = *(long *)(lVar6 + 0x10);
      goto joined_r0x000101b692fc;
    }
    if (*(long *)(param_1 + 0x10) != 0) {
      uVar5 = FUN_101b7842c(*(long *)(param_1 + 0x10),param_3);
      lVar6 = FUN_101ab9e24(5);
      lVar6 = *(long *)(lVar6 + 0x10);
      goto joined_r0x000101b692fc;
    }
  }
  uVar5 = 0;
  lVar6 = FUN_101ab9e24(5);
  lVar6 = *(long *)(lVar6 + 0x10);
joined_r0x000101b692fc:
  do {
    if (lVar6 == 0) {
      if ((uVar5 & 1) == 0) {
LAB_101b6935c:
        iVar1 = FUN_101b64dc0(lVar2);
        if (iVar1 != 0) {
          FUN_101b65ad0(lVar2,param_3);
          return;
        }
      }
      return;
    }
    if (*(int *)(*(long *)(lVar6 + 0x18) + 0x28) == iVar4) {
      if ((uVar5 & 1) != 0) {
        return;
      }
      lVar6 = FUN_101ab9e24(5);
      for (lVar6 = *(long *)(lVar6 + 0x10); lVar6 != 0; lVar6 = *(long *)(lVar6 + 8)) {
        if (((*(int *)(*(long *)(lVar6 + 0x18) + 0x28) == iVar4) &&
            (lVar3 = *(long *)(*(long *)(lVar6 + 0x18) + 0x30), lVar3 != 0)) &&
           (uVar5 = FUN_101b7842c(lVar3,param_3), (uVar5 & 1) != 0)) {
          return;
        }
      }
      goto LAB_101b6935c;
    }
    lVar6 = *(long *)(lVar6 + 8);
  } while( true );
}

