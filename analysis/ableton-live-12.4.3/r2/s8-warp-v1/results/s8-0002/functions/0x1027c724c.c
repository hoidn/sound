
void FUN_1027c724c(double param_1,double param_2,undefined8 param_3,long *param_4)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  long *plVar3;
  long lVar4;
  double dVar5;
  double dVar6;
  double dVar7;
  long local_58;
  long local_50;
  long *local_48;
  
  plVar3 = (long *)param_4[0xcb];
  puVar1 = (undefined8 *)(**(code **)(*plVar3 + 0x60))(plVar3);
  local_58 = (**(code **)*puVar1)(puVar1,plVar3);
  local_50 = *(long *)(local_58 + 0x20);
  local_48 = plVar3;
  if (local_50 == *(long *)(local_58 + 0x18)) goto LAB_1027c72ec;
LAB_1027c72ac:
  lVar4 = *(long *)(local_50 + 0x20);
  if (lVar4 == 0) goto LAB_1027c72ec;
  plVar3 = (long *)(**(code **)(*local_48 + 0x60))();
  lVar4 = (**(code **)(*plVar3 + 0x20))(plVar3,local_48,lVar4);
  dVar5 = (double)FUN_10261026c(*(undefined8 *)(lVar4 + 8));
  lVar4 = local_50;
  do {
    local_50 = lVar4;
    if (dVar5 < param_1) {
      uVar2 = 0;
      if ((lVar4 != 0) && (lVar4 != local_58)) {
        plVar3 = (long *)(**(code **)(*local_48 + 0x60))();
        lVar4 = (**(code **)(*plVar3 + 0x20))(plVar3,local_48,lVar4);
        uVar2 = *(undefined8 *)(lVar4 + 8);
      }
      FUN_10261025c(param_1,param_2,uVar2);
      lVar4 = param_4[0xcb];
      uVar2 = (**(code **)(*param_4 + 0x2d0))(param_4);
      FUN_102612464(param_3,uVar2,lVar4);
      lVar4 = *(long *)(local_50 + 0x20);
      if (lVar4 == *(long *)(local_58 + 0x18)) {
        return;
      }
      local_50 = lVar4;
      if (lVar4 == 0 || lVar4 == local_58) {
        dVar5 = (double)FUN_10261026c(0);
        if (local_50 == *(long *)(local_58 + 0x18)) goto LAB_1027c7478;
LAB_1027c742c:
        lVar4 = *(long *)(local_50 + 0x20);
        if (lVar4 == 0) goto LAB_1027c7478;
        plVar3 = (long *)(**(code **)(*local_48 + 0x60))();
        lVar4 = (**(code **)(*plVar3 + 0x20))(plVar3,local_48,lVar4);
        dVar6 = (double)FUN_10261026c(*(undefined8 *)(lVar4 + 8));
        if (local_50 != *(long *)(local_58 + 0x18)) goto LAB_1027c7494;
      }
      else {
        plVar3 = (long *)(**(code **)(*local_48 + 0x60))();
        lVar4 = (**(code **)(*plVar3 + 0x20))(plVar3,local_48,lVar4);
        dVar5 = (double)FUN_10261026c(*(undefined8 *)(lVar4 + 8));
        if (local_50 != *(long *)(local_58 + 0x18)) goto LAB_1027c742c;
LAB_1027c7478:
        dVar6 = (double)FUN_10261026c(0);
        if (local_50 != *(long *)(local_58 + 0x18)) {
LAB_1027c7494:
          lVar4 = *(long *)(local_50 + 0x20);
          if (lVar4 != 0) {
            plVar3 = (long *)(**(code **)(*local_48 + 0x60))();
            lVar4 = (**(code **)(*plVar3 + 0x20))(plVar3,local_48,lVar4);
            uVar2 = *(undefined8 *)(lVar4 + 8);
            goto LAB_1027c74cc;
          }
        }
      }
      uVar2 = 0;
LAB_1027c74cc:
      dVar7 = (double)FUN_102610264(uVar2);
      lVar4 = local_50;
      uVar2 = 0;
      dVar5 = (dVar5 - dVar6) / (param_1 - dVar6);
      if ((local_50 != 0) && (local_50 != local_58)) {
        plVar3 = (long *)(**(code **)(*local_48 + 0x60))();
        lVar4 = (**(code **)(*plVar3 + 0x20))(plVar3,local_48,lVar4);
        uVar2 = *(undefined8 *)(lVar4 + 8);
      }
      dVar6 = (double)FUN_102610264(uVar2);
      if (ABS(dVar6 - ((dVar7 - dVar7 * dVar5) + param_2 * dVar5)) < 0.001) {
        plVar3 = (long *)(**(code **)(*local_48 + 0x60))();
        (**(code **)(*plVar3 + 0x18))(plVar3,local_48,&local_58);
      }
      return;
    }
    plVar3 = (long *)(**(code **)(*local_48 + 0x60))();
    (**(code **)(*plVar3 + 0x18))(plVar3,local_48,&local_58);
    local_50 = *(long *)(local_58 + 0x20);
    if (local_50 != *(long *)(local_58 + 0x18)) goto LAB_1027c72ac;
LAB_1027c72ec:
    dVar5 = (double)FUN_10261026c(0);
    lVar4 = local_50;
  } while( true );
}

