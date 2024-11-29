import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("小游戏")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (209, 93, 103)
GREEN = (147, 173, 124)

# 定义最小正方形的尺寸
RECT_WIDTH = 24
RECT_HEIGHT = 16

class HollowFrame:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rects = self.create_frame()

    def create_frame(self):
        rects = []

        # 横向总长度是 15 个小矩形的宽度
        total_width = 15 * RECT_WIDTH
        # 纵向总高度是 13 个小矩形的高度
        total_height = 13 * RECT_HEIGHT

        # 上边框
        for i in range(15):
            rect = pygame.Rect(self.x + i * RECT_WIDTH, self.y, RECT_WIDTH, RECT_HEIGHT - 3)
            rects.append(rect)

        # 下边框
        for i in range(15):
            rect = pygame.Rect(self.x + i * RECT_WIDTH, self.y + total_height - RECT_HEIGHT + 3, RECT_WIDTH, RECT_HEIGHT - 3)
            rects.append(rect)

        # 左边框
        for i in range(7):
            rect = pygame.Rect(self.x, self.y + i * (RECT_HEIGHT - 1), RECT_WIDTH - 3, RECT_HEIGHT - 1)
            rects.append(rect)
        # 留下5个A高度的缺口

        # 右边框
        for i in range(7, 12):
            rect = pygame.Rect(self.x + total_width - RECT_WIDTH + 3, self.y + i * (RECT_HEIGHT + 1), RECT_WIDTH - 3, (RECT_HEIGHT + 1))
            rects.append(rect)
        # 留下6个A高度的缺口

        # 中间从上伸出的一个A
        upper_notch = pygame.Rect(self.x + 8 * RECT_WIDTH, self.y + RECT_HEIGHT - 3, RECT_WIDTH - 2, RECT_HEIGHT)
        rects.append(upper_notch)

        # 中间从下伸出的一个A
        lower_notch = pygame.Rect(self.x + 8 * RECT_WIDTH, self.y + total_height - 2 * RECT_HEIGHT + 3, RECT_WIDTH - 2, RECT_HEIGHT)
        rects.append(lower_notch)

        return rects

    def draw(self, surface):
        for rect in self.rects:
            pygame.draw.rect(surface, GREEN, rect)

    def check_collision(self, custom_shape_rects):
        for r in self.rects:
            for csr in custom_shape_rects:
                if r.colliderect(csr):
                    return True
        return False
    
class CustomShape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stat = 0 # 0 原始形状 1 垂直翻转 2 水平翻转 3 垂直翻转
        self.x_old = x
        self.y_old = y
        self.rects = self.create_shape()
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def create_shape(self):
        pass

    def draw(self, surface):
        for rect in self.rects:
            pygame.draw.rect(surface, RED, rect)

    # def flip(self, flip_type):
    #     # 假设翻转是相对于整个形状的中心进行的
    #     center_x = sum(rect.centerx for rect in self.rects) / len(self.rects)
    #     center_y = sum(rect.centery for rect in self.rects) / len(self.rects)

    #     if flip_type == 'vertical':
    #         self.rects = [pygame.Rect(2 * center_x - r.right, r.top, r.width, r.height) for r in self.rects]
    #     elif flip_type == 'horizontal':
    #         self.rects = [pygame.Rect(r.left, 2 * center_y - r.bottom, r.width, r.height) for r in self.rects]

    def handle_event(self, event, group):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 检查是否是左键
                mouse_x, mouse_y = event.pos
                for rect in self.rects:
                    if rect.collidepoint(mouse_x, mouse_y):
                        self.dragging = True
                        self.offset_x = self.x - mouse_x
                        self.offset_y = self.y - mouse_y
                        break
            if event.button == 3:  # 检查是否是右键
                mouse_x, mouse_y = event.pos
                for rect in self.rects:
                    if rect.collidepoint(mouse_x, mouse_y):
                        self.stat = (self.stat + 1) % 4
                        self.rects = self.create_shape()
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.x_old = self.x
                self.y_old = self.y
                self.x = mouse_x + self.offset_x
                self.y = mouse_y + self.offset_y
                self.rects = [pygame.Rect(r.left + self.x - self.x_old, r.top + self.y - self.y_old, r.width, r.height) for r in self.rects]


    def check_collision(self, custom_shape_rects):
        for r in self.rects:
            for csr in custom_shape_rects:
                if r.colliderect(csr):
                    return True
        return False

