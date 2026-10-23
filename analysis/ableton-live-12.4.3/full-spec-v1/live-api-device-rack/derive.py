"""Pure member-span extraction from immutable public-reference inventory data."""
import re


def member_span(entry, member, rows):
    position = next(i for i, row in enumerate(rows) if row['block'] == member['block'])
    heading = rows[position]
    assert heading['tag'] == 'h3' and heading['text'] == member['heading']
    assert heading['section'] == member['category'] and heading['anchor'] == member['anchor']
    end = next((i for i in range(position + 1, len(rows)) if rows[i]['tag'] in ('h1', 'h2', 'h3')), len(rows))
    span = rows[position:end]
    name, _, declared_type = heading['text'].partition(' ')
    access = [r['text'].removeprefix('Access: ').strip() for r in span if r['text'].startswith('Access: ')]
    assert len(access) <= 1
    tokens = re.findall(r'get|set|observe', access[0]) if access else None
    assert not access or ''.join(tokens) == access[0]
    return dict(inventory_member_id=member['id'], reference_entry=entry['id'], reference_name=entry['name'],
                source_id=entry['source_id'], category=member['category'], name=name,
                source_heading=heading['text'], declared_type=declared_type or None,
                declared_access=access[0] if access else None, access_roles=tokens,
                source_blocks=[r['block'] for r in span], source_text=[r['text'] for r in span],
                anchor=heading['anchor'], html_line=heading['html_line'], html_column=heading['html_column'])
