// 0x101447d84 FUN_101447d84 exported  sig: undefined FUN_101447d84()

void FUN_101447d84(undefined4 param_1,long *param_2)

{
  long *plVar1;
  long *plVar2;
  long lVar3;
  
  std::mutex::lock();
  if ((long **)DAT_106f4f248 != &DAT_106f4f240) {
    plVar2 = DAT_106f4f248;
    do {
      if (plVar2[4] == param_2[1] && plVar2[3] == *param_2) {
        if (plVar2 == DAT_106f4f190) {
          DAT_106f4f190 = (long *)DAT_106f4f190[1];
        }
        lVar3 = *plVar2;
        plVar1 = (long *)plVar2[1];
        *(long **)(lVar3 + 8) = plVar1;
        *plVar1 = lVar3;
        DAT_106f4f250 = DAT_106f4f250 + -1;
        operator_delete(plVar2);
        break;
      }
      plVar2 = (long *)plVar2[1];
    } while ((long **)plVar2 != &DAT_106f4f240);
  }
  std::mutex::unlock();
  std::mutex::lock();
  plVar2 = operator_new(0x38);
  *plVar2 = 0;
  plVar2[1] = 0;
  *(undefined4 *)(plVar2 + 2) = param_1;
  lVar3 = *param_2;
  plVar2[4] = param_2[1];
  plVar2[3] = lVar3;
  FUN_1011b5a40(plVar2 + 5);
  *plVar2 = (long)DAT_106f4f240;
  plVar2[1] = (long)&DAT_106f4f240;
  *(long **)((long)DAT_106f4f240 + 8) = plVar2;
  DAT_106f4f250 = DAT_106f4f250 + 1;
  DAT_106f4f240 = plVar2;
  std::mutex::unlock();
  return;
}


