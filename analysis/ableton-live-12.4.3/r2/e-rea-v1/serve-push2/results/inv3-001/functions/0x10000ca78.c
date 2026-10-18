
void FUN_10000ca78(int param_1,void *param_2,undefined8 param_3,long param_4)

{
  ulong uVar1;
  ushort *puVar2;
  byte bVar3;
  int iVar4;
  long *plVar5;
  long *plVar6;
  size_t sVar7;
  undefined4 *puVar8;
  long *plVar9;
  undefined8 uVar10;
  char *pcVar11;
  ushort *puVar12;
  undefined8 uVar13;
  undefined1 auStack_78 [8];
  QArrayData *local_70 [3];
  QArrayData *local_58;
  undefined8 uStack_50;
  Connection aCStack_40 [8];
  QArrayData *local_38;
  
  if (param_1 != 1) {
    if (param_1 != 0) {
      return;
    }
    if (param_2 == (void *)0x0) {
      return;
    }
    operator_delete(param_2);
    return;
  }
  if (**(int **)(param_4 + 8) != 1) {
    if (**(int **)(param_4 + 8) == 3) {
      uVar10 = std::chrono::system_clock::now();
      FUN_100046504(&local_38,4,uVar10);
      iVar4 = FUN_100042ca8(&local_38);
      if (iVar4 != 0) {
        uVar10 = FUN_10003fe68(&local_38,"Loading the resource ");
        QUrl::toString(aCStack_40,*(undefined8 *)((long)param_2 + 0x18),0);
        FUN_100009ee4(&local_58,aCStack_40);
        uVar10 = FUN_100040d48(uVar10,&local_58);
        uVar10 = FUN_10003fe68(uVar10," failed with: ");
        QQmlComponent::errorString();
        FUN_100009ee4(local_70,auStack_78);
        FUN_100040d48(uVar10,local_70);
        FUN_100225ca8(local_70,aCStack_40,&local_58,auStack_78);
      }
      thunk_FUN_10003f9d4(&local_38);
    }
                    /* WARNING: Subroutine does not return */
    _abort();
  }
  plVar9 = *(long **)((long)param_2 + 0x30);
  plVar5 = (long *)QQmlComponent::create(*(QQmlContext **)((long)param_2 + 0x10));
  plVar6 = (long *)*plVar9;
  if ((plVar6 != plVar5) && (*plVar9 = (long)plVar5, plVar6 != (long *)0x0)) {
    (**(code **)(*plVar6 + 0x20))();
  }
  plVar5 = *(long **)((long)param_2 + 0x20);
  uVar10 = **(undefined8 **)((long)param_2 + 0x28);
  if ((*(char *)((long)plVar5 + 0x17) < '\0') && (plVar5 = (long *)*plVar5, plVar5 == (long *)0x0))
  {
    iVar4 = -1;
  }
  else {
    sVar7 = _strlen((char *)plVar5);
    iVar4 = (int)sVar7;
  }
  local_38 = (QArrayData *)QString::fromAscii_helper((char *)plVar5,iVar4);
  FUN_1000c3dd4(uVar10,&local_38);
  if (*(int *)local_38 != -1) {
    if (*(int *)local_38 != 0) {
      LOAcquire();
      iVar4 = *(int *)local_38;
      *(int *)local_38 = iVar4 + -1;
      LORelease();
      if (iVar4 != 1) goto LAB_10000cb6c;
    }
    QArrayData::deallocate(local_38,2,8);
  }
LAB_10000cb6c:
  uVar10 = *(undefined8 *)((long)param_2 + 0x40);
  uVar13 = *(undefined8 *)((long)param_2 + 0x28);
  local_58 = (QArrayData *)PTR_warnings_10029c0d8;
  uStack_50 = 0;
  puVar8 = operator_new(0x18);
  *puVar8 = 1;
  *(code **)(puVar8 + 2) = FUN_10000d074;
  *(undefined8 *)(puVar8 + 4) = uVar13;
  QObject::connectImpl
            (aCStack_40,uVar10,&local_58,uVar10,0,puVar8,1,0,PTR_staticMetaObject_10029c0d0);
  QMetaObject::Connection::~Connection(aCStack_40);
  pcVar11 = (char *)**(undefined8 **)((long)param_2 + 0x30);
  QVariant::QVariant((QVariant *)&local_58,"Full");
  QObject::setProperty(pcVar11,(QVariant *)"emulatorType");
  QVariant::~QVariant((QVariant *)&local_58);
  puVar12 = *(ushort **)((long)param_2 + 0x38);
  bVar3 = *(byte *)((long)puVar12 + 0x17);
  uVar1 = *(ulong *)(puVar12 + 4);
  if (-1 < (char)bVar3) {
    uVar1 = (ulong)bVar3;
  }
  pcVar11 = "Noto Sans CJK JP";
  if (uVar1 == 2) {
    puVar2 = *(ushort **)puVar12;
    if (-1 < (char)bVar3) {
      puVar2 = puVar12;
    }
    if (*puVar2 == 0x524b) {
      pcVar11 = "Noto Sans CJK KR";
    }
    else {
      pcVar11 = "Noto Sans CJK SC";
      if ((ushort)(*puVar2 >> 8 | *puVar2 << 8) != 0x5a48) {
        pcVar11 = "Noto Sans CJK JP";
      }
    }
  }
  uVar10 = std::chrono::system_clock::now();
  FUN_100046504(&local_58,1,uVar10);
  iVar4 = FUN_100042ca8(&local_58);
  if (iVar4 != 0) {
    uVar10 = FUN_10003fe68(&local_58,"Setting up font substition. Language is ");
    uVar10 = FUN_100040d48(uVar10,puVar12);
    uVar10 = FUN_10003fe68(uVar10," and CJK font is ");
    uVar10 = FUN_10003fe68(uVar10,pcVar11);
    FUN_10003fe68(uVar10,".");
  }
  thunk_FUN_10003f9d4(&local_58);
  local_58 = (QArrayData *)QString::fromAscii_helper("Ableton Sans Book",0x11);
  local_70[0] = (QArrayData *)QString::fromAscii_helper(pcVar11,0x10);
  QFont::insertSubstitution((QString *)&local_58,(QString *)local_70);
  if (*(int *)local_70[0] != -1) {
    if (*(int *)local_70[0] != 0) {
      LOAcquire();
      iVar4 = *(int *)local_70[0];
      *(int *)local_70[0] = iVar4 + -1;
      LORelease();
      if (iVar4 != 1) goto LAB_10000cd34;
    }
    QArrayData::deallocate(local_70[0],2,8);
  }
LAB_10000cd34:
  if (*(int *)local_58 != -1) {
    if (*(int *)local_58 != 0) {
      LOAcquire();
      iVar4 = *(int *)local_58;
      *(int *)local_58 = iVar4 + -1;
      LORelease();
      if (iVar4 != 1) goto LAB_10000cd68;
    }
    QArrayData::deallocate(local_58,2,8);
  }
LAB_10000cd68:
  local_58 = (QArrayData *)QString::fromAscii_helper("Ableton Sans Light",0x12);
  local_70[0] = (QArrayData *)QString::fromAscii_helper(pcVar11,0x10);
  QFont::insertSubstitution((QString *)&local_58,(QString *)local_70);
  if (*(int *)local_70[0] != -1) {
    if (*(int *)local_70[0] != 0) {
      LOAcquire();
      iVar4 = *(int *)local_70[0];
      *(int *)local_70[0] = iVar4 + -1;
      LORelease();
      if (iVar4 != 1) goto LAB_10000cdcc;
    }
    QArrayData::deallocate(local_70[0],2,8);
  }
LAB_10000cdcc:
  if (*(int *)local_58 != -1) {
    if (*(int *)local_58 != 0) {
      LOAcquire();
      iVar4 = *(int *)local_58;
      *(int *)local_58 = iVar4 + -1;
      LORelease();
      if (iVar4 != 1) goto LAB_10000ce00;
    }
    QArrayData::deallocate(local_58,2,8);
  }
LAB_10000ce00:
  local_58 = (QArrayData *)QString::fromAscii_helper("Ableton Sans ExtraLight",0x17);
  local_70[0] = (QArrayData *)QString::fromAscii_helper(pcVar11,0x10);
  QFont::insertSubstitution((QString *)&local_58,(QString *)local_70);
  if (*(int *)local_70[0] != -1) {
    if (*(int *)local_70[0] != 0) {
      LOAcquire();
      iVar4 = *(int *)local_70[0];
      *(int *)local_70[0] = iVar4 + -1;
      LORelease();
      if (iVar4 != 1) goto LAB_10000ce64;
    }
    QArrayData::deallocate(local_70[0],2,8);
  }
LAB_10000ce64:
  if (*(int *)local_58 != -1) {
    if (*(int *)local_58 != 0) {
      LOAcquire();
      iVar4 = *(int *)local_58;
      *(int *)local_58 = iVar4 + -1;
      LORelease();
      if (iVar4 != 1) {
        return;
      }
    }
    QArrayData::deallocate(local_58,2,8);
  }
  return;
}

