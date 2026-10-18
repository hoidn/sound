// 0x1002fcc08 ableton::utility::detail::CallbackTypes<ALiveApp,void,ADefaultApp*>::CallMemberFunc<&ALiveApp::StartAppAddOns> exported-with-warnings  sig: void __cdecl CallMemberFunc<&ALiveApp::StartAppAddOns>(void * param_1, ADefaultApp * param_2)

/* void ableton::utility::detail::CallbackTypes<ALiveApp, void,
   ADefaultApp*>::CallMemberFunc<&ALiveApp::StartAppAddOns>(void*, ADefaultApp*) */

void ableton::utility::detail::CallbackTypes<ALiveApp,void,ADefaultApp*>::
     CallMemberFunc<&ALiveApp::StartAppAddOns>(void *param_1,ADefaultApp *param_2)

{
  int iVar1;
  long lVar2;
  int *piStack_60;
  long lStack_58;
  long *plStack_50;
  undefined **appuStack_48 [3];
  undefined ***pppuStack_30;
  long lStack_28;
  
  lStack_28 = *(long *)PTR____stack_chk_guard_1064f8818;
  FUN_1029650f8(&lStack_58);
  FUN_1011db828(&piStack_60);
  appuStack_48[0] = &PTR_FUN_10659d0c8;
  pppuStack_30 = appuStack_48;
  (**(code **)(*plStack_50 + 0x28))(plStack_50,&piStack_60,appuStack_48,600000);
  if (pppuStack_30 == appuStack_48) {
    lVar2 = 0x20;
  }
  else {
    if (pppuStack_30 == (undefined ***)0x0) goto LAB_1002cad84;
    lVar2 = 0x28;
  }
  (**(code **)((long)*pppuStack_30 + lVar2))();
LAB_1002cad84:
  if (piStack_60 != (int *)0x0) {
    iVar1 = *piStack_60;
    *piStack_60 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (lStack_58 != 0) {
    iVar1 = *(int *)(lStack_58 + 8) + -1;
    *(int *)(lStack_58 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == lStack_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


