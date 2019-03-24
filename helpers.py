import cocos


def draw_rect(rect, layer):
    # bottom line
    line = cocos.draw.Line(rect.get_origin(),
                           (rect.x + rect.width, rect.y),
                           (255, 0, 0, 255), 5)
    layer.add(line)

    # top line
    line = cocos.draw.Line((rect.x + rect.width, rect.y + rect.height),
                           (rect.x, rect.y + rect.height),
                           (255, 0, 0, 255), 5)
    layer.add(line)

    # left line
    line = cocos.draw.Line(rect.get_origin(),
                           (rect.x, rect.y + rect.height),
                           (255, 0, 0, 255), 5)
    layer.add(line)

    # right line
    line = cocos.draw.Line((rect.x + rect.width, rect.y),
                           (rect.x + rect.width, rect.y + rect.height),
                           (255, 0, 0, 255), 5)
    layer.add(line)
