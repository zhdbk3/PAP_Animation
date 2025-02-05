#
# Created by MC着火的冰块(zhdbk3) on 2025/2/3
#

from manim import *
import numpy as np
from numpy import sin, cos

from config import *
from mobj import *
from utils import get_circle, get_gp_dot

# 数据来自 https://github.com/zhdbk3/PhotoAstrologicalPositioning/blob/main/src/calc.py
# 需修改（还是加个 print）
STARS_DATA = [  # (纬度, 经度, 天顶角)
    (0.42201334092701226, 2.4009810932395625, 0.35529958390883354),
    (0.23831113457675462, 2.0761760466639396, 0.493355619375492),
    (0.07303475699074605, 2.2029902156728043, 0.6510268854498817),
    (0.0582581208042085, 2.120135072757503, 0.6662405546005195),
    (-0.23454849559766353, 2.445663703752183, 0.9959864545506584)
]


class Part5(ThreeDScene):
    title: Tex
    subtitle: Subtitle

    def construct(self):
        load_config()

        self.subtitle = Subtitle(self)

        self.begin()
        self.part51()
        self.part52()

    def begin(self) -> None:
        big_title = Tex('5. 定位计算', font_size=DEFAULT_FONT_SIZE)
        self.title = Tex('5. 定位计算').to_corner(UL)

        self.play(Write(big_title, run_time=2))
        self.wait(2)
        self.play(ReplacementTransform(big_title, self.title))
        self.add_fixed_in_frame_mobjects(self.title)
        self.wait()

    def part51(self) -> None:
        """5.1 平面方程"""
        earth_sphere = Sphere(ORIGIN, 2, color=BLUE, fill_opacity=0.5)
        lat, lon, zenith_angle = 30 * DEGREES, 0, 30 * DEGREES
        gp = Dot((np.sqrt(3), 0, 1))
        circle = get_circle(lat, lon, zenith_angle, YELLOW)
        # θ 为天顶角
        # (cosϕcosλ)x + (cosϕsinλ)y + (sinϕ)z = cosθ
        plane = Surface(lambda x, y: 2 * np.array((  # 才想起来 manim 中半径是 2，看了半天……
            x, y, (cos(zenith_angle) - cos(lat) * cos(lon) * x - cos(lat) * sin(lon) * y) / sin(lat)
        )), (0.25, 1.25), (-1, 1), resolution=(1, 1), fill_opacity=0.5).set_color(YELLOW)

        self.move_camera(60 * DEGREES, 0)
        self.subtitle.set_text('在“双星定位法”那一节中，我们发现已知一颗星星的 GP 和天顶角，观测者就一定在一个确定的圆上',
                               'assets/sounds/part5/1/在双星定位法.wav', block=False)
        self.play(Create(earth_sphere))
        self.add_fixed_orientation_mobjects(gp)
        self.play(Create(VGroup(gp, circle)))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text('圆上的点和 GP 分别与地心连线，形成的夹角就是天顶角',
                               'assets/sounds/part5/1/圆上的点.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('那么，如何表示出这个圆呢？', 'assets/sounds/part5/1/那么如何.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('这个圆可以视作空间中一个平面去截地球，得到的公共部分',
                               'assets/sounds/part5/1/这个圆.wav', block=False)
        self.play(Create(plane))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text('那么我们只要求出这个平面，再与球联立，就可以表示出这个圆',
                               'assets/sounds/part5/1/那么我们.wav')
        self.subtitle.pause(1)
        self.move_camera(PI / 2, -PI / 2)
        # 转到 xOy 平面上处理
        Group(earth_sphere, circle, plane, self.camera.light_source).rotate(PI / 2, LEFT, ORIGIN)
        gp.move_to((np.sqrt(3), 1, 0))
        self.set_camera_orientation(0, -PI / 2)

        earth_circle = Circle(2, BLUE)
        f = lambda x: -np.sqrt(3) * (x - 2)
        plane_line = Line((0.5, f(0.5), 0), (2.5, f(2.5), 0), color=YELLOW)
        n = Vector(gp.get_center(), color=YELLOW)
        n_label = MathTex(r'\boldsymbol n').next_to(n.end, UP).set_color(YELLOW)
        dl1 = DashedLine(ORIGIN, RIGHT * 2)
        dl2 = DashedLine(ORIGIN, (1, np.sqrt(3), 0))
        theta = AngleMark(ORIGIN, n, dl2, r'\theta')
        n_cos_theta = Vector(gp.get_center() * cos(zenith_angle), color=GREEN)
        n_cos_theta_label = MathTex(r'\boldsymbol n \cos\theta').next_to(n_cos_theta.end).set_color(GREEN)

        self.play(ReplacementTransform(earth_sphere, earth_circle),
                  ReplacementTransform(VGroup(circle, plane), plane_line))
        self.wait()
        self.subtitle.set_text(r'记星星的单位方向向量为 $\boldsymbol n$，天顶角为 $\theta$',
                               'assets/sounds/part5/1/记星星.wav', block=False)
        self.play(Create(n), Write(n_label))
        self.play(Create(VGroup(dl1, dl2, theta)))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text(r'不难看出，$\boldsymbol n$ 就是平面的法向量', 'assets/sounds/part5/1/不难看出.wav')
        self.subtitle.pause()
        self.subtitle.set_text(r'而平面经过 $\boldsymbol n \cos\theta$ 的末端',
                               'assets/sounds/part5/1/而平面.wav', block=False)
        self.play(Create(n_cos_theta), Write(n_cos_theta_label))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)

        n_abc = MathTex(r'\boldsymbol n & = (a, b, c)').next_to(self.title, DOWN, aligned_edge=LEFT)
        eq_abc = WithBackground(MathTex(r'a(x - a\cos\theta) + b(y - b\cos\theta) + c(z - c\cos\theta) = 0'))
        n_expr = (WithBackground(MathTex(r'\boldsymbol n = (\cos\phi\cos\lambda, \cos\phi\sin\lambda, \sin\phi)'))
                  .next_to(self.title, DOWN, aligned_edge=LEFT))
        phi_lam = Tex(r'（$\phi$ 为纬度，$\lambda$ 为经度）').next_to(n_expr, DOWN)
        substituted = WithBackground(MathTex(
            r'(\cos\phi\cos\lambda)(x - \cos\phi\cos\lambda\cos\theta) \\'
            r'+ (\cos\phi\sin\lambda)(y - \cos\phi\sin\lambda\cos\theta) \\'
            r'+ (\sin\phi)(z - \sin\phi\cos\theta) = 0',
            tex_environment='gather*'
        ))
        expanded = WithBackground(MathTex(
            r'(\cos\phi\cos\lambda)x + (\cos\phi\sin\lambda)y + (\sin\phi)z \\'
            r'- \cos^2\phi\cos^2\lambda\cos\theta - \cos^2\phi\sin^2\lambda\cos\theta'
            r'- \sin^2\phi\cos\theta = 0',
            tex_environment='gather*'
        ))
        simplified_1 = WithBackground(MathTex(
            r'(\cos\phi\cos\lambda)x + (\cos\phi\sin\lambda)y + (\sin\phi)z \\'
            r'- \cos^2\phi(\cos^2\lambda + \sin^2\lambda)\cos\theta - \sin^2\phi\cos\theta = 0',
            tex_environment='gather*'
        ))
        simplified_2 = WithBackground(MathTex(
            r'(\cos\phi\cos\lambda)x + (\cos\phi\sin\lambda)y + (\sin\phi)z \\'
            r'- \cos^2\phi\cos\theta - \sin^2\phi\cos\theta = 0',
            tex_environment='gather*'
        ))
        simplified_3 = WithBackground(MathTex(
            r'(\cos\phi\cos\lambda)x + (\cos\phi\sin\lambda)y + (\sin\phi)z \\'
            r'- (\cos^2\phi + \sin^2\phi)\cos\theta = 0',
            tex_environment='gather*'
        ))
        final = WithBackground(MathTex(
            r'(\cos\phi\cos\lambda)x + (\cos\phi\sin\lambda)y + (\sin\phi)z = \cos\theta'
        ))

        self.subtitle.set_text(r'由此，若 $\boldsymbol n = (a, b, c)$，则可列出平面的方程',
                               'assets/sounds/part5/1/由此若.wav', block=False)
        self.play(Write(n_abc, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.play(Write(eq_abc, run_time=3))
        self.wait(3)
        self.subtitle.set_text(r'还记得 $\boldsymbol n$ 是怎么用 GP 经纬度表示的吗？',
                               'assets/sounds/part5/1/还记得.wav', block=False)
        self.wait()
        self.play(ReplacementTransform(n_abc, VGroup(n_expr, phi_lam)))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.play(ReplacementTransform(eq_abc, substituted))
        self.wait(3)
        self.play(ReplacementTransform(substituted, expanded))
        self.wait(3)
        self.play(ReplacementTransform(expanded, simplified_1))
        self.wait(3)
        self.play(ReplacementTransform(simplified_1, simplified_2))
        self.wait(3)
        self.play(ReplacementTransform(simplified_2, simplified_3))
        self.wait(3)
        self.play(ReplacementTransform(simplified_3, final))
        self.wait(3)
        self.subtitle.set_text('这，就是一颗星星的平面方程', 'assets/sounds/part5/1/这就是.wav')
        self.subtitle.pause(5)
        self.play(FadeOut(n_expr, phi_lam, final, earth_circle, dl1, dl2, gp,
                          n, n_cos_theta, n_label, n_cos_theta_label, plane_line, theta))
        self.wait(1)

    def part52(self) -> None:
        """5.2 双星定位与最终结果"""
        eq_group = MathTex(r'\begin{cases}'
                           r'A_1x + B_1y + C_1z = D_1 \\'
                           r'A_2x + B_2y + C_2z = D_2 \\'
                           r'x^2 + y^2 + z^2 = 1'
                           r'\end{cases}')
        cart2sph = MathTex(r'\begin{cases}'
                           r'\phi = \arcsin z \\'
                           r'\lambda = \mathrm{atan2}(y, x)'
                           r'\end{cases}')

        self.subtitle.set_text('现在来到最后一步！', 'assets/sounds/part5/2/现在来到.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('我们已经有了每颗星星的平面方程', 'assets/sounds/part5/2/我们已经.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('对于一次双星定位，我们只要把两颗星星的平面方程和地球的方程联立',
                               'assets/sounds/part5/2/对于一次.wav', block=False)
        self.play(Write(eq_group, run_time=3))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(3)
        self.subtitle.set_text('不出意外的话会得到两组解（出意外的话就把这次舍掉）', 'assets/sounds/part5/2/不出意外.wav')
        self.subtitle.pause()
        self.subtitle.set_text('是两个空间直角坐标', 'assets/sounds/part5/2/是两个.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('我们把空间直角坐标转化为经纬度', 'assets/sounds/part5/2/我们把.wav', block=False)
        self.play(eq_group.animate.next_to(self.title, DOWN, aligned_edge=LEFT))
        self.play(Write(cart2sph, run_time=2))
        self.subtitle.pause(5)
        self.play(FadeOut(eq_group, cart2sph))

        earth = Sphere(ORIGIN, 2, color=BLUE, fill_opacity=0.5)
        gp_dots = VGroup()
        circles = VGroup()
        for data, color in zip(STARS_DATA, [RED, ORANGE, YELLOW, GREEN, LIGHT_PINK]):
            lat, lon, zenith_angle = data
            gp_dots.add(get_gp_dot(lat, lon, color))
            circles.add(get_circle(lat, lon, zenith_angle, color))
        result = (41.5 * DEGREES, 124.4 * DEGREES)
        result_dot = Star(outer_radius=0.03, color=WHITE, fill_opacity=1).move_to(get_gp_dot(*result, WHITE))

        self.move_camera(75 * DEGREES, 135 * DEGREES)
        self.subtitle.set_text('对星星两两进行定位，会得到很多个坐标', 'assets/sounds/part5/2/对星星.wav', block=False)
        self.play(Create(earth))
        for gp_dot, circle in zip(gp_dots, circles):
            self.add_fixed_orientation_mobjects(gp_dot)
            self.play(Create(VGroup(gp_dot, circle), run_time=0.5))
        self.subtitle.pause(1)
        self.subtitle.set_text('挑出每次双星定位两个坐标中正确的那个', 'assets/sounds/part5/2/挑出每次.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('对它们的纬度和经度取中位数，就能得到最终的结果',
                               'assets/sounds/part5/2/对它们.wav', block=False)
        self.move_camera(PI / 2 - result[0], result[1])
        self.move_camera(zoom=5)
        self.add_fixed_orientation_mobjects(result_dot)
        self.play(Create(result_dot))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(1)
        self.subtitle.set_text('恭喜你完成了一次照片测星定位！', 'assets/sounds/part5/2/恭喜你.wav')
        self.subtitle.pause(3)
        self.play(FadeOut(self.title, earth, gp_dots, circles))
        self.wait()

        thanks = Text('非常感谢您能看到这里！', font_size=DEFAULT_FONT_SIZE)

        self.set_camera_orientation(0, -PI / 2, zoom=1)
        result_dot.center()
        self.play(ReplacementTransform(result_dot, thanks))
        self.wait(3)
        self.play(FadeOut(thanks))
        self.wait()
