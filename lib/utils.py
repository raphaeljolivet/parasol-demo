from time import perf_counter
from contextlib import contextmanager
import streamlit as st


class timer:

    def __init__(self, name=""):
        self.name = name

    def __enter__(self, name=""):
        self.time = perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        self.time = perf_counter() - self.time
        self.readout = f'[{self.name}] Time: {self.time:.3f} seconds'
        print(self.readout)


@contextmanager
def exception_context(context):
    try:
        yield
    except Exception as e:
        e.args = (f"{e.args[0]} | context: {str(context)}",) + e.args[1:]
        raise
