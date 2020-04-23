import copy

__all__ = ['fix_repeats']


def fix_repeats(names):
    names = copy.deepcopy(names)
    count = {}
    for i, name in enumerate(names):
        try:
            count[name].append(i)
        except KeyError:
            count[name] = [i]

    for c, indices in count.items():
        if len(indices) > 1:
            for i, index in enumerate(indices):
                names[index] += f"_{i}"

    return names
