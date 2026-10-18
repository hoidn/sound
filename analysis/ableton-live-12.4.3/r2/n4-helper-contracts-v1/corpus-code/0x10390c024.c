// 0x10390c024 FUN_10390c024 exported  sig: undefined FUN_10390c024()

undefined8 FUN_10390c024(undefined8 param_1,long param_2,undefined8 param_3)

{
  undefined *puVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  undefined8 *puVar4;
  long lVar5;
  undefined4 *local_60 [3];
  long local_48;
  undefined *local_40;
  undefined8 uStack_38;
  
  puVar2 = (undefined8 *)FUN_1038f1fcc(param_1,param_3,param_2);
  *puVar2 = &PTR_FUN_106a3f088;
  *(undefined2 *)(puVar2 + 0x30) = 1;
  *(undefined1 *)((long)puVar2 + 0x182) = 0;
  puVar2[0x31] = 0;
  *(undefined4 *)(puVar2 + 0x32) = 0;
  FUN_101458fc8(local_60,param_1);
  puVar1 = PTR_CallMemberFunc<&TPushClientConnection::OnFlipModelChanged>_106530e28;
  local_60[0] = &DAT_106592510;
  local_40 = PTR_CallMemberFunc<&TPushClientConnection::OnFlipModelChanged>_106530e28;
  puVar2 = *(undefined8 **)(param_2 + 0x240);
  uStack_38 = param_1;
  if (puVar2 < *(undefined8 **)(param_2 + 0x248)) {
    puVar3 = puVar2 + 2;
    *puVar3 = 0;
    puVar2[1] = 0;
    puVar2[3] = local_48;
    if (local_48 != 0) {
      lVar5 = *(long *)(local_48 + 0x10);
      puVar4 = puVar2;
      if (lVar5 != 0) {
        puVar3 = (undefined8 *)(lVar5 + 8);
        puVar4 = (undefined8 *)*puVar3;
        puVar2[2] = lVar5;
        puVar4[2] = puVar2;
      }
      puVar2[1] = puVar4;
      *puVar3 = puVar2;
      *(undefined8 **)(local_48 + 0x10) = puVar2;
    }
    *puVar2 = &DAT_106592510;
    puVar2[5] = param_1;
    puVar2[4] = puVar1;
    puVar2 = puVar2 + 6;
  }
  else {
    puVar2 = (undefined8 *)FUN_1039ba280(param_2 + 0x238,local_60);
  }
  *(undefined8 **)(param_2 + 0x240) = puVar2;
  FUN_101459068(local_60);
  return param_1;
}


