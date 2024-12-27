m = True

print(f"Initial m: {m}")  # Debugging point to show initial value of m

if 50 < 10:
    print("First condition (5 < 10) is True.")
    if 4 < 5:
        print("Second condition (4 < 5) is True, modifying m.")
        m = False  # This changes the value of m
        print(f"Modified m: {m}")  # Debugging point to show modified value of m
elif 60 > 10:
    print("First condition (5 < 10) is False, but second (60 > 10) is True.")
    if 5 > 3:
        print("Third condition (5 > 3) is True.")
        print(m)  # At this point, m is still False due to the previous modification
