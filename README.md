# Steinhart-Hart Equation

The [Steinhart-Hart equation][1] is used to describe the relationship between
resistance and temperature of semiconductor devices. The original publication
from Steinhart and Hart is:

> J. S. Steinhart and S. R. Hart. [Calibration curves for thermistors][2]. In
> Deep Sea Research and Oceanographic Abstracts, volume 15, pages 497–503.
> Elsevier, 1968.

This project was created to quickly convert between the resistance and
temperature of thermistors packaged in semiconductor lasers.

## Use as a library

Simply include the [`steinhart_hart.py`](./steinhart_hart.py) file in your
project. Refer to the file for usage &mdash; the module itself is very short
and well documented.

## Use as a binary

The [`steinhart_hart.py`](./steinhart_hart.py) file can be executed. Some
examples:

```
$ python3 steinhart_hart.py 25
25.000 °C -> 10021.351 Ω

$ python3 steinhart_hart.py 298 -K
298.000 K -> 10087.532 Ω

$ python3 steinhart_hart.py 10000
10000.000 Ω -> 25.049 °C
```

By default, the argument is assumed to be a temperature in °C if it is less
than 1000 and a resistance in Ω if it is greater than or equal to 1000. The
argument can be forced to a temperature by specifying `-T` or resistance with
`-R`. The temperature units can be made °C with `-C` and K with `-K`.

Run with the `--help` option to see the full usage options.

[1]: https://wikipedia.org/wiki/Steinhart-Hart_equation
[2]: https://doi.org/10.1016/0011-7471(68)90057-0
