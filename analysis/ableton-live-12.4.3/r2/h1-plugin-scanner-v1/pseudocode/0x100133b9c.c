
bool FUN_100133b9c(long param_1,undefined8 *param_2)

{
  size_t sVar1;
  ulong uVar2;
  size_t sVar3;
  undefined8 *puVar4;
  undefined8 *puVar5;
  byte bVar6;
  byte bVar7;
  code *pcVar8;
  bool bVar9;
  int iVar10;
  undefined *puVar11;
  char *pcVar12;
  long lVar13;
  long *plVar14;
  undefined **local_88 [2];
  char local_71;
  undefined4 local_70;
  undefined2 uStack_6c;
  undefined2 uStack_6a;
  char local_59;
  undefined **local_58;
  
  local_59 = 5;
  local_70 = 0x65736572;
  uStack_6c = 0x74;
  plVar14 = *(long **)(param_1 + 0x18);
  do {
    if (plVar14 == (long *)0x0) {
      return false;
    }
    uVar2 = plVar14[5];
    puVar4 = (void *)plVar14[4];
    if (-1 < (char)*(byte *)((long)plVar14 + 0x37)) {
      uVar2 = (ulong)*(byte *)((long)plVar14 + 0x37);
      puVar4 = plVar14 + 4;
    }
    sVar1 = uVar2;
    if (4 < uVar2) {
      sVar1 = 5;
    }
    iVar10 = _memcmp(&local_70,puVar4,sVar1);
    if (iVar10 == 0) {
      if (uVar2 < 6) goto LAB_100133c4c;
    }
    else if (-1 < iVar10) {
LAB_100133c4c:
      iVar10 = _memcmp(puVar4,&local_70,sVar1);
      if (iVar10 == 0) {
        if (uVar2 < 5) goto LAB_100133bf4;
      }
      else if (iVar10 < 0) {
LAB_100133bf4:
        plVar14 = plVar14 + 1;
        goto LAB_100133bf8;
      }
      local_59 = '\x05';
      local_70 = 0x65736572;
      uStack_6c = 0x74;
      plVar14 = (long *)FUN_10016bf7c(param_1,&local_70);
      puVar11 = PTR_typeinfo_100b1c300;
      if ((long *)*plVar14 != (long *)0x0) {
        puVar11 = (undefined *)(**(code **)(*(long *)*plVar14 + 0x10))();
      }
      if (((char *)(*(ulong *)(puVar11 + 8) & 0x7fffffffffffffff) !=
           "NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE") &&
         (iVar10 = _strcmp((char *)(*(ulong *)(puVar11 + 8) & 0x7fffffffffffffff),
                           "NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE"),
         iVar10 != 0)) {
        local_88[0] = (undefined **)0x0;
        std::bad_cast::bad_cast((bad_cast *)local_88);
        local_88[0] = &PTR__bad_cast_100b43d08;
        FUN_100138a40(local_88);
        goto LAB_100133ec0;
      }
      lVar13 = *plVar14;
      bVar6 = *(byte *)(lVar13 + 0x1f);
      uVar2 = *(ulong *)(lVar13 + 0x10);
      if (-1 < (char)bVar6) {
        uVar2 = (ulong)bVar6;
      }
      if (uVar2 == 3) {
        plVar14 = (long *)*(long *)(lVar13 + 8);
        if (-1 < (char)bVar6) {
          plVar14 = (long *)(lVar13 + 8);
        }
        if ((short)*plVar14 == 0x6c61 && *(char *)((long)plVar14 + 2) == 'l') {
          bVar9 = true;
          goto joined_r0x000100133e48;
        }
      }
      local_71 = '\x05';
      local_88[0] = (undefined **)CONCAT26(local_88[0]._6_2_,0x7465736572);
      plVar14 = (long *)FUN_10016bf7c(param_1,local_88);
      if ((long *)*plVar14 == (long *)0x0) {
        pcVar12 = (char *)(*(ulong *)(PTR_typeinfo_100b1c300 + 8) & 0x7fffffffffffffff);
        if (pcVar12 != "NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE")
        goto LAB_100133db4;
      }
      else {
        lVar13 = (**(code **)(*(long *)*plVar14 + 0x10))();
        pcVar12 = (char *)(*(ulong *)(lVar13 + 8) & 0x7fffffffffffffff);
        if (pcVar12 != "NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE") {
LAB_100133db4:
          iVar10 = _strcmp(pcVar12,"NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE")
          ;
          if (iVar10 != 0) {
            local_58 = (undefined **)0x0;
            std::bad_cast::bad_cast((bad_cast *)&local_58);
            local_58 = &PTR__bad_cast_100b43d08;
            FUN_100138a40(&local_58);
LAB_100133ec0:
                    /* WARNING: Does not return */
            pcVar8 = (code *)SoftwareBreakpoint(1,0x100133ec4);
            (*pcVar8)();
          }
        }
      }
      lVar13 = *plVar14;
      bVar6 = *(byte *)(lVar13 + 0x1f);
      sVar1 = *(size_t *)(lVar13 + 0x10);
      if (-1 < (char)bVar6) {
        sVar1 = (ulong)bVar6;
      }
      bVar7 = *(byte *)((long)param_2 + 0x17);
      sVar3 = param_2[1];
      if (-1 < (char)bVar7) {
        sVar3 = (ulong)bVar7;
      }
      if (sVar1 == sVar3) {
        puVar4 = *(void **)(lVar13 + 8);
        if (-1 < (char)bVar6) {
          puVar4 = (undefined8 *)(lVar13 + 8);
        }
        puVar5 = (void *)*param_2;
        if (-1 < (char)bVar7) {
          puVar5 = param_2;
        }
        iVar10 = _memcmp(puVar4,puVar5,sVar1);
        bVar9 = iVar10 == 0;
      }
      else {
        bVar9 = false;
      }
      if (local_71 < '\0') {
        operator_delete(local_88[0]);
      }
joined_r0x000100133e48:
      if (-1 < local_59) {
        return bVar9;
      }
      operator_delete((void *)CONCAT26(uStack_6a,CONCAT24(uStack_6c,local_70)));
      return bVar9;
    }
LAB_100133bf8:
    plVar14 = (long *)*plVar14;
  } while( true );
}

