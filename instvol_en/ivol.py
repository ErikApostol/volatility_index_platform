import numpy as np

def ivol(P, T, N, M, delta=1/50, isSmooth=1):
    """
    Computes the spot variance by the Fourier estimator with Dirichlet kernel and FFT
    P vector of the observed log-prices
    N maximum Fourier frequency for price returns
    M maximum Fourier frequency for spot variance
    """
    r = np.diff(P)
    fft_v = np.fft.fft(r)
    ff = fft_v[M+N:0:-1]
    fft_def = np.concatenate( (np.conjugate(ff), fft_v[0:M+N+1]),axis=0 )
    fft_def = fft_def/T # Fourier coeff. of log-returns

    idxk = np.arange(-N,N+1,1)
    nshift = M + N

    coeff = []
    for kk in range(-M,M+1):
        idxx = idxk + nshift + kk
        Capp = fft_def[idxx]
        coeff.append( np.inner(Capp, np.conjugate(fft_def[nshift-N:nshift+N+1])))

    coeff = np.array(coeff)

    C = coeff*(T/(2*N+1)) # Fourier coeff. of variance
    k = np.arange(-M,M+1)
    smoothKernel = np.array([(np.sin(delta*x) ** 2) / ((delta * x) ** 2) if x != 0 else 1 for x in k+M])
    f = C*( 1 - abs(k)/M ) #original
    Fsum = (2*M+1) * np.fft.ifft(f)
    Fsum = np.exp( (-1j *2* np.pi *M*(k+M)/(2*M+1)) ) * Fsum
    spot = np.real(Fsum)
    
    return spot
