from .model import ContinuityVector
class V1Compatibility:
    @staticmethod
    def epoch_from_v2(cv): return cv.recovery
    @staticmethod
    def deps_for_v1(): return frozenset({"recovery"})
