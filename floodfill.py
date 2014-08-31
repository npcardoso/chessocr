def inside(x, boundaries):
    for i in range(len(x)):
        if x[i] < boundaries[0][i] or \
           x[i] > boundaries[1][i]:
            return False
    return True


def neighbors(p, boundaries):
    deltas = [[0,1], [1,0],
              [0,-1], [-1,0],
              [1,1], [1,-1],
              [1,-1], [-1,-1]]
    ret = []
    for d in deltas:
        pp = [p[0] + d[0], p[1] + d[1]]
        if inside(pp, boundaries):
            ret.append(pp)
    return ret


def floodfill (pix, point, color, fg, boundaries):
    x, y = point
    if pix[x, y] != fg:
        return 0

    pix[x, y] = color

    queue = [point]
    points = [point]

    while(queue):
        el = queue.pop()
        for x, y in neighbors(el, boundaries):
            if pix[x, y] == fg:
                pix[x, y] = color
                p = (x,y)
                queue.append(p)
                points.append(p)

    return points
