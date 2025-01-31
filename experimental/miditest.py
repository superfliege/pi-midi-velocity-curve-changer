import math

def adjust_velocity(velocity, max_value=70, exponent=0.60):
    if velocity == 0:
        return 0
    result = 127 * math.pow((velocity / max_value), exponent)
    if result > 127:
        result = 127
    elif result < 1 or math.isnan(result):
        result = 1
    return int(result)

# Test values
test_values = range(0,127)

# Calculate and print results
results = {v: adjust_velocity(v) for v in test_values}
print(results)
