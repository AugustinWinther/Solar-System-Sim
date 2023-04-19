# Local imports
from uib_inf100_graphics import *
from simulation import *
from control import *
from draw import *
from body import *
from view import *


def app_started(app) -> None:
    """Called one time when app starts"""
    init_bodies(app)
    init_view(app)
    init_control(app)
    init_simulation(app)

if __name__ == "__main__":
    run_app(width=900, height=900, title="Solar System Sim")


# UNCOMMENT TO DEBUG PERFOMANCE https://stackoverflow.com/a/6880574
# import cProfile
# import pstats
# if __name__ == "__main__":
#     with cProfile.Profile() as pr:
#         run_app(width=900, height=900, title="Gravity Playground")
#
#     stats = pstats.Stats(pr)
#     stats.sort_stats(pstats.SortKey.TIME)
#     stats.dump_stats("perf.prof")
#     # Use snakeviz to see perf.prof (pip install snakeviz)
