

def update_and_copy_list(items, value, index_to_set: int):
    if index_to_set >= len(items) or index_to_set < 0:
        raise IndexError(f'update_and_copy_list index ({index_to_set}) out of range')

    return [value if i == index_to_set else item for i, item in enumerate(items)]
