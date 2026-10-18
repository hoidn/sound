
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1030cf96c(long param_1,undefined8 param_2)

{
  int iVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  int *local_c0;
  int *local_b8;
  int *local_b0;
  int *local_a8;
  int *local_a0;
  int *local_98;
  int *local_90;
  int *local_88;
  int *local_80;
  int *local_78;
  int *local_70;
  int *local_68;
  int *local_60;
  undefined8 *local_58;
  int *local_50;
  int *local_48;
  int *local_40;
  int *local_38;
  
  FUN_101427680(&local_38,"Mallet");
  uVar3 = *(undefined8 *)(param_1 + 0x30);
  FUN_10142dd4c(&local_40,&local_38," On/Off");
  FUN_1011cb734(&local_48);
  FUN_1031980a4(uVar3,&local_40,1,&local_48);
  if (local_48 != (int *)0x0) {
    iVar1 = *local_48;
    *local_48 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_40 != (int *)0x0) {
    iVar1 = *local_40;
    *local_40 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar4 = *(undefined8 *)(param_1 + 0x48);
  FUN_10142dd4c(&local_50,&local_38," Volume");
  puVar2 = (undefined8 *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *puVar2 = &PTR_thunk_FUN_10128edf8_1068c5778;
  *(undefined4 *)(puVar2 + 3) = 1;
  uVar3 = _DAT_10561dfd0;
  puVar2[5] = _UNK_10561dfd8;
  puVar2[4] = uVar3;
  *(int *)(puVar2 + 1) = *(int *)(puVar2 + 1) + 1;
  local_58 = puVar2;
  FUN_1011cb734(&local_60);
  FUN_103197830(0x3f000000,param_2,uVar4,&local_50,puVar2,&local_60,0,0);
  if (local_60 != (int *)0x0) {
    iVar1 = *local_60;
    *local_60 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  iVar1 = *(int *)(puVar2 + 1);
  *(int *)(puVar2 + 1) = iVar1 + -1;
  if (iVar1 + -1 == 0) {
    FUN_10128eea0(puVar2);
  }
  if (local_50 != (int *)0x0) {
    iVar1 = *local_50;
    *local_50 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = *(undefined8 *)(param_1 + 0x60);
  FUN_10142dd4c(&local_68,&local_38," Volume < Vel");
  FUN_1030cb214(0,param_2,uVar3,&local_68);
  if (local_68 != (int *)0x0) {
    iVar1 = *local_68;
    *local_68 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = *(undefined8 *)(param_1 + 0x78);
  FUN_10142dd4c(&local_70,&local_38," Volume < Key");
  FUN_1030cdf18(0,param_2,uVar3,&local_70);
  if (local_70 != (int *)0x0) {
    iVar1 = *local_70;
    *local_70 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = *(undefined8 *)(param_1 + 0x90);
  FUN_10142dd4c(&local_78,&local_38," Stiffness");
  FUN_1011cb734(&local_80);
  FUN_103197830(0x3f000000,param_2,uVar3,&local_78,0,&local_80,0,0);
  if (local_80 != (int *)0x0) {
    iVar1 = *local_80;
    *local_80 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_78 != (int *)0x0) {
    iVar1 = *local_78;
    *local_78 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = *(undefined8 *)(param_1 + 0xa8);
  FUN_10142dd4c(&local_88,&local_38," Stiffness < Vel");
  FUN_1030cb214(0,param_2,uVar3,&local_88);
  if (local_88 != (int *)0x0) {
    iVar1 = *local_88;
    *local_88 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = *(undefined8 *)(param_1 + 0xc0);
  FUN_10142dd4c(&local_90,&local_38," Stiffness < Key");
  FUN_1030cdf18(0,param_2,uVar3,&local_90);
  if (local_90 != (int *)0x0) {
    iVar1 = *local_90;
    *local_90 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = *(undefined8 *)(param_1 + 0xd8);
  FUN_10142dd4c(&local_98,&local_38," Noise Amount");
  FUN_1011cb734(&local_a0);
  FUN_103197830(0x3f000000,param_2,uVar3,&local_98,0,&local_a0,0,0);
  if (local_a0 != (int *)0x0) {
    iVar1 = *local_a0;
    *local_a0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_98 != (int *)0x0) {
    iVar1 = *local_98;
    *local_98 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = *(undefined8 *)(param_1 + 0xf0);
  FUN_10142dd4c(&local_a8,&local_38," Noise Amount < Vel");
  FUN_1030cb214(0,param_2,uVar3,&local_a8);
  if (local_a8 != (int *)0x0) {
    iVar1 = *local_a8;
    *local_a8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = *(undefined8 *)(param_1 + 0x108);
  FUN_10142dd4c(&local_b0,&local_38," Noise Amount < Key");
  FUN_1030cdf18(0,param_2,uVar3,&local_b0);
  if (local_b0 != (int *)0x0) {
    iVar1 = *local_b0;
    *local_b0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = *(undefined8 *)(param_1 + 0x120);
  FUN_10142dd4c(&local_b8,&local_38," Noise Color");
  FUN_1011cb734(&local_c0);
  FUN_103197830(0x3f000000,param_2,uVar3,&local_b8,0,&local_c0,0,0);
  if (local_c0 != (int *)0x0) {
    iVar1 = *local_c0;
    *local_c0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_b8 != (int *)0x0) {
    iVar1 = *local_b8;
    *local_b8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_38 != (int *)0x0) {
    iVar1 = *local_38;
    *local_38 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

