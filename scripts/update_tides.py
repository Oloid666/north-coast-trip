"""Refresh official CWA 30-day town tide forecasts; standard library, no key."""
import json
import re
import urllib.request
from datetime import datetime, date
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

STATIONS = {'shimen': ('石門', 'T500022'), 'tamsui': ('淡水', 'T500010')}
BASE = 'https://www.cwa.gov.tw/V8/C/M/Fishery/tide_30day_MOD/'

class TideTable(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell = [], None, None
    def handle_starttag(self, tag, attrs):
        if tag == 'tr': self.row = []
        if tag == 'td' and self.row is not None:
            self.cell = {'attrs': dict(attrs), 'text': ''}
    def handle_data(self, text):
        if self.cell is not None: self.cell['text'] += text
    def handle_endtag(self, tag):
        if tag == 'td' and self.cell is not None:
            self.row.append(self.cell)
            self.cell = None
        if tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None

def parse_tides(html, today):
    table = TideTable()
    table.feed(html)
    days, current = {}, None
    for row in table.rows:
        for cell in row:
            if cell['attrs'].get('headers') == 'date':
                md = re.search(r'(\d{1,2})/(\d{1,2})', cell['text'])
                if not md: raise ValueError('Missing CWA forecast date')
                month, day = map(int, md.groups())
                candidates = [date(y, month, day) for y in [today.year-1, today.year, today.year+1]]
                current = min(candidates, key=lambda d: abs((d-today).days)).isoformat()
                days.setdefault(current, [])
        if current is None: continue
        fields = {c['attrs'].get('headers', '').split()[-1]: c['text'].strip()
                  for c in row if c['attrs'].get('headers')}
        if 'time' not in fields: continue
        tide = fields.get('tide', '')
        if tide not in ('滿潮', '乾潮') or not re.fullmatch(r'\d{2}:\d{2}', fields['time']):
            raise ValueError('Unexpected CWA tide format')
        height = fields.get('Above_Local_MSL', '')
        days[current].append({'type': tide, 'time': fields['time'],
                              'heightCm': int(height) if re.fullmatch(r'-?\d+', height) else None})
    if len(days) < 20: raise ValueError('Incomplete CWA tide table; keep previous data')
    if today.isoformat() not in days: raise ValueError('CWA table does not include today')
    for key, events in days.items():
        if not 2 <= len(events) <= 4: raise ValueError(f'Incomplete tide events: {key}')
        events.sort(key=lambda item: item['time'])
    return days

def main():
    now = datetime.now(ZoneInfo('Asia/Taipei'))
    result = {'source': '交通部中央氣象署', 'fetchedAt': now.isoformat(),
              'timeZone': 'Asia/Taipei', 'heightDatum': '相對當地平均海平面，公分', 'stations': {}}
    for key, (name, code) in STATIONS.items():
        url = BASE + code + '.html'
        req = urllib.request.Request(url, headers={'User-Agent': 'NorthCoastTrip/1.0'})
        with urllib.request.urlopen(req, timeout=30) as response: html = response.read().decode('utf-8')
        result['stations'][key] = {'name': name, 'kind': '鄉鎮潮汐預報（非即時測站）',
                                   'sourceUrl': url, 'days': parse_tides(html, now.date())}
    target = Path(__file__).resolve().parents[1] / 'data' / 'tides.json'
    target.parent.mkdir(exist_ok=True)
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(target)
    print('Updated official CWA forecasts:', ', '.join(s['name'] for s in result['stations'].values()))

if __name__ == '__main__': main()
