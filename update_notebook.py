import nbformat
from nbformat.v4 import new_code_cell

notebook_path = "/Users/chielg/Documents/GitHub/yourquant/discrete algos (optimized per)/draft_1_ta_gridsearch.ipynb"

new_cell_6_content = """# Parameter grid for EMA Triple Crossover, MACD, and AROON
import itertools as it

# EMA Triple Crossover parameters (Fast < Medium < Slow)
EMA_FAST_RANGE = list(range(5, 21, 2))       # 5, 7, 9, ..., 19
EMA_MEDIUM_RANGE = list(range(15, 51, 5))    # 15, 20, 25, ..., 50
EMA_SLOW_RANGE = list(range(50, 201, 10))    # 50, 60, 70, ..., 200

# MACD parameters
MACD_FAST_RANGE = list(range(8, 21, 2))      # 8, 10, 12, ..., 20
MACD_SLOW_RANGE = list(range(21, 41, 3))     # 21, 24, 27, ..., 39
MACD_SIGNAL_RANGE = list(range(6, 16, 2))    # 6, 8, 10, 12, 14

# AROON parameters
AROON_PERIOD_RANGE = list(range(10, 31, 5))  # 10, 15, 20, 25, 30

ALL_PARAM_COMBINATIONS = [
    (ema_fast, ema_medium, ema_slow, macd_fast, macd_slow, macd_signal, aroon_period)
    for ema_fast, ema_medium, ema_slow, macd_fast, macd_slow, macd_signal, aroon_period in it.product(
        EMA_FAST_RANGE, EMA_MEDIUM_RANGE, EMA_SLOW_RANGE, 
        MACD_FAST_RANGE, MACD_SLOW_RANGE, MACD_SIGNAL_RANGE, 
        AROON_PERIOD_RANGE
    )
    if ema_fast < ema_medium < ema_slow and macd_fast < macd_slow
]

print(f"Total param combos: {len(ALL_PARAM_COMBINATIONS):,}")
print("Example first 10:")
print(ALL_PARAM_COMBINATIONS[:10])
print()
print("Parameter ranges:")
print(f"EMA Fast: {min(EMA_FAST_RANGE)} to {max(EMA_FAST_RANGE)}")
print(f"EMA Medium: {min(EMA_MEDIUM_RANGE)} to {max(EMA_MEDIUM_RANGE)}")
print(f"EMA Slow: {min(EMA_SLOW_RANGE)} to {max(EMA_SLOW_RANGE)}")
print(f"MACD Fast: {min(MACD_FAST_RANGE)} to {max(MACD_FAST_RANGE)}")
print(f"MACD Slow: {min(MACD_SLOW_RANGE)} to {max(MACD_SLOW_RANGE)}")
print(f"MACD Signal: {min(MACD_SIGNAL_RANGE)} to {max(MACD_SIGNAL_RANGE)}")
print(f"AROON Period: {min(AROON_PERIOD_RANGE)} to {max(AROON_PERIOD_RANGE)}")"""

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    # Find and update Cell 6 (index 5)
    # Assuming Cell 6 starts with '# Expanded parameter grid (massive)' or similar
    # I will be replacing the entire cell content.
    if len(notebook.cells) > 6 and \
       notebook.cells[6].cell_type == 'code' and \
       ("RSI_LEN_RANGE" in notebook.cells[6].source or "# Parameter grid for EMA Triple Crossover" in notebook.cells[6].source):
        notebook.cells[6].source = new_cell_6_content
        print("Successfully updated Cell 6 (Parameter Grid).")
    else:
        print("Warning: Cell 6 not found or not in expected format. Appending as new cell.")
        notebook.cells.insert(6, new_code_cell(new_cell_6_content))

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(notebook, f)
    print(f"Notebook '{notebook_path}' updated successfully.")

except FileNotFoundError:
    print(f"Error: Notebook file not found at '{notebook_path}'")
except Exception as e:
    print(f"An error occurred: {e}")
