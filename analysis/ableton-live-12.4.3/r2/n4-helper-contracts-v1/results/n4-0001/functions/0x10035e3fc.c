
/* void ableton::utility::detail::CallbackTypes<APluginSettingsPreferencesModel, void, ARemoteable*,
   TRemoteableUpdate>::CallMemberFunc<&APluginSettingsPreferencesModel::OnRescanPlugins>(void*,
   ARemoteable*, TRemoteableUpdate) */

void ableton::utility::detail::
     CallbackTypes<APluginSettingsPreferencesModel,void,ARemoteable*,TRemoteableUpdate>::
     CallMemberFunc<&APluginSettingsPreferencesModel::OnRescanPlugins>
               (long param_1,undefined8 param_2,int param_3)

{
  long *plVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined4 local_28;
  undefined4 local_24;
  
  if (param_3 != 4) {
    plVar1 = (long *)FUN_10178f9d0(*(undefined8 *)(param_1 + 0x28));
    local_24 = (**(code **)(*plVar1 + 0x570))();
    local_28 = FUN_101294398();
    uVar2 = FUN_1012946e8(&local_24,&local_28);
    uVar3 = FUN_103168da4();
    FUN_10316a4c0(uVar3,uVar2);
    (**(code **)(**(long **)(param_1 + 0x168) + 0x248))(*(long **)(param_1 + 0x168),1);
  }
  return;
}

