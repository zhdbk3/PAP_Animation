#
# Created by MC着火的冰块(zhdbk3) on 2025/1/30
#

from manim import *

from mobj import *
from config import *


class Part2(Scene):
    title: Tex
    subtitle: Subtitle

    def construct(self):
        load_config()

        self.subtitle = Subtitle(self)

        self.begin()
        self.part21()
        self.part22()

    def begin(self) -> None:
        big_title = Tex('2. 星星 GP 的确定', font_size=DEFAULT_FONT_SIZE)
        self.title = Tex('2. 星星 GP 的确定').to_corner(UL)

        self.play(Write(big_title, run_time=2))
        self.wait(2)
        self.play(ReplacementTransform(big_title, self.title))
        self.wait()

    def part21(self) -> None:
        """2.1 经纬度的表示"""
        with_direction = Tex(r'(11.4°N, 51.4°E) \qquad (19.19°S, 81.0°W)', font_size=DEFAULT_FONT_SIZE)
        with_sign_1 = Tex(r'(11.4°, 51.4°) \qquad  (-19.19°, -81.0°)',
                          font_size=DEFAULT_FONT_SIZE).next_to(with_direction, DOWN)
        with_sign_2 = Tex(r'(11.4°, 51.4°) \qquad  (-19.19°, 279°)',
                          font_size=DEFAULT_FONT_SIZE).next_to(with_direction, DOWN)
        VGroup(with_direction, with_sign_1, with_sign_2).center()

        self.wait()
        self.subtitle.set_text('在这一切开始之前，我们先看看怎么统一便捷地处理经纬度',
                               'assets/sounds/part2/1/在这一切.wav', block=False)
        self.play(Write(with_direction, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text('纬度分南北，经度分东西，一直带个小尾巴处理那就太麻烦了',
                               'assets/sounds/part2/1/纬度分南北.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('为此，我们规定：北纬为正，南纬为负；东经为正，西经为负',
                               'assets/sounds/part2/1/为此.wav', block=False)
        self.play(TransformFromCopy(with_direction, with_sign_1))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text(r'当然，把西经转到 180°\textasciitilde360° 也是一样的',
                               'assets/sounds/part2/1/当然.wav', block=False)
        self.play(ReplacementTransform(with_sign_1, with_sign_2))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(3)
        self.play(FadeOut(with_direction, with_sign_2))
        self.wait()

    def part22(self) -> None:
        """2.2 时角、赤纬与 GP"""
        stellarium = ImageMobject('assets/img/stellarium.png').scale_to_fit_height(5)
        rectangle = Rectangle(RED, 0.5, 5).shift(DOWN * 2.3)

        self.subtitle.set_text(
            '打开星图软件（如 Stellarium），调好时间，把位置调到 (0°, 0°)，我们可以查询到星星的时角和赤纬',
            'assets/sounds/part2/2/打开星图.wav', block=False)
        self.play(FadeIn(stellarium))
        self.wait()
        self.play(Create(rectangle))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(1)
        self.play(FadeOut(stellarium, rectangle))
        self.wait()

        earth = Sphere(ORIGIN, 2, fill_opacity=0.3).rotate(PI / 2, LEFT)
        n_label = WithBackground(Text('N')).next_to(earth, UP)
        celestial_sphere = Circle(3.5, WHITE)
        equator = DashedLine(LEFT * 3.5, RIGHT * 3.5)
        equator_label = Text('天赤道').next_to(equator)
        # 艹，才发现原来点坐标不用 np.array() 套一下也可以
        star = Star(outer_radius=0.1, color=WHITE).move_to((3.5 * np.cos(1), 3.5 * np.sin(1), 0))
        line = Line(ORIGIN, star.get_center())
        gp = Dot((2 * np.cos(1), 2 * np.sin(1), 0))
        gp_label = Text('GP').next_to(gp)
        lat = AngleMark(ORIGIN, equator, line, r'\phi = \delta')
        lat.label.shift(RIGHT * 0.5)
        formula_lat = WithBackground(MathTex(r'\text{纬度}(\phi) = \text{赤纬}(\delta)',
                                             tex_template=TexTemplateLibrary.ctex)).next_to(self.title, DOWN).set_x(0)

        self.subtitle.set_text('赤纬是纬度在天球上的投影，就等于 GP 的纬度',
                               'assets/sounds/part2/2/赤纬是.wav', block=False)
        self.play(Create(earth), Create(equator), Write(equator_label), Write(n_label),
                  Create(VGroup(celestial_sphere, star, line, gp, gp_label, lat), run_time=2))
        self.bring_to_back(earth)
        self.bring_to_front(self.subtitle.mobj)
        self.wait(self.subtitle.duration - 2)
        self.subtitle.disappear()
        self.play(Write(formula_lat, run_time=2))
        self.wait(5)
        self.play(FadeOut(equator, equator_label, star, line, gp, gp_label, lat, formula_lat))
        self.wait()

        prime_meridian = DashedLine(ORIGIN, RIGHT * 3.5)
        prime_label = Tex('0° 经线').next_to(prime_meridian)
        star = Star(outer_radius=0.1, color=WHITE).move_to((3.5 * np.cos(-PI / 6), 3.5 * np.sin(-PI / 6), 0))
        line = Line(ORIGIN, star.get_center())
        gp = Dot((2 * np.cos(-PI / 6), 2 * np.sin(-PI / 6), 0))
        gp_label = Text('GP').next_to(gp)
        t = AngleMark(ORIGIN, line, prime_meridian, 't')
        lam = AngleMark(ORIGIN, prime_meridian, line, r'\lambda')
        formula_lon = WithBackground(
            MathTex(r'\text{经度}(\lambda) = 360^{\circ} - \text{时角}(t) \times 15^{\circ}/\mathrm{h}',
                    tex_template=TexTemplateLibrary.ctex)).next_to(self.title, DOWN).set_x(0)

        def updater(_: Mobject) -> None:
            """星星缓慢转动"""
            VGroup(star, line, gp).rotate(0.1 * DEGREES, IN, ORIGIN)
            gp_label.next_to(gp)

        self.play(Rotate(VGroup(earth, n_label), PI / 2, RIGHT, ORIGIN, rate_func=smooth),
                  n_label.animate.center())
        self.wait()
        self.subtitle.set_text('时角就等于从你所在的经线向西转到星星 GP 所在的经线，转过的角度',
                               'assets/sounds/part2/2/时角就等于.wav', block=False)
        self.play(Create(prime_meridian), Write(prime_label),
                  Create(VGroup(star, line, gp, gp_label, t, lam), run_time=2))
        star.add_updater(updater)
        t.start_updater()
        lam.start_updater()
        self.wait(self.subtitle.duration - 2, frozen_frame=False)
        self.subtitle.pause(1)
        self.subtitle.set_text('单位用 24 h 划分了一圈，换成角度就是 1 h 15°', 'assets/sounds/part2/2/单位用.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('由于刚才已经站到了 0° 经线上，我们便能得到 GP 经度的计算公式',
                               'assets/sounds/part2/2/由于刚才.wav')
        self.subtitle.pause(1)
        self.play(Write(formula_lon, run_time=2))
        self.wait(5, frozen_frame=False)
        star.remove_updater(updater)
        t.stop_updater()
        lam.stop_updater()
        self.play(FadeOut(earth, celestial_sphere, prime_meridian, prime_label, star, line, gp, gp_label, t,
                          lam, formula_lon, n_label))
        self.wait()

        formula_lon.next_to(formula_lat, DOWN)
        VGroup(formula_lat, formula_lon).center()

        self.subtitle.set_text('这样，我们就可以得到每颗星星的 GP 啦',
                               'assets/sounds/part2/2/这样.wav', block=False)
        self.play(FadeIn(formula_lat, formula_lon))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(5)
        self.play(FadeOut(formula_lat, formula_lon, self.title))
        self.wait()
