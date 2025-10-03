import pygame
import sys
import math
import random  # 导入random模块用于随机选择
import time # 导入时间模块用于计时
import os
import subprocess

# 初始化pygame
pygame.init()

# 获取资源路径的函数
def resource_path(relative_path):
    """ 获取资源文件的绝对路径 """
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# 设置窗口大小为固定尺寸而非全屏
screen_width = 800
screen_height = 600

# 设置窗口大小为普通窗口模式
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("快写史鸡")

# 设置背景颜色
background_color = (135, 206, 235)  # 天空蓝

# 创建一个比窗口小的桌面区域
desktop_margin = 50  # 距离窗口边缘的距离
desktop_rect = pygame.Rect(
    desktop_margin, 
    desktop_margin, 
    screen_width - 2 * desktop_margin, 
    screen_height - 2 * desktop_margin
)

# 圆角半径
corner_radius = 20

# 加载手的图片
hand_image = pygame.image.load(resource_path("hand_left.png"))
# 缩放图片以适应显示（可调整大小）
hand_image = pygame.transform.scale(hand_image, (450, 300))  # 调整为合适的尺寸

# 加载右手的图片
hand_right_image = pygame.image.load(resource_path("hand_right.png"))
# 缩放图片以适应显示（可调整大小）
hand_right_image = pygame.transform.scale(hand_right_image, (300, 300))  # 调整为合适的尺寸

# 加载老师背影图片
teacher_back_image = pygame.image.load(resource_path("teacher_back.png"))
# 缩放图片以适应显示（可调整大小）
teacher_back_image = pygame.transform.scale(teacher_back_image, (450, 300))  # 调整为合适的尺寸

# 加载老师正面图片
teacher_face_image = pygame.image.load(resource_path("teacher_face.png"))
# 缩放图片以适应显示（可调整大小）
teacher_face_image = pygame.transform.scale(teacher_face_image, (450, 300))  # 调整为合适的尺寸

# 添加字体用于文本渲染
font = pygame.font.SysFont(None, 24)
text_font = pygame.font.SysFont(None, 20)

# 添加时钟用于控制动画
clock = pygame.time.Clock()

# 添加黑板显示状态标志
show_blackboard = False

# 添加当前老师形象变量
current_teacher_image = teacher_back_image

# 初始化老师转身相关变量
start_time = time.time()
teacher_display_time = random.randint(3, 10)
turning_around = False
facing_back = True

# 添加游戏状态变量
game_state = "playing"  # "playing" 或 "lost"
fullscreen = False

# 添加玩家抬头状态变量
head_up = False  # 玩家是否抬头

# 添加打字相关的变量
typed_text = ""  # 已输入的文字
max_chars_per_page = 100  # 每页最多字符数
total_chars_typed = 0  # 总共输入的字符数

