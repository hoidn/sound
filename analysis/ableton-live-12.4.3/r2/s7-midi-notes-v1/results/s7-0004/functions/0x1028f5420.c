
void FUN_1028f5420(long param_1,undefined8 param_2,undefined8 param_3,int param_4)

{
  undefined *puVar1;
  int iVar2;
  uint uVar3;
  int iVar4;
  undefined8 uVar5;
  ulong uVar6;
  undefined8 uVar7;
  long lVar8;
  long lVar9;
  long lVar10;
  undefined8 *local_60;
  long lStack_58;
  undefined8 local_50;
  undefined1 uStack_41;
  
  if (0xfffffffd < param_4 - 3U) {
    uVar5 = FUN_10156da2c(*(undefined8 *)(param_1 + 0x430),param_3);
    iVar4 = (int)param_3;
    if (param_4 == 2) {
      uVar6 = FUN_101542640();
      if ((uVar6 & 1) == 0) {
        uVar7 = FUN_1028abe68(uVar5);
        iVar2 = FUN_10155ede4();
        if (iVar2 != 0) {
          lVar8 = FUN_10155ee2c(uVar7,0);
          uVar3 = FUN_10155ede4(uVar7);
          puVar1 = PTR_piecewise_construct_106537430;
          if (uVar3 != 0) {
            if ((int)uVar3 < 1) {
              FUN_105424d70();
LAB_1028f5618:
              lVar8 = FUN_105424d50();
              if (iVar4 != 4) {
                *(undefined1 *)(lVar8 + 0x589) = 1;
              }
              return;
            }
            lVar10 = (ulong)uVar3 * 0x30;
            do {
              local_50 = FUN_1028da61c(lVar8);
              local_60 = &local_50;
              lVar9 = FUN_10290fe58(param_1 + 0x560,&local_50,puVar1,&local_60,&uStack_41);
              *(int *)(lVar9 + 0x18) = *(int *)(lVar9 + 0x18) + -1;
              lVar8 = lVar8 + 0x30;
              lVar10 = lVar10 + -0x30;
            } while (lVar10 != 0);
          }
        }
      }
      uVar7 = FUN_1028abe68(uVar5);
      local_60 = (undefined8 *)PTR_CallMemberFunc<&AMidiNotes::OnKeyTrackUpdate>_10652a008;
      lStack_58 = param_1;
      FUN_10155f028(uVar7,param_1,&local_60);
      iVar4 = FUN_1028aca40(uVar5);
      *(undefined8 *)(param_1 + (long)iVar4 * 8 + 0x28) = 0;
    }
    else {
      uVar7 = FUN_1028abe68(uVar5);
      local_60 = (undefined8 *)PTR_CallMemberFunc<&AMidiNotes::OnKeyTrackUpdate>_10652a008;
      lStack_58 = param_1;
      iVar4 = (int)&local_60;
      FUN_10155ee3c(uVar7,param_1,&local_60,1);
      iVar2 = FUN_1028aca40(uVar5);
      *(undefined8 *)(param_1 + (long)iVar2 * 8 + 0x28) = uVar5;
      uVar6 = FUN_101542640();
      if ((uVar6 & 1) == 0) {
        uVar5 = FUN_1028abe68(uVar5);
        iVar2 = FUN_10155ede4();
        if (iVar2 != 0) {
          lVar8 = FUN_10155ee2c(uVar5,0);
          uVar3 = FUN_10155ede4(uVar5);
          puVar1 = PTR_piecewise_construct_106537430;
          if (uVar3 != 0) {
            if ((int)uVar3 < 1) goto LAB_1028f5618;
            lVar10 = (ulong)uVar3 * 0x30;
            do {
              local_50 = FUN_1028da61c(lVar8);
              local_60 = &local_50;
              lVar9 = FUN_10290fe58(param_1 + 0x560,&local_50,puVar1,&local_60,&uStack_41);
              *(int *)(lVar9 + 0x18) = *(int *)(lVar9 + 0x18) + 1;
              lVar8 = lVar8 + 0x30;
              lVar10 = lVar10 + -0x30;
            } while (lVar10 != 0);
          }
        }
      }
    }
    *(undefined1 *)(param_1 + 0x588) = 1;
  }
  return;
}

