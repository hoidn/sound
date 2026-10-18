// eng 0xe7400 OEngineReWireData::IsReWireDeviceNameAnAbletonOne state=exported-with-warnings chunk=chunk-00044.jsonl code_sha256=86b8024df8e24dc7db9f2540530fa5567d12ba7c1d5f422abeef6e55cd8ed5a2

/* OEngineReWireData::IsReWireDeviceNameAnAbletonOne(char const*) const */

ulong __thiscall
OEngineReWireData::IsReWireDeviceNameAnAbletonOne(OEngineReWireData *this,char *param_1)

{
  long *plVar1;
  void *pvVar2;
  ulong uVar3;
  size_t sVar4;
  void *pvVar5;
  long *plVar6;
  void *pvVar7;
  long *plVar8;
  ulong uVar9;
  undefined8 local_48;
  size_t local_40;
  void *local_38;
  
  if (param_1 == (char *)0x0) {
    uVar9 = 0;
    goto LAB_000e753f;
  }
  sVar4 = _strlen(param_1);
  if (0xfffffffffffffff7 < sVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00040c70(&local_48);
  }
  pvVar2 = (void *)((long)&local_48 + 1);
  if (sVar4 < 0x17) {
    local_48 = CONCAT71(local_48._1_7_,(char)sVar4 * '\x02');
    pvVar5 = pvVar2;
    if (sVar4 != 0) goto LAB_000e7484;
  }
  else {
    uVar9 = 0x1a;
    if ((sVar4 | 7) != 0x17) {
      uVar9 = (sVar4 | 7) + 1;
    }
    pvVar5 = operator_new(uVar9);
    local_48 = uVar9 + 1;
    local_40 = sVar4;
    local_38 = pvVar5;
LAB_000e7484:
    _memcpy(pvVar5,param_1,sVar4);
  }
  uVar3 = local_48;
  *(undefined1 *)((long)pvVar5 + sVar4) = 0;
  pvVar5 = local_38;
  uVar9 = local_48 >> 1 & 0x7f;
  if ((local_48 & 1) != 0) {
    uVar9 = local_40;
    pvVar2 = local_38;
  }
  if ((long)uVar9 < 0xc) {
    uVar9 = 0;
  }
  else {
    plVar1 = (long *)(uVar9 + (long)pvVar2);
    pvVar7 = pvVar2;
    do {
      plVar6 = _memchr(pvVar7,0x41,uVar9 - 0xb);
      plVar8 = plVar1;
      if ((plVar6 == (long *)0x0) ||
         (plVar8 = plVar6, (int)plVar6[1] == 0x6576694c && *plVar6 == 0x206e6f74656c6241)) break;
      pvVar7 = (void *)((long)plVar6 + 1);
      uVar9 = (long)plVar1 - (long)pvVar7;
      plVar8 = plVar1;
    } while (0xb < (long)uVar9);
    uVar9 = CONCAT71((int7)((ulong)plVar1 >> 8),
                     (long)plVar8 - (long)pvVar2 != -1 && plVar8 != plVar1);
  }
  if ((uVar3 & 1) != 0) {
    operator_delete(pvVar5);
  }
LAB_000e753f:
  return uVar9 & 0xffffffff;
}

