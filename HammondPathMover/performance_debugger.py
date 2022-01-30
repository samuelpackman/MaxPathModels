import cProfile
import pstats
from main2 import changing_board

def test():
    changing_board(n = 30, ensemble_size = 3, framerate = 24, num_reps  = 5)

profile = cProfile.Profile()
profile.runcall(test)
ps = pstats.Stats(profile)
ps.print_stats()
