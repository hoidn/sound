// 0x1014b7214 FUN_1014b7214 state=exported-with-warnings warnings=['/* WARNING: Could not recover jumptable at 0x0001014b7714. Too many branches */', '/* WARNING: Treating indirect jump as call */']

void FUN_1014b7214(long *param_1)

{
  undefined8 *******pppppppuVar1;
  int iVar2;
  int iVar3;
  undefined8 uVar4;
  ulong uVar5;
  long lVar6;
  undefined8 *puVar7;
  long *plVar8;
  undefined8 uVar9;
  long lVar10;
  long lVar11;
  void *local_d8 [2];
  char local_c1;
  void *local_c0;
  undefined8 uStack_b8;
  long local_b0;
  undefined8 ******local_a0;
  long lStack_98;
  long local_90;
  undefined8 ******local_80;
  long lStack_78;
  long local_70;
  
  if (((DAT_106f4f9d0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_106f4f9d0), iVar2 != 0)) {
    thunk_FUN_10146bd64(&DAT_106f4fae0,"Scene");
    ___cxa_atexit(FUN_101480bac,&DAT_106f4fae0,0x100000000);
    ___cxa_guard_release(&DAT_106f4f9d0);
  }
  if (((DAT_106f4f9d8 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_106f4f9d8), iVar2 != 0)) {
    thunk_FUN_10146bd64(&DAT_106f4faf8,
                        "Track,MasterTrack,AudioTrack,MidiTrack,PlayerTrack,PreHearTrack,AbstractGroupTrack,AbstractSendTrack,GroupTrack,SendTrack,MetronomeTrack,BrowserTrack,AudioBrowserTrack,MidiBrowserTrack"
                       );
    ___cxa_atexit(FUN_101480bac,&DAT_106f4faf8,0x100000000);
    ___cxa_guard_release(&DAT_106f4f9d8);
  }
  if (((DAT_106f4f9e0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_106f4f9e0), iVar2 != 0)) {
    thunk_FUN_10146bd64(&DAT_106f4fb10,
                        "GroupDeviceBranch,MidiEffectBranch,AudioBranch,AudioEffectBranch,ReturnBranch,DrumBranch,MidiToAudioBranch,InstrumentBranch"
                       );
    ___cxa_atexit(FUN_101480bac,&DAT_106f4fb10,0x100000000);
    ___cxa_guard_release(&DAT_106f4f9e0);
  }
  if (((DAT_106f4f9e8 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_106f4f9e8), iVar2 != 0)) {
    thunk_FUN_10146bd64(&DAT_106f4fb28,
                        "GroupDevice,AudioEffectGroupDevice,DrumGroupDevice,InstrumentGroupDevice,MidiEffectGroupDevice,MidiGroupDevice"
                       );
    ___cxa_atexit(FUN_101480bac,&DAT_106f4fb28,0x100000000);
    ___cxa_guard_release(&DAT_106f4f9e8);
  }
  if (((DAT_106f4f9f0 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_106f4f9f0), iVar2 != 0)) {
    thunk_FUN_10146bd64(&DAT_106f4fb40,"Clip,AudioClip,MidiClip");
    ___cxa_atexit(FUN_101480bac,&DAT_106f4fb40,0x100000000);
    ___cxa_guard_release(&DAT_106f4f9f0);
  }
  uVar4 = (**(code **)(*param_1 + 0x28))(param_1);
  uVar5 = FUN_10120e310();
  lVar6 = DAT_106f4fae8;
  if (((uVar5 & 1) == 0) && (lVar10 = DAT_106f4fae0, DAT_106f4fae0 != DAT_106f4fae8)) {
    do {
      uVar5 = FUN_10120e048(lVar10,uVar4);
      lVar11 = lVar10;
      if ((uVar5 & 1) != 0) break;
      lVar10 = lVar10 + 0x10;
      lVar11 = lVar6;
    } while (lVar10 != lVar6);
    if (lVar11 != DAT_106f4fae8) goto LAB_1014b73a8;
  }
  uVar4 = (**(code **)(*param_1 + 0x28))(param_1);
  uVar5 = FUN_10120e310();
  lVar6 = DAT_106f4fb00;
  if (((uVar5 & 1) == 0) && (lVar10 = DAT_106f4faf8, DAT_106f4faf8 != DAT_106f4fb00)) {
    do {
      uVar5 = FUN_10120e048(lVar10,uVar4);
      lVar11 = lVar10;
      if ((uVar5 & 1) != 0) break;
      lVar10 = lVar10 + 0x10;
      lVar11 = lVar6;
    } while (lVar10 != lVar6);
    if (lVar11 != DAT_106f4fb00) goto LAB_1014b73a8;
  }
  uVar4 = (**(code **)(*param_1 + 0x28))(param_1);
  uVar5 = FUN_10120e310();
  lVar6 = DAT_106f4fb18;
  if (((uVar5 & 1) == 0) && (lVar10 = DAT_106f4fb10, DAT_106f4fb10 != DAT_106f4fb18)) {
    do {
      uVar5 = FUN_10120e048(lVar10,uVar4);
      lVar11 = lVar10;
      if ((uVar5 & 1) != 0) break;
      lVar10 = lVar10 + 0x10;
      lVar11 = lVar6;
    } while (lVar10 != lVar6);
    if (lVar11 != DAT_106f4fb18) {
LAB_1014b73a8:
      uVar4 = FUN_1014766b4(param_1,"ColorIndex");
      lVar6 = FUN_1014766b4(uVar4,"Value");
      if (lVar6 == 0) {
        uVar4 = 0xffffffff;
      }
      else {
        iVar2 = AAbstractNode::GetValue<int>();
        uVar4 = FUN_101480068(iVar2);
      }
      uVar9 = (**(code **)(*param_1 + 0x80))(param_1,"RemoteableDocumentColor",1,"Color");
      FUN_1014f75e0(uVar9,uVar4);
      FUN_101476608(param_1,"ColorIndex");
      return;
    }
  }
  uVar4 = (**(code **)(*param_1 + 0x28))(param_1);
  uVar5 = FUN_10120e310();
  lVar6 = DAT_106f4fb30;
  if (((uVar5 & 1) == 0) && (lVar10 = DAT_106f4fb28, DAT_106f4fb28 != DAT_106f4fb30)) {
    do {
      uVar5 = FUN_10120e048(lVar10,uVar4);
      lVar11 = lVar10;
      if ((uVar5 & 1) != 0) break;
      lVar10 = lVar10 + 0x10;
      lVar11 = lVar6;
    } while (lVar10 != lVar6);
    if (lVar11 != DAT_106f4fb30) {
      iVar2 = 0;
      do {
        while( true ) {
          std::to_string(iVar2);
          puVar7 = (undefined8 *)std::string::insert((ulong)&local_c0,(char *)0x0,0x105b98c2b);
          lStack_98 = puVar7[1];
          local_a0 = (undefined8 ******)*puVar7;
          local_90 = puVar7[2];
          puVar7[1] = 0;
          puVar7[2] = 0;
          *puVar7 = 0;
          plVar8 = (long *)std::string::append((char *)&local_a0,0x105af9420);
          lStack_78 = plVar8[1];
          local_80 = (undefined8 ******)*plVar8;
          local_70 = plVar8[2];
          plVar8[1] = 0;
          plVar8[2] = 0;
          *plVar8 = 0;
          if (local_90 < 0) {
            operator_delete(local_a0);
          }
          if (local_b0 < 0) {
            operator_delete(local_c0);
          }
          pppppppuVar1 = (undefined8 *******)local_80;
          if (-1 < local_70) {
            pppppppuVar1 = &local_80;
          }
          uVar4 = FUN_1014766b4(param_1,pppppppuVar1);
          lVar6 = FUN_1014766b4(uVar4,"Value");
          if (lVar6 == 0) {
            uVar4 = 0xffffffff;
          }
          else {
            iVar3 = AAbstractNode::GetValue<int>();
            uVar4 = FUN_101480068(iVar3);
          }
          pppppppuVar1 = (undefined8 *******)local_80;
          if (-1 < local_70) {
            pppppppuVar1 = &local_80;
          }
          FUN_101476608(param_1,pppppppuVar1);
          std::to_string(iVar2);
          puVar7 = (undefined8 *)std::string::insert((ulong)local_d8,(char *)0x0,0x105b98c3c);
          uStack_b8 = puVar7[1];
          local_c0 = (void *)*puVar7;
          local_b0 = puVar7[2];
          puVar7[1] = 0;
          puVar7[2] = 0;
          *puVar7 = 0;
          plVar8 = (long *)std::string::append((char *)&local_c0,0x105af9420);
          lStack_98 = plVar8[1];
          local_a0 = (undefined8 ******)*plVar8;
          local_90 = plVar8[2];
          plVar8[1] = 0;
          plVar8[2] = 0;
          *plVar8 = 0;
          if (local_b0 < 0) {
            operator_delete(local_c0);
          }
          if (local_c1 < '\0') {
            operator_delete(local_d8[0]);
          }
          pppppppuVar1 = (undefined8 *******)local_a0;
          if (-1 < local_90) {
            pppppppuVar1 = &local_a0;
          }
          uVar9 = (**(code **)(*param_1 + 0x80))(param_1,"RemoteableDocumentColor",1,pppppppuVar1);
          FUN_1014f75e0(uVar9,uVar4);
          if (-1 < local_90) break;
          operator_delete(local_a0);
          if (local_70 < 0) goto LAB_1014b7618;
LAB_1014b7480:
          iVar2 = iVar2 + 1;
          if (iVar2 == 8) {
            return;
          }
        }
        if (-1 < local_70) goto LAB_1014b7480;
LAB_1014b7618:
        operator_delete(local_80);
        iVar2 = iVar2 + 1;
        if (iVar2 == 8) {
          return;
        }
      } while( true );
    }
  }
  uVar4 = (**(code **)(*param_1 + 0x28))(param_1);
  uVar5 = FUN_10120e310();
  lVar6 = DAT_106f4fb48;
  if (((uVar5 & 1) == 0) && (lVar10 = DAT_106f4fb40, DAT_106f4fb40 != DAT_106f4fb48)) {
    do {
      uVar5 = FUN_10120e048(lVar10,uVar4);
      lVar11 = lVar10;
      if ((uVar5 & 1) != 0) break;
      lVar10 = lVar10 + 0x10;
      lVar11 = lVar6;
    } while (lVar10 != lVar6);
    if ((lVar11 != DAT_106f4fb48) &&
       (plVar8 = (long *)FUN_1014766b4(param_1,"ColorIndex"), plVar8 != (long *)0x0)) {
      (**(code **)(*plVar8 + 0x30))(plVar8,"RemoteableInt","RemoteableDocumentColor");
                    /* WARNING: Could not recover jumptable at 0x0001014b7714. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(*param_1 + 200))(param_1,"ColorIndex","Color");
      return;
    }
  }
  return;
}


// 0x1014b80fc FUN_1014b80fc state=exported-with-warnings warnings=['/* WARNING: Could not recover jumptable at 0x0001014b8148. Too many branches */', '/* WARNING: Treating indirect jump as call */']

void FUN_1014b80fc(long *param_1)

{
  int iVar1;
  
  iVar1 = (**(code **)(*param_1 + 0x70))(param_1,"SceneNames");
  if (iVar1 != 0) {
                    /* WARNING: Could not recover jumptable at 0x0001014b8148. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*param_1 + 200))(param_1,"SceneNames","Scenes");
    return;
  }
  return;
}


// 0x1014b8158 FUN_1014b8158 state=exported warnings=[]

void FUN_1014b8158(undefined8 param_1)

{
  int iVar1;
  int iVar2;
  long *plVar3;
  undefined8 uVar4;
  undefined1 auStack_30 [8];
  int *local_28;
  
  plVar3 = (long *)FUN_1014766b4(param_1,"TimeSelection");
  if (plVar3 != (long *)0x0) {
    uVar4 = (**(code **)(*plVar3 + 0x28))();
    FUN_10120d76c(auStack_30,"SongTimeSelection",0x11);
    iVar2 = FUN_10120e048(uVar4,auStack_30);
    if (local_28 != (int *)0x0) {
      iVar1 = *local_28;
      *local_28 = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_101449efc();
      }
    }
    if (iVar2 != 0) {
      (**(code **)(*plVar3 + 0x30))(plVar3,"SongTimeSelection","TimeSelection");
    }
  }
  return;
}


// 0x1014b8434 FUN_1014b8434 state=exported-with-warnings warnings=['/* WARNING: Could not recover jumptable at 0x0001014b8480. Too many branches */', '/* WARNING: Treating indirect jump as call */']

void FUN_1014b8434(long *param_1)

{
  int iVar1;
  
  iVar1 = (**(code **)(*param_1 + 0x70))(param_1,"IsContentSelected");
  if (iVar1 != 0) {
                    /* WARNING: Could not recover jumptable at 0x0001014b8480. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*param_1 + 200))(param_1,"IsContentSelected","IsContentSelectedInDocument");
    return;
  }
  return;
}


// 0x1014b8490 FUN_1014b8490 state=exported warnings=[]

void FUN_1014b8490(long *param_1)

{
  bool bVar1;
  undefined8 uVar2;
  long lVar3;
  
  uVar2 = FUN_1014766b4(param_1,"EnvelopeModePreferred");
  lVar3 = FUN_1014766b4(uVar2,"Value");
  if (lVar3 == 0) {
    bVar1 = false;
  }
  else {
    bVar1 = AAbstractNode::GetValue<bool>();
  }
  uVar2 = (**(code **)(*param_1 + 0x80))(param_1,"RemoteableInt",1,"PreferredContentViewMode");
  FUN_1014f75e0(uVar2,bVar1);
  FUN_101476608(param_1,"EnvelopeModePreferred");
  return;
}


// 0x1014b8bf4 FUN_1014b8bf4 state=exported warnings=[]

void FUN_1014b8bf4(long *param_1)

{
  int iVar1;
  undefined8 uVar2;
  ulong uVar3;
  undefined8 uVar4;
  long lVar5;
  TString TVar6;
  int **ppiVar7;
  undefined8 uVar8;
  int *local_68;
  undefined1 auStack_60 [8];
  int *piStack_58;
  int *local_50;
  int *local_48;
  
  uVar2 = (**(code **)(*param_1 + 0x60))(param_1,"Scenes");
  FUN_10146b5c4(&piStack_58,uVar2);
  FUN_10146b644(auStack_60,uVar2);
  uVar3 = FUN_10146b928(&piStack_58,auStack_60);
  if ((uVar3 & 1) == 0) {
    uVar8 = 0;
    do {
      uVar4 = FUN_10146b8e0(&piStack_58);
      uVar4 = FUN_1014766b4(uVar4,"Name");
      lVar5 = FUN_1014766b4(uVar4,"Value");
      if (lVar5 == 0) {
LAB_1014b8dec:
        FUN_10146b6f0(auStack_60);
        ppiVar7 = &piStack_58;
        goto LAB_1014b8df8;
      }
      AAbstractNode::GetValue<TString>();
      FUN_1014300e0(&local_48,&local_50,&PTR_u__10666fa18);
      if (local_50 != (int *)0x0) {
        iVar1 = *local_50;
        *local_50 = iVar1 + -1;
        if (iVar1 + -1 == 0) {
          FUN_101449efc();
        }
      }
      if (local_48 == (int *)0x0) {
        lVar5 = -1;
      }
      else {
        lVar5 = (long)(local_48[1] / 2 + -1);
      }
      uVar4 = FUN_1002c3ce8(local_48 + 4,lVar5);
      if (local_48 != (int *)0x0) {
        iVar1 = *local_48;
        *local_48 = iVar1 + -1;
        if (iVar1 + -1 == 0) {
          FUN_101449efc();
        }
      }
      if (((uint)((ulong)uVar4 >> 0x20) & (uint)((int)uVar8 + 1 == (int)uVar4)) == 0)
      goto LAB_1014b8dec;
      FUN_10146b8cc(&piStack_58);
      uVar3 = FUN_10146b928(&piStack_58,auStack_60);
      uVar8 = uVar4;
    } while ((uVar3 & 1) == 0);
  }
  FUN_10146b6f0(auStack_60);
  FUN_10146b6f0(&piStack_58);
  FUN_10146b5c4(&local_48,uVar2);
  FUN_10146b644(&local_50,uVar2);
  while (iVar1 = FUN_10146b928(&local_48,&local_50), iVar1 == 0) {
    uVar2 = FUN_10146b8e0(&local_48);
    uVar2 = FUN_1014766b4(uVar2,"Name");
    TVar6.field0_0x0.field0_0x0 = (TArray<char16_t>)FUN_1014766b4(uVar2,"Value");
    FUN_1011cb734(&local_68);
    AAbstractNode::SetValue<TString>(TVar6);
    if (local_68 != (int *)0x0) {
      iVar1 = *local_68;
      *local_68 = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_101449efc();
      }
    }
    FUN_10146b8cc(&local_48);
  }
  FUN_10146b6f0(&local_50);
  ppiVar7 = &local_48;
LAB_1014b8df8:
  FUN_10146b6f0(ppiVar7);
  return;
}


// 0x1014b9254 FUN_1014b9254 state=exported warnings=[]

void FUN_1014b9254(undefined8 param_1)

{
  int iVar1;
  long *plVar2;
  long lVar3;
  long lVar4;
  undefined8 local_48;
  int *local_40;
  undefined8 *puStack_38;
  int aiStack_30 [2];
  int *local_28;
  
  plVar2 = (long *)thunk_FUN_1014763d4(param_1,"DeviceChain/DeviceChain");
  if (plVar2 != (long *)0x0) {
    local_48 = param_1;
    FUN_101427680(&local_40,"Hybrid");
    if (local_40 == (int *)0x0) {
      lVar4 = -1;
    }
    else {
      lVar4 = (long)(local_40[1] / 2 + -1);
    }
    FUN_10120d7d0(aiStack_30,local_40 + 4,lVar4);
    if ((local_40 != (int *)0x0) && (iVar1 = *local_40, *local_40 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
    local_40 = aiStack_30;
    puStack_38 = &local_48;
    FUN_1014f7f20(&local_40,plVar2);
    lVar3 = (**(code **)(*plVar2 + 0x150))(plVar2);
    for (lVar4 = *(long *)(lVar3 + 8); lVar4 != lVar3; lVar4 = *(long *)(lVar4 + 8)) {
      FUN_1014f8258(*(undefined8 *)(lVar4 + 0x20),&local_40);
    }
    if ((local_28 != (int *)0x0) && (iVar1 = *local_28, *local_28 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  return;
}


// 0x1014b9578 FUN_1014b9578 state=exported warnings=[]

void FUN_1014b9578(undefined8 param_1)

{
  int iVar1;
  long *plVar2;
  long lVar3;
  long lVar4;
  undefined8 local_48;
  int *local_40;
  undefined8 *puStack_38;
  int aiStack_30 [2];
  int *local_28;
  
  plVar2 = (long *)thunk_FUN_1014763d4(param_1,"DeviceChain/DeviceChain");
  if (plVar2 != (long *)0x0) {
    local_48 = param_1;
    FUN_101427680(&local_40,"PhaserNew");
    if (local_40 == (int *)0x0) {
      lVar4 = -1;
    }
    else {
      lVar4 = (long)(local_40[1] / 2 + -1);
    }
    FUN_10120d7d0(aiStack_30,local_40 + 4,lVar4);
    if ((local_40 != (int *)0x0) && (iVar1 = *local_40, *local_40 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
    local_40 = aiStack_30;
    puStack_38 = &local_48;
    FUN_1014f8540(&local_40,plVar2);
    lVar3 = (**(code **)(*plVar2 + 0x150))(plVar2);
    for (lVar4 = *(long *)(lVar3 + 8); lVar4 != lVar3; lVar4 = *(long *)(lVar4 + 8)) {
      FUN_1014f8a74(*(undefined8 *)(lVar4 + 0x20),&local_40);
    }
    if ((local_28 != (int *)0x0) && (iVar1 = *local_28, *local_28 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  return;
}


// 0x1014b9d68 FUN_1014b9d68 state=exported-with-warnings warnings=['/* WARNING: Could not recover jumptable at 0x0001014b9dd8. Too many branches */', '/* WARNING: Treating indirect jump as call */']

void FUN_1014b9d68(long *param_1)

{
  ulong uVar1;
  long *plVar2;
  
  uVar1 = (**(code **)(*param_1 + 0x70))(param_1,"ResetNonautomatedMidiControllersOnClipStarts");
  if ((uVar1 & 1) != 0) {
    return;
  }
  plVar2 = (long *)(**(code **)(*param_1 + 0x90))
                             (param_1,"RemoteableBool",
                              "ResetNonautomatedMidiControllersOnClipStarts");
                    /* WARNING: Could not recover jumptable at 0x0001014b9dd8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(*plVar2 + 0x98))(plVar2,"Value",0);
  return;
}


// 0x1014ba764 FUN_1014ba764 state=exported-with-warnings warnings=['/* WARNING: Subroutine does not return */', '/* WARNING: Does not return */']

void FUN_1014ba764(long *param_1)

{
  int iVar1;
  code *pcVar2;
  int iVar3;
  uint uVar4;
  undefined8 uVar5;
  ulong uVar6;
  long *plVar7;
  long lVar8;
  long lVar9;
  long lVar10;
  int *local_68;
  long **pplStack_60;
  int aiStack_58 [2];
  int *local_50;
  long *local_48 [2];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_1064f8818;
  if (((DAT_106f4fa00 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_106f4fa00), iVar3 != 0)) {
    thunk_FUN_10146bd64(&DAT_106f4fb70,
                        "Track,MasterTrack,AudioTrack,MidiTrack,PlayerTrack,PreHearTrack,AbstractGroupTrack,AbstractSendTrack,GroupTrack,SendTrack,MetronomeTrack,BrowserTrack,AudioBrowserTrack,MidiBrowserTrack"
                       );
    ___cxa_atexit(FUN_101480bac,&DAT_106f4fb70,0x100000000);
    ___cxa_guard_release(&DAT_106f4fa00);
  }
  uVar5 = (**(code **)(*param_1 + 0x28))(param_1);
  uVar6 = FUN_10120e310();
  lVar9 = DAT_106f4fb78;
  if (((uVar6 & 1) == 0) && (lVar8 = DAT_106f4fb70, DAT_106f4fb70 != DAT_106f4fb78)) {
    do {
      uVar6 = FUN_10120e048(lVar8,uVar5);
      lVar10 = lVar8;
      if ((uVar6 & 1) != 0) break;
      lVar8 = lVar8 + 0x10;
      lVar10 = lVar9;
    } while (lVar8 != lVar9);
    if (lVar10 != DAT_106f4fb78) {
      plVar7 = (long *)thunk_FUN_1014763d4(param_1,"DeviceChain/DeviceChain");
      if (plVar7 != (long *)0x0) {
        local_48[0] = param_1;
        FUN_101427680(&local_68,"Reverb");
        if (local_68 == (int *)0x0) {
          lVar9 = -1;
        }
        else {
          lVar9 = (long)(local_68[1] / 2 + -1);
        }
        FUN_10120d7d0(aiStack_58,local_68 + 4,lVar9);
        if ((local_68 != (int *)0x0) && (iVar3 = *local_68, *local_68 = iVar3 + -1, iVar3 + -1 == 0)
           ) {
          FUN_101449efc();
        }
        local_68 = aiStack_58;
        pplStack_60 = local_48;
        FUN_1014f8ef8(&local_68,plVar7);
        lVar8 = (**(code **)(*plVar7 + 0x150))(plVar7);
        for (lVar9 = *(long *)(lVar8 + 8); lVar9 != lVar8; lVar9 = *(long *)(lVar9 + 8)) {
          FUN_1014f9200(*(undefined8 *)(lVar9 + 0x20),&local_68);
        }
        if ((local_50 != (int *)0x0) && (iVar3 = *local_50, *local_50 = iVar3 + -1, iVar3 + -1 == 0)
           ) {
          FUN_101449efc();
        }
      }
      goto LAB_1014ba8ec;
    }
  }
  uVar5 = (**(code **)(*param_1 + 0x28))(param_1);
  FUN_10120d76c(aiStack_58,"Reverb",6);
  iVar3 = FUN_10120e048(uVar5,aiStack_58);
  if ((local_50 != (int *)0x0) && (iVar1 = *local_50, *local_50 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  if (iVar3 != 0) {
    lVar9 = FUN_1014766b4(param_1,"RoomType");
    if ((lVar9 != 0) && (lVar9 = thunk_FUN_1014763d4(lVar9,"Manual/Value"), lVar9 != 0)) {
      uVar4 = AAbstractNode::GetValue<int>();
      if (2 < uVar4) {
        FUN_101471a98(lVar9,"Enum out of range");
        goto LAB_1014baa28;
      }
      AAbstractNode::SetValue<int>((int)lVar9);
    }
LAB_1014ba8ec:
    if (*(long *)PTR____stack_chk_guard_1064f8818 == local_38) {
      return;
    }
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  FUN_101471a98(param_1,"Incorrect node type for this translator. Should be Reverb or Tracks only.")
  ;
LAB_1014baa28:
                    /* WARNING: Does not return */
  pcVar2 = (code *)SoftwareBreakpoint(1,0x1014baa2c);
  (*pcVar2)();
}


// 0x1014baca4 FUN_1014baca4 state=exported-with-warnings warnings=['/* WARNING: Could not recover jumptable at 0x0001014bacf0. Too many branches */', '/* WARNING: Treating indirect jump as call */']

void FUN_1014baca4(long *param_1)

{
  int iVar1;
  
  iVar1 = (**(code **)(*param_1 + 0x70))(param_1,"ReWireSlaveMidiTargetId");
  if (iVar1 != 0) {
                    /* WARNING: Could not recover jumptable at 0x0001014bacf0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*param_1 + 200))(param_1,"ReWireSlaveMidiTargetId","ReWireDeviceMidiTargetId");
    return;
  }
  return;
}


// 0x1014bb578 FUN_1014bb578 state=exported warnings=[]

void FUN_1014bb578(long *param_1)

{
  int iVar1;
  long *plVar2;
  long *plVar3;
  TString TVar4;
  long lVar5;
  int *local_38;
  
  iVar1 = (**(code **)(*param_1 + 0x70))(param_1,"MasterTrack");
  if (iVar1 != 0) {
    plVar2 = (long *)(**(code **)(*param_1 + 0x60))(param_1,"MasterTrack");
    (**(code **)(*plVar2 + 0x30))(plVar2,"MasterTrack","MainTrack");
    iVar1 = (**(code **)(*plVar2 + 0x70))(plVar2,"DeviceChain");
    if (iVar1 != 0) {
      plVar3 = (long *)(**(code **)(*plVar2 + 0x60))(plVar2,"DeviceChain");
      (**(code **)(*plVar3 + 0x30))(plVar3,"MasterTrackDeviceChain","MainTrackDeviceChain");
      iVar1 = (**(code **)(*plVar3 + 0x70))(plVar3,"TrackDevice");
      if (iVar1 != 0) {
        plVar3 = (long *)(**(code **)(*plVar3 + 0x60))(plVar3,"TrackDevice");
        (**(code **)(*plVar3 + 0x30))(plVar3,"MasterTrackDevice","MainTrackDevice");
      }
    }
    iVar1 = (**(code **)(*plVar2 + 0x70))(plVar2,"Name");
    if (iVar1 != 0) {
      plVar2 = (long *)(**(code **)(*plVar2 + 0x60))(plVar2,"Name");
      iVar1 = (**(code **)(*plVar2 + 0x70))(plVar2,"EffectiveName");
      if (iVar1 != 0) {
        plVar2 = (long *)(**(code **)(*plVar2 + 0x60))(plVar2,"EffectiveName");
        iVar1 = (**(code **)(*plVar2 + 0x70))(plVar2,"Value");
        if (iVar1 != 0) {
          TVar4.field0_0x0.field0_0x0 =
               (TArray<char16_t>)(**(code **)(*plVar2 + 0x60))(plVar2,"Value");
          FUN_10142d468(&local_38,L"Main");
          AAbstractNode::SetValue<TString>(TVar4);
          if (local_38 != (int *)0x0) {
            iVar1 = *local_38;
            *local_38 = iVar1 + -1;
            if (iVar1 + -1 == 0) {
              FUN_101449efc();
            }
          }
        }
      }
    }
    (**(code **)(*param_1 + 200))(param_1,"MasterTrack","MainTrack");
  }
  iVar1 = (**(code **)(*param_1 + 0x70))(param_1,"AutoColorPickerForReturnAndMasterTracks");
  if (iVar1 != 0) {
    (**(code **)(*param_1 + 200))
              (param_1,"AutoColorPickerForReturnAndMasterTracks",
               "AutoColorPickerForReturnAndMainTracks");
  }
  iVar1 = (**(code **)(*param_1 + 0x70))(param_1,"SongMasterValues");
  if (iVar1 != 0) {
    plVar2 = (long *)(**(code **)(*param_1 + 0x60))(param_1,"SongMasterValues");
    iVar1 = (**(code **)(*plVar2 + 0x70))(plVar2,"SessionScrollerPos");
    if (iVar1 != 0) {
      lVar5 = (**(code **)(*plVar2 + 0x60))(plVar2,"SessionScrollerPos");
      if (lVar5 != 0) {
        *(int *)(lVar5 + 8) = *(int *)(lVar5 + 8) + 1;
      }
      (**(code **)(*param_1 + 0xc0))(param_1,"SongMasterValues");
      (**(code **)(*param_1 + 0xb0))(param_1,lVar5,"SessionScrollPos");
      if (lVar5 != 0) {
        iVar1 = *(int *)(lVar5 + 8) + -1;
        *(int *)(lVar5 + 8) = iVar1;
        if (iVar1 == 0) {
          FUN_10128eea0(lVar5);
        }
      }
    }
  }
  return;
}


// 0x1014bbb3c FUN_1014bbb3c state=exported warnings=[]

void FUN_1014bbb3c(long *param_1)

{
  bool bVar1;
  int iVar2;
  long *plVar3;
  long *plVar4;
  
  iVar2 = (**(code **)(*param_1 + 0x70))(param_1,"MidiFoldIn");
  if ((iVar2 != 0) && (iVar2 = (**(code **)(*param_1 + 0x70))(param_1,"MidiFoldMode"), iVar2 != 0))
  {
    plVar3 = (long *)(**(code **)(*param_1 + 0x60))(param_1,"MidiFoldIn");
    plVar4 = (long *)(**(code **)(*param_1 + 0x60))(param_1,"MidiFoldMode");
    iVar2 = (**(code **)(*plVar3 + 0x70))(plVar3,"Value");
    if ((iVar2 != 0) && (iVar2 = (**(code **)(*plVar4 + 0x70))(plVar4,"Value"), iVar2 != 0)) {
      (**(code **)(*plVar3 + 0x60))(plVar3,"Value");
      bVar1 = AAbstractNode::GetValue<bool>();
      if (!bVar1) {
        iVar2 = (**(code **)(*plVar4 + 0x60))(plVar4,"Value");
        AAbstractNode::SetValue<int>(iVar2);
        return;
      }
    }
  }
  return;
}


// 0x1014bbc44 FUN_1014bbc44 state=exported warnings=[]

void FUN_1014bbc44(long *param_1)

{
  int iVar1;
  undefined8 uVar2;
  long lVar3;
  
  if ((param_1 != (long *)0x0) &&
     (iVar1 = (**(code **)(*param_1 + 0x70))(param_1,"InKey"), iVar1 != 0)) {
    uVar2 = (**(code **)(*param_1 + 0x60))(param_1,"InKey");
    lVar3 = FUN_1014766b4(uVar2,"Value");
    if (lVar3 != 0) {
      AAbstractNode::SetValue<bool>(SUB81(lVar3,0));
      return;
    }
  }
  return;
}


// 0x1014bbf24 FUN_1014bbf24 state=exported warnings=[]

void FUN_1014bbf24(undefined8 param_1)

{
  int iVar1;
  long lVar2;
  long *plVar3;
  undefined1 auStack_40 [8];
  undefined1 auStack_38 [8];
  
  lVar2 = FUN_1014766b4(param_1,"ExpressionLanes");
  if (lVar2 != 0) {
    FUN_10146b5c4(auStack_38,lVar2);
    FUN_10146b644(auStack_40,lVar2);
    while (iVar1 = FUN_10146b928(auStack_38,auStack_40), iVar1 == 0) {
      plVar3 = (long *)FUN_10146b8e0(auStack_38);
      (**(code **)(*plVar3 + 0x30))(plVar3,"ExpressionLane","MidiEditorLaneModel");
      FUN_10146b8cc(auStack_38);
    }
    FUN_10146b6f0(auStack_40);
    FUN_10146b6f0(auStack_38);
  }
  lVar2 = FUN_1014766b4(param_1,"ContentLanes");
  if (lVar2 != 0) {
    FUN_10146b5c4(auStack_38,lVar2);
    FUN_10146b644(auStack_40,lVar2);
    while (iVar1 = FUN_10146b928(auStack_38,auStack_40), iVar1 == 0) {
      plVar3 = (long *)FUN_10146b8e0(auStack_38);
      (**(code **)(*plVar3 + 0x30))(plVar3,"ExpressionLane","MidiEditorLaneModel");
      FUN_10146b8cc(auStack_38);
    }
    FUN_10146b6f0(auStack_40);
    FUN_10146b6f0(auStack_38);
  }
  return;
}


// 0x1014bc4bc FUN_1014bc4bc state=exported warnings=[]

void FUN_1014bc4bc(undefined8 param_1)

{
  int iVar1;
  long lVar2;
  long *plVar3;
  undefined8 uVar4;
  undefined1 auStack_70 [8];
  undefined1 auStack_68 [8];
  
  lVar2 = FUN_1014766b4(param_1,"NoteAlgorithms");
  if (lVar2 != 0) {
    FUN_10146b5c4(auStack_68,lVar2);
    FUN_10146b644(auStack_70,lVar2);
    while (iVar1 = FUN_10146b928(auStack_68,auStack_70), iVar1 == 0) {
      plVar3 = (long *)FUN_10146b8e0(auStack_68);
      (**(code **)(*plVar3 + 0x28))();
      uVar4 = FUN_10120e26c();
      iVar1 = FUN_1014289f4(uVar4,"BeatAlgorithm");
      if (iVar1 != 0) {
        FUN_101476608(plVar3,"PatternSize");
        FUN_101476608(plVar3,"Pattern");
        FUN_101476608(plVar3,"Accents");
        FUN_101476608(plVar3,"NumberOfRepetitions");
        FUN_101476608(plVar3,"Repetitions");
        FUN_101476608(plVar3,"StepDuration");
        FUN_101476608(plVar3,"Pitch");
        FUN_101476608(plVar3,"Velocity");
        (**(code **)(*plVar3 + 0x30))(plVar3,"BeatAlgorithm","RhythmAlgorithm");
      }
      (**(code **)(*plVar3 + 0x28))(plVar3);
      uVar4 = FUN_10120e26c();
      iVar1 = FUN_1014289f4(uVar4,"PermuteAlgorithm");
      if (iVar1 != 0) {
        (**(code **)(*plVar3 + 0x30))(plVar3,"PermuteAlgorithm","RecombineAlgorithm");
      }
      (**(code **)(*plVar3 + 0x28))(plVar3);
      uVar4 = FUN_10120e26c();
      iVar1 = FUN_1014289f4(uVar4,"MelodyAlgorithm");
      if (iVar1 != 0) {
        (**(code **)(*plVar3 + 0x30))(plVar3,"MelodyAlgorithm","ShapeAlgorithm");
      }
      (**(code **)(*plVar3 + 0x28))(plVar3);
      uVar4 = FUN_10120e26c();
      iVar1 = FUN_1014289f4(uVar4,"RandomAlgorithm");
      if (iVar1 != 0) {
        (**(code **)(*plVar3 + 0x30))(plVar3,"RandomAlgorithm","SeedAlgorithm");
      }
      FUN_10146b8cc(auStack_68);
    }
    FUN_10146b6f0(auStack_70);
    FUN_10146b6f0(auStack_68);
  }
  return;
}


// 0x1014bceb4 FUN_1014bceb4 state=exported-with-warnings warnings=['/* WARNING: Subroutine does not return */', '/* WARNING: Subroutine does not return */', '/* WARNING: Subroutine does not return */']

void FUN_1014bceb4(undefined8 param_1)

{
  ulong uVar1;
  int *piVar2;
  long lVar3;
  int *piVar4;
  int iVar5;
  int iVar6;
  long *plVar7;
  long lVar8;
  undefined8 uVar9;
  long *plVar10;
  int *piVar11;
  int *piVar12;
  int *piVar13;
  ulong uVar14;
  int *piVar15;
  ulong uVar16;
  undefined1 (*pauVar17) [16];
  undefined1 (*pauVar18) [16];
  long lVar19;
  size_t sVar20;
  long lVar21;
  undefined1 auVar22 [16];
  undefined1 auVar23 [16];
  undefined1 auVar24 [16];
  undefined1 auVar25 [16];
  undefined1 auStack_90 [8];
  undefined1 auStack_88 [8];
  undefined1 auStack_80 [8];
  int *local_78;
  int *local_70;
  int *local_68;
  
  plVar7 = (long *)FUN_1014766b4(param_1,"NoteAlgorithms");
  if (plVar7 != (long *)0x0) {
    lVar8 = (**(code **)(*plVar7 + 0x150))();
    for (lVar21 = *(long *)(lVar8 + 8); lVar21 != lVar8; lVar21 = *(long *)(lVar21 + 8)) {
      plVar7 = *(long **)(lVar21 + 0x20);
      (**(code **)(*plVar7 + 0x28))(plVar7);
      uVar9 = FUN_10120e26c();
      iVar5 = FUN_1014289f4(uVar9,"ChordAlgorithm");
      if ((iVar5 != 0) && (plVar7 = (long *)FUN_1014766b4(plVar7,"Sequence"), plVar7 != (long *)0x0)
         ) {
        iVar5 = (**(code **)(*plVar7 + 0xd0))();
        local_78 = (int *)0x0;
        local_70 = (int *)0x0;
        local_68 = (int *)0x0;
        if (iVar5 != 0) {
          if (iVar5 < 0) {
                    /* WARNING: Subroutine does not return */
            FUN_100256744(&local_78);
          }
          local_70 = operator_new((long)iVar5 << 2);
          local_68 = local_70 + iVar5;
        }
        local_78 = local_70;
        FUN_10146b5c4(auStack_80,plVar7);
        iVar5 = 0;
        while( true ) {
          FUN_10146b644(auStack_88,plVar7);
          iVar6 = FUN_10146b928(auStack_80,auStack_88);
          FUN_10146b6f0(auStack_88);
          if (iVar6 != 0) break;
          plVar10 = (long *)FUN_10146b8e0(auStack_80);
          (**(code **)(*plVar10 + 0x28))();
          uVar9 = FUN_10120e26c();
          iVar6 = FUN_1014289f4(uVar9,"EmptyChordSequenceElement");
          piVar4 = local_78;
          if (iVar6 != 0) {
            if (local_70 < local_68) {
              *local_70 = iVar5;
              local_70 = local_70 + 1;
            }
            else {
              sVar20 = (long)local_70 - (long)local_78;
              lVar19 = (long)sVar20 >> 2;
              uVar1 = lVar19 + 1;
              if (uVar1 >> 0x3e != 0) {
                    /* WARNING: Subroutine does not return */
                FUN_100256744(&local_78);
              }
              uVar14 = (long)local_68 - (long)local_78 >> 1;
              if (uVar14 <= uVar1) {
                uVar14 = uVar1;
              }
              if (0x7ffffffffffffffb < (ulong)((long)local_68 - (long)local_78)) {
                uVar14 = 0x3fffffffffffffff;
              }
              if (uVar14 == 0) {
                piVar11 = (int *)0x0;
              }
              else {
                if (uVar14 >> 0x3e != 0) {
                    /* WARNING: Subroutine does not return */
                  FUN_10024a858();
                }
                piVar11 = operator_new(uVar14 << 2);
              }
              piVar12 = piVar11 + lVar19 + 1;
              piVar11[lVar19] = iVar5;
              _memcpy(piVar11,piVar4,sVar20);
              local_78 = piVar11;
              local_70 = piVar12;
              local_68 = piVar11 + uVar14;
              if (piVar4 != (int *)0x0) {
                operator_delete(piVar4);
                local_70 = piVar12;
              }
            }
          }
          FUN_10146b7b4(auStack_90,auStack_80);
          FUN_10146b8cc(auStack_80);
          iVar5 = iVar5 + 1;
          FUN_10146b6f0(auStack_90);
        }
        FUN_10146b6f0(auStack_80);
        piVar4 = local_70;
        piVar11 = local_78;
        if ((local_78 != local_70) && (piVar12 = local_70 + -1, local_78 < piVar12)) {
          piVar15 = local_70 + -2;
          if (local_70 + -2 <= local_78 + 1) {
            piVar15 = local_78 + 1;
          }
          piVar15 = piVar15 + -1;
          lVar3 = (long)piVar15 - (long)local_78;
          lVar19 = 1;
          if (lVar3 != 0) {
            lVar19 = 2;
          }
          uVar1 = lVar19 + (lVar3 - (ulong)(lVar3 != 0) >> 3);
          piVar2 = local_78;
          if (0xb < uVar1) {
            if (piVar15 != local_78) {
              piVar2 = (int *)((long)local_78 + 1);
            }
            uVar14 = (ulong)((long)piVar15 - (long)piVar2) >> 3;
            if (piVar15 != local_78) {
              uVar14 = uVar14 + 1;
            }
            if ((local_70 <= local_78) ||
               (piVar2 = local_78, local_78 + uVar14 + 1 <= piVar12 + -uVar14)) {
              uVar16 = uVar1 & 0x3ffffffffffffff8;
              piVar12 = piVar12 + -uVar16;
              pauVar17 = (undefined1 (*) [16])(local_78 + 4);
              pauVar18 = (undefined1 (*) [16])(local_70 + -4);
              uVar14 = uVar16;
              do {
                auVar22 = pauVar17[-1];
                auVar23 = *pauVar17;
                auVar24 = NEON_rev64(*pauVar18,4);
                auVar24 = NEON_ext(auVar24,auVar24,8,1);
                auVar25 = NEON_rev64(pauVar18[-1],4);
                auVar25 = NEON_ext(auVar25,auVar25,8,1);
                *(long *)((long)pauVar17[-1] + 8) = auVar24._8_8_;
                *(long *)pauVar17[-1] = auVar24._0_8_;
                *(long *)((long)*pauVar17 + 8) = auVar25._8_8_;
                *(long *)*pauVar17 = auVar25._0_8_;
                auVar22 = NEON_rev64(auVar22,4);
                auVar22 = NEON_ext(auVar22,auVar22,8,1);
                auVar23 = NEON_rev64(auVar23,4);
                auVar23 = NEON_ext(auVar23,auVar23,8,1);
                *(long *)((long)pauVar18[-1] + 8) = auVar23._8_8_;
                *(long *)pauVar18[-1] = auVar23._0_8_;
                *(long *)((long)*pauVar18 + 8) = auVar22._8_8_;
                *(long *)*pauVar18 = auVar22._0_8_;
                pauVar17 = pauVar17 + 2;
                pauVar18 = pauVar18 + -2;
                uVar14 = uVar14 - 8;
              } while (uVar14 != 0);
              piVar2 = local_78 + uVar16;
              if (uVar1 == uVar16) goto LAB_1014bd1e8;
            }
          }
          do {
            piVar13 = piVar2 + 1;
            iVar5 = *piVar2;
            *piVar2 = *piVar12;
            piVar15 = piVar12 + -1;
            *piVar12 = iVar5;
            piVar12 = piVar15;
            piVar2 = piVar13;
          } while (piVar13 < piVar15);
        }
LAB_1014bd1e8:
        for (; piVar11 != piVar4; piVar11 = piVar11 + 1) {
          (**(code **)(*plVar7 + 0x128))(plVar7,*piVar11);
        }
        if (local_78 != (int *)0x0) {
          local_70 = local_78;
          operator_delete(local_78);
        }
      }
    }
  }
  return;
}


// 0x1014bd2a8 FUN_1014bd2a8 state=exported warnings=[]

void FUN_1014bd2a8(undefined8 param_1)

{
  int iVar1;
  long *plVar2;
  long lVar3;
  undefined8 uVar4;
  long lVar5;
  uint uVar6;
  
  plVar2 = (long *)FUN_1014766b4(param_1,"NoteAlgorithms");
  if (plVar2 != (long *)0x0) {
    lVar3 = (**(code **)(*plVar2 + 0x150))();
    for (lVar5 = *(long *)(lVar3 + 8); lVar5 != lVar3; lVar5 = *(long *)(lVar5 + 8)) {
      plVar2 = *(long **)(lVar5 + 0x20);
      (**(code **)(*plVar2 + 0x28))(plVar2);
      uVar4 = FUN_10120e26c();
      iVar1 = FUN_1014289f4(uVar4,"ChordAlgorithm");
      if (((iVar1 != 0) &&
          (plVar2 = (long *)FUN_1014766b4(plVar2,"Sequence"), plVar2 != (long *)0x0)) &&
         (iVar1 = (**(code **)(*plVar2 + 0xd0))(), 4 < iVar1)) {
        uVar6 = iVar1 + 1;
        do {
          (**(code **)(*plVar2 + 0x128))(plVar2,uVar6 - 2);
          uVar6 = uVar6 - 1;
        } while (5 < uVar6);
      }
    }
  }
  return;
}


// 0x1014bd69c FUN_1014bd69c state=exported warnings=[]

void FUN_1014bd69c(undefined8 param_1)

{
  int iVar1;
  long lVar2;
  long *plVar3;
  undefined8 uVar4;
  undefined1 auStack_40 [8];
  undefined1 auStack_38 [8];
  
  lVar2 = FUN_1014766b4(param_1,"NoteAlgorithms");
  if (lVar2 != 0) {
    FUN_10146b5c4(auStack_38,lVar2);
    FUN_10146b644(auStack_40,lVar2);
    while (iVar1 = FUN_10146b928(auStack_38,auStack_40), iVar1 == 0) {
      plVar3 = (long *)FUN_10146b8e0(auStack_38);
      (**(code **)(*plVar3 + 0x28))();
      uVar4 = FUN_10120e26c();
      iVar1 = FUN_1014289f4(uVar4,"ChordAlgorithm");
      if (iVar1 != 0) {
        (**(code **)(*plVar3 + 0x30))(plVar3,"ChordAlgorithm","StacksAlgorithm");
      }
      FUN_10146b8cc(auStack_38);
    }
    FUN_10146b6f0(auStack_40);
    FUN_10146b6f0(auStack_38);
  }
  return;
}


// 0x1014bd7a4 FUN_1014bd7a4 state=exported-with-warnings warnings=['/* WARNING: Subroutine does not return */', '/* WARNING: Does not return */']

void FUN_1014bd7a4(long *param_1)

{
  int iVar1;
  code *pcVar2;
  int iVar3;
  uint uVar4;
  undefined8 uVar5;
  ulong uVar6;
  long *plVar7;
  long lVar8;
  long lVar9;
  long lVar10;
  int *local_68;
  long **pplStack_60;
  int aiStack_58 [2];
  int *local_50;
  long *local_48 [2];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_1064f8818;
  if (((DAT_106f4fa18 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_106f4fa18), iVar3 != 0)) {
    thunk_FUN_10146bd64(&DAT_106f4fb88,
                        "Track,MasterTrack,AudioTrack,MidiTrack,PlayerTrack,PreHearTrack,AbstractGroupTrack,AbstractSendTrack,GroupTrack,SendTrack,MetronomeTrack,BrowserTrack,AudioBrowserTrack,MidiBrowserTrack"
                       );
    ___cxa_atexit(FUN_101480bac,&DAT_106f4fb88,0x100000000);
    ___cxa_guard_release(&DAT_106f4fa18);
  }
  uVar5 = (**(code **)(*param_1 + 0x28))(param_1);
  uVar6 = FUN_10120e310();
  lVar9 = DAT_106f4fb90;
  if (((uVar6 & 1) == 0) && (lVar8 = DAT_106f4fb88, DAT_106f4fb88 != DAT_106f4fb90)) {
    do {
      uVar6 = FUN_10120e048(lVar8,uVar5);
      lVar10 = lVar8;
      if ((uVar6 & 1) != 0) break;
      lVar8 = lVar8 + 0x10;
      lVar10 = lVar9;
    } while (lVar8 != lVar9);
    if (lVar10 != DAT_106f4fb90) {
      plVar7 = (long *)thunk_FUN_1014763d4(param_1,"DeviceChain/DeviceChain");
      if (plVar7 != (long *)0x0) {
        local_48[0] = param_1;
        FUN_101427680(&local_68,"Roar");
        if (local_68 == (int *)0x0) {
          lVar9 = -1;
        }
        else {
          lVar9 = (long)(local_68[1] / 2 + -1);
        }
        FUN_10120d7d0(aiStack_58,local_68 + 4,lVar9);
        if ((local_68 != (int *)0x0) && (iVar3 = *local_68, *local_68 = iVar3 + -1, iVar3 + -1 == 0)
           ) {
          FUN_101449efc();
        }
        local_68 = aiStack_58;
        pplStack_60 = local_48;
        FUN_1014f9d0c(&local_68,plVar7);
        lVar8 = (**(code **)(*plVar7 + 0x150))(plVar7);
        for (lVar9 = *(long *)(lVar8 + 8); lVar9 != lVar8; lVar9 = *(long *)(lVar9 + 8)) {
          FUN_1014fa048(*(undefined8 *)(lVar9 + 0x20),&local_68);
        }
        if ((local_50 != (int *)0x0) && (iVar3 = *local_50, *local_50 = iVar3 + -1, iVar3 + -1 == 0)
           ) {
          FUN_101449efc();
        }
      }
      goto LAB_1014bd9c4;
    }
  }
  uVar5 = (**(code **)(*param_1 + 0x28))(param_1);
  FUN_10120d76c(aiStack_58,"Roar",4);
  iVar3 = FUN_10120e048(uVar5,aiStack_58);
  if ((local_50 != (int *)0x0) && (iVar1 = *local_50, *local_50 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  if (iVar3 == 0) {
    FUN_101471a98(param_1,"Incorrect node type for this translator. Should be Roar or Tracks only.")
    ;
    goto LAB_1014bdb00;
  }
  lVar9 = FUN_1014766b4(param_1,"Stage1_Shaper_Type");
  if ((lVar9 == 0) || (lVar9 = thunk_FUN_1014763d4(lVar9,"Manual/Value"), lVar9 == 0)) {
LAB_1014bd92c:
    lVar9 = FUN_1014766b4(param_1,"Stage2_Shaper_Type");
    if ((lVar9 != 0) && (lVar9 = thunk_FUN_1014763d4(lVar9,"Manual/Value"), lVar9 != 0)) {
      uVar4 = AAbstractNode::GetValue<int>();
      if (0xb < uVar4) goto LAB_1014bdadc;
      AAbstractNode::SetValue<int>((int)lVar9);
    }
    lVar9 = FUN_1014766b4(param_1,"Stage3_Shaper_Type");
    if ((lVar9 == 0) || (lVar9 = thunk_FUN_1014763d4(lVar9,"Manual/Value"), lVar9 == 0)) {
LAB_1014bd9c4:
      if (*(long *)PTR____stack_chk_guard_1064f8818 == local_38) {
        return;
      }
                    /* WARNING: Subroutine does not return */
      ___stack_chk_fail();
    }
    uVar4 = AAbstractNode::GetValue<int>();
    if (uVar4 < 0xc) {
      AAbstractNode::SetValue<int>((int)lVar9);
      goto LAB_1014bd9c4;
    }
  }
  else {
    uVar4 = AAbstractNode::GetValue<int>();
    if (uVar4 < 0xc) {
      AAbstractNode::SetValue<int>((int)lVar9);
      goto LAB_1014bd92c;
    }
  }
LAB_1014bdadc:
  FUN_101471a98(lVar9,"Enum out of range");
LAB_1014bdb00:
                    /* WARNING: Does not return */
  pcVar2 = (code *)SoftwareBreakpoint(1,0x1014bdb04);
  (*pcVar2)();
}


// 0x1014bdbe0 FUN_1014bdbe0 state=exported warnings=[]

void FUN_1014bdbe0(undefined8 param_1)

{
  int iVar1;
  long lVar2;
  long *plVar3;
  undefined8 uVar4;
  undefined1 auStack_40 [8];
  undefined1 auStack_38 [8];
  
  lVar2 = FUN_1014766b4(param_1,"NoteAlgorithms");
  if (lVar2 != 0) {
    FUN_10146b5c4(auStack_38,lVar2);
    FUN_10146b644(auStack_40,lVar2);
    while (iVar1 = FUN_10146b928(auStack_38,auStack_40), iVar1 == 0) {
      plVar3 = (long *)FUN_10146b8e0(auStack_38);
      (**(code **)(*plVar3 + 0x28))();
      uVar4 = FUN_10120e26c();
      iVar1 = FUN_1014289f4(uVar4,"ArticulateAlgorithm");
      if (iVar1 != 0) {
        (**(code **)(*plVar3 + 0x30))(plVar3,"ArticulateAlgorithm","SpanAlgorithm");
      }
      FUN_10146b8cc(auStack_38);
    }
    FUN_10146b6f0(auStack_40);
    FUN_10146b6f0(auStack_38);
  }
  return;
}


// 0x1014bdce8 FUN_1014bdce8 state=exported warnings=[]

void FUN_1014bdce8(long *param_1)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  undefined8 uVar4;
  long *plVar5;
  ulong uVar6;
  long lVar7;
  int *piVar8;
  long lVar9;
  int *piVar10;
  int **local_60;
  undefined8 *puStack_58;
  int *local_50;
  int *local_48;
  undefined8 local_38;
  
  uVar4 = (**(code **)(*param_1 + 0x28))();
  FUN_10120d76c(&local_50,"MidiTrack",9);
  iVar3 = FUN_10120e048(uVar4,&local_50);
  if ((local_48 != (int *)0x0) && (iVar1 = *local_48, *local_48 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  if (iVar3 == 0) {
    iVar3 = (**(code **)(*param_1 + 0x70))(param_1,"ReferencePitch");
    if ((iVar3 != 0) &&
       (uVar6 = (**(code **)(*param_1 + 0x70))(param_1,"DefaultReferencePitch"), (uVar6 & 1) == 0))
    {
      plVar5 = (long *)(**(code **)(*param_1 + 0x48))(param_1,"ReferencePitch");
      (**(code **)(*plVar5 + 0x38))(&local_50);
      (**(code **)(*param_1 + 0xb0))(param_1,local_50,"DefaultReferencePitch");
      if ((local_50 != (int *)0x0) &&
         (iVar3 = local_50[2], local_50[2] = iVar3 + -1, iVar3 + -1 == 0)) {
        FUN_10128eea0();
      }
    }
  }
  else {
    iVar3 = (**(code **)(*param_1 + 0x70))(param_1,"Tuned");
    if (iVar3 == 0) {
      plVar5 = (long *)(**(code **)(*param_1 + 0x80))(param_1,"RemoteableBool",1,"IsTuned");
      local_38 = (**(code **)(*plVar5 + 0x80))(plVar5,"Bool",0,"Value");
      AAbstractNode::SetValue<bool>(SUB81(local_38,0));
      thunk_FUN_10146bd64(&local_50,"DrumGroupDevice,InstrumentImpulse");
      puStack_58 = &local_38;
      local_60 = &local_50;
      uVar4 = (**(code **)(*param_1 + 0x28))(param_1);
      uVar6 = FUN_10120e310();
      piVar2 = local_48;
      if (((uVar6 & 1) == 0) && (piVar10 = local_50, local_50 != local_48)) {
        do {
          uVar6 = FUN_10120e048(piVar10,uVar4);
          piVar8 = piVar10;
          if ((uVar6 & 1) != 0) break;
          piVar10 = piVar10 + 4;
          piVar8 = piVar2;
        } while (piVar10 != piVar2);
        if (piVar8 != local_48) {
          AAbstractNode::SetValue<bool>(SUB81(local_38,0));
        }
      }
      lVar7 = (**(code **)(*param_1 + 0x150))(param_1);
      piVar2 = local_50;
      for (lVar9 = *(long *)(lVar7 + 8); local_50 = piVar2, lVar9 != lVar7;
          lVar9 = *(long *)(lVar9 + 8)) {
        FUN_1014fa330(*(undefined8 *)(lVar9 + 0x20),&local_60);
        piVar2 = local_50;
      }
      piVar10 = local_48;
      if (piVar2 != (int *)0x0) {
        for (; piVar10 != piVar2; piVar10 = piVar10 + -4) {
          piVar8 = *(int **)(piVar10 + -2);
          if ((piVar8 != (int *)0x0) && (iVar3 = *piVar8, *piVar8 = iVar3 + -1, iVar3 + -1 == 0)) {
            FUN_101449efc();
          }
        }
        operator_delete(local_50);
        return;
      }
    }
    else {
      (**(code **)(*param_1 + 200))(param_1,"Tuned","IsTuned");
    }
  }
  return;
}


// 0x1014be538 FUN_1014be538 state=exported warnings=[]

void FUN_1014be538(long *param_1)

{
  bool bVar1;
  int iVar2;
  ulong uVar3;
  long lVar4;
  long *plVar5;
  
  uVar3 = (**(code **)(*param_1 + 0x70))(param_1,"ShouldSceneTempoAndTimeSignatureBeVisible");
  if (((uVar3 & 1) == 0) &&
     (lVar4 = thunk_FUN_1014763d4(param_1,
                                  "MainTrack/DeviceChain/TrackDevice/ViewStateSesstionTrackWidth/Value"
                                 ), lVar4 != 0)) {
    iVar2 = AAbstractNode::GetValue<int>();
    if (iVar2 < 0xa9) {
      if (iVar2 < 0x83) {
        return;
      }
    }
    else {
      uVar3 = FUN_1014fab80(param_1,"IsTempoEnabled/Value");
      if (((uVar3 & 1) != 0) ||
         (uVar3 = FUN_1014fab80(param_1,"IsTimeSignatureEnabled/Value"), (uVar3 & 1) != 0))
      goto LAB_1014be5d4;
    }
    iVar2 = FUN_1014fab80(param_1,"IsTempoEnabled/Value");
    if (iVar2 != 0) {
LAB_1014be5d4:
      AAbstractNode::SetValue<int>((int)lVar4);
      plVar5 = (long *)(**(code **)(*param_1 + 0x80))
                                 (param_1,"RemoteableBool",1,
                                  "ShouldSceneTempoAndTimeSignatureBeVisible");
      bVar1 = (bool)(**(code **)(*plVar5 + 0x80))(plVar5,"Bool",0,"Value");
      AAbstractNode::SetValue<bool>(bVar1);
      return;
    }
  }
  return;
}


// 0x1014be794 FUN_1014be794 state=exported warnings=[]

void FUN_1014be794(long *param_1)

{
  long lVar1;
  int iVar2;
  undefined8 uVar3;
  ulong uVar4;
  long lVar5;
  long lVar6;
  
  if ((DAT_106f4fa28 & 1) == 0) goto LAB_1014be974;
  do {
    if (((DAT_106f4fa30 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_106f4fa30), iVar2 != 0)) {
      thunk_FUN_10146bd64(&DAT_106f4fbd0,"SongPrefData");
      ___cxa_atexit(FUN_101480bac,&DAT_106f4fbd0,0x100000000);
      ___cxa_guard_release(&DAT_106f4fa30);
    }
    if (((DAT_106f4fa38 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_106f4fa38), iVar2 != 0)) {
      thunk_FUN_10146bd64(&DAT_106f4fbe8,
                          "Song,ArrangerSong,LiveDocument,MidiSong,MockMidiSongNoUnit,PluginSong,SampleSong,VideoSong"
                         );
      ___cxa_atexit(FUN_101480bac,&DAT_106f4fbe8,0x100000000);
      ___cxa_guard_release(&DAT_106f4fa38);
    }
    uVar3 = (**(code **)(*param_1 + 0x28))(param_1);
    uVar4 = FUN_10120e310();
    lVar1 = DAT_106f4fbc0;
    if (((uVar4 & 1) == 0) && (lVar5 = DAT_106f4fbb8, DAT_106f4fbb8 != DAT_106f4fbc0)) {
      do {
        uVar4 = FUN_10120e048(lVar5,uVar3);
        lVar6 = lVar5;
        if ((uVar4 & 1) != 0) break;
        lVar5 = lVar5 + 0x10;
        lVar6 = lVar1;
      } while (lVar5 != lVar1);
      if (lVar6 != DAT_106f4fbc0) {
        FUN_101476654(param_1,"ViewStateSesstionTrackWidth","ViewStateSessionTrackWidth");
        return;
      }
    }
    uVar3 = (**(code **)(*param_1 + 0x28))(param_1);
    uVar4 = FUN_10120e310();
    lVar1 = DAT_106f4fbd8;
    if (((uVar4 & 1) == 0) && (lVar5 = DAT_106f4fbd0, DAT_106f4fbd0 != DAT_106f4fbd8)) {
      do {
        uVar4 = FUN_10120e048(lVar5,uVar3);
        lVar6 = lVar5;
        if ((uVar4 & 1) != 0) break;
        lVar5 = lVar5 + 0x10;
        lVar6 = lVar1;
      } while (lVar5 != lVar1);
      if (lVar6 != DAT_106f4fbd8) {
        FUN_101476654(param_1,"DockViewGuestHeight","DeviceBreakoutViewHeight");
        return;
      }
    }
    uVar3 = (**(code **)(*param_1 + 0x28))(param_1);
    uVar4 = FUN_10120e310();
    lVar1 = DAT_106f4fbf0;
    if (((uVar4 & 1) == 0) && (lVar5 = DAT_106f4fbe8, DAT_106f4fbe8 != DAT_106f4fbf0)) {
      do {
        uVar4 = FUN_10120e048(lVar5,uVar3);
        lVar6 = lVar5;
        if ((uVar4 & 1) != 0) break;
        lVar5 = lVar5 + 0x10;
        lVar6 = lVar1;
      } while (lVar5 != lVar1);
      if (lVar6 != DAT_106f4fbf0) {
        FUN_101476654(param_1,"ViewStateSessionMixerHeight",
                      "ViewStateSessionMixerVolumeSectionHeight");
        return;
      }
    }
    FUN_101471a98(param_1,
                  "Incorrect node type for this translator. Should be TrackDevice, SongPrefData or Song only."
                 );
LAB_1014be974:
    iVar2 = ___cxa_guard_acquire(&DAT_106f4fa28);
    if (iVar2 != 0) {
      thunk_FUN_10146bd64(&DAT_106f4fbb8,"TrackDevice,MainTrackDevice");
      ___cxa_atexit(FUN_101480bac,&DAT_106f4fbb8,0x100000000);
      ___cxa_guard_release(&DAT_106f4fa28);
    }
  } while( true );
}


// 0x1014bed60 FUN_1014bed60 state=exported-with-warnings warnings=['/* WARNING: Subroutine does not return */']

void FUN_1014bed60(long *param_1)

{
  int iVar1;
  int iVar2;
  undefined8 uVar3;
  ulong uVar4;
  long *plVar5;
  long lVar6;
  _Unwind_Exception *exception_object;
  long lVar7;
  long lVar8;
  long *local_70;
  long **pplStack_68;
  long **local_60;
  long *local_58;
  int *local_50;
  undefined1 *puStack_48;
  int aiStack_40 [2];
  int *local_38;
  
  local_60 = &local_58;
  local_58 = param_1;
  if (((DAT_106f4fa40 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_106f4fa40), iVar2 != 0)) {
    thunk_FUN_10146bd64(&DAT_106f4fc00,
                        "Track,AbstractGroupTrack,AbstractSendTrack,AudioBrowserTrack,AudioTrack,BrowserTrack,GroupTrack,MainTrack,MetronomeTrack,MidiBrowserTrack,MidiTrack,PlayerTrack,PreHearTrack,SendTrack"
                       );
    ___cxa_atexit(FUN_101480bac,&DAT_106f4fc00,0x100000000);
    ___cxa_guard_release(&DAT_106f4fa40);
  }
  uVar3 = (**(code **)(*local_58 + 0x28))();
  uVar4 = FUN_10120e310();
  lVar7 = DAT_106f4fc08;
  if (((uVar4 & 1) == 0) && (lVar6 = DAT_106f4fc00, DAT_106f4fc00 != DAT_106f4fc08)) {
    do {
      uVar4 = FUN_10120e048(lVar6,uVar3);
      lVar8 = lVar6;
      if ((uVar4 & 1) != 0) break;
      lVar6 = lVar6 + 0x10;
      lVar8 = lVar7;
    } while (lVar6 != lVar7);
    if (lVar8 != DAT_106f4fc08) {
      plVar5 = (long *)thunk_FUN_1014763d4(local_58,"DeviceChain/DeviceChain");
      if (plVar5 == (long *)0x0) {
        return;
      }
      local_70 = local_58;
      pplStack_68 = local_60;
      FUN_101427680(&local_50,"Limiter");
      if (local_50 == (int *)0x0) {
        lVar7 = -1;
      }
      else {
        lVar7 = (long)(local_50[1] / 2 + -1);
      }
      FUN_10120d7d0(aiStack_40,local_50 + 4,lVar7);
      if ((local_50 != (int *)0x0) && (iVar2 = *local_50, *local_50 = iVar2 + -1, iVar2 + -1 == 0))
      {
        FUN_101449efc();
      }
      local_50 = aiStack_40;
      puStack_48 = (undefined1 *)&local_70;
      uVar3 = (**(code **)(*plVar5 + 0x28))(plVar5);
      iVar2 = FUN_10120e048(aiStack_40,uVar3);
      if (iVar2 != 0) {
        FUN_1014fac78(&pplStack_68,plVar5,local_70);
      }
      lVar6 = (**(code **)(*plVar5 + 0x150))(plVar5);
      for (lVar7 = *(long *)(lVar6 + 8); lVar7 != lVar6; lVar7 = *(long *)(lVar7 + 8)) {
        FUN_1014fb0a8(*(undefined8 *)(lVar7 + 0x20),&local_50);
      }
      if (local_38 == (int *)0x0) {
        return;
      }
      iVar2 = *local_38;
      *local_38 = iVar2 + -1;
      if (iVar2 + -1 != 0) {
        return;
      }
      FUN_101449efc();
      return;
    }
  }
  uVar3 = (**(code **)(*local_58 + 0x28))();
  FUN_10120d76c(aiStack_40,"Limiter",7);
  iVar2 = FUN_10120e048(uVar3,aiStack_40);
  if ((local_38 != (int *)0x0) && (iVar1 = *local_38, *local_38 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  if (iVar2 != 0) {
    FUN_1014fac78(&local_60,local_58,0);
    return;
  }
  exception_object = (_Unwind_Exception *)FUN_105413524();
  ___cxa_guard_abort(&DAT_106f4fa40);
                    /* WARNING: Subroutine does not return */
  __Unwind_Resume(exception_object);
}


// 0x1014bf1a0 FUN_1014bf1a0 state=exported warnings=[]

void FUN_1014bf1a0(undefined8 param_1)

{
  bool bVar1;
  int iVar2;
  int iVar3;
  long *plVar4;
  long *plVar5;
  undefined8 uVar6;
  int *local_40;
  long *local_38;
  
  plVar4 = (long *)FUN_1014766b4(param_1,"ContentLanes");
  if (plVar4 != (long *)0x0) {
    FUN_10146b5c4(&local_38,plVar4);
    FUN_10146b644(&local_40,plVar4);
    while (iVar2 = FUN_10146b928(&local_38,&local_40), iVar2 == 0) {
      plVar5 = (long *)FUN_10146b8e0(&local_38);
      (**(code **)(*plVar5 + 0x28))();
      uVar6 = FUN_10120e26c();
      iVar2 = FUN_1014289f4(uVar6,"MidiEditorLaneModel");
      if ((iVar2 != 0) && (iVar2 = (**(code **)(*plVar5 + 0x70))(plVar5,"Type"), iVar2 != 0)) {
        iVar2 = (**(code **)(*plVar5 + 0x60))(plVar5,"Type");
        iVar3 = AAbstractNode::GetValue<int>();
        if ((iVar3 == 5) || (iVar3 == 4)) {
          AAbstractNode::SetValue<int>(iVar2);
        }
      }
      FUN_10146b8cc(&local_38);
    }
    FUN_10146b6f0(&local_40);
    FUN_10146b6f0(&local_38);
    FUN_10142d468(&local_40,L"MidiEditorLaneModel");
    FUN_10146c94c(&local_38,&local_40,1);
    if ((local_40 != (int *)0x0) && (iVar2 = *local_40, *local_40 = iVar2 + -1, iVar2 + -1 == 0)) {
      FUN_101449efc();
    }
    iVar2 = (**(code **)(*local_38 + 0x80))(local_38,"Int",0,"Type");
    AAbstractNode::SetValue<int>(iVar2);
    plVar5 = (long *)(**(code **)(*local_38 + 0x80))(local_38,"RemoteableBool",1,"IsMinimized");
    bVar1 = (bool)(**(code **)(*plVar5 + 0x80))(plVar5,"Bool",0,"Value");
    AAbstractNode::SetValue<bool>(bVar1);
    (**(code **)(*plVar4 + 0x120))(plVar4,local_38,1,0x80000000);
    if ((local_38 != (long *)0x0) &&
       (iVar2 = (int)local_38[1] + -1, *(int *)(local_38 + 1) = iVar2, iVar2 == 0)) {
      FUN_10128eea0();
    }
  }
  return;
}


// 0x1014bf65c FUN_1014bf65c state=exported-with-warnings warnings=['/* WARNING: Could not recover jumptable at 0x0001014bf6dc. Too many branches */', '/* WARNING: Treating indirect jump as call */']

void FUN_1014bf65c(long *param_1)

{
  int iVar1;
  long *plVar2;
  
  iVar1 = (**(code **)(*param_1 + 0x70))(param_1,"ChooserBar");
  if (iVar1 != 0) {
    (**(code **)(*param_1 + 200))(param_1,"ChooserBar","SelectedDocumentViewInMainWindow");
    plVar2 = (long *)(**(code **)(*param_1 + 0x60))(param_1,"SelectedDocumentViewInMainWindow");
                    /* WARNING: Could not recover jumptable at 0x0001014bf6dc. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar2 + 0x30))(plVar2,"RemoteableInt","RemoteableEnum");
    return;
  }
  return;
}


// 0x1014bf8e4 FUN_1014bf8e4 state=exported-with-warnings warnings=['/* WARNING: Does not return */', '/* WARNING: Subroutine does not return */']

void FUN_1014bf8e4(long *param_1)

{
  int iVar1;
  code *pcVar2;
  int iVar3;
  uint uVar4;
  undefined8 uVar5;
  ulong uVar6;
  long *plVar7;
  long lVar8;
  long lVar9;
  long lVar10;
  int *local_68;
  long **pplStack_60;
  int aiStack_58 [2];
  int *local_50;
  long *local_48 [2];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_1064f8818;
  if (((DAT_106f4fa48 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_106f4fa48), iVar3 != 0)) {
    thunk_FUN_10146bd64(&DAT_106f4fc18,
                        "Track,MasterTrack,AudioTrack,MidiTrack,PlayerTrack,PreHearTrack,AbstractGroupTrack,AbstractSendTrack,GroupTrack,SendTrack,MetronomeTrack,BrowserTrack,AudioBrowserTrack,MidiBrowserTrack"
                       );
    ___cxa_atexit(FUN_101480bac,&DAT_106f4fc18,0x100000000);
    ___cxa_guard_release(&DAT_106f4fa48);
  }
  uVar5 = (**(code **)(*param_1 + 0x28))(param_1);
  uVar6 = FUN_10120e310();
  lVar9 = DAT_106f4fc20;
  if (((uVar6 & 1) == 0) && (lVar8 = DAT_106f4fc18, DAT_106f4fc18 != DAT_106f4fc20)) {
    do {
      uVar6 = FUN_10120e048(lVar8,uVar5);
      lVar10 = lVar8;
      if ((uVar6 & 1) != 0) break;
      lVar8 = lVar8 + 0x10;
      lVar10 = lVar9;
    } while (lVar8 != lVar9);
    if (lVar10 != DAT_106f4fc20) {
      plVar7 = (long *)thunk_FUN_1014763d4(param_1,"DeviceChain/DeviceChain");
      if (plVar7 != (long *)0x0) {
        local_48[0] = param_1;
        FUN_101427680(&local_68,"Saturator");
        if (local_68 == (int *)0x0) {
          lVar9 = -1;
        }
        else {
          lVar9 = (long)(local_68[1] / 2 + -1);
        }
        FUN_10120d7d0(aiStack_58,local_68 + 4,lVar9);
        if ((local_68 != (int *)0x0) && (iVar3 = *local_68, *local_68 = iVar3 + -1, iVar3 + -1 == 0)
           ) {
          FUN_101449efc();
        }
        local_68 = aiStack_58;
        pplStack_60 = local_48;
        FUN_1014fb6dc(&local_68,plVar7);
        lVar8 = (**(code **)(*plVar7 + 0x150))(plVar7);
        for (lVar9 = *(long *)(lVar8 + 8); lVar9 != lVar8; lVar9 = *(long *)(lVar9 + 8)) {
          FUN_1014fb9e4(*(undefined8 *)(lVar9 + 0x20),&local_68);
        }
        if ((local_50 != (int *)0x0) && (iVar3 = *local_50, *local_50 = iVar3 + -1, iVar3 + -1 == 0)
           ) {
          FUN_101449efc();
        }
      }
      goto LAB_1014bfb08;
    }
  }
  uVar5 = (**(code **)(*param_1 + 0x28))(param_1);
  FUN_10120d76c(aiStack_58,"Saturator",9);
  iVar3 = FUN_10120e048(uVar5,aiStack_58);
  if ((local_50 != (int *)0x0) && (iVar1 = *local_50, *local_50 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  if (((iVar3 != 0) && (lVar9 = FUN_1014766b4(param_1,"Type"), lVar9 != 0)) &&
     (lVar9 = thunk_FUN_1014763d4(lVar9,"Manual/Value"), lVar9 != 0)) {
    uVar4 = AAbstractNode::GetValue<int>();
    if (7 < uVar4) {
      FUN_101471a98(lVar9,"Enum out of range");
                    /* WARNING: Does not return */
      pcVar2 = (code *)SoftwareBreakpoint(1,0x1014bfb98);
      (*pcVar2)();
    }
    AAbstractNode::SetValue<int>((int)lVar9);
  }
LAB_1014bfb08:
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


// 0x1014bfc24 FUN_1014bfc24 state=exported-with-warnings warnings=['/* WARNING: Subroutine does not return */']

void FUN_1014bfc24(long *param_1)

{
  int iVar1;
  int iVar2;
  undefined8 uVar3;
  ulong uVar4;
  long *plVar5;
  long lVar6;
  _Unwind_Exception *exception_object;
  long lVar7;
  long lVar8;
  long *local_70;
  long **pplStack_68;
  long **local_60;
  long *local_58;
  int *local_50;
  undefined1 *puStack_48;
  int aiStack_40 [2];
  int *local_38;
  
  local_60 = &local_58;
  local_58 = param_1;
  if (((DAT_106f4fa50 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_106f4fa50), iVar2 != 0)) {
    thunk_FUN_10146bd64(&DAT_106f4fc30,
                        "Track,AbstractGroupTrack,AbstractSendTrack,AudioBrowserTrack,AudioTrack,BrowserTrack,GroupTrack,MainTrack,MetronomeTrack,MidiBrowserTrack,MidiTrack,PlayerTrack,PreHearTrack,SendTrack"
                       );
    ___cxa_atexit(FUN_101480bac,&DAT_106f4fc30,0x100000000);
    ___cxa_guard_release(&DAT_106f4fa50);
  }
  uVar3 = (**(code **)(*local_58 + 0x28))();
  uVar4 = FUN_10120e310();
  lVar7 = DAT_106f4fc38;
  if (((uVar4 & 1) == 0) && (lVar6 = DAT_106f4fc30, DAT_106f4fc30 != DAT_106f4fc38)) {
    do {
      uVar4 = FUN_10120e048(lVar6,uVar3);
      lVar8 = lVar6;
      if ((uVar4 & 1) != 0) break;
      lVar6 = lVar6 + 0x10;
      lVar8 = lVar7;
    } while (lVar6 != lVar7);
    if (lVar8 != DAT_106f4fc38) {
      plVar5 = (long *)thunk_FUN_1014763d4(local_58,"DeviceChain/DeviceChain");
      if (plVar5 == (long *)0x0) {
        return;
      }
      local_70 = local_58;
      pplStack_68 = local_60;
      FUN_101427680(&local_50,"Saturator");
      if (local_50 == (int *)0x0) {
        lVar7 = -1;
      }
      else {
        lVar7 = (long)(local_50[1] / 2 + -1);
      }
      FUN_10120d7d0(aiStack_40,local_50 + 4,lVar7);
      if ((local_50 != (int *)0x0) && (iVar2 = *local_50, *local_50 = iVar2 + -1, iVar2 + -1 == 0))
      {
        FUN_101449efc();
      }
      local_50 = aiStack_40;
      puStack_48 = (undefined1 *)&local_70;
      uVar3 = (**(code **)(*plVar5 + 0x28))(plVar5);
      iVar2 = FUN_10120e048(aiStack_40,uVar3);
      if (iVar2 != 0) {
        FUN_1014fbccc(&pplStack_68,plVar5,local_70);
      }
      lVar6 = (**(code **)(*plVar5 + 0x150))(plVar5);
      for (lVar7 = *(long *)(lVar6 + 8); lVar7 != lVar6; lVar7 = *(long *)(lVar7 + 8)) {
        FUN_1014fc0e0(*(undefined8 *)(lVar7 + 0x20),&local_50);
      }
      if (local_38 == (int *)0x0) {
        return;
      }
      iVar2 = *local_38;
      *local_38 = iVar2 + -1;
      if (iVar2 + -1 != 0) {
        return;
      }
      FUN_101449efc();
      return;
    }
  }
  uVar3 = (**(code **)(*local_58 + 0x28))();
  FUN_10120d76c(aiStack_40,"Saturator",9);
  iVar2 = FUN_10120e048(uVar3,aiStack_40);
  if ((local_38 != (int *)0x0) && (iVar1 = *local_38, *local_38 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  if (iVar2 != 0) {
    FUN_1014fbccc(&local_60,local_58,0);
    return;
  }
  exception_object = (_Unwind_Exception *)FUN_105413548();
  ___cxa_guard_abort(&DAT_106f4fa50);
                    /* WARNING: Subroutine does not return */
  __Unwind_Resume(exception_object);
}


// 0x1014c09f8 FUN_1014c09f8 state=exported warnings=[]

void FUN_1014c09f8(long *param_1)

{
  int iVar1;
  undefined8 uVar2;
  long lVar3;
  
  (**(code **)(*param_1 + 0x28))();
  uVar2 = FUN_10120e26c();
  iVar1 = FUN_1014289f4(uVar2,"AudioTrack");
  if ((iVar1 != 0) && (lVar3 = thunk_FUN_1014763d4(param_1,"DeviceChain/MainSequencer"), lVar3 != 0)
     ) {
    FUN_1014fc22c();
  }
  lVar3 = thunk_FUN_1014763d4(param_1,"DeviceChain/FreezeSequencer");
  if (lVar3 != 0) {
    FUN_1014fc22c();
    return;
  }
  return;
}


