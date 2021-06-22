

def fibonacci_timing_pattern(Data, count, step, step_two, step_three, close, buy, sell):
    # Bullish Fibonacci Timing Pattern
    counter = -1
    for i in range(len(Data)):
        if Data[i, close] < Data[i - step, close] and \
                Data[i, close] < Data[i - step_two, close] and \
                Data[i, close] < Data[i - step_three, close]:

            Data[i, buy] = counter
            counter += -1

            if counter == -count - 1:
                counter = 0
            else:
                continue

        elif Data[i, close] >= Data[i - step, close]:
            counter = -1
            Data[i, buy] = 0

            # Bearish Fibonacci Timing Pattern
    counter = 1

    for i in range(len(Data)):
        if Data[i, close] > Data[i - step, close] and \
                Data[i, close] > Data[i - step_two, close] and \
                Data[i, close] > Data[i - step_three, close]:

            Data[i, sell] = counter
            counter += 1
            if counter == count + 1:
                counter = 0
            else:
                continue

        elif Data[i, close] <= Data[i - step, close]:
            counter = 1
            Data[i, sell] = 0

    return Data