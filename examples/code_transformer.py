from manim import *
from hackermanim import CodeTransformer

class Sc(Scene):
    def construct(self):
        # The primary way of using this transformer is to have some starting code
        tfmr = CodeTransformer('let a = 1;', language = 'rust')

        # Ingest the code in the next frame
        tfmr.ingest(Code(code='let b = 2;', language='rust'))

        # Write the starting code
        self.play(tfmr.writes())

        # Unwrite the differing pieces
        self.play(tfmr.unwrites())

        # Transform the common parts for proper positioning
        self.play(tfmr.transforms())

        # Rewrite the code from the next frame
        self.play(tfmr.rewrites())

        # You can either pass in a Code object or a raw string with the language
        # The code object has the advantage that you can move it around with the
        # shift method like so
        tfmr.ingest(Code(code='let c: Box<dyn Lol> = Box::new(Lol::new());', language='rust').shift(2 * UP))

        # If you want to perform a different animation during the unwrites
        # you can access the differing code pieces using the unwritables method

        # Here, instead of the unwrite animation, we're using a FadeOut
        self.play(FadeOut(x) for x in tfmr.unwritables())

        # You can also access the respective pieces of code to be transformed
        # or rewritten using the transformables and rewritables methods

        print(tfmr.transformables())
        print('rewritables', tfmr.rewrites())
        self.play(tfmr.transforms())
        self.play(tfmr.rewrites())

# If in a notebook, uncomment the following to render the scene:
# %manim -ql -v WARNING Sc
