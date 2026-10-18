
/* WARNING: Removing unreachable block (ram,0x000103198554) */
/* WARNING: Removing unreachable block (ram,0x00010319861c) */
/* WARNING: Type propagation algorithm not settling */

undefined8 FUN_1031983d4(long param_1,undefined8 *param_2)

{
  int iVar1;
  int *piVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  int *piVar6;
  void *local_120;
  undefined8 local_118;
  char local_109;
  void *local_100 [2];
  char local_e9;
  undefined4 local_e8;
  undefined4 uStack_e4;
  char local_d1;
  undefined4 local_d0;
  undefined4 uStack_cc;
  char local_b9;
  long local_b8;
  long *local_b0;
  void *local_a8 [2];
  char local_91;
  undefined1 local_90 [24];
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 local_50;
  
  piVar6 = (int *)*param_2;
  if (piVar6 != (int *)0x0) {
    *piVar6 = *piVar6 + 1;
  }
  piVar2 = *(int **)(param_1 + 0x18);
  if ((piVar2 != (int *)0x0) && (iVar1 = *piVar2, *piVar2 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
    piVar6 = (int *)*param_2;
  }
  *(int **)(param_1 + 0x18) = piVar6;
  FUN_1011db938(&local_b8);
  (**(code **)(*local_b0 + 0xc0))(local_a8);
  local_d0 = 0x69766544;
  uStack_cc = 0x736563;
  local_b9 = '\a';
  FUN_100241e54(local_90,local_a8,&local_d0);
  local_e8 = 0x63614d;
  local_d1 = '\x03';
  FUN_100241e54(&local_120,local_90,&local_e8);
  FUN_101463578(local_100,param_2);
  FUN_100241e54(&local_78,&local_120,local_100);
  FUN_10025dc7c(&local_78,".bundle","");
  local_50 = local_68;
  uStack_58 = uStack_70;
  local_60 = local_78;
  uStack_70 = 0;
  local_68 = 0;
  local_78 = 0;
  if (local_e9 < '\0') {
    operator_delete(local_100[0]);
  }
  if (local_109 < '\0') {
    operator_delete(local_120);
  }
  if (local_d1 < '\0') {
    operator_delete((void *)CONCAT44(uStack_e4,local_e8));
  }
  if (local_b9 < '\0') {
    operator_delete((void *)CONCAT44(uStack_cc,local_d0));
  }
  if (local_91 < '\0') {
    operator_delete(local_a8[0]);
  }
  if ((local_b8 != 0) &&
     (iVar1 = *(int *)(local_b8 + 8) + -1, *(int *)(local_b8 + 8) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  uVar3 = FUN_103e9728c(&local_60);
  if ((int)uVar3 != 0) {
    uVar4 = FUN_101aa0f14(&local_60);
    uVar5 = FUN_101a9419c();
    FUN_101ab7348(&local_120,&DAT_107027d98,0x100500,0x200600,0);
    FUN_101a9c618(local_118,uVar5);
    FUN_101a9c600(local_118,uVar4);
    (**(code **)((long)local_120 + 0x10))(&local_120);
    FUN_101ab786c(&local_120);
    *(undefined8 *)(param_1 + 0x20) = uVar5;
  }
  return uVar3;
}

