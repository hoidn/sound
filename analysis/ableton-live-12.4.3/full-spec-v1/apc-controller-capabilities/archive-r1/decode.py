"""Bounded static CPython3.11 data recognizer; no original imports or calls.

CALL instructions become opaque data nodes. Imported names remain symbols.
This is not a Python evaluator, host shim or controller implementation.
"""
import dis
import importlib.util
import io
import marshal
import re
import sys
import types

MAGIC = bytes.fromhex('a70d0d0a')
CALL_NAMES = {'controller_id', 'inport', 'outport'}


def environment():
    assert sys.version_info[:2] == (3, 11), 'Use existing CPython3.11; never decode with mismatched dis tables'
    assert importlib.util.MAGIC_NUMBER == MAGIC


def read_code(data):
    environment()
    assert len(data) >= 16 and data[:4] == MAGIC, 'Invalid/truncated/mismatched pyc header'
    flags = int.from_bytes(data[4:8], 'little')
    assert flags in (0, 1, 3), 'Invalid PEP552 flags'
    payload = io.BytesIO(data[16:])
    code = marshal.load(payload)
    assert payload.tell() == len(data) - 16, 'Unexpected trailing marshal bytes'
    assert isinstance(code, types.CodeType) and code.co_name == '<module>', 'Not module code data'
    return code


def normalized_argument(instruction, code):
    if instruction.opname == 'KW_NAMES':
        return repr(code.co_consts[instruction.arg])
    if isinstance(instruction.argval, types.CodeType):
        return '<code ' + instruction.argval.co_qualname + '>'
    return re.sub(r' at 0x[0-9a-fA-F]+', '', instruction.argrepr)


def instructions(code):
    return [dict(offset=i.offset, op=i.opname, arg=i.arg, text=normalized_argument(i, code), line=i.starts_line)
            for i in dis.get_instructions(code, show_caches=False, adaptive=False)]


def capability_imports(module, needed):
    """Inspect module import declarations, without importing any target module."""
    found = {}
    current = None
    pending = None
    for i in dis.get_instructions(module, show_caches=False, adaptive=False):
        if i.opname == 'IMPORT_NAME':
            current = i.argval
        elif i.opname == 'IMPORT_FROM':
            pending = dict(module=current, imported_name=i.argval, import_offset=i.offset)
        elif i.opname == 'STORE_NAME':
            if pending and i.argval in needed:
                assert 'capabilities' in pending['module'].lower(), 'Unexpected capability-symbol provenance'
                found[i.argval] = dict(pending, binding_offset=i.offset)
            pending = None
    assert set(found) == set(needed), 'Unresolved/rebound capability global'
    return found


def declaration(function, bindings):
    """Recognize only straight-line literal/list/map/opaque-call forms as data."""
    assert isinstance(function, types.CodeType) and function.co_argcount == function.co_kwonlyargcount == function.co_posonlyargcount == 0
    assert not function.co_freevars and not function.co_cellvars and not function.co_exceptiontable
    assert not (function.co_flags & (0x04 | 0x08 | 0x20 | 0x80 | 0x200)), 'No varargs/generator/coroutine forms'
    rows = list(dis.get_instructions(function, show_caches=False, adaptive=False))
    assert len(rows) < 150
    stack, calls, keywords = [], [], None
    result = None
    for i in rows:
        if i.opname == 'RESUME':
            continue
        if i.opname == 'LOAD_GLOBAL':
            assert i.argval in bindings
            stack.append(dict(kind='symbol', name=i.argval, load_offset=i.offset))
        elif i.opname == 'LOAD_CONST':
            assert type(i.argval) in (int, str, bool, type(None)), 'Nonliteral get_capabilities constant'
            stack.append(dict(kind='literal', value=i.argval, const_index=i.arg, load_offset=i.offset))
        elif i.opname == 'BUILD_LIST':
            assert i.arg > 0 and len(stack) >= i.arg
            items = stack[-i.arg:]
            del stack[-i.arg:]
            stack.append(dict(kind='list-declaration', items=items, build_offset=i.offset))
        elif i.opname == 'KW_NAMES':
            assert keywords is None
            keywords = function.co_consts[i.arg]
            assert isinstance(keywords, tuple) and all(type(s) is str for s in keywords)
            assert len(set(keywords)) == len(keywords)
        elif i.opname == 'PRECALL':
            assert keywords is not None and len(keywords) == i.arg
        elif i.opname == 'CALL':
            assert keywords is not None and len(keywords) == i.arg and len(stack) >= i.arg + 1
            values = stack[-i.arg:]
            del stack[-i.arg:]
            target = stack.pop()
            assert target['kind'] == 'symbol' and target['name'] in CALL_NAMES, 'Unknown call shape; do not interpret'
            node = dict(kind='opaque-call', callee=target['name'], callee_offset=target['load_offset'],
                        call_offset=i.offset, keywords={k: v for k, v in zip(keywords, values)})
            calls.append(node)
            stack.append(node)
            keywords = None
        elif i.opname == 'BUILD_MAP':
            assert i.arg > 0 and len(stack) == 2 * i.arg
            entries = [dict(key=stack[j], value=stack[j + 1]) for j in range(0, len(stack), 2)]
            assert all(e['key']['kind'] == 'symbol' for e in entries)
            stack = [dict(kind='map-declaration', entries=entries, build_offset=i.offset)]
        elif i.opname == 'RETURN_VALUE':
            assert result is None and len(stack) == 1 and keywords is None
            result = dict(node=stack.pop(), return_offset=i.offset)
        else:
            raise AssertionError('Unsupported opcode/branch; retain unknown: ' + i.opname)
    assert result and not stack and result['node']['kind'] == 'map-declaration'
    assert len([c for c in calls if c['callee'] == 'controller_id']) == 1
    return dict(function=function.co_qualname, first_line=function.co_firstlineno,
                instructions=instructions(function), calls=calls, **result)


