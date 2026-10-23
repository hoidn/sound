"""Apply the retained narrow documentation delta; source/catalog bytes stay fixed."""
from pathlib import Path
import json
P = Path(__file__).resolve().parent
ROOT = P.parents[3]
response = json.loads((P / 'response-author-r2.json').read_text())
for change in response['page_changes']:
    text = (P / change['archive_input']).read_text()
    for edit in change['replacements']:
        assert text.count(edit['before']) == edit['occurrences'], edit['before']
        text = text.replace(edit['before'], edit['after'])
    text += change['append']
    (ROOT / change['canonical']).write_text(text)
    snapshot = P / change['snapshot']
    if snapshot.exists():
        assert snapshot.read_text() == text, snapshot
    else:
        snapshot.write_text(text)
print('Applied narrow revision; no source, requirements or cases rewritten.')
