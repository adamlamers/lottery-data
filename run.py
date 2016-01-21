#!/usr/bin/env python3
from .lotteries import LotteryManager, LOTTERIES

if __name__ == "__main__":
    manager = LotteryManager()
    for lottery in LOTTERIES:
        manager.add_lottery(lottery())

    manager.run()

