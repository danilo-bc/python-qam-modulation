import sys
from qam import Qam
from matplotlib import pyplot as plt

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <data-bits>")
        exit(1)

    modulation = { 
        '00' : (1,   0),
        '01' : (1,  90),
        '10' : (1, 180),
        '11' : (1, 270),
        }

    q = Qam(baud_rate = 10,
            bits_per_baud = 2,
            carrier_freq = 50,
            modulation = modulation)

    s = q.generate_signal(sys.argv[1])

    plt.figure(1)
    q.plot_constellation()
    plt.figure(2)
    s.plot(dB=False, phase=False, stem=False, frange=(0,500))
