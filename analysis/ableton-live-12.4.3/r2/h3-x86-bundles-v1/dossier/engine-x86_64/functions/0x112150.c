
/* void* OSharedMemory::SInit<false>(int, bool) */

void * OSharedMemory::SInit<false>(int param_1,bool param_2)

{
  TResourceArbiter *this;
  char cVar1;
  int iVar2;
  int *piVar3;
  char *pcVar4;
  int *piVar5;
  undefined8 uVar6;
  int iVar7;
  int iVar8;
  ulong uVar9;
  long lVar10;
  TStamp local_40 [16];
  LineLogger local_30 [8];
  
  TDebugOptionValue<void>::Init((TDebugOptionValue<void> *)&DAT_0180c2f0);
  TSharedMemory::SInit
            (false,&DAT_01814320,&DAT_01814324,(void **)&DAT_01814328,(void **)&DAT_01814330);
  DAT_01814338 = DAT_01814328;
  iVar8 = param_1 + DAT_01814324 + 0xb2437;
  iVar8 = iVar8 - iVar8 % DAT_01814324;
  piVar3 = (int *)TSharedMemory::SAllocBlock(0,iVar8,(void *)0x0);
  if (piVar3 == (int *)0x0) {
                    /* WARNING: Subroutine does not return */
    ASystem::SOutOfMemory();
  }
  DAT_01814348 = '\x01';
  DAT_01814340 = piVar3;
  if (param_2) {
    piVar5 = piVar3;
    if (((*piVar3 == 0x61626c65) && ((char)piVar3[1] == '\0')) &&
       (DAT_01814349 = 1, piVar3[2] == 0xd)) {
      pcVar4 = (char *)AVersionInformation::AppAndVersionString();
      iVar2 = _strncmp((char *)(piVar3 + 3),pcVar4,0x3ff);
      piVar5 = DAT_01814340;
      if (iVar2 != 0) goto joined_r0x00112233;
      DAT_01814349 = 0;
      LOCK();
      *DAT_01814340 = 0;
      UNLOCK();
      TStamp::TStamp(local_40);
      TStamp::Stamp(local_40);
      iVar2 = *DAT_01814340;
      piVar5 = DAT_01814340;
      while (DAT_01814340 = piVar5, iVar2 != 0x61626c65) {
        iVar2 = TStamp::DifferenceInMilliSec(local_40);
        iVar7 = 3000;
        if (DAT_01824380 != '\0') {
          iVar7 = 0;
        }
        if (iVar7 <= iVar2) {
          DAT_01824380 = '\x01';
          uVar6 = std::chrono::system_clock::now();
          ableton::logging::getLogger((logging *)local_30,3,uVar6);
          cVar1 = ableton::logging::detail::LineLogger::isEnabled(local_30);
          if (cVar1 != '\0') {
            ableton::logging::detail::LineLogger::operator<<
                      (local_30,"OSharedMemory: ReWire handshake timed out.");
          }
          ableton::logging::detail::LineLogger::~LineLogger(local_30);
          piVar5 = DAT_01814340;
          goto joined_r0x00112233;
        }
        ASystem::GiveTime();
        piVar5 = DAT_01814340;
        iVar2 = *DAT_01814340;
      }
      DAT_01814348 = '\0';
      *(undefined1 *)(piVar5 + 1) = 1;
    }
    else {
joined_r0x00112233:
      DAT_01814340 = piVar5;
      if (DAT_01814348 != '\0') goto LAB_00112239;
    }
    piVar3 = piVar3 + 0x2c90e;
    DAT_0181434b = 0;
    DAT_0181434c = 0;
    uVar9 = 0;
  }
  else {
LAB_00112239:
    TSharedMemory::SFreeBlock(0);
    DAT_0181434a = 1;
    piVar5 = _malloc((long)iVar8);
    if (piVar5 == (int *)0x0) {
      return (void *)0x0;
    }
    piVar3 = piVar5 + 0x2c90e;
    DAT_0181434b = 0;
    DAT_0181434c = 0;
    uVar9 = 0;
    DAT_01814340 = piVar5;
    if (DAT_01814348 == '\x01') {
      LOCK();
      piVar5[0x24905] = 0;
      UNLOCK();
      LOCK();
      piVar5[0x24906] = -1;
      UNLOCK();
      LOCK();
      piVar5[0x24907] = -1;
      UNLOCK();
      ___bzero(piVar5 + 0x104,0x92000);
      LOCK();
      piVar5[0x24904] = 0;
      UNLOCK();
      lVar10 = 0x92420;
      do {
        piVar5 = DAT_01814340;
        this = (TResourceArbiter *)((long)DAT_01814340 + lVar10);
        TResourceArbiter::TResourceArbiter(this);
        *(undefined8 *)((long)piVar5 + lVar10 + 4) = 0;
        *(undefined8 *)((long)piVar5 + lVar10 + 0x10) = 0;
        *(undefined4 *)((long)piVar5 + lVar10 + 0x18) = 0;
        LOCK();
        *(undefined4 *)((long)piVar5 + lVar10 + 4) = 0;
        UNLOCK();
        LOCK();
        *(undefined4 *)((long)piVar5 + lVar10 + 8) = 0;
        UNLOCK();
        LOCK();
        *(undefined8 *)((long)piVar5 + lVar10 + 0x10) = 0;
        UNLOCK();
        LOCK();
        *(undefined4 *)((long)piVar5 + lVar10 + 0x18) = 0xffffffff;
        UNLOCK();
        TResourceArbiter::Provide(this);
        piVar5 = DAT_01814340;
        lVar10 = lVar10 + 0x20;
      } while (lVar10 != 0xb2420);
      LOCK();
      DAT_01814340[0x2c908] = 0;
      UNLOCK();
      LOCK();
      piVar5[0x2c909] = 0;
      UNLOCK();
      piVar5[0x2c90b] = 0;
      piVar5[0x2c90d] = 0;
      uVar9 = (ulong)DAT_0181434c;
    }
  }
  LOCK();
  piVar5[uVar9 + 0x2c908] = 1;
  UNLOCK();
  SIdle();
  return piVar3;
}

