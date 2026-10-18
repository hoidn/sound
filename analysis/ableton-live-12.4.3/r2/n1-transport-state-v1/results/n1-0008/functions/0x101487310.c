
void FUN_101487310(long *param_1,long *param_2,undefined8 param_3)

{
  undefined4 *puVar1;
  undefined8 *puVar2;
  int iVar3;
  uint uVar4;
  code *pcVar5;
  bool bVar6;
  wchar16 wVar7;
  int iVar8;
  undefined4 uVar9;
  long lVar10;
  long lVar11;
  undefined8 uVar12;
  int *piVar13;
  longlong lVar14;
  undefined1 extraout_w1;
  long *plVar15;
  long lVar16;
  float fVar17;
  double dVar18;
  undefined1 auVar19 [16];
  int *local_60;
  int *local_58;
  
  lVar10 = (**(code **)(*param_2 + 0x150))(param_2);
  lVar16 = *(long *)(lVar10 + 8);
  do {
    if (lVar16 == lVar10) {
      return;
    }
    local_60 = *(int **)(lVar16 + 0x10);
    if (local_60 != (int *)0x0) {
      *local_60 = *local_60 + 1;
    }
    lVar11 = (**(code **)(*param_1 + 0x170))(param_1);
    lVar11 = FUN_10148c70c(lVar11 + 0x88,&local_60);
    if (lVar11 == 0) {
      lVar11 = 0;
    }
    else {
      lVar11 = *(long *)(lVar11 + 0x18);
      if ((lVar11 != 0) && (*(int *)(lVar11 + 8) == 0)) {
        FUN_10128eea0(lVar11);
      }
    }
    if ((local_60 != (int *)0x0) && (iVar8 = *local_60, *local_60 = iVar8 + -1, iVar8 + -1 == 0)) {
      FUN_101449efc();
    }
    if ((lVar11 == 0) || ((*(byte *)(lVar11 + 0x74) & 1) != 0)) goto switchD_101487448_caseD_1a;
    uVar12 = (**(code **)(**(long **)(lVar16 + 0x20) + 0x28))();
    iVar8 = FUN_10120e0f4(uVar12,lVar11 + 0x50);
    if (iVar8 != 0) {
      local_60 = *(int **)(lVar16 + 0x10);
      if (local_60 != (int *)0x0) {
        *local_60 = *local_60 + 1;
      }
      uVar12 = (**(code **)(**(long **)(lVar16 + 0x20) + 0x28))();
      FUN_1014867b0(param_1,param_3,&local_60,uVar12,lVar11 + 0x50);
                    /* WARNING: Does not return */
      pcVar5 = (code *)SoftwareBreakpoint(1,0x101487b1c);
      (*pcVar5)();
    }
    iVar8 = FUN_10120e310(lVar11 + 0x50);
    if (iVar8 == 0) {
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      plVar15 = *(long **)((long)plVar15 + (long)*(int *)(lVar11 + 0x38) + 8);
      uVar12 = *(undefined8 *)(lVar16 + 0x20);
      FUN_1011b5224();
      (**(code **)(*plVar15 + 200))(plVar15);
      (**(code **)(*plVar15 + 0x140))(plVar15,uVar12,param_3);
      iVar8 = FUN_1015192c0(param_3);
      if (iVar8 != 0) {
        uVar12 = FUN_1015183fc(param_3);
        (**(code **)(*plVar15 + 0xd0))(plVar15,uVar12);
      }
      goto switchD_101487448_caseD_1a;
    }
    uVar9 = FUN_10120e264(lVar11 + 0x50);
    switch(uVar9) {
    case 0x10:
      bVar6 = AAbstractNode::GetValue<bool>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      *(bool *)((long)plVar15 + (long)*(int *)(lVar11 + 0x38)) = bVar6;
      break;
    case 0x11:
      iVar8 = AAbstractNode::GetValue<int>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      *(int *)((long)plVar15 + (long)*(int *)(lVar11 + 0x38)) = iVar8;
      break;
    case 0x12:
      fVar17 = AAbstractNode::GetValue<float>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      *(float *)((long)plVar15 + (long)*(int *)(lVar11 + 0x38)) = fVar17;
      break;
    case 0x13:
      wVar7 = AAbstractNode::GetValue<char16_t>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      *(wchar16 *)((long)plVar15 + (long)*(int *)(lVar11 + 0x38)) = wVar7;
      break;
    case 0x14:
      AAbstractNode::GetValue<TString>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      iVar8 = *(int *)(lVar11 + 0x38);
      if (local_60 != (int *)0x0) {
        *local_60 = *local_60 + 1;
      }
      piVar13 = *(int **)((long)plVar15 + (long)iVar8);
      if ((piVar13 != (int *)0x0) && (iVar3 = *piVar13, *piVar13 = iVar3 + -1, iVar3 + -1 == 0)) {
        FUN_101449efc();
      }
      *(int **)((long)plVar15 + (long)iVar8) = local_60;
      if ((local_60 != (int *)0x0) && (iVar8 = *local_60, *local_60 = iVar8 + -1, iVar8 + -1 == 0))
      {
        FUN_101449efc();
      }
      break;
    case 0x15:
      lVar14 = AAbstractNode::GetValue<TBasicPoint<int>>();
      uVar4 = *(uint *)(lVar11 + 0x30);
      goto joined_r0x0001014879c0;
    case 0x16:
      auVar19 = AAbstractNode::GetValue<TBasicRect<int>>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      *(undefined1 (*) [16])((long)plVar15 + (long)*(int *)(lVar11 + 0x38)) = auVar19;
      break;
    case 0x17:
      dVar18 = AAbstractNode::GetValue<double>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      *(double *)((long)plVar15 + (long)*(int *)(lVar11 + 0x38)) = dVar18;
      break;
    case 0x18:
      lVar14 = AAbstractNode::GetValue<long_long>();
      uVar4 = *(uint *)(lVar11 + 0x30);
joined_r0x0001014879c0:
      plVar15 = param_1;
      if (-1 < (int)uVar4) {
        plVar15 = *(long **)((long)param_1 + (ulong)uVar4);
      }
      *(longlong *)((long)plVar15 + (long)*(int *)(lVar11 + 0x38)) = lVar14;
      break;
    case 0x19:
      uVar12 = AAbstractNode::GetValue<TIdentifier>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      puVar2 = (undefined8 *)((long)plVar15 + (long)*(int *)(lVar11 + 0x38));
      *puVar2 = uVar12;
      *(undefined1 *)(puVar2 + 1) = extraout_w1;
      break;
    case 0x20:
      AAbstractNode::GetValue<TClassId>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      puVar1 = (undefined4 *)((long)plVar15 + (long)*(int *)(lVar11 + 0x38));
      *puVar1 = local_60._0_4_;
      if (local_58 != (int *)0x0) {
        *local_58 = *local_58 + 1;
      }
      piVar13 = *(int **)(puVar1 + 2);
      if ((piVar13 != (int *)0x0) && (iVar8 = *piVar13, *piVar13 = iVar8 + -1, iVar8 + -1 == 0)) {
        FUN_101449efc();
      }
      *(int **)(puVar1 + 2) = local_58;
      if ((local_58 != (int *)0x0) && (iVar8 = *local_58, *local_58 = iVar8 + -1, iVar8 + -1 == 0))
      {
        FUN_101449efc();
      }
      break;
    case 0x30:
      AAbstractNode::GetValue<TArray<signed_char>>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      iVar8 = *(int *)(lVar11 + 0x38);
      if (local_60 != (int *)0x0) {
        *local_60 = *local_60 + 1;
      }
      piVar13 = *(int **)((long)plVar15 + (long)iVar8);
      if ((piVar13 != (int *)0x0) && (iVar3 = *piVar13, *piVar13 = iVar3 + -1, iVar3 + -1 == 0)) {
        FUN_101449efc();
      }
      *(int **)((long)plVar15 + (long)iVar8) = local_60;
      if ((local_60 != (int *)0x0) && (iVar8 = *local_60, *local_60 = iVar8 + -1, iVar8 + -1 == 0))
      {
        FUN_101449efc();
      }
      break;
    case 0x31:
      AAbstractNode::GetValue<TArray<unsigned_char>>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      iVar8 = *(int *)(lVar11 + 0x38);
      if (local_60 != (int *)0x0) {
        *local_60 = *local_60 + 1;
      }
      piVar13 = *(int **)((long)plVar15 + (long)iVar8);
      if ((piVar13 != (int *)0x0) && (iVar3 = *piVar13, *piVar13 = iVar3 + -1, iVar3 + -1 == 0)) {
        FUN_101449efc();
      }
      *(int **)((long)plVar15 + (long)iVar8) = local_60;
      if ((local_60 != (int *)0x0) && (iVar8 = *local_60, *local_60 = iVar8 + -1, iVar8 + -1 == 0))
      {
        FUN_101449efc();
      }
      break;
    case 0x32:
      AAbstractNode::GetValue<TArray<short>>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      iVar8 = *(int *)(lVar11 + 0x38);
      if (local_60 != (int *)0x0) {
        *local_60 = *local_60 + 1;
      }
      piVar13 = *(int **)((long)plVar15 + (long)iVar8);
      if ((piVar13 != (int *)0x0) && (iVar3 = *piVar13, *piVar13 = iVar3 + -1, iVar3 + -1 == 0)) {
        FUN_101449efc();
      }
      *(int **)((long)plVar15 + (long)iVar8) = local_60;
      if ((local_60 != (int *)0x0) && (iVar8 = *local_60, *local_60 = iVar8 + -1, iVar8 + -1 == 0))
      {
        FUN_101449efc();
      }
      break;
    case 0x33:
      AAbstractNode::GetValue<TArray<unsigned_short>>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      iVar8 = *(int *)(lVar11 + 0x38);
      if (local_60 != (int *)0x0) {
        *local_60 = *local_60 + 1;
      }
      piVar13 = *(int **)((long)plVar15 + (long)iVar8);
      if ((piVar13 != (int *)0x0) && (iVar3 = *piVar13, *piVar13 = iVar3 + -1, iVar3 + -1 == 0)) {
        FUN_101449efc();
      }
      *(int **)((long)plVar15 + (long)iVar8) = local_60;
      if ((local_60 != (int *)0x0) && (iVar8 = *local_60, *local_60 = iVar8 + -1, iVar8 + -1 == 0))
      {
        FUN_101449efc();
      }
      break;
    case 0x35:
      AAbstractNode::GetValue<TArray<int>>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      iVar8 = *(int *)(lVar11 + 0x38);
      if (local_60 != (int *)0x0) {
        *local_60 = *local_60 + 1;
      }
      piVar13 = *(int **)((long)plVar15 + (long)iVar8);
      if ((piVar13 != (int *)0x0) && (iVar3 = *piVar13, *piVar13 = iVar3 + -1, iVar3 + -1 == 0)) {
        FUN_101449efc();
      }
      *(int **)((long)plVar15 + (long)iVar8) = local_60;
      if ((local_60 != (int *)0x0) && (iVar8 = *local_60, *local_60 = iVar8 + -1, iVar8 + -1 == 0))
      {
        FUN_101449efc();
      }
      break;
    case 0x36:
      AAbstractNode::GetValue<TArray<unsigned_int>>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      iVar8 = *(int *)(lVar11 + 0x38);
      if (local_60 != (int *)0x0) {
        *local_60 = *local_60 + 1;
      }
      piVar13 = *(int **)((long)plVar15 + (long)iVar8);
      if ((piVar13 != (int *)0x0) && (iVar3 = *piVar13, *piVar13 = iVar3 + -1, iVar3 + -1 == 0)) {
        FUN_101449efc();
      }
      *(int **)((long)plVar15 + (long)iVar8) = local_60;
      if ((local_60 != (int *)0x0) && (iVar8 = *local_60, *local_60 = iVar8 + -1, iVar8 + -1 == 0))
      {
        FUN_101449efc();
      }
      break;
    case 0x40:
      AAbstractNode::GetValue<TArray<float>>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      iVar8 = *(int *)(lVar11 + 0x38);
      if (local_60 != (int *)0x0) {
        *local_60 = *local_60 + 1;
      }
      piVar13 = *(int **)((long)plVar15 + (long)iVar8);
      if ((piVar13 != (int *)0x0) && (iVar3 = *piVar13, *piVar13 = iVar3 + -1, iVar3 + -1 == 0)) {
        FUN_101449efc();
      }
      *(int **)((long)plVar15 + (long)iVar8) = local_60;
      if ((local_60 != (int *)0x0) && (iVar8 = *local_60, *local_60 = iVar8 + -1, iVar8 + -1 == 0))
      {
        FUN_101449efc();
      }
      break;
    case 0x50:
      AAbstractNode::GetValue<TArray<bool>>();
      plVar15 = param_1;
      if (-1 < (int)*(uint *)(lVar11 + 0x30)) {
        plVar15 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar11 + 0x30));
      }
      iVar8 = *(int *)(lVar11 + 0x38);
      if (local_60 != (int *)0x0) {
        *local_60 = *local_60 + 1;
      }
      piVar13 = *(int **)((long)plVar15 + (long)iVar8);
      if ((piVar13 != (int *)0x0) && (iVar3 = *piVar13, *piVar13 = iVar3 + -1, iVar3 + -1 == 0)) {
        FUN_101449efc();
      }
      *(int **)((long)plVar15 + (long)iVar8) = local_60;
      if ((local_60 != (int *)0x0) && (iVar8 = *local_60, *local_60 = iVar8 + -1, iVar8 + -1 == 0))
      {
        FUN_101449efc();
      }
    }
switchD_101487448_caseD_1a:
    lVar16 = *(long *)(lVar16 + 8);
  } while( true );
}

