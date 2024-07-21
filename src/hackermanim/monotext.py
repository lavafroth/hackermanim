from manim import Paragraph, Text

class MonoText(Text):
    font = "monospace"
    def __init__(self, *args, **kwargs):
        if kwargs['font']:
            raise ValueError('MonoText font is not supposed to be set during instantiation')
        super().__init__(*args, **kwargs, font=MonoText.font)

    @classmethod
    def set_font(cls, font: str):
        cls.font = font

class MonoParagraph(Paragraph):
    font = "monospace"
    def __init__(self, *args, **kwargs):
        if kwargs['font']:
            raise ValueError('MonoParagraph font is not supposed to be set during instantiation')
        super().__init__(*args, **kwargs, font=MonoParagraph.font)

    @classmethod
    def set_font(cls, font: str):
        cls.font = font
