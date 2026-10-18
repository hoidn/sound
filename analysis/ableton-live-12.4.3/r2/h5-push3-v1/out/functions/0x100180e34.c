// 0x100180e34 FUN_100180e34 state=exported role=nanomsg send wrapper
// source chunk chunk-00065.jsonl; code_sha256=8ff03ea39d461c2156abae1de4b38a0f01cac2e1af41790b0dddd9e2684e1fe5

undefined8 FUN_100180e34(long *param_1,long *param_2,int param_3)

{
  int iVar1;
  
  iVar1 = (**(code **)(*param_1 + 0x10))();
  if (iVar1 != 0) {
    iVar1 = FUN_100a1c590(param_1[1],(int)param_1[3],*param_2,param_2[1] - *param_2,param_3 == 1);
    if (iVar1 != -1) {
      return 0;
    }
    iVar1 = thunk_FUN_100a35af0(param_1[1]);
    if ((param_3 == 1) && (iVar1 == 0x23)) {
      return 2;
    }
    if ((param_3 == 0) && (iVar1 == 0x3c)) {
      return 3;
    }
    FUN_1001813c4(param_1);
  }
  return 1;
}

