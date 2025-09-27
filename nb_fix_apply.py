import re, json
from pathlib import Path
p=Path('StochRSI-BTC_USD copy.ipynb')
src=p.read_text()
nb=json.loads(src)
changed=0
# helper patterns
patterns=[
    # val_stoch_k comparisons
    (re.compile(r'^(?P<indent>\s*)val_entries\s*=\s*val_stoch_k\s*>\s*val_stoch_d.*$', re.M),
     lambda m: f"{m.group('indent')}val_entries, val_exits = generate_stochrsi_signals(val_stoch_k, val_stoch_d)"),
    (re.compile(r'^(?P<indent>\s*)val_exits\s*=\s*val_stoch_k\s*<\s*val_stoch_d.*$', re.M),
     lambda m: f"{m.group('indent')}# val_exits handled by generate_stochrsi_signals"),
    # non-val stoch_k comparisons
    (re.compile(r'^(?P<indent>\s*)entries\s*=\s*stoch_k\s*>\s*stoch_d.*$', re.M),
     lambda m: f"{m.group('indent')}entries, exits = generate_stochrsi_signals(stoch_k, stoch_d)"),
    (re.compile(r'^(?P<indent>\s*)exits\s*=\s*stoch_k\s*<\s*stoch_d.*$', re.M),
     lambda m: f"{m.group('indent')}# exits handled by generate_stochrsi_signals"),
    # val_ variants using > < with comments
    (re.compile(r'^(?P<indent>\s*)val_entries\s*=\s*val_stoch_k\s*>\s*val_stoch_d\s*#.*$', re.M),
     lambda m: f"{m.group('indent')}val_entries, val_exits = generate_stochrsi_signals(val_stoch_k, val_stoch_d)"),
]
new_src=src
for patt, repl in patterns:
    new_src, n = patt.subn(repl, new_src)
    if n>0:
        changed+=n
if changed>0:
    p.write_text(new_src)
    print(f'Applied {changed} replacements')
else:
    print('No replacements needed')
