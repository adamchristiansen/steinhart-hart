#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import numpy as np

def steinhart3(r):
  # Coefficients are taken as the defaults used for ILX Lightwave laser diode controllers.
  #
  # ILX Lightwave. Application Note #4: Thermistor Calibration and the
  # Steinhart-Hart Equation, 2006. Rev. 03.071709. Available:
  # https://www.newport.com/medias/sys_master/images/images/h67/hc1/8797049487390/AN04-Thermistor-Calibration-and-Steinhart-Hart.pdf.
  C1 = 1.125e-3
  C2 = 2.347e-4
  C3 = 0.855e-7
  return 1 / (C1 + C2 * np.log(r) + C3 * np.log(r) ** 3) - 273.15

def steinhart3_inv(t, rs):
  return rs[np.argmin(np.abs(steinhart3(rs) - t))]

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
  parser.add_argument(
    '--rmin',
    type=int, action='store', default=3000,
    help='Minimum thermistor value')
  parser.add_argument(
    '--rmax',
    type=int, action='store', default=25000,
    help='Maximum thermistor value')
  args = parser.parse_args()

  DECIMALS = args.decimals if args.decimals is not None else \
    (0 if args.temperature is not None else 3)

  rs = np.linspace(args.rmin, args.rmax,
    10 ** DECIMALS * np.abs(args.rmax - args.rmin) + 1)

  if args.temperature is not None:
    t = args.temperature
    r = steinhart3_inv(t, rs)
    print(f"{{:g}} °C -> {{:.0{DECIMALS}f}} Ω".format(t, r))
  else:
    r = args.resistance
    t = steinhart3(r)
    print(f"{{:g}} Ω -> {{:.0{DECIMALS}f}} °C".format(r, t))
