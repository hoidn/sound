
void FUN_1027200f8(long param_1,undefined8 param_2)

{
  int iVar1;
  int iVar2;
  long *plVar3;
  undefined8 uVar4;
  long *plVar5;
  long lVar6;
  long lVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  long *plVar10;
  long local_90;
  long *local_88;
  char *local_80;
  undefined1 local_78;
  char *local_70;
  undefined1 local_68;
  
  FUN_102322ba0(*(undefined8 *)(param_1 + 8));
  *(undefined8 *)(param_1 + 0x2b0) = param_2;
  plVar3 = (long *)FUN_10248256c(param_2,1);
  iVar1 = (**(code **)(*plVar3 + 0x370))();
  if (iVar1 < 0) {
    FUN_10246a3d4(*(undefined8 *)(param_1 + 0xa8),1);
    FUN_1023490d0(*(undefined8 *)(param_1 + 8),*(undefined8 *)(param_1 + 0xa8));
    lVar7 = *(long *)(param_1 + 0x2f8);
  }
  else {
    FUN_1023490d0(*(undefined8 *)(param_1 + 8),*(undefined8 *)(param_1 + 0x2a8));
    FUN_1023490d0(*(undefined8 *)(param_1 + 8),*(undefined8 *)(param_1 + 0x98));
    FUN_1023490d0(*(undefined8 *)(param_1 + 8),*(undefined8 *)(param_1 + 0x28));
    FUN_1023490d0(*(undefined8 *)(param_1 + 8),*(undefined8 *)(param_1 + 0x298));
    FUN_10234945c(*(undefined8 *)(param_1 + 8),*(undefined8 *)(param_1 + 0x2a0));
    lVar7 = *(long *)(param_1 + 0x2f8);
  }
  if (lVar7 != 0) {
    FUN_1023490d0(*(undefined8 *)(param_1 + 8));
    FUN_1023490d0(*(undefined8 *)(param_1 + 8),*(undefined8 *)(param_1 + 0x2f0));
    FUN_1023490d0(*(undefined8 *)(param_1 + 8),*(undefined8 *)(param_1 + 0x300));
  }
  local_70 = "Speaker";
  local_68 = 0;
  FUN_102321e6c(*(undefined8 *)(param_1 + 0x40),*(undefined8 *)(param_1 + 0x20),&local_70,4);
  local_70 = "SoloPrehear";
  local_68 = 0;
  FUN_102321e6c(*(undefined8 *)(param_1 + 0x30),*(undefined8 *)(param_1 + 0x20),&local_70,0);
  local_70 = "PanMode";
  local_68 = 0;
  FUN_102321e6c(*(undefined8 *)(param_1 + 0x48),*(undefined8 *)(param_1 + 0x20),&local_70,0);
  local_70 = "Out";
  local_68 = 0;
  local_80 = "Pan";
  local_78 = 0;
  FUN_102321c3c(*(undefined8 *)(param_1 + 0x50),&local_70,*(undefined8 *)(param_1 + 0x20),&local_80,
                4);
  local_70 = "Out";
  local_68 = 0;
  local_80 = "StereoSplitPanL";
  local_78 = 0;
  FUN_102321c3c(*(undefined8 *)(param_1 + 0x58),&local_70,*(undefined8 *)(param_1 + 0x20),&local_80,
                4);
  local_70 = "Out";
  local_68 = 0;
  local_80 = "StereoSplitPanR";
  local_78 = 0;
  FUN_102321c3c(*(undefined8 *)(param_1 + 0x60),&local_70,*(undefined8 *)(param_1 + 0x20),&local_80,
                4);
  if (iVar1 < 0) {
    local_70 = "Out";
    local_68 = 0;
    FUN_102321d9c(*(undefined8 *)(param_1 + 0x68),&local_70,*(undefined8 *)(param_1 + 0xa8),4);
    uVar4 = *(undefined8 *)(param_1 + 0xa8);
    uVar8 = *(undefined8 *)(param_1 + 0x20);
    local_70 = "Volume";
    uVar9 = 4;
  }
  else {
    local_70 = "Out";
    local_68 = 0;
    local_80 = "Volume";
    local_78 = 0;
    FUN_102321c3c(*(undefined8 *)(param_1 + 0x68),&local_70,*(undefined8 *)(param_1 + 0x28),
                  &local_80,4);
    local_70 = "Volume";
    local_68 = 0;
    FUN_102321e6c(*(undefined8 *)(param_1 + 0x28),*(undefined8 *)(param_1 + 0x20),&local_70,4);
    local_70 = "SendOutsConnected";
    local_68 = 0;
    FUN_102321e6c(*(undefined8 *)(param_1 + 0xa0),*(undefined8 *)(param_1 + 0x20),&local_70,0);
    local_70 = "CrossFadeState";
    local_68 = 0;
    FUN_102321e6c(*(undefined8 *)(param_1 + 0x70),*(undefined8 *)(param_1 + 0x28),&local_70,4);
    uVar4 = *(undefined8 *)(param_1 + 0x98);
    uVar8 = *(undefined8 *)(param_1 + 0x28);
    local_70 = "Curve";
    uVar9 = 0;
  }
  local_68 = 0;
  FUN_102321e6c(uVar4,uVar8,&local_70,uVar9);
  local_70 = "PreHearL";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0xb8),4);
  local_70 = "PreHearR";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0xc0),4);
  local_70 = "PreHearX";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 200),0);
  local_70 = "Send0L";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0xd0),4);
  local_70 = "Send0R";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0xd8),4);
  local_70 = "Send0X";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 400),0);
  local_70 = "Send1L";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0xe0),4);
  local_70 = "Send1R";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0xe8),4);
  local_70 = "Send1X";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x198),0);
  local_70 = "Send2L";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0xf0),4);
  local_70 = "Send2R";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0xf8),4);
  local_70 = "Send2X";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x1a0),0);
  local_70 = "Send3L";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x100),4);
  local_70 = "Send3R";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x108),4);
  local_70 = "Send3X";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x1a8),0);
  local_70 = "Send4L";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x110),4);
  local_70 = "Send4R";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x118),4);
  local_70 = "Send4X";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x1b0),0);
  local_70 = "Send5L";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x120),4);
  local_70 = "Send5R";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x128),4);
  local_70 = "Send5X";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x1b8),0);
  local_70 = "Send6L";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x130),4);
  local_70 = "Send6R";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x138),4);
  local_70 = "Send6X";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x1c0),0);
  local_70 = "Send7L";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x140),4);
  local_70 = "Send7R";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x148),4);
  local_70 = "Send7X";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x1c8),0);
  local_70 = "Send8L";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x150),4);
  local_70 = "Send8R";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x158),4);
  local_70 = "Send8X";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x1d0),0);
  local_70 = "Send9L";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x160),4);
  local_70 = "Send9R";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x168),4);
  local_70 = "Send9X";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x1d8),0);
  local_70 = "Send10L";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x170),4);
  local_70 = "Send10R";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x178),4);
  local_70 = "Send10X";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x1e0),0);
  local_70 = "Send11L";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x180),4);
  local_70 = "Send11R";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x188),4);
  local_70 = "Send11X";
  local_68 = 0;
  FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x1e8),0);
  local_70 = "OutMeterL";
  local_68 = 0;
  local_80 = "InL";
  local_78 = 0;
  FUN_102321c3c(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x10),&local_80,
                0);
  local_70 = "OutMeterR";
  local_68 = 0;
  local_80 = "InR";
  local_78 = 0;
  FUN_102321c3c(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x10),&local_80,
                0);
  local_70 = "OutMeterX";
  local_68 = 0;
  local_80 = "InX";
  local_78 = 0;
  FUN_102321c3c(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x10),&local_80,
                0);
  local_70 = "OutMeterDisplayType";
  local_68 = 0;
  local_80 = "InDisplayType";
  local_78 = 0;
  FUN_102321c3c(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x10),&local_80,
                0);
  if (iVar1 < 0) {
    uVar4 = (**(code **)(*plVar3 + 0x170))(plVar3);
    uVar8 = FUN_102575f7c();
    iVar2 = FUN_10147fd68(uVar4,uVar8);
    if (iVar2 == 0) goto LAB_102720afc;
  }
  else {
    FUN_102322028(*(undefined8 *)(param_1 + 0x2a0),*(undefined8 *)(param_1 + 0x298),0);
    local_70 = "PrePostState";
    local_68 = 0;
    FUN_102321e6c(*(undefined8 *)(param_1 + 0x298),*(undefined8 *)(param_1 + 0x20),&local_70,0);
    local_70 = "CrossFade";
    local_68 = 0;
    FUN_102321e6c(*(undefined8 *)(param_1 + 0x2a8),*(undefined8 *)(param_1 + 0x28),&local_70,4);
  }
  (**(code **)(**(long **)(param_1 + 0x68) + 0x280))();
  (**(code **)(**(long **)(param_1 + 0x50) + 0x280))();
  (**(code **)(**(long **)(param_1 + 0x58) + 0x280))();
  (**(code **)(**(long **)(param_1 + 0x60) + 0x280))();
  (**(code **)(**(long **)(param_1 + 0x40) + 0x288))();
