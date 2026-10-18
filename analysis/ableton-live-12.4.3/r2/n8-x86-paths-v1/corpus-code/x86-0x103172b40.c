// x86 0x103172b40 FUN_103172b40 state=exported-with-warnings chunk=chunk-02309.jsonl code_sha256=9a87f3d85911177efde64f5eee210034bebbdc66a1d97be771d35173df76a26f

void FUN_103172b40(undefined8 param_1,undefined8 param_2,undefined4 param_3,undefined8 param_4,
                  undefined8 *param_5,undefined4 param_6,undefined1 param_7,undefined8 *param_8)

{
  void *pvVar1;
  void *pvVar2;
  ulong uVar3;
  
  *param_5 = param_1;
  param_5[1] = param_2;
  *(undefined4 *)(param_5 + 2) = param_3;
  *(undefined4 *)((long)param_5 + 0x14) = param_6;
  param_5[3] = param_4;
  *(undefined1 *)(param_5 + 4) = 1;
  *(undefined1 *)((long)param_5 + 0x21) = param_7;
  param_5[5] = 0;
  param_5[6] = 0;
  param_5[7] = 0;
  pvVar1 = (void *)*param_8;
  uVar3 = param_8[1] - (long)pvVar1;
  if (uVar3 != 0) {
    if ((long)uVar3 < 0) {
                    /* WARNING: Subroutine does not return */
      FUN_10317e620(param_5 + 5);
    }
    pvVar2 = operator_new(uVar3);
    param_5[5] = pvVar2;
    param_5[6] = pvVar2;
    param_5[7] = (long)pvVar2 + uVar3;
    _memcpy(pvVar2,pvVar1,uVar3);
    param_5[6] = (long)pvVar2 + uVar3;
  }
  return;
}

