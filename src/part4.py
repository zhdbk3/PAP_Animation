#
# Created by MC着火的冰块(zhdbk3) on 2025/2/2
#

from manim import *
import numpy as np

from config import *
from mobj import *
from utils import all_points_of_lines_intersection

# 数据来自 https://github.com/zhdbk3/PhotoAstrologicalPositioning/blob/main/src/get_zenith.py
# 需修改（加个 print）
# 这些坐标是以左上角为原点的
lines = [
    [(1088, 934), (1299, 1285)],
    [(902, 1383), (996, 1732)],
    [(1022, 1096), (1177, 1445)],
    [(983, 1188), (1174, 1686)],
    [(1161, 1288), (1287, 1546)],
    [(1117, 874), (1299, 1145)],
    [(221, 739), (272, 619)],
    [(569, 146), (616, 319)],
    [(1049, 968), (1223, 1295)],
    [(980, 1560), (1028, 1729)],
    [(1038, 1131), (1299, 1717)],
    [(853, 1517), (899, 1732)],
    [(1003, 1143), (1135, 1456)],
    [(957, 407), (1133, 572)],
    [(0, 1258), (140, 928)],
    [(854, 1524), (898, 1732)],
    [(402, 348), (476, 156)],
    [(1125, 1216), (1151, 1269)],
    [(918, 1343), (964, 1502)],
    [(36, 1300), (92, 1153)],
    [(1030, 1623), (1064, 1732)],
    [(1067, 1000), (1299, 1436)],
    [(1195, 1356), (1299, 1569)],
    [(1084, 1339), (1223, 1668)],
    [(1021, 1097), (1090, 1252)],
    [(0, 868), (96, 714)],
    [(1178, 964), (1299, 1143)],
    [(936, 1311), (976, 1448)],
    [(1043, 959), (1137, 1135)],
    [(982, 1184), (1035, 1322)],
    [(1039, 1039), (1154, 1275)],
    [(1120, 881), (1189, 983)],
    [(221, 410), (355, 239)],
    [(713, 178), (840, 296)],
    [(968, 1244), (1018, 1391)],
    [(968, 1243), (1019, 1391)],
    [(1145, 1486), (1249, 1732)],
    [(1142, 802), (1287, 988)],
    [(1064, 1517), (1138, 1732)],
    [(1004, 1142), (1057, 1268)],
    [(301, 348), (346, 282)],
    [(1166, 834), (1299, 1005)],
    [(573, 147), (621, 315)],
    [(1173, 727), (1298, 866)],
    [(20, 1213), (146, 916)],
    [(0, 871), (94, 720)],
    [(1032, 1622), (1065, 1731)],
    [(905, 1398), (994, 1731)],
    [(797, 597), (837, 687)],
    [(311, 367), (381, 256)],
    [(258, 361), (424, 149)],
    [(1109, 1521), (1175, 1693)],
    [(1216, 777), (1299, 869)],
    [(254, 419), (367, 251)],
    [(1042, 1047), (1114, 1194)],
    [(896, 480), (987, 600)],
    [(2, 788), (84, 671)],
    [(1087, 935), (1199, 1121)],
    [(533, 447), (533, 392)],
    [(1236, 1316), (1299, 1434)],
    [(319, 325), (460, 116)],
    [(611, 139), (796, 448)],
    [(682, 176), (787, 293)],
    [(999, 1233), (1173, 1686)],
    [(880, 399), (999, 531)],
    [(652, 251), (696, 341)],
    [(948, 1349), (981, 1463)],
    [(580, 158), (605, 244)],
    [(716, 182), (799, 259)],
    [(882, 400), (979, 508)],
    [(1003, 1636), (1026, 1719)],
    [(1184, 975), (1299, 1146)],
    [(328, 338), (452, 139)],
    [(695, 160), (823, 280)],
    [(968, 1248), (999, 1338)],
    [(0, 1392), (31, 1311)],
    [(1210, 645), (1299, 728)],
    [(1216, 1528), (1299, 1714)],
    [(906, 984), (927, 1041)],
    [(269, 350), (308, 300)],
    [(646, 260), (676, 328)],
    [(730, 410), (770, 492)],
    [(934, 1308), (955, 1380)],
    [(2, 693), (54, 627)],
    [(1024, 1195), (1151, 1496)],
    [(0, 1256), (123, 966)],
    [(389, 346), (468, 160)],
    [(811, 800), (840, 883)],
    [(1192, 1599), (1248, 1732)],
    [(922, 1359), (963, 1502)],
    [(1075, 1547), (1138, 1730)],
    [(688, 416), (714, 484)],
    [(620, 256), (642, 319)],
    [(871, 969), (895, 1039)],
    [(1115, 870), (1296, 1138)],
    [(106, 698), (170, 595)],
    [(421, 302), (447, 233)],
    [(896, 481), (961, 567)],
    [(1063, 1518), (1095, 1610)],
    [(82, 672), (118, 619)],
    [(1, 793), (70, 688)],
    [(579, 131), (605, 200)],
    [(633, 195), (698, 316)],
    [(1196, 752), (1261, 824)],
    [(562, 151), (588, 274)],
    [(1010, 1658), (1029, 1728)],
    [(136, 1039), (162, 972)],
    [(48, 790), (90, 722)],
    [(1211, 644), (1273, 702)],
    [(591, 174), (611, 232)],
    [(1200, 759), (1297, 866)],
    [(624, 228), (662, 319)],
    [(1156, 819), (1231, 915)],
    [(906, 1400), (995, 1732)],
    [(1236, 925), (1299, 1006)],
    [(1036, 1325), (1103, 1499)],
    [(1087, 934), (1298, 1285)],
    [(312, 365), (408, 211)],
    [(562, 145), (576, 209)],
    [(265, 703), (316, 572)],
    [(37, 1294), (71, 1205)],
    [(268, 348), (345, 249)],
    [(907, 562), (964, 649)],
    [(1000, 1135), (1086, 1338)],
    [(1243, 1452), (1299, 1567)],
    [(854, 1528), (897, 1732)],
    [(1021, 1096), (1139, 1361)],
    [(853, 660), (884, 724)],
    [(0, 694), (71, 603)],
    [(635, 140), (695, 220)],
    [(896, 351), (946, 396)],
    [(1232, 666), (1297, 727)],
    [(0, 1260), (132, 948)],
    [(1200, 1365), (1230, 1426)],
    [(720, 220), (823, 334)],
    [(962, 411), (1053, 496)],
    [(808, 672), (831, 727)],
    [(1063, 995), (1165, 1187)],
    [(1088, 933), (1299, 1284)],
    [(414, 314), (466, 179)],
    [(892, 1028), (911, 1084)],
    [(577, 132), (621, 260)],
    [(795, 592), (834, 680)],
    [(485, 121), (510, 62)],
]


