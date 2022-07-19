############################################################################
# Signal Processing Module
#
# FEATURES
# - Load/save signal in wav format
# - Manipulate signals in both time and frequency domains
# - Visualize signal in both time and frequency domains
#
# ORIGINAL AUTHOR
#
# Chaiporn (Art) Jaikaeo
# Intelligent Wireless Networking Group (IWING) -- http://iwing.cpe.ku.ac.th
# Department of Computer Engineering
# Kasetsart University
# chaiporn.j@ku.ac.th
############################################################################

import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft
from scipy.io import wavfile

plt.rc('font', family='Sawasdee', weight='bold') # if not available, will fallback to other font
plt.rc('axes', unicode_minus=False)

class Signal(object):
    def __init__(self, duration=1.0, sampling_rate=22050, func=None):
        '''
        Initialize a signal object with the specified duration (in seconds)
        and sampling rate (in Hz).  If func is provided, signal
        data will be initialized to values of this function for the entire
        duration.
        '''
        self.duration = duration
        self.sampling_rate = sampling_rate
        self.freqs = np.arange(int(duration*sampling_rate), dtype=complex)
        self.freqs[:] = 0j
        if func is not None:
            self.sample_time_function(func)

    def set_freq(self, freq, amplitude, phase=0):
        '''
        Set a particular frequency component with the specified amplitude and
        phase-shift (in degree) to the signal
        '''
        n = len(self.freqs)

        # compute the index at which the specified frequency is located in the
        # array
        index = int(np.round(float(freq)*n/self.sampling_rate))

        # distribute the signal amplitude over the real and imaginary axes
        re = float(n)*amplitude*np.cos(phase*np.pi/180.0)
        im = float(n)*amplitude*np.sin(phase*np.pi/180.0)

        # distribute AC component evenly over positive and negative
        # frequencies
        if freq != 0: 
            re = re/2.0
            im = im/2.0

            # to ensure real-valued time-domain signal, the two parts need to
            # be complex conjugate of each other
            self.freqs[ index] = re + 1j*im
            self.freqs[-index] = re - 1j*im

        else:
            # DC component has only one part
            self.freqs[index] = re + 1j*im

    def get_time_domain(self):
        '''
        Return a tuple (X,Y) where X is an array storing the time axis,
        and Y is an array storing time-domain representation of the signal
        '''
        x_axis = np.linspace(0, self.duration, len(self.freqs))
        y_axis = ifft(self.freqs).real
        return x_axis, y_axis

    def clear(self, cond=lambda f:True):
        '''
        Set amplitudes of all frequencies satisfying the condition, cond, to
        zero, where cond is a boolean function that takes a frequency in Hz.
        '''
        n = len(self.freqs)
        for i in range(n):
            # convert index to corresponding frequency value
            f = float(i)*self.sampling_rate/n
            if cond(f):
                self.freqs[i] = 0j

    def square_wave(self, freq, flimit=8000):
        '''
        Generate a band-limited square wave on to the signal object
        '''
        self.clear()
        f = freq
        while f <= flimit:
            self.set_freq(f, 1.0/f, -90)
            f += 2*freq

def test1():
    '''
    generate a 5Hz square wave with 50Hz cutoff frequency
    then display the time-domain signal
    '''
    s = Signal()
    s.square_wave(5,flimit=50)
    x,y = s.get_time_domain()
    plt.plot(x,y)
    plt.grid(True)
    plt.show()

# ###########################################
# def test2():
#     '''
#     generate a 2Hz square wave with 50Hz cutoff frequency
#     then display both time-domain and frequency-domain signal
#     '''
#     s = Signal()
#     s.square_wave(2,flimit=50)
#     s.plot(stem=True,phase=True,frange=(0,50))

# ###########################################
# def test3():
#     '''
#     generate composite signal containing 3 Hz and 2 Hz sine waves
#     '''

#     def test_func(t):
#         return 0.2*np.sin(2*np.pi*t*3) + 0.3*np.sin(2*np.pi*t*2)

#     s = Signal(func=test_func)
#     s.plot(frange=(0,10), stem=True)

# ###########################################
# def test4():
#     '''
#     generate a DTMF (Dual-Tone Multi-Frequency) signal representing keypad '2'
#     then write the wave output to a file
#     '''
#     s = Signal()
#     s.set_freq(770, .3, 0)
#     s.set_freq(1336, .3, 0)
#     s.plot(frange=(0,1500), stem=False)
#     s.write_wav('2.wav')

# ###########################################
# def test5():
#     '''
#     Read a wave file containing keypad '6' DTMF wave form and display its
#     signal and frequency spectrum
#     '''
#     s = Signal()
#     s.read_wav('Dtmf6.wav')
#     s.plot(frange=(0,2000), stem=False)

# ###########################################
# def test6():
#     '''
#     Test frequency shifting and mixing of signals
#     '''
#     s1 = Signal()
#     s1.set_freq(50,.3)
#     s2 = s1.copy()
#     s2.shift_freq(-30)
#     s1.mix(s2)
#     s2.shift_freq(70)
#     s1.mix(s2)
#     s1.plot(stem=True, phase=False, frange=(0,100))


###########################################
if __name__ == '__main__':
    test1()
