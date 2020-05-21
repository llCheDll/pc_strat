class PriceChennel:
    def __init__(self, high, low, period):
        self.high = high
        self.low = low
        self.period = period

    def upper_channel(self):
        channel = []
        high = 0
        counter = 0

        for value in self.high:
            if value > high:
                high = value
                counter = 0
            elif counter >= self.period:
                index = len(channel) - self.period + 1
                high = max(self.high[index:len(channel)+1])
            channel.append(high)
            counter += 1

        return channel

    def lower_channel(self):
        channel = []
        low = self.low[0]
        counter = 0

        for value in self.low:
            if value < low:
                low = value
                counter = 0
            elif counter >= self.period:
                index = len(channel) - self.period + 1
                low = min(self.low[index:len(channel)])
            channel.append(low)
            counter += 1

        return channel
