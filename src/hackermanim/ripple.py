from manim import Mobject, AnimationGroup, ParametricFunction, np, PI, UP, MoveAlongPath
from typing import Iterable

def ripple(mobjects: Iterable[Mobject], center_correction=None) -> AnimationGroup:
    curve = ParametricFunction(lambda t: np.array([0, 0.1 * np.sin(PI * t), 0]), t_range=[0, 1])
    anims = []
    for char in mobjects:
        center_correction = center_correction or 0.05 * UP
        curve = curve.copy().move_to(char.get_center() + center_correction)
        anims.append(MoveAlongPath(char, curve))
    return AnimationGroup(*anims)
