#
# Created by MC着火的冰块(zhdbk3) on 2025/1/20
#

from typing import Self, Optional
import wave

from manim import *
import numpy as np


class AngleMark(VGroup):
    def __init__(self, vertex: np.ndarray | Mobject, initial_side: Line, terminal_side: Line, label: str,
                 r: float | int = 0.55, always_positive: bool = True, add_tip: bool = False):
        """
        一个角的小圆弧标记和名字标记，当角的大小发生变化时，小圆弧和名字会自动调整
        :param vertex: 角的顶点
                       若传入一个坐标，那它就是定点
                       若传入一个 mobj，那顶点会跟随其移动（仅在 AngleMark3D 中实现了）
        :param initial_side: 始边，应指向角延伸的方向
        :param terminal_side: 终边，应指向角延伸的方向
        :param label: 角的名字，应符合 MathTex 语法
        :param r: 小圆弧的半径
        :param always_positive: 是否永远为正角
        :param add_tip: 是否加上表示方向的小箭头
        """
        self.vertex = vertex
        self.initial_side = initial_side
        self.terminal_side = terminal_side
        self.label = MathTex(label)
        self.r = r
        self.always_positive = always_positive
        self.add_tip = add_tip
        self.arc = Arc()
        self.updater(self)
        super().__init__(self.arc, self.label)

    def updater(self, _: Self) -> None:
        """自动调整小圆弧和标签"""
        try:
            # 调整小圆弧
            start_angle = self.initial_side.get_angle()
            end_angle = self.terminal_side.get_angle()
            angle = end_angle - start_angle
            if self.always_positive:
                angle %= TAU
            arc = Arc(self.r, start_angle, angle, arc_center=self.vertex)
            if self.add_tip:
                arc.add_tip(tip_length=0.2, tip_width=0.2 * 2 / 3 * np.sqrt(3))
            self.arc.become(arc)
            # 调整标签
            direction = start_angle + angle / 2
            vec = np.array((np.cos(direction), np.sin(direction), 0))  # 标签相对于圆心的单位方向向量
            self.label.move_to(self.vertex + vec * (self.r + 0.3))
        except ValueError:  # 两线平行时会报此错误
            pass

    def start_updater(self) -> None:
        """开启 updater，较吃性能，及时关闭"""
        self.add_updater(self.updater)

    def stop_updater(self) -> None:
        """关闭 updater"""
        self.remove_updater(self.updater)


class AngleMark3D(AngleMark):
    """一个 3D 场景中的角标，仅实现了用到的功能"""

    def updater(self, _: Self) -> None:
        try:
            if isinstance(self.vertex, Mobject):
                vertex = self.vertex.get_center()
            else:
                vertex = self.vertex
            # 调整小圆弧
            v1 = self.initial_side.end - vertex
            v1 /= np.linalg.norm(v1)
            v2 = self.terminal_side.end - vertex
            v2 /= np.linalg.norm(v2)
            self.arc.become(ArcBetweenPoints(vertex + self.r * v1, vertex + self.r * v2, radius=self.r))
            # 调整标签
            v_m = v1 + v2
            v_m /= np.linalg.norm(v_m)
            self.label.move_to(vertex + (self.r + 0.3) * v_m)
        except ValueError:
            pass

    def start_updater(self) -> None:
        self.add_updater(self.updater)

    def stop_updater(self) -> None:
        self.remove_updater(self.updater)


class WithBackground(VGroup):
    def __init__(self, mobj: Mobject):
        """
        给对象添加一个黑色半透明的背景
        :param mobj: Monject 对象
        """
        self.mobj = mobj
        self.background = Rectangle(BLACK, mobj.height, mobj.width, fill_opacity=0.5, stroke_width=0).move_to(mobj)
        super().__init__(self.background, self.mobj)


class Subtitle:
    def __init__(self, scene: Scene):
        """字幕"""
        self.scene = scene
        self.mobj: WithBackground | None = None
        self.duration = 0  # 音频播放所需的时长

    def disappear(self) -> None:
        """字幕消失"""
        if self.mobj is not None:
            self.scene.remove(self.mobj)
            self.mobj = None
            self.duration = 0

    def set_text(self, text: str, sound_path: Optional[str] = None, block: bool = True) -> None:
        """
        更新字幕，播放音频
        :param text: 符合 Tex 语法的字符串
        :param sound_path: 对应音频的路径，应为 .wav 格式
        :param block: 是否阻塞，等待音频播放完
        :return: None
        """
        self.disappear()
        # 字幕为无衬线体
        self.mobj = WithBackground(Tex(r'\textsf{' + text + '}')).to_edge(DOWN)
        # 显示字幕
        if isinstance(self.scene, ThreeDScene):
            self.scene.add_fixed_in_frame_mobjects(self.mobj)
        else:
            self.scene.add(self.mobj)
        self.scene.bring_to_front(self.mobj)
        # 播放音频（如果有）
        if sound_path is not None:
            self.scene.add_sound(sound_path)
        # 计算需要的世界并等待（如果有）
        self.duration = len(text) / 4 if sound_path is None else self.get_duration(sound_path)
        if block:
            self.scene.wait(self.duration, frozen_frame=False)
            self.scene.remove(self.mobj)

    @staticmethod
    def get_duration(sound_path: str) -> float:
        """
        获取一段音频的时长
        :param sound_path: 音频路径
        :return: 时长秒数
        """
        with wave.open(sound_path) as f:
            f: wave.Wave_read
            return f.getnframes() / f.getframerate()

    def pause(self, t: float = 0.5) -> None:
        """
        两句话中间停顿一小会，会清除已有字幕
        :param t: 停顿秒数
        :return: None
        """
        self.disappear()
        self.scene.wait(t, frozen_frame=False)


PHOTO_WIDTH = 1300
PHOTO_HEIGHT = 1733


class PhotoSimplified(VGroup):
    # 该坐标是以向下为 y 轴正方向的，因此下面需反转 y 坐标
    STARS_COORD = [(-384, -364.5), (44, -130.5), (-97, 97.5), (13, 106.5), (-412, 580.5)]
    ZENITH_COORD = (-117.5, -857.5)

    def __init__(self, has_zenith: bool = False):
        """
        一张简化后的照片
        由于 ImageMobject 不是 VMobject，无法在三维空间中正常显示，故以此作为替代
        :param has_zenith: 是否带有天顶
        """
        rect = Rectangle(WHITE, PHOTO_HEIGHT, PHOTO_WIDTH)
        self.stars = [Star(5, outer_radius=10, color=WHITE).move_to((i[0], -i[1], 0)) for i in self.STARS_COORD]
        super().__init__(rect, *self.stars)
        self.zenith = Dot((self.ZENITH_COORD[0], -self.ZENITH_COORD[1], 0), radius=20, color=YELLOW)
        if has_zenith:
            self.add(self.zenith)


__all__ = ['AngleMark', 'AngleMark3D', 'WithBackground', 'Subtitle', 'PhotoSimplified', 'PHOTO_HEIGHT', 'PHOTO_WIDTH']
