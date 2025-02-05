#
# Created by MC着火的冰块(zhdbk3) on 2025/1/18
#

from manim import *

from mobj import *
from config import *


class Introduction(Scene):
    subtitle: Subtitle

    def construct(self):
        load_config()

        self.subtitle = Subtitle(self)

        reference = Text('每多一个晚上愿意多抬头仰望星空一会儿的年轻人，\n这个民族就离真正的星辰大海更近一步。',
                         font_size=40).shift(UP)
        author = Text('——鬼蝉', font_size=40).to_edge(RIGHT)
        self.play(Write(reference, run_time=5))
        self.wait()
        self.play(Write(author))
        self.wait(3)
        self.play(FadeOut(reference, author))
        self.wait()

        photo = ImageMobject('assets/img/photo.jpg').scale_to_fit_height(6)
        result = ImageMobject('assets/img/result.png').scale_to_fit_width(10)
        videos = ImageMobject('assets/img/videos.jpeg').scale_to_fit_width(10)
        app = ImageMobject('assets/img/app.jpeg').scale_to_fit_width(10)

        self.subtitle.set_text('照片测星定位，是一种根据照片上的星星、时间、铅垂线等信息，计算出拍摄位置的技术',
                               'assets/sounds/introduction/照片测星定位.wav', block=False)
        self.play(FadeIn(photo))
        self.bring_to_front(self.subtitle.mobj)
        self.wait(3)
        self.play(FadeIn(result))
        self.wait(self.subtitle.duration - 5)
        self.subtitle.pause(2)
        self.subtitle.set_text('如果你还不是很了解它，推荐先看下这些视频',
                               'assets/sounds/introduction/如果你还.wav', block=False)
        self.play(FadeIn(videos))
        self.bring_to_front(self.subtitle.mobj)
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(2)
        self.remove(videos)
        self.add(app)
        self.subtitle.set_text('我们也把它做成了软件，推荐也去看看哦',
                               'assets/sounds/introduction/我们也把.wav')
        self.wait(2)
        self.play(FadeOut(app))
        self.wait()
        self.subtitle.set_text('本期视频将为大家讲解照片测星定位的详细数学原理，初中生也能看懂！',
                               'assets/sounds/introduction/本期视频.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('看完后，你也可以自己定位！', 'assets/sounds/introduction/看完后.wav')
        self.subtitle.pause(2)
        self.play(FadeOut(photo, result))
        self.wait()
