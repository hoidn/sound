
/* WARNING: Removing unreachable block (ram,0x000102966574) */
/* WARNING: Removing unreachable block (ram,0x0001029662f4) */
/* WARNING: Removing unreachable block (ram,0x000102966320) */
/* WARNING: Removing unreachable block (ram,0x00010296653c) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_102966254(long param_1)

{
  undefined6 uVar1;
  undefined2 uVar2;
  int iVar3;
  long *plVar4;
  undefined8 uVar5;
  int *piVar6;
  undefined8 *puVar7;
  undefined8 *puVar8;
  undefined8 uVar9;
  int **local_a0;
  undefined *puStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  long *local_78;
  int *local_70;
  undefined6 local_68;
  undefined2 uStack_62;
  undefined6 local_60;
  undefined1 uStack_5a;
  undefined1 uStack_59;
  undefined8 local_58;
  undefined1 local_50 [24];
  int *local_38;
  
  FUN_1014412dc(&local_38,7);
  plVar4 = operator_new(0x58);
  FUN_1014320f0(local_50,&local_38);
  FUN_1002725dc(&local_a0,local_50,0);
  *plVar4 = (long)&PTR_thunk_FUN_10027a25c_1065928b0;
  plVar4[1] = (long)(plVar4 + 2);
  *(undefined8 *)((long)plVar4 + 0x14) = DAT_1055d3960;
  *(undefined4 *)((long)plVar4 + 0x1c) = 0xffffffff;
  if (local_90 < 0) {
    FUN_10023448c(plVar4 + 4,local_a0,puStack_98);
    *(undefined4 *)(plVar4 + 7) = 0;
    plVar4[9] = 0;
    plVar4[10] = 0;
    plVar4[8] = 0;
    if (local_90 < 0) {
      operator_delete(local_a0);
    }
  }
  else {
    plVar4[5] = (long)puStack_98;
    plVar4[4] = (long)local_a0;
    plVar4[6] = local_90;
    *(undefined4 *)(plVar4 + 7) = 0;
    plVar4[9] = 0;
    plVar4[10] = 0;
    plVar4[8] = 0;
  }
  local_a0 = (int **)CONCAT17(local_a0._7_1_,0x736e4f646441);
  local_90._7_1_ = '\x06';
  local_68._0_1_ = s_Ableton_AddOns_105bd3bb8[0];
  local_68._1_1_ = s_Ableton_AddOns_105bd3bb8[1];
  local_68._2_1_ = s_Ableton_AddOns_105bd3bb8[2];
  local_68._3_1_ = s_Ableton_AddOns_105bd3bb8[3];
  local_68._4_1_ = s_Ableton_AddOns_105bd3bb8[4];
  local_68._5_1_ = s_Ableton_AddOns_105bd3bb8[5];
  uStack_62._0_1_ = s_Ableton_AddOns_105bd3bb8[6];
  uStack_62._1_1_ = s_Ableton_AddOns_105bd3bb8[7];
  local_60._0_1_ = s_Ableton_AddOns_105bd3bb8[8];
  local_60._1_1_ = s_Ableton_AddOns_105bd3bb8[9];
  local_60._2_1_ = s_Ableton_AddOns_105bd3bb8[10];
  local_60._3_1_ = s_Ableton_AddOns_105bd3bb8[0xb];
  local_60._4_1_ = s_Ableton_AddOns_105bd3bb8[0xc];
  local_60._5_1_ = s_Ableton_AddOns_105bd3bb8[0xd];
  uStack_5a = 0;
  local_58._7_1_ = '\x0e';
  FUN_1011e8540(local_50,&local_a0,&local_68);
  if (local_58._7_1_ < '\0') {
    operator_delete((void *)CONCAT26(uStack_62,local_68));
  }
  if (local_90._7_1_ < '\0') {
    operator_delete(local_a0);
  }
  local_68 = 0;
  uStack_62 = 0;
  local_60 = 0;
  uStack_5a = 0;
  uStack_59 = 0;
  local_58 = (undefined8 *)0x0;
  local_a0 = &local_38;
  puStack_98 = PTR_format_custom<TString>_106509e70;
  FUN_10143e88c(&local_70,L"--cid={}",8,0xf,&local_a0);
  puVar7 = (undefined8 *)CONCAT17(uStack_59,CONCAT16(uStack_5a,local_60));
  if (puVar7 < local_58) {
    *puVar7 = 0;
    puVar8 = puVar7 + 1;
    *puVar7 = local_70;
    local_60 = SUB86(puVar8,0);
    uStack_5a = (undefined1)((ulong)puVar8 >> 0x30);
    uStack_59 = (undefined1)((ulong)puVar8 >> 0x38);
  }
  else {
    uVar5 = FUN_10025cbfc(&local_68,&local_70);
    local_60 = (undefined6)uVar5;
    uStack_5a = (undefined1)((ulong)uVar5 >> 0x30);
    uStack_59 = (undefined1)((ulong)uVar5 >> 0x38);
    if ((local_70 != (int *)0x0) && (iVar3 = *local_70, *local_70 = iVar3 + -1, iVar3 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  uVar5 = std::chrono::system_clock::now();
  FUN_103f3ffec(&local_a0,2,uVar5);
  iVar3 = FUN_103f3c8b8(&local_a0);
  if (iVar3 != 0) {
    FUN_103f39a78(&local_a0,"AddOns: start process");
  }
  thunk_FUN_103f395e4(&local_a0);
  uVar9 = *(undefined8 *)(param_1 + 0x48);
  puStack_98 = (undefined *)_UNK_10589a12c;
  local_a0 = _DAT_10589a124;
  uStack_88 = _UNK_10589a13c;
  local_90 = _DAT_10589a134;
  local_78 = plVar4;
  uVar5 = FUN_1014416b0(&local_a0,2);
  FUN_1025da348(uVar9,local_50,&local_68,&local_78,1,uVar5);
  plVar4 = local_78;
  local_78 = (long *)0x0;
  if (plVar4 != (long *)0x0) {
    (**(code **)(*plVar4 + 8))();
  }
  uVar2 = uStack_62;
  uVar1 = local_68;
  *(int *)(param_1 + 100) = *(int *)(param_1 + 100) + 1;
  puVar7 = (undefined8 *)CONCAT26(uStack_62,local_68);
  if (puVar7 != (undefined8 *)0x0) {
    puVar8 = (undefined8 *)CONCAT17(uStack_59,CONCAT16(uStack_5a,local_60));
    if (puVar8 != puVar7) {
      do {
        puVar8 = puVar8 + -1;
        piVar6 = (int *)*puVar8;
        if ((piVar6 != (int *)0x0) && (iVar3 = *piVar6, *piVar6 = iVar3 + -1, iVar3 + -1 == 0)) {
          FUN_101449efc();
        }
      } while (puVar8 != puVar7);
      puVar7 = (undefined8 *)CONCAT26(uStack_62,local_68);
    }
    local_60 = uVar1;
    uStack_5a = (undefined1)uVar2;
    uStack_59 = (undefined1)((ushort)uVar2 >> 8);
    operator_delete(puVar7);
  }
  if ((local_38 != (int *)0x0) && (iVar3 = *local_38, *local_38 = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_101449efc();
  }
  return;
}