# # 该函数来自
# # https://github.com/BengbuGuards/StarLocator/blob/main/prototype/core/positioning/top_point/methods/median2.py
# def intersection(lines: list) -> tuple:
#     """
#     Find the intersection point of given lines.
#     params:
#         lines: numpy array, each row contains two points. [((x1, y1), (x2, y2)), ...]
#     return:
#         intersection point (x, y)
#     """
#     ## 计算每两条线的交点
#     points = all_points_of_lines_intersection(lines)
#
#     points = np.array(points, dtype=np.float32)
#     ## 剔除2倍标准差之外的点
#     points = points[
#         np.abs(points[:, 0] - np.mean(points[:, 0])) < 2 * np.std(points[:, 0])
#         ]
#     points = points[
#         np.abs(points[:, 1] - np.mean(points[:, 1])) < 2 * np.std(points[:, 1])
#         ]
#     ## 计算中位数交点
#     point = np.median(points, axis=0)
#     return point


class Part4(ThreeDScene):
    title: Tex
    subtitle: Subtitle

    def construct(self):
        load_config()

        self.subtitle = Subtitle(self)

        self.begin()
        self.part41()
        self.part42()

    def begin(self) -> None:
        big_title = Tex('4. 天顶位置确定与天顶角', font_size=DEFAULT_FONT_SIZE)
        self.title = Tex('4. 天顶位置确定与天顶角').to_corner(UL)

        self.play(Write(big_title, run_time=2))
        self.wait(2)
        self.play(ReplacementTransform(big_title, self.title))
        self.add_fixed_in_frame_mobjects(self.title)
        self.wait()

    def part41(self) -> None:
        """4.1 天顶位置确定"""
        photo = ImageMobject('assets/img/photo.jpg').scale_to_fit_height(6)
        photo_zenith = ImageMobject('assets/img/zenith.jpg').scale_to_fit_height(6)
        matrix_inverse = ImageMobject('assets/img/matrix_inverse.png').scale_to_fit_height(6)
        algorithm_list = ImageMobject('assets/img/algorithm_list.png').scale_to_fit_height(6)
        rect = Rectangle(RED, 0.8, 9, stroke_width=8).shift(UP * 0.4)

        self.play(FadeIn(photo))
        self.subtitle.set_text('根据透视原理，一张照片上的平行线必将交汇于一点', 'assets/sounds/part4/1/根据透视.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('我们让这张照片上的铅垂线都交汇于一点，这个点就是天顶',
                               'assets/sounds/part4/1/我们让.wav', block=False)
        self.play(FadeIn(photo_zenith))
        self.remove(photo)
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text('但是，直线这么多，误差又不可避免，怎么确定到底取哪里呢？',
                               'assets/sounds/part4/1/但是直线.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('诶，我们可以用这个矩阵伪逆算法', 'assets/sounds/part4/1/诶我们.wav', block=False)
        self.play(FadeIn(matrix_inverse))
        self.remove(photo_zenith)
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text('这时候就有观众要问了', 'assets/sounds/part4/1/这时候.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('主播主播，你的矩阵伪逆确实很强（并不是我的，这里为套公式需要）',
                               'assets/sounds/part4/1/主播主播.wav')
        self.subtitle.set_text('但还是太吃操作了（指需要线代知识）', 'assets/sounds/part4/1/但还是.wav')
        self.subtitle.set_text('有没有更加简单又强势的算法推荐一下吗', 'assets/sounds/part4/1/有没有.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('有的兄弟，有的', 'assets/sounds/part4/1/有的兄弟.wav')
        self.subtitle.pause()
        self.subtitle.set_text('这么强的算法当然是不止一个了，一共有 6 位',
                               'assets/sounds/part4/1/这么强的.wav', block=False)
        self.play(FadeIn(algorithm_list))
        self.remove(matrix_inverse)
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.subtitle.set_text('这里给大家推荐初中生也能轻松掌握，且精度不错的中位数 2 算法',
                               'assets/sounds/part4/1/这里给大家.wav', block=False)
        self.play(Create(rect))
        self.wait(self.subtitle.duration - 1)
        self.subtitle.pause(1)
        self.play(FadeOut(algorithm_list, rect))
        self.wait(1)

        def ul_origin_to_center_origin(coord: tuple[float, float]) -> tuple[float, float]:
            """
            ul: up left
            将照片上以左上角为原点的坐标转化为以中心为原点的坐标
            """
            x, y = coord
            x -= PHOTO_WIDTH / 2
            y -= PHOTO_HEIGHT / 2
            return x, y

        points = all_points_of_lines_intersection(lines)
        # 转换原点
        points = list(map(ul_origin_to_center_origin, points))
        points = np.array(points, dtype=np.float32)
        points_text = Text(str(points), font='Consolas').next_to(self.title, DOWN, aligned_edge=LEFT)
        x_mean = np.mean(points[:, 0])
        y_mean = np.mean(points[:, 1])
        x_std = np.std(points[:, 0])
        y_std = np.std(points[:, 1])
        statistics = MathTex(r'\begin{matrix}'
                             r'\overline{x} = %s & \sigma_x = %s \\'
                             r'\overline{y} = %s & \sigma_y = %s'
                             r'\end{matrix}' % (x_mean, x_std, y_mean, y_std)
                             ).next_to(points_text, RIGHT, aligned_edge=UP)

        self.subtitle.set_text('首先，画出所有的直线，两两计算它们的交点',
                               'assets/sounds/part4/1/首先画出.wav', block=False)
        self.play(Write(points_text, run_time=3))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(1)
        self.subtitle.set_text(
            r'然后，对于横坐标和纵坐标，我们分别计算它们的平均值和标准差（标准差就是方差的算术平方根，记作 $\sigma$）',
            'assets/sounds/part4/1/然后对于.wav', block=False)
        self.play(Write(statistics, run_time=4))
        self.wait(self.subtitle.duration - 4)
        self.subtitle.pause(1)

        # 剔除2倍标准差之外的点
        old = points.copy()
        points = points[np.abs(points[:, 0] - x_mean) < 2 * x_std]
        points = points[np.abs(points[:, 1] - y_mean) < 2 * y_std]
        xy_range = MathTex(r'\begin{matrix}'
                           r'\overline{x} - 2\sigma_x \le x \le \overline{x} + 2\sigma_x \\'
                           r'\overline{y} - 2\sigma_y \le y \le \overline{y} + 2\sigma_y'
                           r'\end{matrix}').next_to(statistics, DOWN)
        # 显示移除的点
        removed = np.array([i for i in old if i not in points])
        np.set_printoptions(threshold=10)  # 缩略显示
        removed_text = Text(str(removed), font='Consolas').next_to(points_text, DOWN, aligned_edge=LEFT)
        # 计算中位数交点
        point = np.median(points, axis=0)
        zenith = tuple(map(float, point))
        zenith_text = MathTex(str(zenith))

        self.subtitle.set_text('排除掉所有横坐标或纵坐标与平均值相差大于两倍标准差的离谱的数据',
                               'assets/sounds/part4/1/排除掉.wav', block=False)
        self.play(Write(xy_range, run_time=3), Succession(
            TransformFromCopy(points_text, removed_text),
            Animation(Mobject()),  # 没有动画，占位 1 秒
            Uncreate(removed_text)))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(1)
        self.subtitle.set_text('对于留下来的数据，分别取它们的中位数',
                               'assets/sounds/part4/1/对于留下.wav', block=False)
        self.play(Write(zenith_text, run_time=2))
        self.wait(self.subtitle.duration - 2)
        self.subtitle.pause(1)
        self.subtitle.set_text('这样就能得到一个较精确的坐标，我们把它作为天顶的坐标',
                               'assets/sounds/part4/1/这样就能.wav')
        self.subtitle.pause(3)
        self.play(FadeOut(points_text, statistics, zenith_text, xy_range))
        self.wait()

    def part42(self) -> None:
        """4.2 天顶角"""
        # 这里和 part3.Part3.part32 开头是差不多的
        axes = ThreeDAxes(z_range=(-7, 7, 1), z_length=14)
        axes.y_axis.scale(-1)
        y_label = axes.get_axis_labels()[1]
        y_label.shift(DOWN * 2 * y_label.get_y())
        photo_img = ImageMobject('assets/img/zenith.jpg').scale_to_fit_height(6)
        photo_simplified = PhotoSimplified(has_zenith=True).scale_to_fit_height(6, about_point=ORIGIN)
        z = photo_simplified.width
        viewpoint = Dot(OUT * z)
        zenith_line = (Line(viewpoint.get_center(), photo_simplified.zenith.get_center(), stroke_width=1, color=YELLOW)
                       .scale(10, about_point=viewpoint.get_center()))
        lights = VGroup(*[Line(viewpoint.get_center(), i.get_center(), stroke_width=1)
                        .scale(10, about_point=viewpoint.get_center())
                          for i in photo_simplified.stars])
        formula = MathTex(r'\theta = \arccos\left(\frac{\boldsymbol a \cdot \boldsymbol b}'
                          r'{|\boldsymbol a| |\boldsymbol b|}\right)').next_to(self.title, DOWN, aligned_edge=LEFT)

        self.play(FadeIn(photo_img))
        self.wait()
        self.subtitle.set_text('现在，我们已经知道了照片上各星星的位置、天顶位置与像素焦距',
                               'assets/sounds/part4/2/现在我们.wav', block=False)
        self.play(Create(photo_simplified, run_time=2))
        self.play(FadeOut(photo_img))
        self.move_camera(60 * DEGREES, 30 * DEGREES, 120 * DEGREES, frame_center=(0, 0, z / 2))
        self.add_fixed_orientation_mobjects(viewpoint)
        self.play(Create(VGroup(axes, axes.axis_labels, viewpoint)))
        self.subtitle.pause(1)
        self.subtitle.set_text('还是用老方法，就可以算出每颗星星的天顶角',
                               'assets/sounds/part4/2/还是用.wav', block=False)
        self.play(Create(VGroup(zenith_line, lights)))
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula, run_time=2))
        self.wait(self.subtitle.duration - 3)
        self.subtitle.pause(3)
        self.subtitle.set_text('回顾一下，我们已经得到了每颗星星的 GP 和天顶角', 'assets/sounds/part4/2/回顾一下.wav')
        self.subtitle.pause(1)
        self.subtitle.set_text('那么现在，就万事俱备，只欠东风了', 'assets/sounds/part4/2/那么现在.wav')
        self.subtitle.pause(1)
        self.play(FadeOut(axes, axes.axis_labels, photo_simplified,
                          viewpoint, zenith_line, lights, formula, self.title))
        self.wait()