LAB_102720afc:
  (**(code **)(**(long **)(param_1 + 0x20) + 0xb8))
            (*(long **)(param_1 + 0x20),*(undefined8 *)(param_1 + 0x2b0));
  (**(code **)(**(long **)(param_1 + 0x40) + 0xb8))
            (*(long **)(param_1 + 0x40),*(undefined8 *)(*(long *)(param_1 + 0x2b0) + 0x330));
  (**(code **)(**(long **)(param_1 + 0x30) + 0xb8))
            (*(long **)(param_1 + 0x30),*(undefined8 *)(*(long *)(param_1 + 0x2b0) + 0x1d8));
  plVar10 = *(long **)(param_1 + 0x38);
  plVar5 = (long *)(**(code **)(*plVar3 + 0x278))(plVar3);
  lVar7 = (**(code **)(*plVar5 + 0x1f0))();
  (**(code **)(*plVar10 + 0xb8))(plVar10,*(undefined8 *)(lVar7 + 0x118));
  (**(code **)(**(long **)(param_1 + 0x48) + 0xb8))
            (*(long **)(param_1 + 0x48),*(undefined8 *)(*(long *)(param_1 + 0x2b0) + 0x2b8));
  (**(code **)(**(long **)(param_1 + 0x50) + 0xb8))
            (*(long **)(param_1 + 0x50),*(undefined8 *)(*(long *)(param_1 + 0x2b0) + 0x2d0));
  (**(code **)(**(long **)(param_1 + 0x58) + 0xb8))
            (*(long **)(param_1 + 0x58),*(undefined8 *)(*(long *)(param_1 + 0x2b0) + 0x2e8));
  (**(code **)(**(long **)(param_1 + 0x60) + 0xb8))
            (*(long **)(param_1 + 0x60),*(undefined8 *)(*(long *)(param_1 + 0x2b0) + 0x300));
  (**(code **)(**(long **)(param_1 + 0x68) + 0xb8))
            (*(long **)(param_1 + 0x68),*(undefined8 *)(*(long *)(param_1 + 0x2b0) + 0x318));
  (**(code **)(**(long **)(param_1 + 0x70) + 0xb8))
            (*(long **)(param_1 + 0x70),*(undefined8 *)(*(long *)(param_1 + 0x2b0) + 0x348));
  if (-1 < iVar1) {
    plVar5 = *(long **)(param_1 + 0x2a8);
    (**(code **)(*plVar3 + 0x3a0))(plVar3);
    uVar4 = FUN_10268c51c();
    (**(code **)(*plVar5 + 0xb8))(plVar5,uVar4);
    plVar5 = *(long **)(param_1 + 0x98);
    (**(code **)(*plVar3 + 0x3a0))(plVar3);
    uVar4 = FUN_102694b18();
    (**(code **)(*plVar5 + 0xb8))(plVar5,uVar4);
  }
  (**(code **)(**(long **)(param_1 + 0x18) + 0xb8))
            (*(long **)(param_1 + 0x18),*(undefined8 *)(*(long *)(param_1 + 0x2b0) + 0x160));
  FUN_1022f9494(*(undefined8 *)(param_1 + 0x10),*(undefined8 *)(*(long *)(param_1 + 0x2b0) + 0x158))
  ;
  (**(code **)(**(long **)(param_1 + 0xb0) + 0xb8))
            (*(long **)(param_1 + 0xb0),*(undefined8 *)(*(long *)(param_1 + 0x2b0) + 0x360));
  plVar5 = *(long **)(param_1 + 0x2c0);
  (**(code **)(*plVar3 + 0x278))(plVar3);
  uVar4 = FUN_1023c5370();
  (**(code **)(*plVar5 + 0x280))(plVar5,uVar4,1);
  plVar5 = *(long **)(param_1 + 0x2c8);
  (**(code **)(*plVar3 + 0x278))(plVar3);
  uVar4 = FUN_1023c5388();
  (**(code **)(*plVar5 + 0x280))(plVar5,uVar4,1);
  if (*(long *)(param_1 + 0x2f8) != 0) {
    plVar10 = *(long **)(param_1 + 0x2f0);
    plVar5 = (long *)(**(code **)(*plVar3 + 0x278))(plVar3);
    (**(code **)(*plVar5 + 0x200))();
    uVar4 = FUN_10265e5a4();
    (**(code **)(*plVar10 + 0xb8))(plVar10,uVar4);
    plVar10 = *(long **)(param_1 + 0x2f8);
    plVar5 = (long *)(**(code **)(*plVar3 + 0x278))(plVar3);
    uVar4 = (**(code **)(*plVar5 + 0x200))();
    (**(code **)(*plVar10 + 0xb8))(plVar10,uVar4);
    lVar7 = (**(code **)(*plVar3 + 0x468))(plVar3);
    if (lVar7 == 0) {
      local_70 = "OutRoutingL";
      local_68 = 0;
      local_80 = "InL";
      local_78 = 0;
      FUN_102321c3c(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x300),
                    &local_80,4);
      local_70 = "OutRoutingR";
      local_68 = 0;
      local_80 = "InR";
      local_78 = 0;
      FUN_102321c3c(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x300),
                    &local_80,4);
      local_70 = "OutRoutingX";
      local_68 = 0;
      local_80 = "InX";
      local_78 = 0;
      FUN_102321c3c(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x300),
                    &local_80,4);
      local_70 = "OutL";
      local_68 = 0;
      local_80 = "InRenderL";
      local_78 = 0;
      FUN_102321c3c(*(undefined8 *)(param_1 + 0x300),&local_70,*(undefined8 *)(param_1 + 0x2f8),
                    &local_80,4);
      local_70 = "OutR";
      local_68 = 0;
      local_80 = "InRenderR";
      local_78 = 0;
      FUN_102321c3c(*(undefined8 *)(param_1 + 0x300),&local_70,*(undefined8 *)(param_1 + 0x2f8),
                    &local_80,4);
      local_70 = "OutL";
      local_68 = 0;
      FUN_102322044(*(undefined8 *)(param_1 + 600),&local_70,*(undefined8 *)(param_1 + 0x210),4);
      local_70 = "OutR";
      local_68 = 0;
      FUN_102322044(*(undefined8 *)(param_1 + 600),&local_70,*(undefined8 *)(param_1 + 0x218),4);
      local_70 = "OutX";
      local_68 = 0;
      FUN_102321d9c(*(undefined8 *)(param_1 + 600),&local_70,*(undefined8 *)(param_1 + 0x230),0);
      local_70 = "OutRouteChanged";
      local_68 = 0;
      FUN_102322044(*(undefined8 *)(param_1 + 600),&local_70,*(undefined8 *)(param_1 + 0x228),0);
    }
    else {
      local_70 = "OutRoutingL";
      local_68 = 0;
      local_80 = "InL";
      local_78 = 0;
      FUN_102321420(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x300),
                    &local_80,0,0);
      local_70 = "OutRoutingR";
      local_68 = 0;
      local_80 = "InR";
      local_78 = 0;
      FUN_102321420(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x300),
                    &local_80,0,0);
      local_70 = "OutRoutingX";
      local_68 = 0;
      local_80 = "InX";
      local_78 = 0;
      FUN_102321420(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x300),
                    &local_80,0,0);
      local_70 = "OutL";
      local_68 = 0;
      local_80 = "InRenderL";
      local_78 = 0;
      FUN_102321420(*(undefined8 *)(param_1 + 0x300),&local_70,*(undefined8 *)(param_1 + 0x2f8),
                    &local_80,0,0);
      local_70 = "OutR";
      local_68 = 0;
      local_80 = "InRenderR";
      local_78 = 0;
      FUN_102321420(*(undefined8 *)(param_1 + 0x300),&local_70,*(undefined8 *)(param_1 + 0x2f8),
                    &local_80,0,0);
      local_70 = "OutL";
      local_68 = 0;
      local_80 = "InL";
      local_78 = 0;
      FUN_102321c3c(*(undefined8 *)(param_1 + 0x2f8),&local_70,*(undefined8 *)(param_1 + 0x20),
                    &local_80,4);
      local_70 = "OutR";
      local_68 = 0;
      local_80 = "InR";
      local_78 = 0;
      FUN_102321c3c(*(undefined8 *)(param_1 + 0x2f8),&local_70,*(undefined8 *)(param_1 + 0x20),
                    &local_80,4);
      local_70 = "OutX";
      local_68 = 0;
      local_80 = "InX";
      local_78 = 0;
      FUN_102321c3c(*(undefined8 *)(param_1 + 0x2f8),&local_70,*(undefined8 *)(param_1 + 0x20),
                    &local_80,0);
      local_70 = "OutL";
      local_68 = 0;
      FUN_102322044(*(undefined8 *)(param_1 + 0x2f8),&local_70,*(undefined8 *)(param_1 + 0x210),4);
      local_70 = "OutR";
      local_68 = 0;
      FUN_102322044(*(undefined8 *)(param_1 + 0x2f8),&local_70,*(undefined8 *)(param_1 + 0x218),4);
      local_70 = "OutX";
      local_68 = 0;
      FUN_102321d9c(*(undefined8 *)(param_1 + 0x2f8),&local_70,*(undefined8 *)(param_1 + 0x230),0);
      local_70 = "OutRouteChanged";
      local_68 = 0;
      FUN_102322044(*(undefined8 *)(param_1 + 0x2f8),&local_70,*(undefined8 *)(param_1 + 0x228),0);
      plVar5 = (long *)(**(code **)(*plVar3 + 0x278))(plVar3);
      lVar7 = (**(code **)(*plVar5 + 0x1f8))();
      if (lVar7 != 0) {
        plVar5 = (long *)(**(code **)(*plVar3 + 0x278))(plVar3);
        plVar5 = (long *)(**(code **)(*plVar5 + 0x1f8))();
        iVar1 = (**(code **)(*plVar5 + 0x580))();
        if (iVar1 != 0) {
          local_70 = "OutMidi";
          local_68 = 0;
          local_80 = s_InMidi_105be550c;
          local_78 = 0;
          FUN_102321c3c(*(undefined8 *)(param_1 + 0x2f8),&local_70,*(undefined8 *)(param_1 + 0x20),
                        &local_80,4);
        }
      }
      iVar1 = (**(code **)(**(long **)(param_1 + 0x2f8) + 0x2e0))();
      if (iVar1 != 0) {
        local_70 = "InMonitoringState";
        local_68 = 0;
        FUN_102321e6c(*(undefined8 *)(param_1 + 0x2f0),*(undefined8 *)(param_1 + 0x2f8),&local_70,0)
        ;
      }
    }
  }
  FUN_102322110(*(undefined8 *)(param_1 + 0x230),*(undefined8 *)(param_1 + 0x220),3);
  lVar7 = (**(code **)(*plVar3 + 0x468))(plVar3);
  if ((lVar7 == 0) || (lVar7 = *(long *)(param_1 + 0x2f8), lVar7 == 0)) {
    lVar7 = *(long *)(param_1 + 0x20);
  }
  iVar1 = (**(code **)(*plVar3 + 0x228))(plVar3);
  if (iVar1 == 0) {
    FUN_1022f6640(&local_88);
    local_70 = "AudioInterDomainBufferMonitor";
    local_68 = 0;
    (**(code **)(*local_88 + 0x280))(local_88,&local_70,1);
    FUN_1023490d0(*(undefined8 *)(param_1 + 8),local_88);
    local_70 = "InL";
    local_68 = 0;
    FUN_102321f5c(*(undefined8 *)(param_1 + 0x260),local_88,&local_70,4);
    local_70 = "InR";
    local_68 = 0;
    FUN_102321f5c(*(undefined8 *)(param_1 + 0x268),local_88,&local_70,4);
    local_70 = "InX";
    local_68 = 0;
    FUN_102321f5c(*(undefined8 *)(param_1 + 0x270),local_88,&local_70,0);
    local_70 = "InRouteChanged";
    local_68 = 0;
    FUN_102321f5c(*(undefined8 *)(param_1 + 0x278),local_88,&local_70,0);
    local_70 = "OutL";
    local_68 = 0;
    local_80 = "InMonitorL";
    local_78 = 0;
    FUN_102321c3c(local_88,&local_70,*(undefined8 *)(param_1 + 0x20),&local_80,4);
    local_70 = "OutR";
    local_68 = 0;
    local_80 = "InMonitorR";
    local_78 = 0;
    FUN_102321c3c(local_88,&local_70,*(undefined8 *)(param_1 + 0x20),&local_80,4);
    local_70 = "OutX";
    local_68 = 0;
    local_80 = "InMonitorX";
    local_78 = 0;
    FUN_102321c3c(local_88,&local_70,*(undefined8 *)(param_1 + 0x20),&local_80,0);
    if ((local_88 != (long *)0x0) &&
       (iVar1 = (int)local_88[1] + -1, *(int *)(local_88 + 1) = iVar1, iVar1 == 0)) {
      FUN_10128eea0();
    }
  }
  else {
    FUN_10231a9b4();
    local_70 = "InterDomainMidiBuffer";
    local_68 = 0;
    FUN_102348ce8(local_88,&local_70,0,1);
    FUN_10231b464(0x3f800000,local_88,2,1);
    FUN_1023490d0(*(undefined8 *)(param_1 + 8),local_88);
    FUN_10231a9b4(&local_90);
    local_70 = "InterDomainMidiBufferMonitor";
    local_68 = 0;
    FUN_102348ce8(local_90,&local_70,0,1);
    FUN_10231b464(0x3f800000,local_90,2,1);
    FUN_1023490d0(*(undefined8 *)(param_1 + 8),local_90);
    FUN_102322028(*(undefined8 *)(param_1 + 0x290),local_88,4);
    local_70 = s_InMidi_105be550c;
    local_68 = 0;
    FUN_102321e6c(local_88,lVar7,&local_70,4);
    FUN_102322028(*(undefined8 *)(param_1 + 0x288),local_90,0);
    local_70 = "InMidiMonitor";
    local_68 = 0;
    FUN_102321e6c(local_90,*(undefined8 *)(param_1 + 0x20),&local_70,0);
    local_70 = "OutMidiLevel";
    local_68 = 0;
    local_80 = s_InMidi_105be550c;
    local_78 = 0;
    FUN_102321c3c(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x18),
                  &local_80,0);
    local_70 = "OutMidiDisplayType";
    local_68 = 0;
    local_80 = "InMeterDisplayType";
    local_78 = 0;
    FUN_102321c3c(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x18),
                  &local_80,0);
    local_70 = "OutMidi";
    local_68 = 0;
    FUN_102321d9c(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x2c8),4);
    local_70 = "OutMidi";
    local_68 = 0;
    FUN_102322044(*(undefined8 *)(param_1 + 0x20),&local_70,*(undefined8 *)(param_1 + 0x1f0),4);
    if ((local_90 != 0) &&
       (iVar1 = *(int *)(local_90 + 8) + -1, *(int *)(local_90 + 8) = iVar1, iVar1 == 0)) {
      FUN_10128eea0();
    }
    if ((local_88 != (long *)0x0) &&
       (iVar1 = (int)local_88[1] + -1, *(int *)(local_88 + 1) = iVar1, iVar1 == 0)) {
      FUN_10128eea0();
    }
  }
  local_70 = "InL";
  local_68 = 0;
  FUN_102321f5c(*(undefined8 *)(param_1 + 0x238),*(undefined8 *)(param_1 + 600),&local_70,4);
  local_70 = "InR";
  local_68 = 0;
  FUN_102321f5c(*(undefined8 *)(param_1 + 0x240),*(undefined8 *)(param_1 + 600),&local_70,4);
  local_70 = "InX";
  local_68 = 0;
  FUN_102321f5c(*(undefined8 *)(param_1 + 0x248),*(undefined8 *)(param_1 + 600),&local_70,0);
  local_70 = "InRouteChanged";
  local_68 = 0;
  FUN_102321f5c(*(undefined8 *)(param_1 + 0x250),*(undefined8 *)(param_1 + 600),&local_70,0);
  local_70 = "OutL";
  local_68 = 0;
  local_80 = "InL";
  local_78 = 0;
  FUN_102321c3c(*(undefined8 *)(param_1 + 600),&local_70,lVar7,&local_80,4);
  local_70 = "OutR";
  local_68 = 0;
  local_80 = "InR";
  local_78 = 0;
  FUN_102321c3c(*(undefined8 *)(param_1 + 600),&local_70,lVar7,&local_80,4);
  local_70 = "OutX";
  local_68 = 0;
  local_80 = "InX";
  local_78 = 0;
  FUN_102321c3c(*(undefined8 *)(param_1 + 600),&local_70,lVar7,&local_80,0);
  local_70 = "InRouteChanged";
  local_68 = 0;
  lVar6 = FUN_102321648(lVar7,&local_70);
  if (lVar6 != 0) {
    local_70 = "OutRouteChanged";
    local_68 = 0;
    local_80 = "InRouteChanged";
    local_78 = 0;
    FUN_102321c3c(*(undefined8 *)(param_1 + 600),&local_70,lVar7,&local_80,0);
  }
  iVar1 = FUN_1015661b8(*(undefined8 *)(*(long *)(param_1 + 0x2b0) + 0x1d8));
  if (iVar1 != 0) {
    plVar3 = *(long **)(*(long *)(param_1 + 0x2b0) + 0x1d8);
    (**(code **)(*plVar3 + 0x1b8))(plVar3,1);
  }
  FUN_102721b8c(param_1);
  return;
}

