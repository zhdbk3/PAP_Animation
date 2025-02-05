#
# Created by MC着火的冰块(zhdbk3) on 2025/2/1
#

"""
原始方程
\cos\theta = \frac{x_1 x_2 + y_1 y_2 + z^2}{\sqrt{x_1^2 + y_1^2 + z^2} \sqrt{x_2^2 + y_2^2 + z^2}}
令 z^2 = t
\cos\theta = \frac{t + x_1 x_2 + y_1 y_2}{\sqrt{t + x_1^2 + y_1^2} \sqrt{t + x_2^2 + y_2^2}}
两边平方
\cos^2\theta = \frac{\left(t + x_1 x_2 + y_1 y_2\right)^2}{\left(t + x_1^2 + y_1^2\right) \left(t + x_2^2 + y_2^2\right)}
整理为一元二次方程
\left(t + x_1^2 + y_1^2\right) \left(t + x_2^2 + y_2^2\right) \cos^2\theta = \left(t + x_1 x_2 + y_1 y_2\right)^2
\left(t + x_1^2 + y_1^2\right) \left(t + x_2^2 + y_2^2\right) \cos^2\theta - \left(t + x_1 x_2 + y_1 y_2\right)^2 = 0
t^2 \cos^2\theta - t^2 + t x_1^2 \cos^2\theta - 2 t x_1 x_2 + t x_2^2 \cos^2\theta + t y_1^2 \cos^2\theta - 2 t y_1 y_2 + t y_2^2 \cos^2\theta + x_1^2 x_2^2 \cos^2\theta - x_1^2 x_2^2 + x_1^2 y_2^2 \cos^2\theta - 2 x_1 x_2 y_1 y_2 + x_2^2 y_1^2 \cos^2\theta + y_1^2 y_2^2 \cos^2\theta - y_1^2 y_2^2 = 0
t^2 \left(\cos^2\theta - 1\right) + t \left(x_1^2 \cos^2\theta - 2 x_1 x_2 + x_2^2 \cos^2\theta + y_1^2 \cos^2\theta - 2 y_1 y_2 + y_2^2 \cos^2\theta\right) + x_1^2 x_2^2 \cos^2\theta - x_1^2 x_2^2 + x_1^2 y_2^2 \cos^2\theta - 2 x_1 x_2 y_1 y_2 + x_2^2 y_1^2 \cos^2\theta + y_1^2 y_2^2 \cos^2\theta - y_1^2 y_2^2 = 0
解得 t =
\frac{x_1^2 \cos^2\theta - 2 x_1 x_2 + x_2^2 \cos^2\theta + y_1^2 \cos^2\theta - 2 y_1 y_2 + y_2^2 \cos^2\theta + \sqrt{x_1^{4} \cos^2\theta - 4 x_1^{3} x_2 - 2 x_1^2 x_2^2 \cos^2\theta + 8 x_1^2 x_2^2 + 2 x_1^2 y_1^2 \cos^2\theta - 4 x_1^2 y_1 y_2 - 2 x_1^2 y_2^2 \cos^2\theta + 4 x_1^2 y_2^2 - 4 x_1 x_2^{3} - 4 x_1 x_2 y_1^2 + 8 x_1 x_2 y_1 y_2 - 4 x_1 x_2 y_2^2 + x_2^{4} \cos^2\theta - 2 x_2^2 y_1^2 \cos^2\theta + 4 x_2^2 y_1^2 - 4 x_2^2 y_1 y_2 + 2 x_2^2 y_2^2 \cos^2\theta + y_1^{4} \cos^2\theta - 4 y_1^{3} y_2 - 2 y_1^2 y_2^2 \cos^2\theta + 8 y_1^2 y_2^2 - 4 y_1 y_2^{3} + y_2^{4} \cos^2\theta} \cos\theta}{2 \sin^2\theta}
所以 z =
\frac{\sqrt2 \sqrt{\frac{x_1^2 \cos^2\theta - 2 x_1 x_2 + x_2^2 \cos^2\theta + y_1^2 \cos^2\theta - 2 y_1 y_2 + y_2^2 \cos^2\theta + \sqrt{x_1^{4} \cos^2\theta - 4 x_1^{3} x_2 - 2 x_1^2 x_2^2 \cos^2\theta + 8 x_1^2 x_2^2 + 2 x_1^2 y_1^2 \cos^2\theta - 4 x_1^2 y_1 y_2 - 2 x_1^2 y_2^2 \cos^2\theta + 4 x_1^2 y_2^2 - 4 x_1 x_2^{3} - 4 x_1 x_2 y_1^2 + 8 x_1 x_2 y_1 y_2 - 4 x_1 x_2 y_2^2 + x_2^{4} \cos^2\theta - 2 x_2^2 y_1^2 \cos^2\theta + 4 x_2^2 y_1^2 - 4 x_2^2 y_1 y_2 + 2 x_2^2 y_2^2 \cos^2\theta + y_1^{4} \cos^2\theta - 4 y_1^{3} y_2 - 2 y_1^2 y_2^2 \cos^2\theta + 8 y_1^2 y_2^2 - 4 y_1 y_2^{3} + y_2^{4} \cos^2\theta} \cos\theta}{\sin^2\theta}}}2
"""

from sympy import *
from sympy.vector import CoordSys3D, Vector

x1, y1, x2, y2, z, theta = symbols('x1 y1 x2 y2 z theta')
N = CoordSys3D('N')


def vector(x: Expr, y: Expr, z: Expr) -> Vector:
    return x * N.i + y * N.j + z * N.k


def print_simplified_latex(expr: Expr) -> None:
    print(latex(expr).replace(r'{\left(\theta \right)}', r'\theta').replace('{1}', '1').replace('{2}', '2'))


a = vector(x1, y1, z)
b = vector(x2, y2, z)

print('原始方程')
eq = Eq(cos(theta), a.dot(b) / (a.magnitude() * b.magnitude()))
print_simplified_latex(eq)

print('令 z^2 = t')
t = Symbol('t', negative=False)
eq = eq.subs(z ** 2, t)
print_simplified_latex(eq)

print('两边平方')
eq = Eq(eq.lhs ** 2, eq.rhs ** 2)
print_simplified_latex(eq)

print('整理为一元二次方程')
# 去分母
denom = eq.rhs.as_numer_denom()[1]
eq = Eq(eq.lhs * denom, eq.rhs * denom)
print_simplified_latex(eq)
# 移项
eq = Eq(eq.lhs - eq.rhs, 0)
print_simplified_latex(eq)
# 展开
eq = expand(eq)
print_simplified_latex(eq)
# 整理系数
eq = Eq(collect(eq.lhs, t), 0)
print_simplified_latex(eq)

print('解得 t =')
t_solution = solve(eq, t)[1]  # 取较大者（即 +sqrt(delta) 的那个）
t_solution = simplify(t_solution)
print_simplified_latex(t_solution)

print('所以 z =')
print_simplified_latex(simplify(sqrt(t_solution)))
