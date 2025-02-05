#
# Created by MC着火的冰块(zhdbk3) on 2025/1/22
#

import random

from manim import *

from mobj import *
from config import *
from utils import get_circle


class Part1(ThreeDScene):
    title: Tex
    subtitle: Subtitle

    def construct(self):
        load_config()

        self.subtitle = Subtitle(self)

        self.begin()
        self.part11_12()

    def begin(self):
        text1 = Text('正片开始', font_size=72)
        text2 = Text('照片测星定位', font_size=96).next_to(text1, DOWN)
        text3 = Text('Photographical Astronomical Positioning').next_to(text2, DOWN)
        group = VGroup(text1, text2, text3)
        group.move_to(ORIGIN)

        self.play(FadeIn(group))
        self.wait(3)
        self.play(FadeOut(group))
        self.wait()

        big_title = Tex('1. 从“过洋牵星术”到双星定位法', font_size=DEFAULT_FONT_SIZE)
        self.title = Tex('1. 从“过洋牵星术”到双星定位法').to_corner(UL)

        self.play(Write(big_title, run_time=2))
        self.wait(2)
        self.play(ReplacementTransform(big_title, self.title))
        self.wait()

    def part11_12(self):
        # 过洋牵星术
        # 该英文翻译来自 https://www.ntsc.cas.cn/ztlm/zggddhjs/cssnqxgh/201904/t20190417_5276624.html
        img = ImageMobject('assets/img/star-guided_ocean_crossing_technique.jpg').scale_to_fit_height(5)

        self.subtitle.set_text('早在古代，就有了一种叫“过洋牵星术”的技术',
                               'assets/sounds/part1/1/早在古代.wav', block=False)
        self.play(FadeIn(img))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause()
        self.subtitle.set_text('人们通过测量北极星的高度，就可以在茫茫大海上确定自己的纬度',
                               'assets/sounds/part1/1/人们通过.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('这是怎么做到的呢？', 'assets/sounds/part1/1/这是怎么.wav')
        self.play(FadeOut(img))
        self.wait()

        earth_dot = Dot(color=BLUE)
        earth_label = Text('地球', color=BLUE).next_to(earth_dot)
        r = 3.5  # 天球半径
        celestial_sphere = Circle(r, color=WHITE)
        # 随机生成星星
        stars = VGroup(Star(color=WHITE, fill_opacity=1, outer_radius=0.1)
                       .shift(RIGHT * r).rotate(random.random() * TAU, about_point=ORIGIN)
                       for _ in range(20))
        # 北极星
        polaris = Star(color=WHITE, fill_opacity=1, outer_radius=0.1).shift(UP * r)
        direct_light_1 = Arrow(polaris.get_center(), ORIGIN)

        self.subtitle.set_text('为方便研究，我们可以假想星星都投影在一个以地球为中心的半径无穷大的天球上',
                               'assets/sounds/part1/1/为方便研究.wav', block=False)
        self.play(FadeIn(earth_dot, earth_label), Create(celestial_sphere))
        self.play(Create(VGroup(stars, polaris), run_time=2))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(1)
        self.subtitle.set_text('恒星在天球上的位置几乎固定不变，因而得名“恒星”', 'assets/sounds/part1/1/恒星在.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('其中，北极星就几乎处于北天极的位置', 'assets/sounds/part1/1/其中北极星.wav', block=False)
        self.play(polaris.animate.set_color(YELLOW))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text('也就是说，它的直射点在地球的北极', 'assets/sounds/part1/1/也就是说.wav', block=False)
        self.play(Create(direct_light_1))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)

        R = 2  # 地球半径
        earth_circle = Circle(R, color=BLUE)
        direct_light_2 = Line(UP * 10, UP * R)
        dl_gp_center = DashedLine(ORIGIN, UP * R)
        gp_label = WithBackground(Text('GP')).next_to(UP * R, RIGHT)
        ship = Dot(np.array((-np.sqrt(3) / 2 * R, R / 2, 0)), color=YELLOW)
        ground = TangentLine(earth_circle, 5 / 12, 3)
        light = Line(ship.get_center(), ship.get_center() + UP * 10)
        elevation_angle = AngleMark(ship.get_center(), ground.rotate(PI), light, r'\phi')
        zenith_line = DashedLine(ORIGIN, np.array((-4, 4 / 3 * np.sqrt(3), 0)))
        equator = DashedLine(RIGHT * R, LEFT * R)
        latitude = AngleMark(ORIGIN, zenith_line, equator, r'\phi')

        self.play(VGroup(celestial_sphere, stars, polaris).animate.scale(10))
        self.play(FadeOut(earth_label), ReplacementTransform(earth_dot, earth_circle),
                  ReplacementTransform(direct_light_1, VGroup(direct_light_2, dl_gp_center)))
        self.subtitle.set_text('星星的直射点，我们称为星星的地理位置，英文简称 GP',
                               'assets/sounds/part1/1/星星的直射点.wav', block=False)
        self.play(Write(gp_label))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text(r'现在有一艘船，上面的人已经测出了北极星的高度角 $\phi$，如何知道它所在的纬度呢？',
                               'assets/sounds/part1/1/现在有一艘船.wav', block=False)
        self.play(Create(VGroup(ship, ground, light, elevation_angle), run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text('让我们画上辅助线', 'assets/sounds/part1/1/让我们画上辅助线.wav', block=False)
        self.play(Create(VGroup(zenith_line, equator), run_time=1))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(3)
        self.subtitle.set_text(r'没错，纬度就是高度角 $\phi$！', 'assets/sounds/part1/1/没错纬度.wav', block=False)
        self.play(Create(latitude))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(5)
        self.play(FadeOut(equator, latitude))
        self.wait()

        # 双星定位法
        zenith_label = Text('天顶').next_to(zenith_line.get_end(), UP)
        zenith_angle = AngleMark(ship.get_center(), light, zenith_line, r'\theta')
        center_angel = AngleMark(ORIGIN, dl_gp_center, zenith_line, r'\theta')
        left = ship.get_center()
        right = np.array((np.sqrt(3) / 2 * R, R / 2, 0))
        solid_semicircle = Line(left, right, path_arc=0.5, color=YELLOW)
        dashed_semicircle = DashedLine(left, right, path_arc=-0.5, color=YELLOW)

        self.subtitle.set_text('尝试一下，这个结论可以推广到任何星星吗？', 'assets/sounds/part1/2/尝试一下.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('这里，我们再引入天顶的概念', 'assets/sounds/part1/2/这里我们.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('抬头看向你的正上方，那个方向就是天顶', 'assets/sounds/part1/2/抬头看向.wav', block=False)
        self.play(Write(zenith_label))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text(r'星星与天顶的夹角，称为星星的天顶角，这里记作 $\theta$',
                               'assets/sounds/part1/2/星星与天顶.wav', block=False)
        self.play(Create(zenith_angle))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text('不难看出，天顶角就是高度角的余角', 'assets/sounds/part1/2/不难看出.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('相信已经有眼尖的观众发现了，这个角就等于天顶角啊',
                               'assets/sounds/part1/2/相信已经.wav', block=False)
        self.play(Create(center_angel))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text(
            '也就是说，观测者所在地和星星的 GP 分别与地心连线，形成的夹角就等于观测者看这颗星星的天顶角！',
            'assets/sounds/part1/2/也就是说.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('反过来，已知一颗星星的 GP 和天顶角，那么观测者一定在一个确定的圆上',
                               'assets/sounds/part1/2/反过来.wav', block=False)
        self.play(Create(solid_semicircle))
        self.play(Create(dashed_semicircle))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)

        earth_sphere = Sphere(ORIGIN, R, fill_opacity=0.5)
        circle1 = get_circle(90 * DEGREES, 0, 60 * DEGREES, YELLOW)
        circle2 = get_circle(11 * DEGREES, 4 * DEGREES, 51.4 * DEGREES, RED)
        circle3 = get_circle(19.1 * DEGREES, 91.810 * DEGREES, 35 * DEGREES, GREEN)

        self.play(FadeOut(direct_light_2, light, ground, dl_gp_center, zenith_line, zenith_label, gp_label,
                          elevation_angle, zenith_angle, center_angel, ship),
                  ReplacementTransform(earth_circle, earth_sphere),
                  ReplacementTransform(VGroup(solid_semicircle, dashed_semicircle), circle1))
        self.add_fixed_in_frame_mobjects(self.title)
        self.move_camera(45 * DEGREES, 45 * DEGREES)
        self.subtitle.set_text('如果你知道两颗星星，那么就会得到两个交点',
                               'assets/sounds/part1/2/如果你.wav', block=False)
        self.play(Create(circle2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text('这时候用一下空间想象力，根据照片上两颗星星的位置关系，就可以得到正确的那个交点',
                               'assets/sounds/part1/2/这时候.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('恭喜你已经掌握了双星定位法！', 'assets/sounds/part1/2/恭喜你.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('想象力不足的朋友们（其实也包括我）也不用担心，因为从第 3 颗星星开始，就只有一个公共点了',
                               'assets/sounds/part1/2/想象力.wav', block=False)
        self.play(Create(circle3))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text('那么下面的思路就很明确了', 'assets/sounds/part1/2/那么下面.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('我们要求出照片上每颗星星的 GP 和天顶角', 'assets/sounds/part1/2/我们要求.wav')
        self.subtitle.pause()
        self.subtitle.set_text('然后的事情就如瓮中捉鳖了', 'assets/sounds/part1/2/然后的.wav')
        self.subtitle.pause(3)
        self.play(FadeOut(earth_sphere, circle1, circle2, circle3, self.title))
        self.wait()
