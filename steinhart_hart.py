#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Optional, Tuple, TypeVar

import numpy as np
import numpy.typing as npt

# A type variable used to describe the generic temperature and resistance
# conversion functions.
T = TypeVar('T', bound=npt.NBitBase)

# The ABC coefficients for the Steinhart-Hart equation as a tuple of (A, B, C).
# The units of the coefficients are K^-1.
ABC = Tuple[float, float, float]

# Coefficients are taken as the defaults used for ILX Lightwave laser diode
# controllers.
#
# References:
#
# [1] https://www.newport.com/medias/sys_master/images/images/h67/hc1/
#       8797049487390/AN04-Thermistor-Calibration-and-Steinhart-Hart.pdf
DEFAULT_ABC: ABC = (1.125e-3, 2.347e-4, 0.855e-7)

def temperature(
    r: npt.NDArray[np.float64],
    /,
    abc: Optional[ABC]=None
  ) -> npt.NDArray[np.float64]:
  """Calculates the temperature of a semiconductor.

  The temperature of a semiconductor is found from its resistance using the
  three term Steinhart-Hart equation.

  Args:
    r:
      The resistance in Ω.
    abc:
      The Steinhart-Hart ABC coefficients as a 3 tuple. If None then the
      DEFAULT_ABC coefficients are used.

  Returns:
    The temperature in Kelvin.
  """
  # References:
  #
  # [1] https://wikipedia.org/wiki/Steinhart-Hart_equation
  # [2] https://doi.org/10.1016/0011-7471(68)90057-0 (Steinhart-Hart 1968)
  a, b, c = DEFAULT_ABC if abc is None else abc
  return 1 / (a + b * np.log(r) + c * np.log(r) ** 3)

def resistance(
    t: npt.NDArray[np.float64],
    /,
    abc: Optional[ABC]=None
  ) -> npt.NDArray[np.float64]:
  """Calculates the resistance of a semiconductor.

  The resistance of a semiconductor is found from its temperature using the
  inverse three term Steinhart-Hart equation.

  Args:
    t:
      The temperature in Kelvin.
    abc:
      The Steinhart-Hart ABC coefficients as a 3 tuple. If None then the
      DEFAULT_ABC coefficients are used.

  Returns:
    The resistance in Ω.
  """
  # Referenes:
  #
  # [1]: https://web.archive.org/web/20110708192840/
  #       http://www.cornerstonesensors.com/reports/
  #       ABC%20Coefficients%20for%20Steinhart-Hart%20Equation.pdf
  a, b, c = DEFAULT_ABC if abc is None else abc
  x = (a - 1 / t) / c
  y = np.sqrt((b / (3 * c)) ** 3 + x ** 2 / 4)
  return np.exp(np.cbrt(y - x / 2) - np.cbrt(y + x / 2))

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(
    description='Model the temperature and resistance of a semiconductor')
  parser.add_argument('x',
    type=float, action='store',
    help='The value to convert')
  arg_type = parser.add_mutually_exclusive_group(required=False)
  arg_type.add_argument('--resistance', '-R',
    action='store_true',
    help='Treat the argument as resistance in Ω')
  arg_type.add_argument('--temperature', '-T',
    action='store_true',
    help='Treat the argument as temperature in °C')
  units = parser.add_mutually_exclusive_group(required=False)
  units.add_argument('--celsius', '-C',
    action='store_true',
    help='Use °C for temperature')
  units.add_argument('--kelvin', '-K',
    action='store_true',
    help='Use K for temperature')
  parser.add_argument('--number-only', '-x',
    action='store_true',
    help='Display just the result instead of the conversion information')
  args = parser.parse_args()

  # Whether the operation is forward (i.e., resistance to temperature) or
  # reverse (i.e., temperature to resistance).
  forward = True if args.resistance else \
    False if args.temperature else args.x >= 1000

  # Decide which functions, units, and adjustements to use.
  #
  # - f is the conversion function.
  # - xunit and xadj are the units and offset added to the argument of f.
  # - yunit and yadj are the units and offset added to the return value of f.
  if forward:
    f = temperature
    xunit, xadj = 'Ω', 0.0
    yunit, yadj = ('°C', -273.15) if not args.kelvin else ('K', 0.0)
  else:
    f = resistance
    xunit, xadj = ('°C', +273.15) if not args.kelvin else ('K', 0.0)
    yunit, yadj = 'Ω', 0.0

  # Perform the conversion.
  y = f(args.x + xadj) + yadj
  if args.number_only:
    print(f"{y:.03f}")
  else:
    print(f"{args.x:.03f} {xunit} -> {y:.03f} {yunit}")
