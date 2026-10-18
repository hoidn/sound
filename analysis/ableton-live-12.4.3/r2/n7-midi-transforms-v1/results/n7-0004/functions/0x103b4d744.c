
undefined8
FUN_103b4d744(undefined4 param_1,undefined8 param_2,long param_3,undefined8 param_4,
             undefined8 param_5,undefined8 param_6,undefined4 *param_7,undefined8 param_8)

{
  int iVar1;
  long lVar2;
  undefined8 uVar3;
  runtime_error *this;
  undefined8 uVar4;
  undefined1 auStack_a8 [8];
  long local_a0;
  int local_98;
  char local_94;
  undefined1 auStack_88 [8];
  long local_80;
  int local_78;
  char local_74;
  int *local_68;
  
  lVar2 = FUN_1026048f0();
  if (lVar2 == 0) {
    this = (runtime_error *)___cxa_allocate_exception(0x10);
    std::runtime_error::runtime_error(this,"The passed midi_map_handle is invalid.");
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(this,PTR_typeinfo_1064f86b0,PTR__runtime_error_1064f8560);
  }
  uVar3 = FUN_1026048f0(param_2);
  uVar4 = *(undefined8 *)(param_3 + 0x18);
  FUN_101b7ca84(auStack_a8,*(undefined1 *)(param_7 + 5));
  FUN_103b55a9c(&local_68,param_7 + 2);
  if (local_68 != (int *)0x0) {
    if (0 < local_68[1]) {
      FUN_101b7cbcc(param_7[4],auStack_88,*param_7,param_7[1],local_68 + 4,local_68[1],
                    *(undefined1 *)(param_7 + 5));
      FUN_101b7cf54(auStack_a8,auStack_88);
      if ((local_80 != 0) && (local_74 == '\x01')) {
        thunk_FUN_101aa0360(local_80,(long)local_78);
      }
      if (local_68 == (int *)0x0) goto LAB_103b4d828;
    }
    iVar1 = *local_68;
    *local_68 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc(local_68);
    }
  }
LAB_103b4d828:
  uVar3 = FUN_102593258(param_1,uVar3,uVar4,param_4,param_5,param_6,auStack_a8,param_8);
  if ((local_a0 != 0) && (local_94 == '\x01')) {
    thunk_FUN_101aa0360(local_a0,(long)local_98);
  }
  return uVar3;
}

