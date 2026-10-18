#!/usr/bin/env python3
"""Package short public-domain / CC0 audio clips from Wikimedia Commons for the offline Corpus demos.

Usage: python3 -I tools/demo_samples.py --ffmpeg PATH --downloads DIR [--out DIR]

For each clip: read the file's Commons metadata and refuse anything not CC0 or public domain,
download it into DIR (an empty, isolated folder), check the published SHA-1, then trim, fade,
loudness-normalize and encode it as Ogg Opus with ffmpeg. Writes samples.js (a script the
file:// page can load; fetch cannot read sibling files there) and samples-manifest.json with
source, author, licence and hashes. Contains no Ableton material.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/ableton-live-12.4.3/demos/corpus-traced'
API = 'https://commons.wikimedia.org/w/api.php'
UA = {'User-Agent': 'sound-analysis-demo/1.0 (offline learning demo; https://github.com/hoidn/sound)'}
ALLOWED = ('cc0', 'public domain')
# (Commons title, label, start s, duration s or None for the whole file, channels, seamless loop)
# Seamless loops keep their full length with no fades so they repeat without a dip.
CLIPS = [
    ('File:Bongo sound.wav', 'Bongos (cumbia loop)', 0, None, 1, True),
    ('File:Funk carioca 8 bar loop.ogg', 'Funk drum loop', 0, None, 2, True),
    ('File:Ceramic Djembe.wav', 'Djembe', 0.5, 10, 2, False),
    ('File:AcousticGuitarSample.ogg', 'Acoustic guitar', 0, 12, 2, False),
    ('File:C major, Middle C, I-IV-V-I-I-V-I chord progression.ogg', 'Piano chords', 0, None, 2, False),
    ('File:Albert Henry Munsell - A Color Notation (LibriVox) 00.mp3', 'Speech (LibriVox reading)', 28, 10, 1, False),
]


def metadata(title):
    q = urllib.parse.urlencode({'action': 'query', 'titles': title, 'prop': 'imageinfo', 'format': 'json',
                                'iiprop': 'url|sha1|extmetadata'})
    page = next(iter(json.load(urllib.request.urlopen(urllib.request.Request(f'{API}?{q}', headers=UA), timeout=30))['query']['pages'].values()))
    if 'imageinfo' not in page:
        raise ValueError(f'{title}: not found on Commons')
    info = page['imageinfo'][0]
    text = lambda k: re.sub('<[^>]+>', '', info['extmetadata'].get(k, {}).get('value', '')).strip()
    meta = {'title': title, 'url': info['url'], 'page': info['descriptionurl'], 'sha1': info['sha1'],
            'license': text('LicenseShortName'), 'license_url': text('LicenseUrl'), 'author': text('Artist')[:200]}
    if not any(a in meta['license'].lower() for a in ALLOWED):
        raise ValueError(f'{title}: licence {meta["license"]!r} is not CC0 or public domain')
    return meta


def fetch(url, tries=5):
    for attempt in range(tries):  # Wikimedia rate-limits bursts; honour Retry-After
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == tries - 1:
                raise
            time.sleep(int(e.headers.get('Retry-After') or 0) or 5 * (attempt + 1))


def download(meta, folder):
    path = folder / meta['title'].removeprefix('File:').replace('/', '_')
    if not path.exists():
        time.sleep(2)
        path.write_bytes(fetch(meta['url']))
    if hashlib.sha1(path.read_bytes()).hexdigest() != meta['sha1']:
        raise ValueError(f'{meta["title"]}: SHA-1 differs from Commons')
    return path


def encode(ffmpeg, src, start, duration, channels, loop):
    span = ['-ss', str(start)] + (['-t', str(duration)] if duration else [])
    fades = '' if loop else 'afade=t=in:d=0.01,areverse,afade=t=in:d=0.25,areverse,'  # fade-out without knowing the length
    cmd = [ffmpeg, '-hide_banner', '-loglevel', 'error', *span, '-i', str(src),
           '-af', f'{fades}loudnorm=I=-18:TP=-1.5', '-ac', str(channels), '-ar', '48000',
           '-c:a', 'libopus', '-b:a', '64k' if channels == 1 else '96k', '-f', 'ogg', 'pipe:1']
    return subprocess.run(cmd, check=True, capture_output=True).stdout


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--ffmpeg', default='ffmpeg')
    parser.add_argument('--downloads', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=OUT)
    args = parser.parse_args(argv)
    args.downloads.mkdir(parents=True, exist_ok=True)
    samples, manifest = [], []
    for title, label, start, duration, channels, loop in CLIPS:
        meta = metadata(title)
        src = download(meta, args.downloads)
        clip = encode(args.ffmpeg, src, start, duration, channels, loop)
        samples.append({'label': label, 'loop': loop, 'data': base64.b64encode(clip).decode()})
        manifest.append({**meta, 'label': label, 'excerpt_seconds': [start, start + duration if duration else None], 'channels': channels, 'seamless_loop': loop,
                         'source_sha256': hashlib.sha256(src.read_bytes()).hexdigest(),
                         'clip_sha256': hashlib.sha256(clip).hexdigest(), 'clip_bytes': len(clip)})
    credits = [{k: m[k] for k in ('label', 'title', 'page', 'author', 'license')} for m in manifest]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'samples.js').write_text('window.DEMO_SAMPLES=' + json.dumps(
        [{**s, **c} for s, c in zip(samples, credits)], ensure_ascii=True).replace('<', '\\u003c') + ';\n', encoding='utf-8')
    (args.out / 'samples-manifest.json').write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps([(m['label'], m['license'], m['clip_bytes']) for m in manifest], indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
