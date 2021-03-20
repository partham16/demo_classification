import h2o

from .config import Config

h2o.init(max_mem_size=Config.h2o_mem_size)
