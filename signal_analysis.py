#!/usr/bin/env python3
"""
Signal Analysis Script - Diagnose continuous signal issues
"""

import yfinance as yf
import vectorbt as vbt
import pandas as pd
import numpy as np

def analyze_signals():
    print("🔍 SIGNAL ANALYSIS: Diagnosing Continuous Signal Issues")
    print("=" * 60)
    
    # Download data
    ticker = 'QQQ'
    start_date = '2018-01-01'
    
    print(f"Downloading {ticker} data from {start_date}...")
    stock_data = yf.download(ticker, start=start_date, interval='1d')
    
    if stock_data.empty:
        print("❌ Failed to download data")
        return
    
    # Extract close prices
    if isinstance(stock_data.columns, pd.MultiIndex):
        close = stock_data[("Close", ticker)]
    else:
        close = stock_data["Close"]
    
    # Split data (70% train, 30% val)
    train_size = int(len(stock_data) * 0.7)
    train_close = close.iloc[:train_size]
    
    print(f"Training data: {len(train_close)} days")
    print(f"Date range: {train_close.index[0].date()} to {train_close.index[-1].date()}")
    
    # Test different MA combinations
    test_combinations = [(5, 30), (10, 50), (20, 60)]
    
    for fast_period, slow_period in test_combinations:
        print(f"\n📊 Testing SMA({fast_period}, {slow_period}):")
        print("-" * 40)
        
        # Calculate indicators
        fast_ma = vbt.MA.run(train_close, fast_period, ewm=False)
        slow_ma = vbt.MA.run(train_close, slow_period, ewm=False)
        
        # Generate signals
        entries = fast_ma.ma_crossed_above(slow_ma.ma)
        exits = fast_ma.ma_crossed_below(slow_ma.ma)
        
        # Count signals
        entry_count = entries.sum()
        exit_count = exits.sum()
        
        print(f"  Entry signals: {entry_count}")
        print(f"  Exit signals: {exit_count}")
        
        # Check for consecutive signals
        consecutive_entries = 0
        max_consecutive_entries = 0
        consecutive_exits = 0
        max_consecutive_exits = 0
        
        for i in range(1, len(entries)):
            if entries.iloc[i] and entries.iloc[i-1]:
                consecutive_entries += 1
                max_consecutive_entries = max(max_consecutive_entries, consecutive_entries)
            else:
                consecutive_entries = 0
            
            if exits.iloc[i] and exits.iloc[i-1]:
                consecutive_exits += 1
                max_consecutive_exits = max(max_consecutive_exits, consecutive_exits)
            else:
                consecutive_exits = 0
        
        print(f"  Max consecutive entries: {max_consecutive_entries}")
        print(f"  Max consecutive exits: {max_consecutive_exits}")
        
        if max_consecutive_entries > 1:
            print("  ⚠️  WARNING: Found consecutive entry signals!")
        if max_consecutive_exits > 1:
            print("  ⚠️  WARNING: Found consecutive exit signals!")
        
        # Show signal pattern for first 30 days
        print(f"  First 30 days signal pattern:")
        for i in range(min(30, len(entries))):
            if entries.iloc[i] or exits.iloc[i]:
                date = train_close.index[i].strftime('%Y-%m-%d')
                price = train_close.iloc[i]
                entry = "BUY" if entries.iloc[i] else "   "
                exit = "SELL" if exits.iloc[i] else "    "
                print(f"    {date}: ${price:.2f} | {entry} | {exit}")
    
    print("\n✅ Signal analysis complete!")
    print("\n💡 RECOMMENDATIONS:")
    print("1. If you see consecutive signals, the issue is in signal generation logic")
    print("2. Proper crossover signals should be discrete (single day events)")
    print("3. Consider using shift() logic to ensure event-based signals")

if __name__ == "__main__":
    analyze_signals()
