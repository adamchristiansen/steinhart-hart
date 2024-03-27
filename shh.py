#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import numpy as np

# Coefficients are taken as the defaults used for ILX Lightwave laser diode
# controllers. This is tuple of (A, B, C).
#
# References:
#
# [1] https://www.newport.com/medias/sys_master/images/images/h67/hc1/
#       8797049487390/AN04-Thermistor-Calibration-and-Steinhart-Hart.pdf
DEFAULT_ABC = (1.125e-3, 2.347e-4, 0.855e-7)

def temperature(r, abc=None):
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
  return 1 / (a + b * np.log(r) + c * np.log(r) ** 3) - 273.15

def resistance(t, abc=None):
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
  x = (a - 1 / (t + 273.15)) / c
  y = np.sqrt((b / (3 * c)) ** 3 + x ** 2 / 4)
  return np.exp(np.cbrt(y - x / 2) - np.cbrt(y + x / 2))

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(
    description='Model the temperature and resistance of a semiconductor')
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument(
    '--temperature', '-T',
    type=float, action='store',
    help='The temperature in °C')
  group.add_argument(
    '--resistance', '-R',
    type=float, action='store',
    help='The resistance in Ω')
  parser.add_argument(
    '--decimals', '-d',
    type=int, action='store', default=None,
    help='Number of decimals in output')
  args = parser.parse_args()

  DECIMALS = args.decimals if args.decimals is not None else \
    (0 if args.temperature is not None else 3)

  if args.temperature is not None:
    t = args.temperature
    r = resistance(t)
    print(f"{{:g}} °C -> {{:.0{DECIMALS}f}} Ω".format(t, r))
  else:
    r = args.resistance
    t = temperature(r)
    print(f"{{:g}} Ω -> {{:.0{DECIMALS}f}} °C".format(r, t))