def decode(data):
    module = read_code(data)
    functions = [c for c in module.co_consts if isinstance(c, types.CodeType) and c.co_name == 'get_capabilities']
    assert len(functions) == 1
    function = functions[0]
    bindings = capability_imports(module, function.co_names)
    declared = declaration(function, bindings)
    identity = next(c for c in declared['calls'] if c['callee'] == 'controller_id')
    assert set(identity['keywords']) == {'vendor_id', 'product_ids', 'model_name'}
    entries = {e['key']['name']: e['value'] for e in declared['node']['entries']}
    assert entries['CONTROLLER_ID_KEY'] == identity
    ports = entries['PORTS_KEY']
    assert ports['kind'] == 'list-declaration'
    assert all(n['kind'] == 'opaque-call' and n['callee'] in ('inport', 'outport') and set(n['keywords']) == {'props'} for n in ports['items'])
    assert all(n['keywords']['props']['kind'] == 'list-declaration' and all(s['kind'] == 'symbol' for s in n['keywords']['props']['items']) for n in ports['items'])
    extra = set(entries) - {'CONTROLLER_ID_KEY', 'PORTS_KEY'}
    assert extra in (set(), {'AUTO_LOAD_KEY'})
    if extra:
        assert entries['AUTO_LOAD_KEY']['kind'] == 'literal' and entries['AUTO_LOAD_KEY']['value'] is True
    return dict(module=dict(name=module.co_name, filename=module.co_filename, first_line=module.co_firstlineno,
                            imports=bindings, instructions=instructions(module),
                            other_code_names=[c.co_qualname for c in module.co_consts if isinstance(c, types.CodeType) and c is not function],
                            other_code_semantics='Not analyzed; creator/classes/framework unresolved'),
                get_capabilities=declared,
                unresolved='Imported constants remain symbols; helper CALL nodes are opaque, never invoked or reduced to helper results. Module load/creator/host matching/ports/autoload/runtime effects unknown.')


def literal_data(node):
    if node['kind'] == 'literal':
        return node['value']
    if node['kind'] == 'list-declaration':
        return [literal_data(n) for n in node['items']]
    raise AssertionError('Only source literal/list data may be projected; no symbol/call results')


def ledger_row(identity, name, source_hash, decoded):
    declared = decoded['get_capabilities']
    call = next(c for c in declared['calls'] if c['callee'] == 'controller_id')
    pairs = {e['key']['name']: e['value'] for e in declared['node']['entries']}
    ports = []
    for i, node in enumerate(pairs['PORTS_KEY']['items'], 1):
        props = node['keywords']['props']
        ports.append(dict(ordinal=i, declaration=node['callee'], property_symbols=[s['name'] for s in props['items']],
                          call_offset=node['call_offset'], props_build_offset=props['build_offset'],
                          property_load_offsets=[s['load_offset'] for s in props['items']]))
    return dict(id=identity, name=name, source_sha256=source_hash,
                identity_literal_inputs={k: literal_data(v) for k, v in call['keywords'].items()},
                identity_call_offset=call['call_offset'], ports=ports,
                autoload_literal=True if 'AUTO_LOAD_KEY' in pairs else None,
                autoload_source_state='literal True associated with imported symbol' if 'AUTO_LOAD_KEY' in pairs else 'symbol/pair not declared; no False inferred',
                map_entry_symbol_order=list(pairs), map_build_offset=declared['node']['build_offset'],
                return_offset=declared['return_offset'], runtime_return=None, complete=False)


def selfchecks(data):
    """Reject bad headers/payloads and control flow without running code objects."""
    environment()
    for bad in (b'', bytes(16), b'xxxx' + data[4:], data[:4] + b'\xff' * 4 + data[8:], data + b'x', data[:-1], data[:16] + marshal.dumps(7)):
        try:
            read_code(bad)
        except (AssertionError, EOFError, ValueError, TypeError):
            pass
        else:
            raise AssertionError('Invalid source accepted')
    own = compile('def analyst_fixture():\n if flag:\n  return 1\n return 2\n', '<analyst static rejection fixture>', 'exec')
    function = next(c for c in own.co_consts if isinstance(c, types.CodeType))
    try:
        declaration(function, {'flag': {}})
    except AssertionError as error:
        assert 'Unsupported opcode/branch' in str(error)
    else:
        raise AssertionError('Conditional bytecode unexpectedly recognized')
    own_call = compile('def analyst_fixture():\n return {KEY: unsafe(x=1)}\n', '<analyst static rejection fixture>', 'exec')
    call_function = next(c for c in own_call.co_consts if isinstance(c, types.CodeType))
    try:
        declaration(call_function, {'KEY': {}, 'unsafe': {}})
    except AssertionError as error:
        assert 'Unknown call shape' in str(error)
    else:
        raise AssertionError('Unknown helper unexpectedly recognized')
    return dict(invalid_header_payload_variants_rejected=7, unsupported_branch_rejected=True,
                unknown_helper_call_rejected=True,
                compiled_analyst_fixture_executed=False, original_functions_called=False)
