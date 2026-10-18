"""Read the document-loader vtable slots of the parameter and device classes (analyst tool; output is data).

usage: python3 -I loader_slots.py <out-dir> <Live.arm64>

N1 (transport-state-native) traced the generic member loader 0x101487310 at vtable +0x140 (stores each
present member's base-type value without a range check) and the post-load hook at +0xd0. This lists both
slots for the Timeable parameter classes and the device and sub-object classes of this packet, found from
their typeinfo names (extract_nested.Image.vtable_slot). Writes <out>/loader_slots.txt.
"""
import importlib.util, os, sys
sys.dont_write_bytecode = True  # do not leave __pycache__ in other packets' directories

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('xn', os.path.join(HERE, 'extract_nested.py'))
xn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(xn)
CLASSES = ['ATimeableSongTempo', 'ALoopStart', 'ATimeableFloat', 'ATimeableEnum', 'ATimeableBool',
           'AUltraAnalog', 'AUltraAnalogSignalChain1', 'AUltraAnalogSignalChain2', 'AUltraAnalogEnvelope',
           'AStringStudio', 'ACollision', 'ACollisionMallet', 'ACollisionNoise', 'ACollisionResonator',
           'ACollisionLfo', 'ACollisionModTarget', 'AAmp', 'ACabinet', 'ALoungeLizard', 'ACorpus']


def main(out, live):
    img = xn.Image(live)
    lines = ['class\t+0x140 loader\t+0xd0 post-load']
    for c in CLASSES:
        try:
            lines.append(f'{c}\t{img.vtable_slot(c, 0x140):#x}\t{img.vtable_slot(c, 0xd0):#x}')
        except AssertionError:
            lines.append(f'{c}\ttypeinfo name not found once\t')
    open(os.path.join(out, 'loader_slots.txt'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main(*sys.argv[1:3])