class CustomShape1(CustomShape):
    def __init__(self, x, y):
        super().__init__(x, y)

    def create_shape(self):
        rects = []
        patterns = []
        heights = []
        if self.stat == 0:
            patterns = [4, 4, 4, 5, 3, 5, 6, 3, 5, 4, 4, 4, 5]
            heights = [1, 1, 2, 0, 2, 0, 0, 2, 1, 2, 2, 2, 1]
        elif self.stat == 1:
            patterns = [5, 4, 4, 4, 5, 3, 6, 5, 3, 5, 4, 4, 4]
            heights = [1, 2, 2, 2, 1, 2, 0, 0, 2, 0, 2, 1, 1]
        elif self.stat == 2:
            patterns = [5, 4, 4, 4, 5, 3, 6, 5, 3, 5, 4, 4, 4]
            heights = [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1]
        elif self.stat == 3:
            patterns = [4, 4, 4, 5, 3, 5, 6, 3, 5, 4, 4, 4, 5]
            heights = [1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0]
        current_x = self.x
        for count, height in zip(patterns, heights):
            rect = pygame.Rect(current_x, self.y + height * RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT * count)
            rects.append(rect)
            current_x += RECT_WIDTH
        return rects

class CustomShape2(CustomShape):
    def __init__(self, x, y):
        super().__init__(x, y)

    def create_shape(self):
        rects = []
        patterns = []
        heights = []
        if self.stat == 0:
            patterns = [4, 4, 4, 4, 5, 4, 4, 3, 5, 3, 4, 3, 4]
            heights = [0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1]
        elif self.stat == 1:
            patterns = [4, 3, 4, 3, 5, 3, 4, 4, 5, 4, 4, 4, 4]
            heights = [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0]
        elif self.stat == 2:
            patterns = [4, 3, 4, 3, 5, 3, 4, 4, 5, 4, 4, 4, 4]
            heights = [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1]
        elif self.stat == 3:
            patterns = [4, 4, 4, 4, 5, 4, 4, 3, 5, 3, 4, 3, 4]
            heights = [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0]
        current_x = self.x
        for count, height in zip(patterns, heights):
            rect = pygame.Rect(current_x, self.y + height * RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT * count)
            rects.append(rect)
            current_x += RECT_WIDTH
        return rects
    
class ShapeGroup:
    def __init__(self):
        self.shapes = []
        self.group_dragging = False

    def add_shape(self, shape):
        self.shapes.append(shape)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.group_dragging = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Calculate the average center of all shapes
                center_x = sum(shape.x + RECT_WIDTH // 2 for shape in self.shapes) // len(self.shapes)
                center_y = sum(shape.y + RECT_HEIGHT // 2 for shape in self.shapes) // len(self.shapes)

                self.group_offset_x = center_x - mouse_x
                self.group_offset_y = center_y - mouse_y


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.group_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.group_dragging:
                mouse_x, mouse_y = event.pos
                dx = mouse_x + self.group_offset_x - (sum(shape.x + RECT_WIDTH // 2 for shape in self.shapes) // len(self.shapes))
                dy = mouse_y + self.group_offset_y - (sum(shape.y + RECT_HEIGHT // 2 for shape in self.shapes) // len(self.shapes))

                for shape in self.shapes:
                    shape.x_old = shape.x
                    shape.y_old = shape.y
                    shape.x += dx
                    shape.y += dy
                    shape.rects = [pygame.Rect(r.left + dx, r.top + dy, r.width, r.height) for r in shape.rects]

        for shape in self.shapes:
            shape.handle_event(event, self)

    def draw(self, surface):
        for shape in self.shapes:
            shape.draw(surface)

def main():
    shape_group = ShapeGroup()
    shape1 = CustomShape1(50, 50)  # 初始化在 (50, 50) 位置
    shape2 = CustomShape2(50, 250)  # 初始化在 (50, 150) 位置
    shape_group.add_shape(shape1)
    shape_group.add_shape(shape2)
    total_width = 15 * RECT_WIDTH
    total_height = 13 * RECT_HEIGHT
    x_centered = SCREEN_WIDTH // 2 - total_width // 2
    y_centered = SCREEN_HEIGHT // 2 - total_height // 2
    frame = HollowFrame(x_centered, y_centered)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            shape_group.handle_event(event)

        if shape1.dragging:
            if frame.check_collision(shape1.rects):
                shape1.x = shape1.x_old
                shape1.y = shape1.y_old
                shape1.rects = shape1.create_shape()
                
            if shape2.check_collision(shape1.rects):
                shape1.x = shape1.x_old
                shape1.y = shape1.y_old
                shape1.rects = shape1.create_shape()
                

        if shape2.dragging:
            if frame.check_collision(shape2.rects):
                shape2.x = shape2.x_old
                shape2.y = shape2.y_old
                shape2.rects = shape2.create_shape()
                
            if shape1.check_collision(shape2.rects):
                shape2.x = shape2.x_old
                shape2.y = shape2.y_old
                shape2.rects = shape2.create_shape()

        if shape_group.group_dragging:
            if frame.check_collision(shape1.rects) or frame.check_collision(shape2.rects):
                for shape in shape_group.shapes:
                    shape.x = shape.x_old
                    shape.y = shape.y_old
                    shape.rects = shape.create_shape()

        # 填充背景
        screen.fill(WHITE)

        # 绘制自定义形状
        shape_group.draw(screen)
        frame.draw(screen)

        # 更新屏幕
        pygame.display.flip()

if __name__ == "__main__":
    main()
