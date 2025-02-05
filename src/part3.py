#
# Created by MC着火的冰块(zhdbk3) on 2025/1/31
#

from manim import *

from config import *
from mobj import *


class Part3(ThreeDScene):
    title: Tex
    subtitle: Subtitle

    def construct(self):
        load_config()

        self.subtitle = Subtitle(self)

        self.begin()
        self.part31()
        self.part32()

    def begin(self) -> None:
        big_title = Tex('3. 照片成像原理与像素焦距', font_size=DEFAULT_FONT_SIZE)
        self.title = Tex('3. 照片成像原理与像素焦距').to_corner(UL)

        self.play(Write(big_title, run_time=2))
        self.wait(2)
        self.play(ReplacementTransform(big_title, self.title))
        self.add_fixed_in_frame_mobjects(self.title)
        self.wait()

    def part31(self) -> None:
        """3.1 理论夹角"""
        earth = Circle(2, BLUE)
        line1 = VGroup(DashedLine(ORIGIN, RIGHT * 2), Line(RIGHT * 2, RIGHT * 10))
        gp1 = Dot(RIGHT * 2)
        gp1_label = Tex('GP$_1$').next_to(gp1, DR)
        line2 = line1.copy().rotate(1, OUT, ORIGIN)
        gp2 = gp1.copy().rotate(1, OUT, ORIGIN)
        gp2_label = Tex('GP$_2$').next_to(gp2, RIGHT)
        theta = AngleMark(ORIGIN, line1[0], line2[0], r'\theta')
        person = gp2.copy().rotate(PI / 2, IN, ORIGIN)
        p_line1 = Line(person.get_center(), person.get_center() + RIGHT * 10)
        p_line2 = p_line1.copy().rotate(1, OUT, person.get_center())
        p_theta = AngleMark(person.get_center(), p_line1, p_line2, r'\theta')

        def updater(_: Mobject) -> None:
            p_line1.move_to(person.get_center(), LEFT)
            p_line2.move_to(person.get_center(), DL)
            p_theta.become(AngleMark(person.get_center(), p_line1, p_line2, r'\theta'))

        self.subtitle.set_text('在上一节中，我们求出了每颗星星的 GP',
                               'assets/sounds/part3/1/在上一节.wav', block=False)
        self.play(Create(VGroup(earth, gp1, gp2), run_time=2),
                  Create(VGroup(line1, line2)),
                  Write(VGroup(gp1_label, gp2_label), run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text('借此，我们就可以计算出星光之间的夹角',
                               'assets/sounds/part3/1/借此.wav', block=False)
        self.play(Create(theta))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text('由于星星十分遥远，这个夹角在地球上任何地方看都是一样的',
                               'assets/sounds/part3/1/由于星星.wav', block=False)
        self.play(Create(VGroup(person, p_line1, p_line2, p_theta)))
        self.wait()
        person.add_updater(updater)
        self.play(Rotate(person, PI - 1, OUT, ORIGIN, rate_func=there_and_back, run_time=4))
        person.remove_updater(updater)
        self.subtitle.pause(1)
        self.play(FadeOut(earth, line1, gp1, gp1_label, line2, gp2, gp2_label, theta,
                          person, p_line1, p_line2, p_theta))
        self.wait()

        axes = ThreeDAxes((-4, 4, 2), (-4, 4, 2), (-4, 4, 2), 8, 8, 8)
        earth = Sphere(ORIGIN, 2, color=BLUE, fill_opacity=0.5)
        north_label = WithBackground(MathTex(r'\mathrm{N}')).next_to(earth, OUT)
        prime_label = WithBackground(MathTex(r'0^{\circ}')).next_to(earth, RIGHT)

        self.subtitle.set_text('要计算这个夹角，首先，我们要把星星的 GP 转化为向量', 'assets/sounds/part3/1/要计算.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('我们把地心放在原点，规定 $z$ 轴正方向为北，$x$ 轴正半轴穿过 (0°, 0°)',
                               'assets/sounds/part3/1/我们把.wav', block=False)
        self.set_camera_orientation(60 * DEGREES, -60 * DEGREES)
        self.play(FadeIn(axes, axes.get_axis_labels()), Create(earth))
        self.add_fixed_orientation_mobjects(north_label, prime_label)
        self.play(Write(VGroup(north_label, prime_label)))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text('为表示与计算方便，在本视频中，地球的半径都为 1', 'assets/sounds/part3/1/为表示.wav')
        # 实际上，在 manim 中，半径是 2，把它当做 1，真是 1 的话就太小了
        self.subtitle.pause(1)
        self.play(FadeOut(north_label, prime_label))

        gp_latlon = (Tex(r'GP $(\phi, \lambda)$', font_size=DEFAULT_FONT_SIZE)
                     .next_to(self.title, DOWN, aligned_edge=LEFT))
        lat, lon = 30 * DEGREES, 30 * DEGREES
        x = 2 * np.cos(lat) * np.cos(lon)
        y = 2 * np.cos(lat) * np.sin(lon)
        z = 2 * np.sin(lat)
        gp = Dot((x, y, z))
        n = Vector((x, y, z), color=YELLOW)
        n_label = MathTex(r'\boldsymbol n').next_to(n.end, UP)
        projection = DashedLine(ORIGIN, (x, y, 0))
        n_x = Vector((x, 0, 0), color=RED)
        n_y = Vector((0, y, 0), color=GREEN)
        n_z = Vector((0, 0, z), color=BLUE)
        dl1 = DashedLine(n.end, projection.end)
        dl2 = DashedLine(projection.end, n_x.end)
        dl3 = DashedLine(projection.end, n_y.end)
        dl4 = DashedLine(n.end, n_z.end)
        lam = AngleMark(ORIGIN, Line(ORIGIN, RIGHT), projection, r'\lambda')
        phi = AngleMark3D(ORIGIN, projection, n, r'\phi')
        n_formula = (WithBackground(MathTex(r'\boldsymbol n = (\cos\phi\cos\lambda, \cos\phi\sin\lambda, \sin\phi)'))
                     .next_to(gp_latlon, DOWN).set_x(0))

        self.subtitle.set_text(r'考虑一个纬度为 $\phi$，经度为 $\lambda$ 的 GP',
                               'assets/sounds/part3/1/考虑一个.wav', block=False)
        self.add_fixed_orientation_mobjects(gp)
        self.add_fixed_in_frame_mobjects(gp_latlon)
        self.play(Create(gp), Write(gp_latlon, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text(r'我们不妨就求这个从地心到 GP 的单位方向向量 $\boldsymbol n$',
                               'assets/sounds/part3/1/我们不妨.wav', block=False)
        self.play(Create(n), FadeOut(earth))
        self.add_fixed_orientation_mobjects(n_label)
        self.play(FadeOut(gp), Write(n_label))
        self.move_camera(zoom=2, frame_center=(x / 2, y / 2, z / 2))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(1)
        self.subtitle.set_text('让我们画上各分量与辅助线，标上已知的角',
                               'assets/sounds/part3/1/让我们.wav', block=False)
        self.play(Create(VGroup(n_x, n_y, n_z)))
        self.play(Create(VGroup(projection, dl1, dl2, dl3, dl4)))
        self.add_fixed_orientation_mobjects(phi.label)
        self.add_fixed_orientation_mobjects(lam.label, phi.label)
        self.play(Create(VGroup(lam, phi)))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(2)
        self.subtitle.set_text(r'看着图，我们就可以写出 $\boldsymbol n$ 的表达式',
                               'assets/sounds/part3/1/看着图.wav')
        self.subtitle.pause()
        self.add_fixed_in_frame_mobjects(n_formula)
        self.play(Write(n_formula, run_time=3))
        self.wait(5)
        self.play(FadeOut(axes, axes.axis_labels, n, n_label, projection, n_x, n_y, n_z,
                          dl1, dl2, dl3, dl4, lam, phi))
        self.move_camera(0, -PI / 2, zoom=1, frame_center=ORIGIN)

        theta_formula = MathTex(r'\theta = \arccos\left(\frac{\boldsymbol a \cdot \boldsymbol b}'
                                r'{|\boldsymbol a| |\boldsymbol b|}\right)').next_to(n_formula, DOWN)
        angle_name = Text('理论夹角', font_size=DEFAULT_FONT_SIZE).next_to(theta_formula, DOWN)

        self.subtitle.set_text('于是，要计算两个星光之间的夹角，我们只要先将 GP 转化为向量',
                               'assets/sounds/part3/1/于是.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('然后用这个公式计算两向量之间的夹角即可',
                               'assets/sounds/part3/1/然后用.wav', block=False)
        self.play(Write(theta_formula, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text('这个夹角，我们称之为理论夹角', 'assets/sounds/part3/1/这个夹角.wav', block=False)
        self.play(Write(angle_name, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(5)
        self.play(FadeOut(gp_latlon, n_formula, theta_formula, angle_name))
        self.wait()

    def part32(self) -> None:
        """3.2 像素焦距的计算"""
        note = WithBackground(Tex(
            r'* 关于照片上的坐标系：为计算机处理方便，我们一般规定向下为 $y$ 轴正方向；为测星定位方便，我们以照片的正中心为原点'
        )).to_corner(DL).shift(UP * 0.5)

        axes = ThreeDAxes(z_range=(-7, 7, 1), z_length=14)
        # 反转 y 轴及其标签
        axes.y_axis.scale(-1)
        y_label = axes.get_axis_labels()[1]
        y_label.shift(DOWN * 2 * y_label.get_y())
        photo_img = ImageMobject('assets/img/photo.jpg').scale_to_fit_height(6)
        photo_simplified = PhotoSimplified().scale_to_fit_height(6)
        # 该照片的像素焦距约为 1300，正好约等于照片的宽度
        z = photo_simplified.width
        viewpoint = Dot(OUT * z)
        lights = VGroup(*[Line(viewpoint.get_center(), i.get_center(), stroke_width=1)
                        .scale(10, about_point=viewpoint.get_center())
                          for i in photo_simplified.stars])
        z_line = Line(viewpoint.get_center(), ORIGIN, color=BLUE)

        self.wait()
        self.play(FadeIn(photo_img))
        self.wait()
        self.play(Create(photo_simplified, run_time=2))
        self.wait()
        self.play(FadeOut(photo_img))
        self.subtitle.pause(1)
        self.subtitle.set_text('一般来说，一张照片可视为从一个视点看外面的世界，投影到一个平面上',
                               'assets/sounds/part3/2/一般来说.wav', block=False)
        self.move_camera(60 * DEGREES, 30 * DEGREES, 120 * DEGREES, frame_center=(0, 0, z / 2))
        self.add_fixed_in_frame_mobjects(note)
        self.play(Create(VGroup(axes, axes.axis_labels)), FadeIn(note))
        self.add_fixed_orientation_mobjects(viewpoint)
        self.play(Create(VGroup(viewpoint, lights)))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text('视点所在的主光轴穿过照片的正中心（除非照片裁过）',
                               'assets/sounds/part3/2/视点所在.wav')
        self.subtitle.disappear()
        self.play(FadeOut(note))
        self.subtitle.set_text('视点到照片的距离，我们称为像素焦距，记为 $z$，单位为像素',
                               'assets/sounds/part3/2/视点到.wav', block=False)
        self.play(Create(z_line))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.disappear()
        self.play(FadeOut(z_line))
        self.wait()

        star1, star2 = photo_simplified.stars[0:2]
        star1: Star  # 你 PyCharm 类型判不出来了
        star2: Star
        light1, light2 = lights[0:2]
        light1: Line
        light2: Line
        light_vec = Line(star1.get_center(), viewpoint.get_center(), color=YELLOW).add_tip()
        light_vec.rotate(PI / 2, light_vec.get_end() - light_vec.get_start())
        theta = AngleMark3D(viewpoint, light2, light1, r'\theta')
        ab = (MathTex(r'\boldsymbol a = (x_1, y_1, z), \boldsymbol b = (x_2, y_2, z)')
              .next_to(self.title, DOWN, aligned_edge=LEFT))

        self.subtitle.set_text('怎么求出像素焦距呢？', 'assets/sounds/part3/2/怎么求出.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('对于一颗照片上位于 $(x, y)$ 的星星来说，其星光的方向向量为 $(x, y, z)$',
                               'assets/sounds/part3/2/对于一颗.wav', block=False)
        self.play(FadeOut(lights[1:]), star1.animate.set_color(YELLOW))
        self.play(Create(light_vec))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.disappear()
        self.play(FadeOut(light_vec))
        self.subtitle.set_text(r'选取两颗星星 $(x_1, y_1)$ 和 $(x_2, y_2)$，'
                               r'它们星光 $\boldsymbol a, \boldsymbol b$ 之间的夹角应该就是刚才计算出来的理论夹角 $\theta$',
                               'assets/sounds/part3/2/选取两颗.wav', block=False)
        self.add_fixed_in_frame_mobjects(ab)
        self.play(star2.animate.set_color(YELLOW), Create(light2), Write(ab, run_time=2))
        self.add_fixed_orientation_mobjects(theta.label)
        self.play(Create(theta))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(1)

        original = WithBackground(MathTex(
            r'\cos\theta = \frac{\boldsymbol a \cdot \boldsymbol b}{|\boldsymbol a| |\boldsymbol b|}'
        ))
        substituted = MathTex(
            r'\cos\theta = \frac{x_1 x_2 + y_1 y_2 + z^2}{\sqrt{x_1^2 + y_1^2 + z^2} \sqrt{x_2^2 + y_2^2 + z^2}}'
        )
        changed = MathTex(
            r'\cos\theta = \frac{t + x_1 x_2 + y_1 y_2}{\sqrt{t + x_1^2 + y_1^2} \sqrt{t + x_2^2 + y_2^2}}'
        )
        let_t = Tex(r'令 $z^2 = t$', font_size=DEFAULT_FONT_SIZE).to_edge(LEFT)
        squared = MathTex(
            r'\cos^2\theta = \frac{\left(t + x_1 x_2 + y_1 y_2\right)^2}'
            r'{\left(t + x_1^2 + y_1^2\right) \left(t + x_2^2 + y_2^2\right)}'
        )
        collected_step1 = MathTex(
            r'\left(t + x_1^2 + y_1^2\right) \left(t + x_2^2 + y_2^2\right) \cos^2\theta '
            r'= \left(t + x_1 x_2 + y_1 y_2\right)^2'
        )
        collected_step2 = MathTex(
            r'\left(t + x_1^2 + y_1^2\right) \left(t + x_2^2 + y_2^2\right) \cos^2\theta '
            r'- \left(t + x_1 x_2 + y_1 y_2\right)^2 = 0'
        )
        collected_step3 = MathTex(
            r't^2 \cos^2\theta - t^2 + t x_1^2 \cos^2\theta - 2 t x_1 x_2 + t x_2^2 \cos^2\theta + ty_1^2\cos^2\theta\\'
            r'- 2 t y_1 y_2 + t y_2^2 \cos^2\theta + x_1^2 x_2^2 \cos^2\theta - x_1^2 x_2^2 + x_1^2 y_2^2\cos^2\theta\\'
            r'- 2 x_1 x_2 y_1 y_2 + x_2^2 y_1^2 \cos^2\theta + y_1^2 y_2^2 \cos^2\theta - y_1^2 y_2^2 = 0',
            tex_environment='gather*'
        )
        collected_step4 = MathTex(
            r'\left(\cos^2\theta - 1\right) t^2 \\'
            r'+ \left(x_1^2 \cos^2\theta - 2 x_1 x_2 + x_2^2 \cos^2\theta + y_1^2 \cos^2\theta - 2 y_1 y_2 '
            r'+ y_2^2 \cos^2\theta\right) t \\'
            r'+ x_1^2 x_2^2 \cos^2\theta - x_1^2 x_2^2 + x_1^2 y_2^2 \cos^2\theta - 2 x_1 x_2 y_1 y_2 '
            r'+ x_2^2 y_1^2 \cos^2\theta \\'
            r'+ y_1^2 y_2^2 \cos^2\theta - y_1^2 y_2^2 = 0',
            tex_environment='gather*'
        )
        collected_step5 = MathTex(
            r'\left(\cos^2\theta - 1\right) t^2 \\'
            r'+ \left[\left(x_1^2 + x_2^2 + y_1^2 + y_2^2\right)\cos^2\theta - 2\left(x_1x_2 + y_1y_2\right)\right]t \\'
            r'+ \left(x_1^2 + y_1^2\right)\left(x_2^2 + y_2^2\right) - \left(x_1x_2 + y_1y_2\right)^2 = 0',
            tex_environment='gather*'
        )
        # sympy 不支持继续化简了，手动算了这一步，没想到还挺漂亮的
        # 后来发现，此式在
        # https://github.com/BengbuGuards/StarLocator/blob/main/prototype/core/positioning/find_z/methods/bi_mean.py
        # 中亦有记载

        self.subtitle.set_text('由此，我们可以列出方程', 'assets/sounds/part3/2/由此.wav')
        self.subtitle.pause()
        self.add_fixed_in_frame_mobjects(original)
        self.play(Write(original, run_time=2))
        self.wait()
        self.play(FadeOut(axes, axes.axis_labels, viewpoint, photo_simplified, light1, light2, theta))
        self.move_camera(0, -PI / 2, 0, frame_center=ORIGIN)
        self.play(ReplacementTransform(original.mobj, substituted))
        self.remove(original.background)
        self.wait(3)
        self.subtitle.set_text('这个方程乍看上去很吓人啊，以至于我去年都没解出来，润去用二分法了',
                               'assets/sounds/part3/2/这个方程.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('但其实，只要换个元，令 $z^2 = t$', 'assets/sounds/part3/2/但其实.wav', block=False)
        self.play(Write(let_t, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.play(ReplacementTransform(substituted, changed))
        self.wait(3)
        self.subtitle.set_text('两边平方一下', 'assets/sounds/part3/2/两边平方.wav')
        self.subtitle.pause(1)
        self.play(FadeOut(let_t), ReplacementTransform(changed, squared))
        self.wait(3)
        self.subtitle.set_text('看出来了吗？这实际上就是一个一元二次方程', 'assets/sounds/part3/2/看出来了.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('让我们把它再整理一下', 'assets/sounds/part3/2/让我们.wav')
        self.subtitle.pause(1)
        self.play(ReplacementTransform(squared, collected_step1))
        self.wait(3)
        self.play(ReplacementTransform(collected_step1, collected_step2))
        self.wait(3)
        self.play(ReplacementTransform(collected_step2, collected_step3))
        self.wait(3)
        self.play(ReplacementTransform(collected_step3, collected_step4))
        self.wait(3)
        self.play(ReplacementTransform(collected_step4, collected_step5))
        self.wait(3)
        self.subtitle.set_text('这式子漂不漂亮？这式子太漂亮了！', 'assets/sounds/part3/2/这式子.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('代入求根公式，就可以解得 $t$', 'assets/sounds/part3/2/代入求根.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('这里，有时 $t$ 的两根为一正一负，取正的即可', 'assets/sounds/part3/2/这里有时.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('但在某些情况下，你会得到两个 $t$ 的正根', 'assets/sounds/part3/2/但在某些.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('为什么会这样呢？这时候又该取哪个 $t$ 呢？', 'assets/sounds/part3/2/为什么会.wav')
        self.subtitle.pause(1)
        self.play(FadeOut(ab, collected_step5))
        self.wait()

        class Updater:
            def __init__(self, star: Star, light: Line):
                """根据给出的星星和线构造一个更新函数，让线跟随视点移动"""
                self.star = star
                self.light = light

            def __call__(self, *args, **kwargs):
                self.light.become(Line(viewpoint.get_center(), self.star.get_center(), stroke_width=1)
                                  .scale(10, about_point=viewpoint.get_center()))

        updater1 = Updater(star1, light1)
        updater2 = Updater(star2, light2)
        updater = lambda _: (updater1(_), updater2(_))

        star1.set_color(WHITE)
        star2.set_color(WHITE)

        self.subtitle.set_text('这就要回到图上来解释了', 'assets/sounds/part3/2/这就要.wav', block=False)
        self.move_camera(60 * DEGREES, 30 * DEGREES, 120 * DEGREES, frame_center=(0, 0, z / 2))
        self.play(FadeIn(axes, axes.axis_labels, photo_simplified))
        self.subtitle.pause(1)
        self.subtitle.set_text('现在我们不知道 $z$ 是多少', 'assets/sounds/part3/2/现在我们.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('尝试取一个 $z$，这时候将视点与星星连线，形成的夹角称为尝试夹角',
                               'assets/sounds/part3/2/尝试取一个.wav', block=False)
        self.play(Create(viewpoint))
        self.play(star1.animate.set_color(YELLOW), star2.animate.set_color(YELLOW),
                  Create(VGroup(light1, light2)))
        self.add_fixed_orientation_mobjects(theta.label)
        self.play(Create(theta))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(1)
        self.subtitle.set_text(
            '对于两个不同象限内的星星，尝试夹角随着 $z$ 的增大而减小（在高中，我们说尝试夹角关于 $z$ 单调递减）',
            'assets/sounds/part3/2/对于两个.wav', block=False)
        viewpoint.add_updater(updater)
        theta.start_updater()
        self.play(viewpoint.animate.move_to(ORIGIN))
        self.wait()
        self.play(viewpoint.animate.shift(OUT * 6), run_time=10, rate_func=linear)
        viewpoint.remove_updater(updater)
        theta.stop_updater()
        self.subtitle.pause(1)
        self.play(FadeOut(viewpoint, light1, light2, theta),
                  star1.animate.set_color(WHITE), star2.animate.set_color(WHITE))
        self.wait()

        star3, star4 = photo_simplified.stars[2], photo_simplified.stars[4]
        light3, light4 = lights[2], lights[4]
        theta = AngleMark3D(viewpoint, light4, light3, r'\theta')
        updater3 = Updater(star3, light3)
        updater4 = Updater(star4, light4)
        updater = lambda _: (updater3(_), updater4(_))
        img = ImageMobject('assets/img/monotonicity.jpg').scale_to_fit_height(5)

        self.subtitle.set_text('而对于两个相同象限内的星星，尝试夹角随着 $z$ 的增大先增大后减小',
                               'assets/sounds/part3/2/而对于.wav', block=False)
        viewpoint.move_to(ORIGIN)
        updater(viewpoint)
        theta.updater(theta)
        self.play(star3.animate.set_color(YELLOW), star4.animate.set_color(YELLOW),
                  Create(VGroup(viewpoint, light3, light4)))
        self.add_fixed_orientation_mobjects(theta.label)
        self.play(Create(theta))
        self.wait()
        viewpoint.add_updater(updater)
        theta.start_updater()
        self.play(viewpoint.animate.shift(OUT * 6), run_time=10, rate_func=linear)
        viewpoint.remove_updater(updater)
        theta.stop_updater()
        self.subtitle.pause(1)
        self.subtitle.set_text('这就会导致在增区间也存在一个 $z$，使该位置的尝试夹角等于理论夹角',
                               'assets/sounds/part3/2/这就会.wav', block=False)
        self.add_fixed_in_frame_mobjects(img)
        self.play(FadeIn(img))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text('很显然，我们要的是较大的那个', 'assets/sounds/part3/2/很显然.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('所以如果你得到了两个 $t$ 的正根，取较大的那个', 'assets/sounds/part3/2/所以如果.wav')
        self.subtitle.pause(1)
        self.play(FadeOut(img, axes, axes.axis_labels, photo_simplified, viewpoint, light3, light4, theta))
        self.move_camera(0, -PI / 2, 0, frame_center=ORIGIN)
        self.subtitle.set_text('最后，细节决定成败', 'assets/sounds/part3/2/最后细节.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('不要忘了将 $t$ 开方得到的才是 $z$！',
                               'assets/sounds/part3/2/不要忘了.wav', block=False)
        self.play(FadeIn(let_t.center()))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(3)
        self.play(FadeOut(self.title, let_t))
        self.wait()
