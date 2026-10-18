
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1024b5060(long param_1,undefined8 param_2,undefined4 param_3)

{
  int *piVar1;
  char cVar2;
  int iVar3;
  undefined4 uVar4;
  int iVar5;
  undefined8 uVar6;
  long lVar7;
  long lVar8;
  ulong extraout_RDX;
  ulong extraout_RDX_00;
  ulong extraout_RDX_01;
  int iVar9;
  undefined1 local_90 [16];
  long local_80;
  long local_78;
  undefined8 local_70;
  int *local_68;
  int *local_60;
  undefined8 local_58;
  undefined4 uStack_50;
  undefined4 uStack_4c;
  undefined8 local_48;
  undefined8 uStack_40;
  int local_34;
  
  cVar2 = FUN_101ab6780();
  if (cVar2 != '\0') {
    local_48 = _DAT_105de827c;
    uStack_40 = _UNK_105de8284;
    local_58 = CONCAT44(_UNK_105de8270,_DAT_105de826c);
    uStack_50 = _UNK_105de8274;
    uStack_4c = _UNK_105de8278;
    FUN_101188890(&local_58);
    if ((extraout_RDX & 1) == 0) {
      cVar2 = FUN_101198610();
      if (cVar2 != '\0') {
        FUN_1024b0300();
      }
    }
  }
  cVar2 = FUN_101ab68f0();
  if (cVar2 != '\0') {
    iVar3 = FUN_10118fec0();
    if (iVar3 == 0) {
      uVar6 = std::chrono::system_clock::now();
      FUN_10410fff0(&local_58,2,uVar6);
      cVar2 = FUN_10410c530(&local_58);
      if (cVar2 != '\0') {
        FUN_104108bf0(&local_58,"ReWire: ReWireHost Open");
      }
      FUN_104108a10(&local_58);
      uVar4 = FUN_101b2d2e0();
      FUN_1024b5410(local_90,param_3,uVar4);
      iVar3 = FUN_1024b54d0(local_90);
      if (iVar3 == 1) {
        *(undefined4 *)(param_1 + 0x40) = 0;
        local_34 = 0;
        iVar3 = FUN_1024b5610(&local_34);
        if (iVar3 == 1) {
          local_78 = param_1 + 0x38;
          FUN_101442600(local_78,local_34 << 3);
          uVar6 = FUN_101ac77d0(0x68);
          FUN_101b2ce90(uVar6,param_2,local_34);
          *(undefined8 *)(param_1 + 0x48) = uVar6;
          local_70 = param_2;
          if (local_34 < 1) {
            iVar3 = 0;
          }
          else {
            iVar9 = 0;
            iVar3 = 0;
            do {
              lVar7 = FUN_1012bd9b0(0x20c0);
              FUN_1024b2f50(lVar7);
              if (lVar7 != 0) {
                *(int *)(lVar7 + 8) = *(int *)(lVar7 + 8) + 1;
              }
              local_80 = lVar7;
              FUN_101479bf0(lVar7);
              local_58 = lVar7;
              if ((lVar7 != 0) && (*(int *)(lVar7 + 8) == 0)) {
                FUN_1012716c0(lVar7);
              }
              *(int *)(lVar7 + 8) = *(int *)(lVar7 + 8) + 1;
              iVar5 = FUN_1024b3450(lVar7,iVar9,param_1,*(undefined8 *)(param_1 + 0x48));
              if (iVar5 == -1) {
                piVar1 = (int *)(lVar7 + 8);
                *piVar1 = *piVar1 + -1;
                if (*piVar1 == 0) {
                  FUN_1012716c0(lVar7);
                }
              }
              else {
                lVar8 = FUN_1003a2880(local_78);
                if (iVar3 <= iVar5) {
                  iVar3 = iVar5;
                }
                iVar5 = *(int *)(param_1 + 0x40);
                *(long *)(lVar8 + (long)iVar5 * 8) = lVar7;
                *(int *)(param_1 + 0x40) = iVar5 + 1;
              }
              piVar1 = (int *)(lVar7 + 8);
              *piVar1 = *piVar1 + -1;
              if (*piVar1 == 0) {
                FUN_1012716c0(lVar7);
              }
              iVar9 = iVar9 + 1;
            } while (iVar9 < local_34);
          }
          if (0 < *(int *)(param_1 + 0x40)) {
            FUN_101a6f970(local_70);
          }
          FUN_101b2cff0(*(undefined8 *)(param_1 + 0x48),iVar3);
          *(undefined1 *)(param_1 + 0x30) = 1;
        }
        else {
          local_48 = _DAT_105de829c;
          uStack_40 = _UNK_105de82a4;
          local_58 = CONCAT44(_UNK_105de8290,_DAT_105de828c);
          uStack_50 = _UNK_105de8294;
          uStack_4c = _UNK_105de8298;
          FUN_101188890(&local_58);
          if ((extraout_RDX_01 & 1) == 0) {
            FUN_1011a7c70(&local_60);
            FUN_1024b39a0("SRWMGetDeviceCount",iVar3,&DAT_1075206c0,&local_60);
            if ((local_60 != (int *)0x0) && (*local_60 = *local_60 + -1, *local_60 == 0)) {
              FUN_101442b40();
            }
          }
        }
      }
      else {
        local_48 = _DAT_105de829c;
        uStack_40 = _UNK_105de82a4;
        local_58 = CONCAT44(_UNK_105de8290,_DAT_105de828c);
        uStack_50 = _UNK_105de8294;
        uStack_4c = _UNK_105de8298;
        FUN_101188890(&local_58);
        if ((extraout_RDX_00 & 1) == 0) {
          FUN_1011a7c70(&local_68);
          FUN_1024b39a0("SRWMOpen",iVar3,&DAT_1075206c0,&local_68);
          if ((local_68 != (int *)0x0) && (*local_68 = *local_68 + -1, *local_68 == 0)) {
            FUN_101442b40();
          }
        }
      }
    }
  }
  return;
}

