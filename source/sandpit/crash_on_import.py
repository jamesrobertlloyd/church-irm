import sys
sys.path.append('../')

from venture_engine_requirements import *
import venture_engine

venture_engine.clear()
print venture_engine.assume('alpha', 1)
