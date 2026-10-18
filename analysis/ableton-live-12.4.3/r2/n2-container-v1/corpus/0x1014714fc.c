
void FUN_1014714fc(undefined4 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  undefined8 local_48;
  undefined8 uStack_40;
  undefined4 local_34;
  
  puVar1 = DAT_106f4f608;
  local_48 = param_3;
  uStack_40 = param_2;
  local_34 = param_1;
  if (DAT_106f4f608 < DAT_106f4f610) {
    puVar2 = DAT_106f4f608 + 2;
    *DAT_106f4f608 = param_1;
    FUN_10146bd64(puVar2,param_3);
    *(undefined8 *)(puVar1 + 8) = param_2;
    DAT_106f4f608 = puVar1 + 10;
    return;
  }
  DAT_106f4f608 = (undefined4 *)FUN_10147859c(&DAT_106f4f600,&local_34,&uStack_40,&local_48);
  return;
}

