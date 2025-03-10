from element import Element
from simulation import simulate

bi_212 = Element(name="Bismut-212", N0=1000, half_life=60.6 * 60, time_steps=60 * 60 * 10, precision=1)
zr_89 = Element(name="Zirconi-89", N0=1000, half_life=78.41 * 60 * 60, time_steps=60 * 60 * 500, precision=60 * 60)

simulate(bi_212, show_plot=False)
# simulate(zr_89, show_plot=False)
