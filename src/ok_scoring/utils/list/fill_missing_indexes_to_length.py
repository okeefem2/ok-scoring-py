def fill_missing_indexes_to_length(items, length, filler):
    current_length = len(items)
    if length <= current_length:
        return items
    # TIL that array multiplication can do some interesting stuff
    # Each item in the array shares the same memory address, so changing one changes all the others
    return items + [filler() for _i in range(length - current_length)]
