def steps(percentage, step_count, change_at_end=True):
    step_size = (1/step_count)

    if percentage == 0:
        return 0

    if percentage == 1:
        return 1

    if change_at_end:
        difference = abs((percentage-step_size) % (1/step_count))
        return percentage - difference

    difference = abs((step_size-percentage) % (1/step_count))
    return percentage + difference
