
long * _CreateInstanceU(void)

{
  int iVar1;
  long *plVar2;
  
  plVar2 = (long *)FUN_00001b7c();
  if ((plVar2 != (long *)0x0) &&
     (iVar1 = (**(code **)(*plVar2 + 0x68))(plVar2,0x15,0,0), iVar1 == 0)) {
    _fwrite("Error creating device: Ableton devices must implement kCanStopProcessing.\n",0x4a,1,
            *(FILE **)PTR____stderrp_0005c098);
    FUN_00001c18(plVar2);
    return (long *)0x0;
  }
  return plVar2;
}

