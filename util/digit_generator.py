def hex_generator(length=0):
    values = ['0', '1', '2', '3', '4', '5', '6', '7', '8',
        '9', 'A', 'B', 'C', 'D', 'E', 'F']
    if length <= 0:
        yield ''
        return
    for d in values:
        for ds in hex_generator(length-1):
            yield d + ds