# 主循环
running = True
while running:
    change = False
    notice = "Teacher is writing..."
    current_teacher_image = teacher_back_image
    
    # 处理老师转身逻辑
    elapsed_time = time.time() - start_time
    
    # 如果老师面朝黑板且到了转身时间，则开始转身
    if facing_back and elapsed_time >= teacher_display_time:
        turning_around = True
        facing_back = False
        notice = "Teacher is seeing you..."
        current_teacher_image = teacher_face_image
    elif turning_around:
        # 如果正在转身过程中
        # 如果转身持续2秒后，老师重新面朝黑板
        if elapsed_time >= teacher_display_time + 2:
            turning_around = False
            facing_back = True
            start_time = time.time()  # 重新开始计时
            teacher_display_time = random.randint(3, 10)  # 重新设置下一次转身时间
            current_teacher_image = teacher_back_image
            notice = "Teacher is writing..."
        else:
            notice = "Teacher is seeing you..."
            current_teacher_image = teacher_face_image

    # 处理事件
    for event in pygame.event.get():
        # 检查是否按下ESC键退出全屏
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # 检查是否按下空格键切换黑板显示
            elif event.key == pygame.K_SPACE:
                if game_state == "playing":
                    head_up = not head_up
                    show_blackboard = not show_blackboard
                else:  # 如果游戏已结束，ESC键重置游戏
                    game_state = "playing"
                    head_up = False  # 重置抬头状态
                    if fullscreen:
                        screen = pygame.display.set_mode((screen_width, screen_height))
                        pygame.display.set_caption("快写史鸡")
                        fullscreen = False
            # 处理打字输入
            elif event.key == pygame.K_BACKSPACE:
                # 删除最后一个字符
                typed_text = typed_text[:-1]
            elif event.key not in [pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT,
                                   pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_TAB, pygame.K_CAPSLOCK,
                                   pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                # 添加可打印字符到输入文本（排除特殊按键）
                if len(typed_text) < max_chars_per_page and game_state == "playing":
                    if event.unicode.isprintable():
                        typed_text += event.unicode
                        total_chars_typed += 1
                    
                    # 如果达到一页的最大字符数，则清空
                    if len(typed_text) >= max_chars_per_page:
                        typed_text = ""
        # 检查是否点击关闭按钮
        elif event.type == pygame.QUIT:
            running = False
    
    # 填充背景色
    screen.fill(background_color)
    
    # 检查游戏状态
    if game_state == "lost":
        # 全屏黑色背景
        if not fullscreen:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            fullscreen = True
        screen.fill((0, 0, 0))
        
        # 显示"You lost"
        lost_font = pygame.font.SysFont(None, 72)
        lost_text = lost_font.render("You lost", True, (255, 255, 255))
        screen.blit(lost_text, (screen.get_width() // 2 - lost_text.get_width() // 2, 
                               screen.get_height() // 2 - lost_text.get_height() // 2))
        
        # 显示提示信息
        hint_font = pygame.font.SysFont(None, 36)
        hint_text_1 = hint_font.render("Press Space to continue", True, (200, 200, 200))
        screen.blit(hint_text_1, (screen.get_width() // 2 - hint_text_1.get_width() // 2, 
                               screen.get_height() // 2 + 50))
        hint_text_2 = hint_font.render("Press ESC to quit", True, (200, 200, 200))
        screen.blit(hint_text_2, (screen.get_width() // 2 - hint_text_2.get_width() // 2, 
                               screen.get_height() // 2 + 100))
    else:
        # 检查是否在老师看你的时候抬头了
        # 修改: 更准确地判断失败条件，只有当老师面朝学生且玩家未抬头时才失败
        if not facing_back and not head_up:
            game_state = "lost"
        
        # 如果需要显示黑板
        if show_blackboard:
            # 绘制黑板
            blackboard_rect = pygame.Rect(100, 100, 600, 400)
            pygame.draw.rect(screen, (0, 0, 0), blackboard_rect)  # 黑色黑板
            pygame.draw.rect(screen, (50, 50, 50), blackboard_rect, 5)  # 灰色边框
            
            # 在黑板上添加一些粉笔字迹（示例）
            font = pygame.font.SysFont(None, 36)
            text = font.render("Shit politics!!!  Shit English teacher!!!", True, (255, 255, 255))
            screen.blit(text, (blackboard_rect.centerx - text.get_width() // 2, 
                              blackboard_rect.centery - text.get_height() // 2))
            
            # 显示提示信息
            notice_font = pygame.font.SysFont(None, 30)
            notice_text = notice_font.render(notice, True, (255, 255, 0))  # 黄色文字
            screen.blit(notice_text, (screen_width // 2 - notice_text.get_width() // 2, 50))

            # 修改: 只有在最后一秒才显示倒计时
            if facing_back:  # 只有在老师背对时才显示倒计时
                time_left = teacher_display_time - elapsed_time
                # 只在最后一秒显示倒计时
                if time_left <= 1 and time_left >= 0:
                    countdown_text = notice_font.render(f"Time left: {time_left:.1f}s", True, (255, 100, 100))
                    screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, 20))
            else:  # 老师面对学生时显示"Watching"
                watching_text = notice_font.render("Watching...", True, (255, 100, 100))
                screen.blit(watching_text, (screen_width // 2 - watching_text.get_width() // 2, 20))

            # 将当前老师图片绘制在黑板的左侧
            teacher_x = blackboard_rect.left - current_teacher_image.get_width() + 400  # 留出一些边距
            teacher_y = blackboard_rect.top + (blackboard_rect.height - current_teacher_image.get_height()) + 100  # 居中偏下
            screen.blit(current_teacher_image, (teacher_x, teacher_y))

        else:
            # 在桌面区域内绘制带圆角的内容（示例：白色圆角矩形）
            pygame.draw.rect(screen, (255, 255, 255), desktop_rect, border_radius=corner_radius)
            
            # 将左手的图片绘制在桌面区域的左侧
            hand_x = desktop_rect.left - 100  # 留出一些边距
            hand_y = desktop_rect.centery  # 居中偏上
            screen.blit(hand_image, (hand_x, hand_y))

            # 绘制作业本 (在桌面区域内部靠右位置)
            homework_width = 150
            homework_height = 200
            homework_x = desktop_rect.right - homework_width - 300  # 距离桌面右边30像素
            homework_y = desktop_rect.top + 150  # 距离桌面顶部150像素
            
            # 作业本主体
            homework_rect = pygame.Rect(homework_x, homework_y, homework_width, homework_height)
            pygame.draw.rect(screen, (255, 255, 200), homework_rect)  # 米黄色作业本
            pygame.draw.rect(screen, (200, 200, 150), homework_rect, 2)  # 边框
            
            # 作业本横线 (表示文字行)
            line_spacing = 20
            for i in range(1, homework_height // line_spacing):
                y_pos = homework_y + i * line_spacing
                pygame.draw.line(screen, (200, 200, 150), 
                                 (homework_x + 10, y_pos), 
                                 (homework_x + homework_width - 10, y_pos), 1)
            
            # 作业本顶部装订线
            pygame.draw.line(screen, (150, 150, 100), 
                             (homework_x, homework_y + 5), 
                             (homework_x + homework_width, homework_y + 5), 3)
            
            # 显示已输入的文字
            words = []
            lines = []
            current_line = ""
            max_chars_per_line = 15  # 每行最多字符数
            
            # 根据字符数分段处理换行
            for i, char in enumerate(typed_text):
                current_line += char
                # 每15个字符或遇到换行符时换行
                if len(current_line) >= max_chars_per_line or char == '\n' or i == len(typed_text) - 1:
                    lines.append(current_line)
                    current_line = ""
            
            # 显示文字内容
            for i, line in enumerate(lines):
                if i < homework_height // line_spacing - 1:  # 确保不超出作业本范围
                    text_surface = text_font.render(line, True, (0, 0, 0))
                    screen.blit(text_surface, (homework_x + 10, homework_y + 10 + i * line_spacing))
            
            # 计算右手的摇摆位置
            time_val = pygame.time.get_ticks() / 1000  # 获取运行时间（秒）
            swing_amount = math.sin(time_val * 3) * 20  # 计算摇摆偏移量
            
            # 将右手的图片绘制在桌面区域的右侧，并添加摇摆效果
            hand_right_x = desktop_rect.right - hand_right_image.get_width() - 100 + swing_amount  # 添加摇摆偏移
            hand_right_y = desktop_rect.centery  # 居中偏上
            screen.blit(hand_right_image, (hand_right_x, hand_right_y))
            
            # 显示提示信息
            notice_font = pygame.font.SysFont(None, 30)
            notice_text = notice_font.render(notice, True, (255, 255, 0))  # 黄色文字
            screen.blit(notice_text, (screen_width // 2 - notice_text.get_width() // 2, 50))
            
            # 显示已打字数
            word_count_text = notice_font.render(f"字数: {total_chars_typed}", True, (0, 0, 0))
            screen.blit(word_count_text, (10, 10))
            
            # 修改: 只有在最后一秒才显示倒计时
            if facing_back:  # 只有在老师背对时才显示倒计时
                time_left = teacher_display_time - elapsed_time
                # 只在最后一秒显示倒计时
                if time_left <= 1 and time_left >= 0:
                    countdown_text = notice_font.render(f"Time left: {time_left:.1f}s", True, (255, 100, 100))
                    screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, 20))
            else:  # 老师面对学生时显示"Watching"
                watching_text = notice_font.render("Watching...", True, (255, 100, 100))
                screen.blit(watching_text, (screen_width // 2 - watching_text.get_width() // 2, 20))
    
    # 更新显示
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(60)

# 退出pygame
pygame.quit()
sys.exit()