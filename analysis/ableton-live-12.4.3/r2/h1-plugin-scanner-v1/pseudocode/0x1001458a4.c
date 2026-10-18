
void FUN_1001458a4(undefined8 *param_1,undefined8 *param_2,int *param_3)

{
  ulong uVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  long lVar5;
  size_t sVar6;
  undefined ***pppuVar7;
  ulong uVar8;
  ostream *this;
  undefined8 *puVar9;
  void *pvVar10;
  undefined ***pppuVar11;
  undefined **local_5a0;
  size_t sStack_598;
  undefined8 local_590;
  undefined **local_588 [2];
  undefined8 auStack_578 [2];
  ulong local_568;
  undefined8 local_560;
  ulong local_558;
  void *local_548;
  undefined8 uStack_540;
  long local_538;
  ulong uStack_530;
  uint local_528;
  undefined **local_520 [6];
  undefined8 local_4f0;
  undefined8 local_498;
  undefined4 local_490;
  undefined8 local_488;
  undefined **local_480;
  size_t sStack_478;
  undefined **local_470;
  char acStack_468 [1024];
  long local_68;
  
  pppuVar7 = &local_5a0;
  pppuVar11 = &local_5a0;
  local_68 = *(long *)PTR____stack_chk_guard_100b1c378;
  *param_3 = 0;
  uVar3 = std::system_category();
  *(undefined8 *)(param_3 + 2) = uVar3;
  uVar3 = *(undefined8 *)PTR__kCFAllocatorDefault_100b1c030;
  uVar8 = param_2[1];
  puVar9 = (undefined8 *)*param_2;
  if (-1 < (char)*(byte *)((long)param_2 + 0x17)) {
    uVar8 = (ulong)*(byte *)((long)param_2 + 0x17);
    puVar9 = param_2;
  }
  uVar4 = FUN_10066f240(param_2,param_3);
  lVar5 = _CFURLCreateFromFileSystemRepresentation(uVar3,puVar9,uVar8,uVar4);
  if (lVar5 == 0) {
    uVar3 = std::generic_category();
    uVar4 = 0x16;
  }
  else {
    _CFAutorelease();
    lVar5 = _CFBundleCreate(uVar3,lVar5);
    if (lVar5 != 0) {
      _CFAutorelease();
      lVar5 = _CFBundleCopyExecutableURL(lVar5);
      if (lVar5 != 0) {
        _CFAutorelease();
        iVar2 = _CFURLGetFileSystemRepresentation(lVar5,1,acStack_468,0x400);
        if (iVar2 != 0) {
          sVar6 = _strlen(acStack_468);
          if (0x7ffffffffffffff7 < sVar6) {
                    /* WARNING: Subroutine does not return */
            FUN_100134f2c(&local_5a0);
          }
          if (sVar6 < 0x17) {
            local_590 = (undefined **)CONCAT17((char)sVar6,(undefined7)local_590);
            if (sVar6 != 0) goto LAB_1001459e8;
          }
          else {
            uVar8 = 0x19;
            if ((sVar6 | 7) != 0x17) {
              uVar8 = (sVar6 | 7) + 1;
            }
            pppuVar7 = operator_new(uVar8);
            local_590 = (undefined **)(uVar8 | 0x8000000000000000);
            local_5a0 = (undefined **)pppuVar7;
            sStack_598 = sVar6;
LAB_1001459e8:
            _memcpy(pppuVar7,acStack_468,sVar6);
            pppuVar11 = pppuVar7;
          }
          *(undefined1 *)((long)pppuVar11 + sVar6) = 0;
          sStack_478 = sStack_598;
          local_480 = local_5a0;
          local_470 = local_590;
          local_488 = FUN_10066f93c(&local_480,param_3);
          if ((*param_3 == 0) && (uVar8 = FUN_10066ff1c(&local_480,param_3), *param_3 == 0)) {
            local_4f0 = 0;
            sStack_598 = 0;
            local_590 = &PTR_FUN_100b43858;
            local_520[0] = &PTR__istream_100b43998;
            local_5a0 = &PTR__istream_100b43970;
            std::ios_base::init(local_520);
            local_490 = 0xffffffff;
            local_498 = 0;
            local_520[0] = &PTR_FUN_100b43880;
            local_5a0 = &PTR_FUN_100b43830;
            local_590 = &PTR_FUN_100b43858;
            std::streambuf::streambuf((streambuf *)local_588);
            local_588[0] = &PTR_FUN_100b43a20;
            uStack_540 = 0;
            local_548 = (void *)0x0;
            uStack_530 = 0;
            local_538 = 0;
            local_528 = 0x18;
            *(uint *)((long)local_588 + (long)local_590[-3]) =
                 *(uint *)((long)local_588 + (long)local_590[-3]) & 0xffffffb5 | 8;
            uVar3 = std::ostream::operator<<((ostream *)&local_590,uVar8);
            this = (ostream *)FUN_10013e5bc(uVar3,":",1);
            *(uint *)(this + *(long *)(*(long *)this + -0x18) + 8) =
                 *(uint *)(this + *(long *)(*(long *)this + -0x18) + 8) & 0xffffffb5 | 8;
            lVar5 = std::chrono::system_clock::to_time_t((time_point *)&local_488);
            std::ostream::operator<<(this,lVar5);
            if ((local_528 >> 4 & 1) == 0) {
              if ((local_528 >> 3 & 1) != 0) {
                puVar9 = auStack_578;
                goto LAB_100145bdc;
              }
              uVar8 = 0;
              *(undefined1 *)((long)param_1 + 0x17) = 0;
            }
            else {
              if (uStack_530 < local_558) {
                uStack_530 = local_558;
              }
              puVar9 = &local_560;
              local_568 = uStack_530;
LAB_100145bdc:
              pvVar10 = (void *)*puVar9;
              uVar8 = local_568 - (long)pvVar10;
              if (0x7ffffffffffffff7 < uVar8) {
                    /* WARNING: Subroutine does not return */
                FUN_100134f2c(param_1);
              }
              if (uVar8 < 0x17) {
                *(char *)((long)param_1 + 0x17) = (char)uVar8;
                puVar9 = param_1;
                if (uVar8 == 0) goto LAB_100145c38;
              }
              else {
                uVar1 = 0x19;
                if ((uVar8 | 7) != 0x17) {
                  uVar1 = (uVar8 | 7) + 1;
                }
                puVar9 = operator_new(uVar1);
                param_1[1] = uVar8;
                param_1[2] = uVar1 | 0x8000000000000000;
                *param_1 = puVar9;
              }
              _memmove(puVar9,pvVar10,uVar8);
              param_1 = puVar9;
            }
LAB_100145c38:
            *(undefined1 *)((long)param_1 + uVar8) = 0;
            local_5a0 = &PTR_FUN_100b43830;
            local_520[0] = &PTR_FUN_100b43880;
            local_590 = &PTR_FUN_100b43858;
            local_588[0] = &PTR_FUN_100b43a20;
            if (local_538 < 0) {
              operator_delete(local_548);
            }
            std::streambuf::~streambuf((streambuf *)local_588);
            std::iostream::~iostream((iostream *)&local_5a0);
            std::ios::~ios((ios *)local_520);
            if ((long)local_470 < 0) {
              operator_delete(local_480);
            }
            goto LAB_100145a5c;
          }
          if ((long)local_470 < 0) {
            operator_delete(local_480);
          }
        }
      }
    }
    uVar3 = std::generic_category();
    uVar4 = 2;
  }
  *(undefined8 *)param_3 = uVar4;
  *(undefined8 *)(param_3 + 2) = uVar3;
  param_1[1] = 0;
  param_1[2] = 0;
  *param_1 = 0;
LAB_100145a5c:
  if (*(long *)PTR____stack_chk_guard_100b1c378 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

