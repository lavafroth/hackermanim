from manim import VMobject, Code, VGroup, AnimationGroup, Write, Transform, Unwrite, SVGMobject
from dataclasses import dataclass
from typing import Optional, List, Any, Union, Tuple
from difflib import SequenceMatcher
from copy import copy

@dataclass
class CodeVMobjectPair:
    char: str # char but there's no way to express one in Python
    vmobject: Optional[VMobject]

@dataclass
class CodeToVMobjectMapper:
    pairs: List[CodeVMobjectPair]
    
    def __init__(self, code: Code, **kwargs):
        all_vmobjects = []
        for line in code[2]:
            for vmobject in line:
                all_vmobjects.append(vmobject)

        pairs = []

        # pointers to the start of each stack
        i, j = 0, 0
        while i < len(code.code_string) and j < len(all_vmobjects):
            if code.code_string[i] == '\n':
                i += 1
                pairs.append(CodeVMobjectPair(code.code_string[i], None))

            pairs.append(CodeVMobjectPair(code.code_string[i], all_vmobjects[j]))
            i += 1
            j += 1
        
        self.pairs = pairs

    def into_chunks(self, breakpoints: Optional[List[int]] = None) -> 'CodeVMobjectChunks':
        chunks = []
        chunk = []
        token = ""
        breakpoints = breakpoints or [i for i, pair in enumerate(self.pairs) if pair.char.isspace()]
        
        for i, pair in enumerate(self.pairs):
            if i in breakpoints:
                if len(chunk) > 0:
                    chunks.append(CodeVMobjectChunk(token, VGroup(*chunk)))
                    chunk.clear()
                    token = ""
                    
            if pair.vmobject is not None:
                token += pair.char
                chunk.append(pair.vmobject)

        if len(chunk) > 0:
            chunks.append(CodeVMobjectChunk(token, VGroup(*chunk)))

        return CodeVMobjectChunks(chunks)


@dataclass
class RawToVMobjectMapper(CodeToVMobjectMapper):
    def __init__(self, raw, **kwargs):
        code = Code(code=raw, **kwargs)
        super().__init__(code)

@dataclass
class CodeVMobjectChunk:
    token: str
    chunk: VGroup

@dataclass
class CodeVMobjectChunks:
    chunks: List[CodeVMobjectChunk]

    def tokens(self) -> List[str]:
        return [chunk.token for chunk in self.chunks]


@dataclass
class CodeTransformer:
    start: Optional[CodeVMobjectChunks]
    end:   Optional[CodeVMobjectChunks]
    post:  Optional[CodeVMobjectChunks]
    diffs: List[Any]
    lag_ratio: float
    _committed_transformation: bool
    
    def __init__(
        self,
        start: Union[str, Code],
        breakpoints: Optional[List[int]] = None,
        lag_ratio: float = 0.3,
        **kwargs
    ):
        self.start = None
        self.end = None
        self.diffs = []
        if isinstance(start, Code):
            self.post = CodeToVMobjectMapper(start).into_chunks(breakpoints)
        else:
            self.post = RawToVMobjectMapper(start, **kwargs).into_chunks(breakpoints)
        self.lag_ratio = lag_ratio
        self._committed_transformation = False

    def writes(self) -> AnimationGroup:
        return AnimationGroup(
            (Write(chunk) for chunk in self.writables()),
            lag_ratio=self.lag_ratio
        )
    
    def writables(self):
        return [chunk.chunk for chunk in self.start.chunks]

    def unwrites(self) -> AnimationGroup:
        return AnimationGroup(
            (Unwrite(x) for x in self.unwritables()),
            lag_ratio=self.lag_ratio
        )

    def unwritables(self) -> List[VGroup]:
        unwrites = []
        for op, i0, i1, _, _ in self.diffs:
            if op == 'delete' or op == 'replace':
                for x in range(i0, i1):
                    unwrites.append(self.start.chunks[x].chunk)
        return unwrites

    def transformables(self) -> List[Tuple[VGroup, VGroup]]:
        transformables = []
        for op, i0, i1, j0, j1 in self.diffs:
            if op == 'equal':
                for x, y in zip(range(i0, i1), range(j0, j1)):
                    transformables.append((self.start.chunks[x].chunk, self.end.chunks[y].chunk))
                    if not self._committed_transformation:
                        self.post.chunks[y] = self.start.chunks[x]

        self._committed_transformation = True
        return transformables

    def transforms(self) -> AnimationGroup:
        transforms = []
        for (x, y) in self.transformables():
            transforms.append(Transform(x, y))
        return AnimationGroup(transforms)

    def rewritables(self) -> List[VGroup]:
        rewritables = []
        for op, _, _, j0, j1 in self.diffs:
            if op == 'insert' or op == 'replace':
                for x in range(j0, j1):
                    rewritables.append(self.end.chunks[x].chunk)
        return rewritables

    def rewrites(self) -> AnimationGroup:
        return AnimationGroup(
            (Write(x) for x in self.rewritables()),
            lag_ratio=self.lag_ratio
        )

    def ingest(self, end: Union[str, Code], breakpoints: Optional[List[int]] = None, **kwargs):
        self.start = self.post
        if isinstance(end, Code):
            self.end = CodeToVMobjectMapper(end).into_chunks(breakpoints)
        else:
            self.end = RawToVMobjectMapper(end, **kwargs).into_chunks(breakpoints)  
        
        sequence_matcher = SequenceMatcher(None, self.start.tokens(), self.end.tokens())
        self.diffs = list(sequence_matcher.get_opcodes())
        self.post = copy(self.end)
        self._committed_transformation = False


def octicon(name: str, *args, **kwargs) -> SVGMobject:
    from os import path
    return SVGMobject(path.join(path.dirname(__file__), 'octicons', 'icons', name), *args, **kwargs)
