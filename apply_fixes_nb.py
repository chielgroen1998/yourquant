import json
from pathlib import Path
p=Path('StochRSI-BTC_USD copy.ipynb')
nb=json.loads(p.read_text())
# Insert helper into cell 2 (if not already present)
helper='''\n# ---- StochRSI helper: discrete crossover signals ----\ndef generate_stochrsi_signals(stoch_k, stoch_d):\n    entries = (stoch_k > stoch_d) & (stoch_k.shift(1) <= stoch_d.shift(1))\n    exits = (stoch_k < stoch_d) & (stoch_k.shift(1) >= stoch_d.shift(1))\n    entries = entries & ~exits\n    exits = exits & ~entries\n    return entries, exits\n# ---- helper end ----\n'''
# safety: check cell count
if len(nb['cells'])>2:
    src=''.join(nb['cells'][2].get('source',[]))
    if 'def generate_stochrsi_signals' not in src:
        # append helper before the last line or at end
        nb['cells'][2]['source']=nb['cells'][2].get('source',[])+[helper]
        print('Inserted helper into cell 2')
    else:
        print('Helper already present in cell 2')
# Replace long expressions with function call
replacements=[(
    "entries = (stoch_k > stoch_d) & (stoch_k.shift(1) <= stoch_d.shift(1))",
    "entries, exits = generate_stochrsi_signals(stoch_k, stoch_d)"
),(
    "exits = (stoch_k < stoch_d) & (stoch_k.shift(1) >= stoch_d.shift(1))",
    "# exits handled by generate_stochrsi_signals"
),(
    "val_entries = val_stoch_k > val_stoch_d",
    "val_entries, val_exits = generate_stochrsi_signals(val_stoch_k, val_stoch_d)"
),(
    "val_exits = val_stoch_k < val_stoch_d",
    "# val_exits handled by generate_stochrsi_signals"
)]
count=0
for cell in nb['cells']:
    if cell.get('cell_type')!='code':
        continue
    src=''.join(cell.get('source',[]))
    newsrc=src
    for a,b in replacements:
        if a in newsrc:
            newsrc=newsrc.replace(a,b)
    if newsrc!=src:
        cell['source']=newsrc.splitlines(True)
        count+=1
print(f'Modified {count} cells')
# Write back
p.write_text(json.dumps(nb, indent=1))
print('Notebook updated')
