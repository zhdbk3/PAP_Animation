#
# Created by MC着火的冰块(zhdbk3) on 2025/1/22
#

from manim import *


def load_config():
    Text.set_default(font_size=24)
    Tex.set_default(font_size=30,  # Tex 的 30 相当于 Text 的 24
                    tex_template=TexTemplateLibrary.ctex)  # 中文支持


__all__ = ['load_config']
