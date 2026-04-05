"""
parameters.py

“Global” parameters e_M, e_M1, e_M2, which are stored on a “blackboard”
that can be read and written by independent actors for communication purposes.

The parameters serve as default validity modulation parameters:

"e_M" (modulation of the validities arguments of logical operators)
"e_M1" (modulation of the premise argument of e_VALIDATE and e_INVALIDATE)
"e_M2" (modulation of the current_hypotheses argument of e_VALIDATE and e_INVALIDATE)
"""

import threading


class Blackboard:
    _instance = None
    _lock = threading.Lock()   # For thread-safe singleton generation

    # ---------------------------
    # Singleton control
    # ---------------------------
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    # ---------------------------
    # Initialization (only once!)
    # ---------------------------
    def __init__(self):
        if self._initialized:
            return

        self._state_lock = threading.RLock()  # For thread-safe parameter access

        self._e_M = 0.0
        self._e_M1 = 0.0
        self._e_M2 = 0.0

        self._initialized = True

    # ----------------------------------------------------
    # Check the validity of the assigned parameter values.
    # ----------------------------------------------------
    @staticmethod
    def _validate_range(value: float, name: str) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be numeric, got {type(value)}")

        if value < -1.0 or value > 1.0:
            raise ValueError(f"{name} must be within [-1, 1], got {value}")

        return float(value)

    # ---------------------------
    # Reset-function
    # ---------------------------
    def reset(self):
        with self._state_lock:
            self._e_M = 0.0
            self._e_M1 = 0.0
            self._e_M2 = 0.0

    # ---------------------------
    # e_M
    # ---------------------------
    @property
    def e_M(self):
        with self._state_lock:
            return self._e_M

    @e_M.setter
    def e_M(self, value):
        with self._state_lock:
            self._e_M = self._validate_range(value, "e_M")

    # ---------------------------
    # e_M1
    # ---------------------------
    @property
    def e_M1(self):
        with self._state_lock:
            return self._e_M1

    @e_M1.setter
    def e_M1(self, value):
        with self._state_lock:
            self._e_M1 = self._validate_range(value, "e_M1")

    # ---------------------------
    # e_M2
    # ---------------------------
    @property
    def e_M2(self):
        with self._state_lock:
            return self._e_M2

    @e_M2.setter
    def e_M2(self, value):
        with self._state_lock:
            self._e_M2 = self._validate_range(value, "e_M2")


# Single global instance
blackboard = Blackboard()