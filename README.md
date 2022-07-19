# python-qam-modulation
Graphical interface and constellation map for Quadrature-Amplitude Modulation (QAM)

## Reason for this fork

-> Convert Python 2 to Python 3 and see how the sample codes work ;)

# Usage

1. Open a python3 terminal inside `src/python3`
2. Pick the desired modulation to test
    - 2psk, 4psk, 8qam, 16qam, ook
3. Run `python <filename> <data_bits>`
    - e.g.: `python 2psk 10`
    - e.g.: `python 16qam 1010 0101`

# TODO list and ideas for future work

- This repository accumulates too many concerns to `sigproc` in its `Signal` class.
- Unused functions such as `get_duration` and `amplify` from `sigproc` were not ported because there is no current use case, aside from user-made extensions
- Data-manipulating structures are coupled with plots. It would be ideal to separate them to allow users to use the data in whatever graphics backend they wish