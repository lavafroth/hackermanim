from manim import Paragraph, Text

class MonoText(Text):
    font = "monospace"
    def __init__(self, *args, **kwargs):
        if kwargs.get('font') and kwargs['font'] == '':
            kwargs['font'] = MonoText.font
        super().__init__(*args, **kwargs)

class MonoParagraph(Paragraph):
    font = "monospace"
    def __init__(self, *args, **kwargs):
        if kwargs.get('font') and kwargs['font'] == '':
            kwargs['font'] = MonoParagraph.font
        super().__init__(*args, **kwargs)
