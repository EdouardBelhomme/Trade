##
## EPITECH PROJECT, 2023
## B-CNA-410-BDX-4-1-trade-edouard.belhomme
## File description:
## trade
##

#!/usr/bin/python3
# -*- coding: iso-8859-1 -*

import sys

class Bot:
    def __init__(self):
        self.botState = BotState()

    def run(self):
        while True:
            reading = input()
            if len(reading) == 0:
                continue
            self.parse(reading)

    def parse(self, info: str):
        tmp = info.split(" ")
        if tmp[0] == "settings":
            self.botState.update_settings(tmp[1], tmp[2])
        if tmp[0] == "update":
            if tmp[1] == "game":
                self.botState.update_game(tmp[2], tmp[3])
        if tmp[0] == "action":
            dollars = self.botState.stacks["USDT"]
            chart = self.botState.charts["USDT_BTC"]
            current_closing_price = chart.closes[-1]
            affordable = dollars / current_closing_price
            print(f'My stacks are {dollars}. The current closing price is {current_closing_price}. So I can afford {affordable}', file=sys.stderr)
            if dollars < 100 or not chart.can_compute_sma(5):
                print("no_moves", flush=True)
            else:
                average = chart.simple_moving_average(5)
                btc = self.botState.stacks["BTC"]
                #conditions d'achat
                if current_closing_price <= average * 0.97:
                    print(f'buy USDT_BTC {affordable}', flush=True)
                    purchase_price = self.botState.update_buy_price(current_closing_price)
                #conditions de vente stop loss
                elif self.botState.buy_price != -1.0 and purchase_price > current_closing_price * 0.9:
                    print(f'sell USDT_BTC {btc}', flush=True)
                    self.botState.update_buy_price(-1.0)
                #conditions de vente stop gain
                elif self.botState.buy_price != -1.0 and purchase_price < current_closing_price * 1.2:
                    print(f'sell USDT_BTC {btc}', flush=True)
                    self.botState.update_buy_price(-1.0)
                else:
                    print("no_moves", flush=True)


class Candle:
    def __init__(self, format, intel):
        tmp = intel.split(",")
        for (i, key) in enumerate(format):
            value = tmp[i]
            if key == "pair":
                self.pair = value
            if key == "date":
                self.date = int(value)
            if key == "high":
                self.high = float(value)
            if key == "low":
                self.low = float(value)
            if key == "open":
                self.open = float(value)
            if key == "close":
                self.close = float(value)
            if key == "volume":
                self.volume = float(value)

    def __repr__(self):
        return str(self.pair) + str(self.date) + str(self.close) + str(self.volume)


class Chart:
    def __init__(self):
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.indicators = {}

    def add_candle(self, candle: Candle):
        self.dates.append(candle.date)
        self.opens.append(candle.open)
        self.highs.append(candle.high)
        self.lows.append(candle.low)
        self.closes.append(candle.close)
        self.volumes.append(candle.volume)

    def simple_moving_average(self, periods):
        return sum(self.closes[-periods:]) / periods

    def can_compute_sma(self, periods):
        return len(self.closes) >= periods


class BotState:
    def __init__(self):
        self.timeBank = 0
        self.maxTimeBank = 0
        self.timePerMove = 1
        self.candleInterval = 1
        self.candleFormat = []
        self.candlesTotal = 0
        self.candlesGiven = 0
        self.initialStack = 0
        self.transactionFee = 0.1
        self.date = 0
        self.stacks = dict()
        self.charts = dict()
        self.buy_price = -1.0

    def update_chart(self, pair: str, new_candle_str: str):
        if not (pair in self.charts):
            self.charts[pair] = Chart()
        new_candle_obj = Candle(self.candleFormat, new_candle_str)
        self.charts[pair].add_candle(new_candle_obj)

    def update_stack(self, key: str, value: float):
        self.stacks[key] = value

    def update_settings(self, key: str, value: str):
        if key == "timebank":
            self.maxTimeBank = int(value)
            self.timeBank = int(value)
        if key == "time_per_move":
            self.timePerMove = int(value)
        if key == "candle_interval":
            self.candleInterval = int(value)
        if key == "candle_format":
            self.candleFormat = value.split(",")
        if key == "candles_total":
            self.candlesTotal = int(value)
        if key == "candles_given":
            self.candlesGiven = int(value)
        if key == "initial_stack":
            self.initialStack = int(value)
        if key == "transaction_fee_percent":
            self.transactionFee = float(value)

    def update_game(self, key: str, value: str):
        if key == "next_candles":
            new_candles = value.split(";")
            self.date = int(new_candles[0].split(",")[1])
            for candle_str in new_candles:
                candle_infos = candle_str.strip().split(",")
                self.update_chart(candle_infos[0], candle_str)
        if key == "stacks":
            new_stacks = value.split(",")
            for stack_str in new_stacks:
                stack_infos = stack_str.strip().split(":")
                self.update_stack(stack_infos[0], float(stack_infos[1]))

    def update_buy_price(self, price: float):
        self.buy_price = price

if __name__ == "__main__":
    mybot = Bot()
    mybot.run()
