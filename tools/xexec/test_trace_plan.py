"""Owned instruction/control fixtures; no original process or image."""
import importlib.util
from pathlib import Path

def check():
    path = Path(__file__).with_name('trace_plan.py')
    assert path.exists(), 'missing reusable trace planner'
    spec = importlib.util.spec_from_file_location('trace_plan', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = [{'addr':16,'length':2,'asm':'cmp $1,%eax'},
            {'addr':18,'length':2,'asm':'je 0x18'},
            {'addr':20,'length':2,'asm':'call *%rax'},
            {'addr':22,'length':2,'asm':'jmp 0x1a'},
            {'addr':24,'length':2,'asm':'ret'},
            {'addr':26,'length':1,'asm':'ret'}]
    plan = module.plan(rows,16,27)
    assert plan['blocks']==[16,20,22,24,26]
    assert plan['calls']==[20] and plan['returns']==[24,26]
    assert plan['branches']==[18,22]
    rejected=[]
    for name,changed in [('gap',[dict(r) for r in rows]),('wrong-end',[dict(r) for r in rows]),('duplicate',[dict(r) for r in rows])]:
        if name=='gap':changed.pop(2)
        elif name=='wrong-end':changed[-1]['length']=2
        else:changed[1]['addr']=16
        try:module.plan(changed,16,27)
        except AssertionError:rejected.append(name)
    assert len(rejected)==3
    assert module.effective('call *0x28(%rax)',{'rax':100},lambda a: a+1000,0,2)==1140
    assert module.effective('call *0x10(%rip)',{},lambda a:a+1000,20,6)==1042
    assert module.effective('jmp *%r11',{'r11':123},lambda a:0,0,2)==123
    assert module.effective('call 0x123 <name>',{},lambda a:0,0,5)==291
    assert module.effective('call *(%rax,%rcx,8)',{'rax':1,'rcx':2},lambda a:0,0,3) is None
    return {'status':'PASS','owned_rejections':rejected,'model_original_calls':0}

if __name__=='__main__':
    print(check())
