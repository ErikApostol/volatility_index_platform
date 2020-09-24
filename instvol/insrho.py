import time
import numpy as np

def insrho(s1,s2,s1_sigma,s2_sigma):
    tStart_1=time.time()
    Nstep=len(s1)
    t=np.zeros(Nstep)
# time domain to frequency domain
    dt = 1/252
    Start_time = 0
    End_time = (len(s1) - 1) * dt
    dim=2
    S=np.array([s1.transpose(),s2.transpose()])
    s1_sigma=np.array(s1_sigma.transpose())
    s2_sigma=np.array(s2_sigma.transpose())
    
    # time domain to frequency domain
    for i in range(Nstep):
        t[i] = 2 * np.pi / (End_time - Start_time) * dt * i
    
    Num_coef_u = Nstep
    Coef_u_a = np.zeros([dim,Nstep])
    Coef_u_b = np.zeros([dim,Nstep])
    R=np.zeros([2,len(s1)])
    #calculate time
    
    for k in range(dim):
    # compute log price
        R[k,:]=np.log(S[k,:])
    # estimate sigma_1 sigma_2 by Fourier
    # Compute the Fourier coefficients of ln-stock price
        Coef_u_a[k,0] = (R[k,-1] - R[k,0]) / (2 * np.pi)    # a_0(du)
        
        for i in range(1,Num_coef_u):
            J= np.arange(0,Nstep-1)
            Coef_u_a[k,i] = Coef_u_a[k,i] + sum(R[k,J] * (np.cos((i) * t[J]) - np.cos((i) * t[J+1])) / np.pi)    # a_k(du) - (u(2pi)-u(0)) / pi
            Coef_u_b[k,i] = Coef_u_b[k,i] - sum(R[k,J] * (np.sin((i) * t[J + 1]) - np.sin((i) * t[J])) / np.pi)    # b_k(du)
            Coef_u_a[k,i] = Coef_u_a[k,i] + (R[k,-1] - R[k,0]) / np.pi    # a_k(du)

         
#------------------------------------------------------------------------
#------------- Compute the Fourier coefficients of rho -------------------
#--------------------------------------------------------------------------
# Compute the Fourier coefficients of variance
    Num_coef_sigma = Nstep
    Coef_sigma_a_rho = np.zeros([1, Num_coef_sigma])
    Coef_sigma_b_rho = np.zeros([1, Num_coef_sigma])


    for i in range(Num_coef_sigma): #0:Num_coef_sigma-1
        J= np.arange(0,Num_coef_sigma-i-1)
        #n0:Num_coef_sigma-i-1
        Coef_sigma_a_rho[0,i] = Coef_sigma_a_rho[0,i] + sum(Coef_u_a[0,J] * Coef_u_a[1,J + i] + Coef_u_b[1,J] * Coef_u_b[0,J + i])
        Coef_sigma_b_rho[0,i] = Coef_sigma_b_rho[0,i] + sum(Coef_u_a[0,J] * Coef_u_b[1,J + i] - Coef_u_b[0,J] * Coef_u_a[1,J + i])
        
        Coef_sigma_a_rho[0,i] = Coef_sigma_a_rho[0,i] * np.pi / (Num_coef_sigma)    # a_k(sigma)
        Coef_sigma_b_rho[0,i] = Coef_sigma_b_rho[0,i] * np.pi / (Num_coef_sigma)    # b_k(sigma)

    # Compute the variance matrix on a time grid
    Num_variance = Nstep
    Rho_process_Fourier = np.zeros([1, Num_variance])
    delta_rho = 1 / 50
    
    for i in range(Num_variance):
        for j in range(Num_coef_sigma):
            Smoothing_parameter_rho = j * delta_rho

            if Smoothing_parameter_rho == 0:
                Fejer_Kernel_rho = 1    # Fejer_Kernel(0) = 1
            else:
                Fejer_Kernel_rho = ((np.sin(Smoothing_parameter_rho)) ** 2) / (Smoothing_parameter_rho ** 2)    # Fejer_Kernel(x) = sin^2(x) / x^2
            Rho_process_Fourier[0,i] = Rho_process_Fourier[0,i] + Fejer_Kernel_rho * ( Coef_sigma_a_rho[0,j] * np.cos(j * t[i]) + Coef_sigma_b_rho[0,j] * np.sin(j * t[i])) # sigma^2(t)


    Rho_process_Fourier =  (Rho_process_Fourier/ ( s1_sigma*s2_sigma))
    ## correction to FTM correlation
    diff_u = R[:,1:-1] - R[:,0:-2]
    
    #-------------------------------------------------------------------------
    #--------------------adjust_1:linear----------------------------------------
    #-------------------------------------------------------------------------
    beta=sum(diff_u[0,:]*diff_u[1,:]) / (np.sum (( Rho_process_Fourier * dt )*(s1_sigma*s2_sigma)))
    rho_adj_linear = beta * Rho_process_Fourier
    if abs(rho_adj_linear[0,0])>1:
        rho_adj_linear[0,0]==0
    for i in range(1,Nstep):
        if abs(rho_adj_linear[0,i])>1:
            rho_adj_linear[0,i]= rho_adj_linear[0,i-1]
    return rho_adj_linear
    

