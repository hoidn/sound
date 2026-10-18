
void FUN_10024a1b4(undefined8 param_1)

{
  undefined8 uVar1;
  long *local_28;
  
  FUN_1002170ac(param_1,"ALTER TABLE plugin_modules   ADD COLUMN processor INTEGER DEFAULT 0; ");
  uVar1 = FUN_1002170d4(param_1);
  FUN_10021728c(&local_28,uVar1,"DELETE FROM plugin_domains");
  if (local_28 != (long *)0x0) {
    (**(code **)(*local_28 + 0xb0))();
  }
  FUN_10020fc48(&local_28);
  uVar1 = FUN_1002170d4(param_1);
  FUN_10021728c(&local_28,uVar1,"DELETE FROM plugin_modules");
  if (local_28 != (long *)0x0) {
    (**(code **)(*local_28 + 0xb0))();
  }
  FUN_10020fc48(&local_28);
  uVar1 = FUN_1002170d4(param_1);
  FUN_10021728c(&local_28,uVar1,"DELETE FROM plugins");
  if (local_28 != (long *)0x0) {
    (**(code **)(*local_28 + 0xb0))();
  }
  FUN_10020fc48(&local_28);
  return;
}

