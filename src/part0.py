#
# Created by MC着火的冰块(zhdbk3) on 2025/1/18
#

from manim import *
import numpy as np

from mobj import *
from config import *


class Part0(ThreeDScene):
    title: Tex | WithBackground  # 显示在左上角的标题
    subtitle: Subtitle  # 字幕

    def construct(self):
        load_config()

        self.subtitle = Subtitle(self)

        self.begin()

        self.change_title('0.1 三角函数 > 0.1.1 弧度制与任意角')
        self.part011()

        self.change_title('0.1 三角函数 > 0.1.2 三角函数，不仅是锐角！', with_background=True)
        self.part012()

        self.change_title('0.1 三角函数 > 0.1.3 反三角函数', with_background=True)
        self.part013()

        self.change_title('0.2 向量 > 0.2.1 向量的概念与表示', with_background=True)
        self.part021()

        self.change_title('0.2 向量 > 0.2.2 向量的线性运算')
        self.part022()

        self.change_title('0.2 向量 > 0.2.3 向量的点乘与夹角 *')
        self.part023()

        self.change_title('0.3 空间解析几何 > 0.3.1 空间直角坐标系')
        self.part031()

        self.change_title('0.3 空间解析几何 > 0.3.2 球')
        self.part032()

        self.change_title('0.3 空间解析几何 > 0.3.3 平面的点法式方程 *')
        self.part033()

        self.play(FadeOut(self.title))
        self.wait()

    def change_title(self, s: str, with_background: bool = False) -> None:
        """
        修改左上角的标题
        :param s: 标题文本
        :param with_background: 是否带黑色的背景，防止被遮挡
        :return: None
        """
        new = Tex(s).to_corner(UL)
        if with_background:  # 背景也会吃性能
            new = WithBackground(new)
        self.play(ReplacementTransform(self.title, new))
        self.title = new
        # 不知道为什么直接 become 太吃性能，所以用 ReplacementTransform

    def begin(self) -> None:
        big_title = Tex('0. 前置知识', font_size=60).shift(UP * 2)
        font_size = 27
        table01 = Tex(r'''
        0.1 三角函数
        \begin{itemize}
            \item 0.1.1 弧度制与任意角
            \item 0.1.2 三角函数，不仅是锐角！
            \item 0.1.3 反三角函数
        \end{itemize}
        ''', tex_environment='flushleft', font_size=font_size)
        table02 = Tex(r'''
        0.2 向量
        \begin{itemize}
            \item 0.2.1 向量的概念与表示
            \item 0.2.2 向量的线性运算
            \item 0.2.3 向量的点乘与夹角 *
        \end{itemize}
        ''', tex_environment='flushleft', font_size=font_size)
        table03 = Tex(r'''
        0.3 空间解析几何
        \begin{itemize}
            \item 0.3.1 空间直角坐标系
            \item 0.3.2 球
            \item 0.3.3 平面的点法式方程 *
        \end{itemize}
        ''', tex_environment='flushleft', font_size=font_size).next_to(table02, RIGHT)
        table01.next_to(table02, LEFT)

        self.play(FadeIn(big_title, table01, table02, table03))
        self.wait(2)
        self.subtitle.set_text('该部分将速通一下用到的初中以外的知识，已经学过的可以跳过',
                               'assets/sounds/part0/begin/该部分将.wav')
        self.wait()
        self.play(FadeOut(big_title))
        self.title = VGroup(table01, table02, table03)  # type: ignore  # 待会把目录翻到左上角

    def part011(self) -> None:
        formula = MathTex(r'\alpha = \frac{l}{r}').next_to(self.title, DOWN).set_x(0)
        center = DOWN + LEFT * 3  # 圆心
        r = 3  # 半径
        initial_side = Line(center, center + RIGHT * r)
        terminal_side = initial_side.copy().rotate(1, OUT, center)
        angle_mark = AngleMark(center, initial_side, terminal_side, r'\alpha')
        arc = AngleMark(center, initial_side, terminal_side, 'l', r=r)  # 用角标模拟圆弧
        r_label = MathTex('r').next_to(initial_side, DOWN)
        alpha_eq = MathTex(r'\alpha =').shift(DR)
        val_deg = DecimalNumber(np.rad2deg(1), unit=r'^{\circ}').next_to(alpha_eq, RIGHT)
        eq = MathTex('=').next_to(val_deg, RIGHT)
        val_rad = DecimalNumber(1).next_to(eq, RIGHT)

        def updater(_: Mobject) -> None:
            """在终边旋转时，更新图上显示的角度"""
            try:
                angle = terminal_side.get_angle() % TAU
                val_rad.set_value(angle)
                val_deg.set_value(np.rad2deg(angle))
            except ValueError:
                pass

        def change_angle(angle: float) -> None:
            """
            改变圆心角的大小及其相关的量，播放动画
            :param angle: 角的弧度
            :return: None
            """
            delta = angle - (terminal_side.get_angle() % TAU)  # 从当前开始，需要旋转的角度
            # 开启各 updater
            angle_mark.start_updater()
            arc.start_updater()
            val_rad.add_updater(updater)
            self.play(Rotate(terminal_side, delta, OUT, center, run_time=2,
                             rate_func=smooth))  # 使终边旋转过去，而不是直接飘过去
            # 关闭各 updater
            angle_mark.stop_updater()
            arc.stop_updater()
            val_rad.remove_updater(updater)

        self.wait()
        self.subtitle.set_text('我们已经知道了如何用角度来表示一个角的大小',
                               'assets/sounds/part0/1/1/我们已经.wav', block=False)
        self.play(Create(VGroup(initial_side, terminal_side, angle_mark), run_time=2),
                  Write(VGroup(alpha_eq, val_deg), run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.set_text('但是为了更加方便与简洁，我们需要引入弧度制', 'assets/sounds/part0/1/1/但是为了.wav')
        self.subtitle.pause()
        self.subtitle.set_text(r'对于一个扇形的圆心角 $\alpha$，其弧度数为弧长 $l$ 与半径 $r$ 的比值',
                               'assets/sounds/part0/1/1/对于一个.wav', block=False)
        self.play(Create(VGroup(arc, r_label), run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause()
        self.subtitle.set_text(r'即 $\alpha = \frac{l}{r}$', 'assets/sounds/part0/1/1/即alpha.wav', block=False)
        self.play(Write(VGroup(formula, eq, val_rad), run_time=3))
        self.subtitle.pause(1)
        self.subtitle.set_text('图中这个角就是 1 弧度', 'assets/sounds/part0/1/1/图中这个.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text(r'弧度的单位为 $\mathrm{rad}$，通常省略不写', 'assets/sounds/part0/1/1/弧度的单位.wav')
        self.subtitle.pause(3)
        for i in [1.14, 5.14, PI]:
            change_angle(i)
            self.wait(2)
        self.wait()
        self.play(FadeOut(formula, initial_side, terminal_side, r_label, angle_mark, arc,
                          alpha_eq, val_deg, eq, val_rad))
        self.wait()

        initial_side = Line(ORIGIN, RIGHT * 10)
        terminal_side = initial_side.copy()
        angle_mark = AngleMark(ORIGIN, initial_side, terminal_side, r'\theta', always_positive=False, add_tip=True)

        self.subtitle.set_text('我们规定，把始边逆时针旋转得到终边，形成的夹角是正的',
                               'assets/sounds/part0/1/1/我们规定.wav', block=False)
        self.play(Create(initial_side))
        self.add(terminal_side, angle_mark)
        angle_mark.start_updater()
        self.play(terminal_side.animate.rotate(1, OUT, ORIGIN))
        angle_mark.stop_updater()
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text('顺时针旋转，形成的夹角是负的，没错，角度也可以是负数',
                               'assets/sounds/part0/1/1/顺时针.wav', block=False)
        angle_mark.start_updater()
        self.play(terminal_side.animate.rotate(-2, OUT, ORIGIN))
        angle_mark.stop_updater()
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(3)
        self.play(FadeOut(initial_side, terminal_side, angle_mark))
        self.wait()

    def part012(self) -> None:
        plane = NumberPlane().add_coordinates()
        initial_side = Line(ORIGIN, RIGHT * 10)
        terminal_side = initial_side.copy()
        angle_mark = AngleMark(ORIGIN, initial_side, terminal_side, r'\theta')
        point = Dot(np.array((3 ** 0.5, 1, 0)))
        p_label = MathTex(r'P(x, y)').next_to(point, RIGHT)
        r_label = MathTex('r').move_to((ORIGIN + point.get_center()) / 2)
        definition = WithBackground(MathTex(r'\begin{aligned}'
                                            r'\sin\theta & = \frac{y}{r} \\'
                                            r'\cos\theta & = \frac{x}{r} \\'
                                            r'\tan\theta & = \frac{y}{x}'
                                            r'\end{aligned}')).next_to(self.title, DOWN, aligned_edge=LEFT)
        theta_eq = MathTex(r'\theta =').next_to(self.title, DOWN, aligned_edge=LEFT)
        theta_val = DecimalNumber(PI / 6).next_to(theta_eq, RIGHT)
        sin_eq = MathTex(r'\sin\theta =').next_to(theta_val, RIGHT, buff=1)
        sin_val = DecimalNumber(0.5).next_to(sin_eq, RIGHT)
        cos_eq = MathTex(r'\cos\theta =').next_to(sin_val, RIGHT, buff=1)
        cos_val = DecimalNumber(3 ** 0.5 / 2).next_to(cos_eq, RIGHT)
        tan_eq = MathTex(r'\tan\theta =').next_to(cos_val, RIGHT, buff=1)
        tan_val = DecimalNumber(3 ** 0.5 / 3).next_to(tan_eq, RIGHT)
        panel = (WithBackground(VGroup(theta_eq, theta_val, sin_eq, sin_val, cos_eq, cos_val, tan_eq, tan_val))
                 .next_to(self.title, DOWN, aligned_edge=LEFT))

        def updater(_: Mobject) -> None:
            """终边旋转时，相应地改变画面上其他元素"""
            try:
                theta = terminal_side.get_angle()
                if angle_mark.always_positive:
                    theta %= TAU
                point.move_to(np.array((2 * np.cos(theta), 2 * np.sin(theta), 0)))
                p_label.next_to(point, RIGHT)
                r_label.move_to((ORIGIN + point.get_center()) / 2)
                theta_val.set_value(theta)
                sin_val.set_value(np.sin(theta))
                cos_val.set_value(np.cos(theta))
                tan_val.set_value(np.tan(theta))
            except ValueError:
                pass

        self.wait()
        self.subtitle.set_text('我们已经学会了锐角三角函数的使用', 'assets/sounds/part0/1/2/我们已经.wav')
        self.subtitle.pause()
        self.subtitle.set_text('但实际上，三角函数的支持范围远不止于此', 'assets/sounds/part0/1/2/但实际上.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text(r'这里，我们来看一下实数范围内的三角函数',
                               'assets/sounds/part0/1/2/这里我们.wav', block=False)
        self.play(Create(plane, run_time=2))
        self.bring_to_back(plane)
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text(r'以 $x$ 轴正半轴为始边，旋转 $\theta$ 得到终边',
                               'assets/sounds/part0/1/2/以x轴.wav', block=False)
        self.add(terminal_side, angle_mark)
        angle_mark.start_updater()
        self.play(Rotate(terminal_side, PI / 6, OUT, ORIGIN, run_time=2))
        angle_mark.stop_updater()
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause()
        self.subtitle.set_text('在终边上取一点 $P(x, y)$，$P$ 到原点的距离为 $r$',
                               'assets/sounds/part0/1/2/在终边上.wav', block=False)
        self.play(Create(VGroup(point, p_label, r_label), run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause()
        self.subtitle.set_text(r'则有 $\begin{matrix} \sin\theta = \frac{y}{r} & \cos\theta = \frac{x}{r} & '
                               r'\tan\theta = \frac{y}{x} \end{matrix}$',
                               'assets/sounds/part0/1/2/则有sin.wav', block=False)
        self.play(Write(definition, run_time=3))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(3)
        self.subtitle.set_text('这就意味着有时三角函数值也可以是负的', 'assets/sounds/part0/1/2/这就意味.wav')
        self.wait()
        self.play(ReplacementTransform(definition, panel))
        self.wait()
        point.add_updater(updater)
        angle_mark.start_updater()
        self.play(Rotate(terminal_side, 5 / 3 * PI, about_point=ORIGIN, rate_func=linear, run_time=10))
        angle_mark.stop_updater()
        self.wait(2)
        angle_mark.start_updater()
        self.play(Rotate(terminal_side, -11 / 6 * PI, about_point=ORIGIN, rate_func=smooth, run_time=2))
        angle_mark.always_positive = False
        self.play(Rotate(terminal_side, -3 / 4 * PI, about_point=ORIGIN, rate_func=linear, run_time=5))
        point.remove_updater(updater)
        angle_mark.stop_updater()
        self.wait(3)
        self.play(FadeOut(plane, terminal_side, angle_mark, panel, point, p_label, r_label))
        self.wait()

        definition = (MathTex(r'\sin\theta = \frac{y}{r} \qquad \cos\theta = \frac{x}{r}')
                      .next_to(self.title, DOWN).set_x(0))
        formula = MathTex(r'\sin^2\alpha + \cos^2\alpha = 1')

        self.subtitle.set_text('再回头看这组定义式，你还能发现什么？',
                               'assets/sounds/part0/1/2/再回头看.wav', block=False)
        self.play(FadeIn(definition))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text(r'由勾股定理，不难发现，对于同一个角 $\alpha$，有',
                               'assets/sounds/part0/1/2/由勾股定理.wav')
        self.subtitle.pause()
        self.play(Write(formula, run_time=2))
        self.wait(5)
        self.play(FadeOut(definition, formula))
        self.wait()

    def part013(self) -> None:
        func = MathTex(r'\begin{aligned}'
                       r'y & = \arcsin x \\'
                       r'y & = \arccos x \\'
                       r'y & = \arctan x'
                       r'\end{aligned}')
        atan2 = WithBackground(MathTex(r'\mathrm{atan2}(y, x)')).next_to(self.title, DOWN).set_x(0)

        self.wait()
        self.subtitle.set_text('反三角函数，就是三角函数的反函数（好像是废话）', 'assets/sounds/part0/1/3/反三角.wav')
        self.subtitle.pause()
        self.subtitle.set_text('它的意思就是已知三角函数值，求这个角', 'assets/sounds/part0/1/3/它的意思.wav')
        self.subtitle.pause()
        self.subtitle.set_text(r'“反”可以用前缀 \textrm{arc-} 表示',
                               'assets/sounds/part0/1/3/反可以用.wav', block=False)
        self.play(Write(func, run_time=3))
        self.subtitle.pause(3)
        self.subtitle.set_text(r'但是，在一圈内，一个 $\tan x$ 对应两个 $x$，无法满足我们的需求',
                               'assets/sounds/part0/1/3/但是在.wav')
        self.subtitle.pause()
        self.subtitle.set_text(r'于是，就有了 $\mathrm{atan2}(y, x)$',
                               'assets/sounds/part0/1/3/于是就有.wav', block=False)
        self.play(FadeOut(func), Write(atan2, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(2)

        plane = NumberPlane().add_coordinates()
        point = Dot(np.array((3, 2, 0)))
        p_label = MathTex('P(x, y)').next_to(point, RIGHT)
        terminal_side = Line(ORIGIN, point.get_center())
        angle_mark = AngleMark(ORIGIN, Line(ORIGIN, RIGHT), terminal_side, r'\theta', always_positive=False)

        def updater(_: Mobject) -> None:
            p_label.next_to(point, RIGHT)
            terminal_side.become(Line(ORIGIN, point.get_center()))

        self.subtitle.set_text('该函数有两个自变量，代表一个点的坐标',
                               'assets/sounds/part0/1/3/该函数有.wav', block=False)
        self.play(FadeIn(plane), Create(VGroup(point, p_label, terminal_side, angle_mark), run_time=2))
        self.bring_to_back(plane)
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause()
        self.subtitle.set_text(r'函数值为该点的方位角，即图中的 $\theta$，范围在 $(-\pi, \pi]$',
                               'assets/sounds/part0/1/3/函数值为.wav')
        for i in [(-2, 3), (-3, -2), (2, -3)]:
            angle_mark.start_updater()
            p_label.add_updater(updater)
            self.play(point.animate.move_to(np.array((*i, 0))))
            angle_mark.stop_updater()
            p_label.remove_updater(updater)
            self.wait()
        self.wait(2)
        self.play(FadeOut(plane, point, p_label, terminal_side, angle_mark, atan2))
        self.wait()

    def part021(self) -> None:
        vec = Vector(RIGHT * 2 + UP, color=GREEN)
        label = MathTex(r'\boldsymbol a').next_to(vec.end, RIGHT)
        plane = NumberPlane().add_coordinates()
        component_x = Vector(RIGHT * 2, color=YELLOW)
        component_y = Vector(UP, color=BLUE)
        dl1 = DashedLine(vec.end, component_x.end)
        dl2 = DashedLine(vec.end, component_y.end)
        eq_val = MathTex(r'= (2, 1)').next_to(label, RIGHT)
        axes = ThreeDAxes().add_coordinates()

        self.add_fixed_in_frame_mobjects(self.title)
        self.subtitle.set_text('向量是既有大小又有方向的量，可以用一个带箭头的线段表示',
                               'assets/sounds/part0/2/1/既有大小.wav', block=False)
        self.play(Create(vec))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(2)
        self.subtitle.set_text(r'向量可记作小写字母，印刷使用粗体 $\boldsymbol a$，手写在在上面加个小箭头 $\vec a$',
                               'assets/sounds/part0/2/1/可记作.wav', block=False)
        self.play(Create(label))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text(r'或是起点在前，终点在后，记作 $\vec{AB}$', 'assets/sounds/part0/2/1/或是起点.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('向量也可以表示为各个方向的分量，记法类似于坐标',
                               'assets/sounds/part0/2/1/分量.wav', block=False)
        self.play(Create(VGroup(plane, dl1, dl2, component_x, component_y), run_time=3),
                  Write(eq_val, run_time=3))
        self.bring_to_back(plane)
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(3)
        self.play(FadeOut(component_x, component_y, dl1, dl2, eq_val, label))
        self.wait(2)
        self.subtitle.set_text('向量也可以是三维甚至一维的', 'assets/sounds/part0/2/1/三维甚至.wav', block=False)
        self.play(ReplacementTransform(plane, axes), Create(axes.get_axis_labels()))
        self.move_camera(60 * DEGREES, -60 * DEGREES)
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause()
        for i in [(1, 1, 4), (-5, 1, -4), (-1.9, -1.9, 8), (1, 0, 0)]:
            self.play(vec.animate.become(Vector(i, color=GREEN)))
        self.wait(2)
        self.move_camera(0, -PI / 2)
        self.wait()
        self.play(FadeOut(axes, axes.axis_labels, vec))
        self.wait()

    def part022(self) -> None:
        a = Vector(UR, color=YELLOW)
        a_label = MathTex(r'\boldsymbol a').next_to(a.end, UP)
        b = Vector(RIGHT * 2 + DOWN, color=BLUE)
        b_label = MathTex(r'\boldsymbol b').next_to(b.end, UP)
        a_plus_b = Vector(RIGHT * 3, color=GREEN)
        a_plus_b_label = MathTex(r'\boldsymbol a + \boldsymbol b').next_to(a_plus_b.end, RIGHT)
        dl1 = DashedLine(a.end, a_plus_b.end)
        dl2 = DashedLine(b.end, a_plus_b.end)
        add_formula = MathTex(r'(a, b) + (c, d) = (a + c, b + d)').next_to(self.title, DOWN, aligned_edge=LEFT)

        self.wait()
        self.subtitle.set_text('向量的加法遵循平行四边形法则', 'assets/sounds/part0/2/2/向量的加法.wav', block=False)
        self.play(Create(VGroup(a, a_label, b, b_label), run_time=2))
        self.play(Create(VGroup(dl1, dl2)))
        self.play(Create(VGroup(a_plus_b, a_plus_b_label)))
        self.subtitle.pause(2)
        self.subtitle.set_text('或三角形法则', 'assets/sounds/part0/2/2/或三角形.wav', block=False)
        self.play(FadeOut(dl1, dl2), VGroup(b, b_label).animate.move_to(a.end, UL))
        self.subtitle.pause(3)
        self.subtitle.set_text('也可以将各分量分别相加，得到向量和',
                               'assets/sounds/part0/2/2/分别相加.wav', block=False)
        self.play(Write(add_formula, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(3)
        self.play(FadeOut(b, b_label, a_plus_b, a_plus_b_label, add_formula))
        self.wait()

        module_formula = (MathTex(r'|\lambda\boldsymbol a| = |\lambda| |\boldsymbol a|')
                          .next_to(self.title, DOWN, aligned_edge=LEFT))
        plus2a = Vector(UR * 2, color=GREEN)
        plus2a_label = MathTex(r'2\boldsymbol a').next_to(plus2a.end, RIGHT)
        minus2a = Vector(DL * 2, color=RED)
        minus2a_label = MathTex(r'-2\boldsymbol a').next_to(minus2a.end, DOWN)
        components_formula = (MathTex(r'\lambda(x, y) = (\lambda x, \lambda y)')
                              .next_to(module_formula, DOWN, aligned_edge=LEFT))

        self.subtitle.set_text(r'一个向量 $\boldsymbol a$ 和一个实数 $\lambda$ 相乘时',
                               'assets/sounds/part0/2/2/一个向量.wav')
        self.subtitle.pause()
        self.subtitle.set_text('其模长满足这个关系', 'assets/sounds/part0/2/2/其模长.wav', block=False)
        self.play(Write(module_formula, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text(r'当 $\lambda > 0$ 时，$\lambda\boldsymbol a$ 与 $\boldsymbol a$ 方向相同',
                               'assets/sounds/part0/2/2/lambda大于0.wav', block=False)
        self.play(Create(VGroup(plus2a, plus2a_label)))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause()
        self.subtitle.set_text(r'当 $\lambda < 0$ 时，$\lambda\boldsymbol a$ 与 $\boldsymbol a$ 方向相反',
                               'assets/sounds/part0/2/2/lambda小于0.wav', block=False)
        self.play(Create(VGroup(minus2a, minus2a_label)))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text(r'也可以将各分量分别与 $\lambda$ 相乘',
                               'assets/sounds/part0/2/2/分别相乘.wav', block=False)
        self.play(Write(components_formula, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(3)
        self.play(FadeOut(module_formula, components_formula,
                          a, a_label, plus2a, plus2a_label, minus2a, minus2a_label))
        self.wait()

        ij = MathTex(r'\boldsymbol i = (1, 0), \boldsymbol j = (0, 1)').next_to(self.title, DOWN).set_x(0)
        ij_formula = MathTex(r'(x, y) = x\boldsymbol i + y\boldsymbol j').next_to(ij, DOWN)

        self.subtitle.set_text(r'基于此，记 $\boldsymbol i = (1, 0), \boldsymbol j = (0, 1)$',
                               'assets/sounds/part0/2/2/基于此.wav', block=False)
        self.play(Write(ij, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text('则任意一向量都可改写成这样的形式', 'assets/sounds/part0/2/2/则任意.wav', block=False)
        self.play(Write(ij_formula, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(2)
        self.subtitle.set_text('实际上，在刚才用坐标表示向量时，已经用到了这种思想', 'assets/sounds/part0/2/2/实际上.wav')
        self.subtitle.pause(1)
        self.play(FadeOut(ij, ij_formula))
        self.wait()

    def part023(self) -> None:
        note = Text('* 该章节难度较大，如果看不懂，只记住结论即可').next_to(self.title, DOWN, aligned_edge=LEFT)

        self.play(FadeIn(note))
        self.wait(3)
        self.play(FadeOut(note))
        self.wait()

        a = Vector(RIGHT * 3, color=BLUE)
        a_label = MathTex(r'\boldsymbol a').next_to(a.end, RIGHT)
        b = Vector(RIGHT * 2 + UP, color=YELLOW)
        b_label = MathTex(r'\boldsymbol b').next_to(b.end, RIGHT)
        theta = AngleMark(ORIGIN, a, b, r'\theta')
        dot_def = (MathTex(r'\boldsymbol a \cdot \boldsymbol b = |\boldsymbol a| |\boldsymbol b| \cos\theta')
                   .next_to(self.title, DOWN, aligned_edge=LEFT))
        cos_expr = (MathTex(r'\cos\theta = \frac{\boldsymbol a \cdot \boldsymbol b}{|\boldsymbol a| |\boldsymbol b|}')
                    .next_to(dot_def, DOWN, aligned_edge=LEFT))
        theta_expr = MathTex(r'\theta = \arccos\left(\frac{\boldsymbol a \cdot \boldsymbol b}'
                             r'{|\boldsymbol a| |\boldsymbol b|}\right)').next_to(dot_def, DOWN, aligned_edge=LEFT)

        self.subtitle.set_text(r'对于两个互成 $\theta$ 角的向量 $\boldsymbol a, \boldsymbol b$，我们规定向量的点乘',
                               'assets/sounds/part0/2/3/对于两个.wav', block=False)
        self.play(Create(VGroup(a, a_label, b, b_label, theta), run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text(r'$\boldsymbol a \cdot \boldsymbol b = |\boldsymbol a| |\boldsymbol b| \cos\theta$',
                               'assets/sounds/part0/2/3/ab.wav', block=False)
        self.play(Write(dot_def, run_time=3))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(3)
        self.subtitle.set_text('我们给它变形一下', 'assets/sounds/part0/2/3/我们给它.wav', block=False)
        self.play(TransformFromCopy(dot_def, cos_expr))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(2)
        self.play(ReplacementTransform(cos_expr, theta_expr))
        self.wait(3)
        self.subtitle.set_text('这时候就有人要问了', 'assets/sounds/part0/2/3/这时候.wav')
        self.subtitle.pause()
        self.subtitle.set_text('up up，我想要的就是向量夹角，但你点乘就要用到夹角啊？', 'assets/sounds/part0/2/3/upup.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('好问题，那么，向量点乘还可以怎么算呢？', 'assets/sounds/part0/2/3/好问题.wav')
        self.subtitle.pause(1)
        self.play(FadeOut(dot_def, cos_expr, theta_expr,
                          a, a_label, b, b_label, theta))
        self.wait()

        i = Vector(RIGHT, color=BLUE)
        i_label = MathTex(r'\boldsymbol i').next_to(i.end, RIGHT)
        j = Vector(UP, color=YELLOW)
        j_label = MathTex(r'\boldsymbol j').next_to(j.end, RIGHT)
        text = (Tex(r'$\boldsymbol i^2 = \boldsymbol j^2 = 1, \boldsymbol i \cdot \boldsymbol j = 0$'
                    r'（$\boldsymbol i^2$ 即 $\boldsymbol i \cdot \boldsymbol i$ 的简写）')
                .next_to(self.title, DOWN, aligned_edge=LEFT))

        self.subtitle.set_text(
            r'还记得我们之前的 $\boldsymbol i = (1, 0), \boldsymbol j = (0, 1)$ 吗？',
            'assets/sounds/part0/2/3/还记得.wav', block=False)
        self.play(Create(VGroup(i, i_label, j, j_label), run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(2)
        self.subtitle.set_text('由点乘的定义，不难得到', 'assets/sounds/part0/2/3/由点乘.wav')
        self.subtitle.pause()
        self.subtitle.set_text(r'$\boldsymbol i^2 = \boldsymbol j^2 = 1, \boldsymbol i \cdot \boldsymbol j = 0$',
                               'assets/sounds/part0/2/3/i2.wav', block=False)
        self.play(Write(text, run_time=3))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(2)
        self.play(FadeOut(i, i_label, j, j_label))
        self.wait()

        dot = MathTex(r'(x_1, y_1) \cdot (x_2, y_2)').next_to(text, DOWN, aligned_edge=LEFT)
        eq1 = MathTex(r'=       (x_1\boldsymbol i + y_1\boldsymbol j)'
                      r'  \cdot (x_2\boldsymbol i + y_2\boldsymbol j)').next_to(dot, RIGHT)
        eq2 = MathTex(r'=   x_1 x_2 \boldsymbol i^2'
                      r'  + x_1 y_2 \boldsymbol i \cdot \boldsymbol j'
                      r'  + x_2 y_1 \boldsymbol i \cdot \boldsymbol j'
                      r'  + y_1 y_2 \boldsymbol j^2').next_to(eq1, DOWN, aligned_edge=LEFT)
        eq3 = MathTex(r'= x_1 x_2 + y_1 y_2').next_to(eq2, DOWN, aligned_edge=LEFT)
        VGroup(dot, eq1, eq2, eq3).set_x(0)
        formula_3d = MathTex(r'(x_1, y_1, z_1) \cdot (x_2, y_2, z_2) = x_1 x_2 + y_1 y_2 + z_1 z_2')

        self.subtitle.set_text('我们来算一下这两个向量的点乘', 'assets/sounds/part0/2/3/我们来算.wav', block=False)
        self.play(Write(dot, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(2)
        self.play(TransformFromCopy(dot, eq1))
        self.wait(3)
        self.play(TransformFromCopy(eq1, eq2))
        self.wait(3)
        self.play(TransformFromCopy(eq2, eq3))
        self.wait(3)
        self.play(FadeOut(eq1, eq2), eq3.animate.next_to(dot, RIGHT, aligned_edge=DOWN))
        self.wait(3)
        self.subtitle.set_text('这样，我们就可以直接计算向量点乘，进而计算向量夹角！',
                               'assets/sounds/part0/2/3/这样我们.wav')
        self.subtitle.pause(2)
        self.subtitle.set_text('该算法在三维同样适用', 'assets/sounds/part0/2/3/该算法.wav', block=False)
        self.play(Write(formula_3d, run_time=3))
        self.subtitle.pause(3)
        self.play(FadeOut(formula_3d, dot, eq3, text))
        self.wait()

        conclusion = Text('结论', font_size=DEFAULT_FONT_SIZE).next_to(self.title, DOWN).set_x(0)
        text = (Tex(r'对于两个向量 $\boldsymbol a = (x_1, y_1), \boldsymbol b = (x_2, y_2)$，'
                    r'要想计算它们之间的夹角 $\theta$，有：')
                .next_to(conclusion, DOWN).align_to(self.title, LEFT))
        formula = (MathTex(r'\begin{aligned}'
                           r'& \boldsymbol a \cdot \boldsymbol b = x_1 x_2 + y_1 y_2 \\'
                           r'& \theta = \arccos\left(\frac{\boldsymbol a \cdot \boldsymbol b}'
                           r'{|\boldsymbol a| |\boldsymbol b|}\right)'
                           r'\end{aligned}')
                   .next_to(text, DOWN).set_x(0))

        self.play(FadeIn(conclusion))
        self.wait()
        self.play(Write(text, run_time=3))
        self.wait()
        self.play(Write(formula, run_time=3))
        self.wait(5)
        self.play(FadeOut(conclusion, text, formula))
        self.wait()

    def part031(self) -> None:
        axes2 = Axes().add_coordinates()
        axes3 = ThreeDAxes().add_coordinates()

        self.subtitle.set_text('我们已经知道了如何使用平面直角坐标系',
                               'assets/sounds/part0/3/1/我们已经.wav', block=False)
        self.play(Create(VGroup(axes2, axes2.get_axis_labels()), run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text('但很可惜我们终究不是二次元，因此需要引入空间直角坐标系',
                               'assets/sounds/part0/3/1/但很可惜.wav', block=False)
        self.play(ReplacementTransform(VGroup(axes2, axes2.axis_labels),
                                       VGroup(axes3, axes3.get_axis_labels()), run_time=2))
        self.add_fixed_in_frame_mobjects(self.title)
        self.move_camera(60 * DEGREES, 60 * DEGREES)
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(2)

        positive_x_axis = Line(ORIGIN, RIGHT * axes3.x_axis.length / 2, color=RED)
        positive_y_axis = Line(ORIGIN, UP * axes3.y_axis.length / 2, color=GREEN)
        positive_z_axis = Line(ORIGIN, OUT * axes3.z_axis.length / 2, color=BLUE)

        self.subtitle.set_text(r'需要注意的是，与 Minecraft 中不同，$x, y, z$ 轴是像图中这样排列的',
                               'assets/sounds/part0/3/1/需要注意.wav', block=False)
        self.play(Create(VGroup(positive_x_axis, positive_y_axis, positive_z_axis), run_time=3),
                  axes3.axis_labels[0].animate.set_color(RED),
                  axes3.axis_labels[1].animate.set_color(GREEN),
                  axes3.axis_labels[2].animate.set_color(BLUE),
                  axes3.x_axis.tip.animate.set_color(RED),
                  axes3.y_axis.tip.animate.set_color(GREEN),
                  axes3.z_axis.tip.animate.set_color(BLUE))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(3)
        self.subtitle.set_text('这样，我们就可以表示三维空间中的点坐标和向量', 'assets/sounds/part0/3/1/这样.wav')
        self.subtitle.pause(1)
        self.play(FadeOut(axes3, axes3.axis_labels, positive_x_axis, positive_y_axis, positive_z_axis))
        self.wait()

    def part032(self) -> None:
        axes = ThreeDAxes()
        sphere = Sphere(radius=2, fill_opacity=0.5)
        eq = MathTex('x^2 + y^2 + z^2 = r^2').next_to(self.title, DOWN, aligned_edge=LEFT)

        self.wait()
        self.add_fixed_in_frame_mobjects(self.title)
        self.move_camera(60 * DEGREES, 60 * DEGREES)
        self.subtitle.set_text('考虑一个球心在原点的球', 'assets/sounds/part0/3/2/考虑一个.wav', block=False)
        self.play(Create(VGroup(axes, axes.get_axis_labels(), sphere), run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text('球面上每个点到球心的距离都是相等的，均为半径 $r$', 'assets/sounds/part0/3/2/球面上.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('由此，我们就可以写出这个球的方程', 'assets/sounds/part0/3/2/由此.wav', block=False)
        self.add_fixed_in_frame_mobjects(eq)
        self.play(Write(eq, run_time=2))
        self.subtitle.pause(5)
        self.play(FadeOut(axes, axes.axis_labels, sphere, eq))
        self.wait()

    def part033(self) -> None:
        axes = ThreeDAxes()
        a, b, c = 1, 1, 2
        n = Vector(np.array((a, b, c)), color=YELLOW)
        n_label = MathTex(r'\boldsymbol n').next_to(n.end, UP)
        # ax + by + cz = 0  # 平面过 n 的起点
        # z = -(ax + by) / c
        z = lambda x, y: -(a * x + b * y) / c
        plane = Surface(lambda u, v: np.array((u, v, z(u, v))), [-1.5, 1.5], [-1.5, 1.5],
                        resolution=(1, 1), fill_opacity=0.5)
        x0, y0 = 1, -1
        p = Dot(np.array((x0, y0, z(x0, y0))))
        p_label = MathTex('P').next_to(p, DOWN)
        cond = (Tex(r'法向量 $\boldsymbol n = (a, b, c)$，点 $P(x_0, y_0, z_0)$')
                .next_to(self.title, DOWN, aligned_edge=LEFT))

        self.add_fixed_in_frame_mobjects(self.title)
        self.move_camera(75 * DEGREES, 15 * DEGREES)
        self.subtitle.set_text('不难想象出，确定空间中平面上一个和平面垂直的向量和平面上一点就可以确定唯一的一个平面',
                               'assets/sounds/part0/3/3/不难想象.wav', block=False)
        self.add_fixed_orientation_mobjects(n_label, p, p_label)
        self.play(FadeIn(axes), Create(VGroup(n, n_label, p, p_label, plane), run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text('我们称这个向量为平面的法向量', 'assets/sounds/part0/3/3/我们称.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text(r'已知法向量 $\boldsymbol n = (a, b, c)$，平面上一点 $P(x_0, y_0, z_0)$',
                               'assets/sounds/part0/3/3/已知法向量.wav', block=False)
        self.add_fixed_in_frame_mobjects(cond)
        self.play(Write(cond, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause()
        self.subtitle.set_text('如何求出这个平面的方程呢？', 'assets/sounds/part0/3/3/如何求出.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('求平面的方程，就是求平面上任意一点都满足的方程', 'assets/sounds/part0/3/3/求平面的.wav')
        self.subtitle.pause(1)

        x_q, y_q = 1, 1
        q = Dot(np.array((x_q, y_q, z(x_q, y_q))))
        q_label = MathTex('Q').next_to(q, UP)
        q_coord = WithBackground(Tex('$Q(x, y, z)$')).next_to(cond, RIGHT)
        vec_pq = Line(p.get_center(), q.get_center(), color=GREEN).add_tip()
        pq_expr = (WithBackground(MathTex(r'\vec{PQ} = (x - x_0, y - y_0, z - z_0)'))
                   .next_to(cond, DOWN, aligned_edge=LEFT))
        eq = (WithBackground(MathTex('a(x - x_0) + b(y - y_0) + c(z - z_0) = 0'))
              .next_to(pq_expr, DOWN, aligned_edge=LEFT))

        self.subtitle.set_text('在平面上任取一点 $Q(x, y, z)$，则有',
                               'assets/sounds/part0/3/3/在平面上.wav', block=False)
        self.add_fixed_orientation_mobjects(q, q_label)
        self.add_fixed_in_frame_mobjects(q_coord)
        self.play(Create(VGroup(q, q_label)), Write(q_coord))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause()
        self.add_fixed_in_frame_mobjects(pq_expr)
        self.play(Write(pq_expr, run_time=2), Create(vec_pq, run_time=2))
        self.wait(2)
        self.subtitle.set_text(r'由于 $\boldsymbol n$ 与平面垂直，所以一定有 $\vec{PQ} \perp \boldsymbol n$',
                               'assets/sounds/part0/3/3/由于n.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('还记得之前的向量点乘吗？', 'assets/sounds/part0/3/3/还记得.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('由定义得，两垂直的向量点积为 0；而同时点积又等于各分量相乘之和',
                               'assets/sounds/part0/3/3/由定义得.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('那么就可以写出这个方程', 'assets/sounds/part0/3/3/那么就可以.wav')
        self.add_fixed_in_frame_mobjects(eq)
        self.play(Write(eq, run_time=3))
        self.wait(3)
        self.subtitle.set_text(r'没错，这就是该平面的方程！好诶\textasciitilde', 'assets/sounds/part0/3/3/没错.wav')
        self.subtitle.pause(3)
        self.play(FadeOut(cond, eq, axes, n, n_label, p, p_label, q, q_label, q_coord, vec_pq, plane, pq_expr))
        self.wait()

        conclusion = Text('结论', font_size=DEFAULT_FONT_SIZE).next_to(self.title, DOWN).set_x(0)
        text1 = (Tex(r'已知平面的法向量 $\boldsymbol n = (a, b, c)$，平面上一点 $P(x_0, y_0, z_0)$')
                 .next_to(conclusion, DOWN))
        text2 = Text(r'平面的方程为').next_to(text1, DOWN)
        eq.next_to(text2, DOWN)

        self.set_camera_orientation(0, -PI / 2)
        self.play(FadeIn(conclusion))
        self.wait()
        self.play(Write(text1, run_time=3))
        self.wait(2)
        self.play(Write(text2, run_time=2))
        self.wait()
        self.play(Write(eq, run_time=3))
        self.wait(5)
        self.play(FadeOut(conclusion, text1, text2, eq))
        self.wait()
