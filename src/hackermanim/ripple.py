from manim import Mobject, AnimationGroup, ParametricFunction, np, PI, UP, MoveAlongPath
from typing import Iterable

def ripple(mobjects: Iterable[Mobject], scale=0.1, t_range=[0, 1], center_correction=None) -> AnimationGroup:
    curve = ParametricFunction(lambda t: np.array([0, scale * np.sin(PI * t), 0]), t_range=t_range)
    anims = []
    for char in mobjects:
        center_correction = center_correction or 0.05 * UP
        curve = curve.copy().move_to(char.get_center() + center_correction)
        anims.append(MoveAlongPath(char, curve))
    return AnimationGroup(*anims, lag_ratio=0.1)
