import random


def normalisation(particles):
    sum = 0.0
    for particle in particles:
        sum += particle[3]
    new_list = []
    if (sum != 0):
        for particle in particles:
            part = list(particle)
            new_weight = part[3] / sum
            part[3] = new_weight
            part = tuple(part)
            new_list.append(part)
        return tuple(new_list)
    else:
        for particle in particles:
            part = list(particle)
            new_weight = 0.01
            part[3] = new_weight
            part = tuple(part)
            new_list.append(part)
        return tuple(new_list)


def resampling(particles):
    weights = 0
    new_list = []
    for particle in particles:
        part = list(particle)
        holder = part[3]
        part[3] += weights
        new_list.append(tuple(part))
        weights += holder
    new_list = tuple(new_list)
    next_list = []
    x = len(new_list)
    for index in range(x):
        r = random.uniform(0, 1)
        for item in new_list:
            if r <= item[3]:
                tmp = list(item)
                tmp[3] = 1.0 / x
                next_list.append(tuple(tmp))
                break
    return tuple(next_list)
