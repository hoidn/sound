// 0x100137948 FUN_100137948 state=exported body_bytes=1184 warnings=0 chunk=chunk-00052.jsonl

void FUN_100137948(undefined8 *param_1,undefined4 *param_2)

{
  char *pcVar1;
  long lVar2;
  byte bVar3;
  long *plVar4;
  long *plVar5;
  int iVar6;
  undefined8 uVar7;
  long *plVar8;
  long lVar9;
  int *local_70;
  long *local_68;
  long *local_60;
  char local_51;
  
  lVar9 = param_1[0x11];
  if (param_1[0x10] == 0 && lVar9 == 0) {
    if ((param_1[0x12] == 0) && (param_1[0x13] == 0)) goto LAB_100137a18;
    lVar9 = 0;
  }
  FUN_100140bac(param_1,param_1[0x10],lVar9,param_1[0x12],param_1[0x13]);
  lVar9 = param_1[0x10];
  if ((lVar9 != 0) && (iVar6 = *(int *)(lVar9 + 8) + -1, *(int *)(lVar9 + 8) = iVar6, iVar6 == 0)) {
    FUN_1002abea8();
  }
  param_1[0x10] = 0;
  lVar9 = param_1[0x11];
  if ((lVar9 != 0) && (iVar6 = *(int *)(lVar9 + 8) + -1, *(int *)(lVar9 + 8) = iVar6, iVar6 == 0)) {
    FUN_1002abea8();
  }
  param_1[0x11] = 0;
  lVar9 = param_1[0x12];
  if ((lVar9 != 0) && (iVar6 = *(int *)(lVar9 + 8) + -1, *(int *)(lVar9 + 8) = iVar6, iVar6 == 0)) {
    FUN_1002abea8();
  }
  param_1[0x12] = 0;
  lVar9 = param_1[0x13];
  if ((lVar9 != 0) && (iVar6 = *(int *)(lVar9 + 8) + -1, *(int *)(lVar9 + 8) = iVar6, iVar6 == 0)) {
    FUN_1002abea8();
  }
  param_1[0x13] = 0;
LAB_100137a18:
  local_51 = '\a';
  local_68 = (long *)&DAT_72656e6e616353;
  uVar7 = std::chrono::system_clock::now();
  FUN_10073cd34(&local_70,1,&local_68,uVar7);
  if (local_51 < '\0') {
    operator_delete(local_68);
  }
  iVar6 = FUN_1007396c0(&local_70);
  if (iVar6 != 0) {
    uVar7 = FUN_100736880(&local_70,"Start scan");
    uVar7 = FUN_100736880(uVar7," (");
    pcVar1 = "full";
    if (*(char *)(param_2 + 1) == '\0') {
      pcVar1 = "manual";
    }
    uVar7 = FUN_100736880(uVar7,pcVar1);
    uVar7 = FUN_100736880(uVar7,"): ");
    uVar7 = FUN_100736880(uVar7,"eventid: ");
    uVar7 = FUN_1007385b8(uVar7,*param_2);
    uVar7 = FUN_100736880(uVar7," number of files: ");
    FUN_1007386cc(uVar7,*(long *)(param_2 + 4) - *(long *)(param_2 + 2) >> 5);
  }
  thunk_FUN_1007363ec(&local_70);
  local_51 = '\a';
  local_68 = (long *)&DAT_72656e6e616353;
  uVar7 = std::chrono::system_clock::now();
  FUN_10073cd34(&local_70,1,&local_68,uVar7);
  if (local_51 < '\0') {
    operator_delete(local_68);
  }
  iVar6 = FUN_1007396c0(&local_70);
  if (iVar6 != 0) {
    FUN_100736880(&local_70,"Requested folders to scan:");
  }
  thunk_FUN_1007363ec(&local_70);
  lVar9 = *(long *)(param_2 + 2);
  lVar2 = *(long *)(param_2 + 4);
  if (lVar9 == lVar2) {
    local_51 = '\a';
    local_68 = (long *)&DAT_72656e6e616353;
    uVar7 = std::chrono::system_clock::now();
    FUN_10073cd34(&local_70,1,&local_68,uVar7);
    if (local_51 < '\0') {
      operator_delete(local_68);
    }
    iVar6 = FUN_1007396c0(&local_70);
    if (iVar6 != 0) {
      FUN_100736880(&local_70," --none--");
    }
    thunk_FUN_1007363ec(&local_70);
  }
  else {
    do {
      local_51 = '\a';
      local_68 = (long *)&DAT_72656e6e616353;
      uVar7 = std::chrono::system_clock::now();
      FUN_10073cd34(&local_70,1,&local_68,uVar7);
      if (local_51 < '\0') {
        operator_delete(local_68);
      }
      iVar6 = FUN_1007396c0(&local_70);
      if (iVar6 != 0) {
        uVar7 = FUN_100736880(&local_70,"  ");
        FUN_10013a004(uVar7,lVar9);
      }
      thunk_FUN_1007363ec(&local_70);
      lVar9 = lVar9 + 0x20;
    } while (lVar9 != lVar2);
  }
  *(undefined1 *)(param_1 + 0xf) = *(undefined1 *)(param_2 + 1);
  plVar8 = (long *)FUN_1002f80e4(0xf0);
  FUN_10015c574(plVar8,param_2,param_1 + 0x25);
  if (plVar8 != (long *)0x0) {
    *(int *)(plVar8 + 1) = (int)plVar8[1] + 1;
  }
  lVar9 = param_1[0x10];
  local_68 = plVar8;
  if ((lVar9 != 0) && (iVar6 = *(int *)(lVar9 + 8) + -1, *(int *)(lVar9 + 8) = iVar6, iVar6 == 0)) {
    FUN_1002abea8();
  }
  param_1[0x10] = plVar8;
  if (*(char *)(param_2 + 1) == '\x01') {
    if (*(long *)(param_2 + 2) == *(long *)(param_2 + 4)) {
      return;
    }
    (**(code **)(*(long *)*param_1 + 0x58))(&local_68);
    plVar5 = local_60;
    plVar4 = local_68;
    for (plVar8 = local_68; local_68 = plVar4, plVar8 != plVar5; plVar8 = plVar8 + 2) {
      if ((long *)plVar8[1] != (long *)0x0) {
        (**(code **)(*(long *)plVar8[1] + 8))(&local_70);
        FUN_10014269c(param_1,&local_70);
        if ((local_70 != (int *)0x0) && (iVar6 = *local_70, *local_70 = iVar6 + -1, iVar6 + -1 == 0)
           ) {
          FUN_100469e84();
        }
      }
      plVar4 = local_68;
    }
    plVar8 = local_60;
    if (plVar4 == (long *)0x0) {
      FUN_1001429a0(param_1);
      bVar3 = *(byte *)(param_2 + 1);
    }
    else {
      while (plVar8 != plVar4) {
        plVar8 = plVar8 + -2;
        lVar9 = *plVar8;
        if ((lVar9 != 0) &&
           (iVar6 = *(int *)(lVar9 + 8) + -1, *(int *)(lVar9 + 8) = iVar6, iVar6 == 0)) {
          FUN_1002abea8();
        }
      }
      local_60 = plVar4;
      operator_delete(local_68);
      FUN_1001429a0(param_1);
      bVar3 = *(byte *)(param_2 + 1);
    }
    if ((bVar3 & 1) != 0) {
      return;
    }
  }
  FUN_10013ff64(param_1,1);
  return;
}

