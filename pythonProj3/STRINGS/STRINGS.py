#!/usr/bin/python

###################################################################################################################################
# STRINGS version 2-00 - Monte Carlo Event Generator for the Prtoduction and Decay of String Resonances in Proton-Proton Collisions
# Authors: F. Lyons, P. Vakilipourtakalou, D. M. Gingrich. October 2020
###################################################################################################################################

from __future__ import division
import lhapdf
import math
import random
import argparse
from subprocess import call

############################################################################################################
# Event Generator Main Code
# All of the input parameters and their default values are defined after the definition of the main function
############################################################################################################

def main(RandGenSEED, Number, Ms, COME, MinMass, MaxMass, yMax, PDFSet, PDFScale, Coupling, CouplingScale, StringCoeff, SecondStringCoeff, QCDCoeff, dMass, uMass, sMass, cMass, bMass, tMass, gg2gg, gg2qqbar, gq2gq, gqbar2gqbar, qqbar2gg, gg2gGamma, gq2qGamma):

    # A seed for the random number generator, by changing this seed different sequences of random numbers are generated
    random.seed(RandGenSEED)
    
    # Printing the input parameters with their values on the screen
    print("####                                                                                                                              ")
    print("#### {0:<10}{1:<22}{2:<30}".format(RandGenSEED, 'RandGenSEED', 'Seed for the the Random Number Generator'))
    print("#### {0:<10}{1:<22}{2:<30}".format(Number, 'Number', 'Number of Events'))
    print("#### {0:<10}{1:<22}{2:<30}".format(Ms, 'Ms', 'String Scale (GeV)'))
    print("#### {0:<10}{1:<22}{2:<30}".format(COME, 'COME', 'Centre of Mass Energy (GeV)'))
    print("#### {0:<10}{1:<22}{2:<30}".format(MinMass, 'MinMass', 'Minimum Invariant Mass (GeV)'))
    print("#### {0:<10}{1:<22}{2:<30}".format(MaxMass, 'MaxMass', 'Maximum Invariant Mass (GeV)'))
    print("#### {0:<10}{1:<22}{2:<30}".format(yMax, 'yMax', 'Upper Bound for the Rapidity of the Outgoing Partons'))
    print("#### {0:<10}{1:<22}{2:<30}".format(PDFSet, 'PDFSet', 'PDF Set of the LHAPDF'))
    if(PDFScale == -22):
        PDFScale = Ms
    print("#### {0:<10}{1:<22}{2:<30}".format(PDFScale, 'PDFScale', 'Scale at Which the PDF Set is Evaluated (GeV)'))
    if(Coupling == -1):
        print("#### {0:<10}{1:<22}{2:<30}".format(Coupling, 'Coupling', 'Running Coupling Constant (alpha_s without 4*pi Factor)'))
        if(CouplingScale == -22):
            CouplingScale = Ms
        print("#### {0:<10}{1:<22}{2:<30}".format(CouplingScale, 'CouplingScale', 'Scale at Which the Running Coupling is Calculated (GeV)'))
    else:
        print("#### {0:<10}{1:<22}{2:<30}".format(Coupling, 'Coupling', 'Coupling Constant (alpha_s without 4*pi Factor)'))
    if(StringCoeff == "true" or StringCoeff == "True"):
        print("#### {0:<10}{1:<22}{2:<30}".format(StringCoeff, 'FirstStringCoeff', '(Enabled)  Production of First  String Resonance ( 2 --> 2 Partonic Scattering and 2-Parton --> Parton-Gamma Scattering )'))
        StringCoeff11 = 1
    else:
        print("#### {0:<10}{1:<22}{2:<30}".format(StringCoeff, 'FirstStringCoeff', '(Disabled) Production of First  String Resonance  ( 2 --> 2 Partonic Scattering and 2-Parton --> Parton-Gamma Scattering )'))
        StringCoeff11 = 0
    if(SecondStringCoeff == "true" or SecondStringCoeff == "True"):
        print("#### {0:<10}{1:<22}{2:<30}".format(SecondStringCoeff, 'SecondStringCoeff', '(Enabled)  Production of Second String Resonance ( 2 --> 2 Partonic Scattering )'))
        SecondStringCoeff11 = 1
    else:
        print("#### {0:<10}{1:<22}{2:<30}".format(SecondStringCoeff, 'SecondStringCoeff', '(Disabled) Production of Second String Resonance ( 2 --> 2 Partonic Scattering )'))
        SecondStringCoeff11 = 0
    if(QCDCoeff == "true" or QCDCoeff == "True"):
        print("#### {0:<10}{1:<22}{2:<30}".format(QCDCoeff, 'QCDCoeff', '(Enabled)  Production of QCD tree-level diparton'))
        QCDCoeff11 = 1
    else:
        print("#### {0:<10}{1:<22}{2:<30}".format(QCDCoeff, 'QCDCoeff', '(Disabled) Production of QCD tree-level diparton'))
        QCDCoeff11 = 0
    print("#### {0:<10}{1:<22}{2:<30}".format(dMass, 'dMass', 'Mass of the Down Quark (GeV)'))  # Fixed typos
    print("#### {0:<10}{1:<22}{2:<30}".format(uMass, 'uMass', 'Mass of the Up Quark (GeV)'))
    print("#### {0:<10}{1:<22}{2:<30}".format(sMass, 'sMass', 'Mass of the Strange Quark (GeV)'))
    print("#### {0:<10}{1:<22}{2:<30}".format(cMass, 'cMass', 'Mass of the Charm Quark (GeV)'))
    print("#### {0:<10}{1:<22}{2:<30}".format(bMass, 'bMass', 'Mass of the Bottom Quark (GeV)'))
    print("#### {0:<10}{1:<22}{2:<30}".format(tMass, 'tMass', 'Mass of the Top Quark (GeV)'))
    NPRUP = 0
    if(gg2gg == "True" or gg2gg == "true"):
        print("#### {0:<10}{1:<22}{2:<30}".format(gg2gg, 'gg2gg', '(Enabled)  gg --> gg Subprocess       (ID = 1)'))
        gg2gg11 = 1
        NPRUP = NPRUP + 1
    else:
        print("#### {0:<10}{1:<22}{2:<30}".format(gg2gg, 'gg2gg', '(Disabled) gg --> gg Subprocess       (ID = 1)'))
        gg2gg11 = 0

    if(gg2qqbar == "True" or gg2qqbar == "true"):
        print("#### {0:<10}{1:<22}{2:<30}".format(gg2qqbar, 'gg2qqbar', '(Enabled)  gg --> qqbar Subprocess    (ID = 2)'))
        gg2qqbar11 = 1
        NPRUP = NPRUP + 1
    else:
        print("#### {0:<10}{1:<22}{2:<30}".format(gg2qqbar, 'gg2qqbar', '(Disabled) gg --> qqbar Subprocess    (ID = 2)'))
        gg2qqbar11 = 0

    if(gq2gq == "True" or gq2gq == "true"):
        print("#### {0:<10}{1:<22}{2:<30}".format(gq2gq, 'gq2gq', '(Enabled)  gq --> gq Subprocess       (ID = 3)'))
        gq2gq11 = 1
        NPRUP = NPRUP + 1
    else:
        print("#### {0:<10}{1:<22}{2:<30}".format(gq2gq, 'gq2gq', '(Disabled) gq --> gq Subprocess       (ID = 3)'))
        gq2gq11 = 0

    if(gqbar2gqbar == "True" or gqbar2gqbar == "true"):
        print("#### {0:<10}{1:<22}{2:<30}".format(gqbar2gqbar, 'gqbar2gqbar', '(Enabled)  gqbar --> gqbar Subprocess (ID = 4)'))
        gqbar2gqbar11 = 1
        NPRUP = NPRUP + 1
    else:
        print("#### {0:<10}{1:<22}{2:<30}".format(gqbar2gqbar, 'gqbar2gqbar', '(Disabled) gqbar --> gqbar Subprocess (ID = 4)'))
        gqbar2gqbar11 = 0

    if(qqbar2gg == "True" or qqbar2gg == "true"):
        print("#### {0:<10}{1:<22}{2:<30}".format(qqbar2gg, 'qqbar2gg', '(Enabled)  qqbar --> gg Subprocess    (ID = 5)'))
        qqbar2gg11 = 1
        NPRUP = NPRUP + 1
    else:
        print("#### {0:<10}{1:<22}{2:<30}".format(qqbar2gg, 'qqbar2gg', '(Disabled) qqbar --> gg Subprocess    (ID = 5)'))
        qqbar2gg11 = 0

    if(gg2gGamma == "True" or gg2gGamma == "true"):
        print("#### {0:<10}{1:<22}{2:<30}".format(gg2gGamma, 'gg2gGamma', '(Enabled)  gg --> gGamma Subprocess   (ID = 6)'))
        gg2gGamma11 = 1
        NPRUP = NPRUP + 1
    else:
        print("#### {0:<10}{1:<22}{2:<30}".format(gg2gGamma, 'gg2gGamma', '(Disabled) gg --> gGamma Subprocess   (ID = 6)'))
        gg2gGamma11 = 0

    if(gq2qGamma == "True" or gq2qGamma == "true"):
        print("#### {0:<10}{1:<22}{2:<30}".format(gq2qGamma, 'gq2qGamma', '(Enabled)  gq --> qGamma Subprocess   (ID = 7)'))
        gq2qGamma11 = 1
        NPRUP = NPRUP + 1
    else:
        print("#### {0:<10}{1:<22}{2:<30}".format(gq2qGamma, 'gq2qGamma', '(Disabled) gq --> qGamma Subprocess   (ID = 7)'))
        gq2qGamma11 = 0
        
    print("####                                                ")
    print("########################################################")
    print("########################################################")
    print("\nInitializing...\n")
    print("\n(Each dot represents generation of 50 events)\n")

    # Specifying the Parton Distribution Functions
    DistFunc = lhapdf.mkPDF(PDFSet, 0)
    
    # Quark Masses
    QuarkMasses = [dMass, uMass, sMass, cMass, bMass, tMass]
    
    # Centre of mass energy
    s = COME**2
    
    # Number of colours and flavours
    N = 3
    Nf = 6
    
    # Coupling constants
    if(Coupling == -1):
        # Running Coupling Constant, calculated at the CouplingScale
        alpha3 = 1/(1/0.118 + 7/2/math.pi*math.log(CouplingScale/91.2))
    else:
        # Fixed coupling constant
        alpha3 = Coupling
    g3 = math.sqrt(4*math.pi*alpha3) # Strong coupling constant
    QED = 1/128  # QED coupling constant
    Q = 1/6      # Fundamental charge

    # Decay widths that will be used in the scattering amplitudes
    # Decay Widths of First Resonances
    GJ0gS   = g3**2/4/math.pi*Ms*N/4
    GJ0cS   = g3**2/4/math.pi*Ms*N/2
    GJhfqS  = g3**2/4/math.pi*Ms*N/8
    GJ2gS   = g3**2/4/math.pi*Ms*(N/10 + Nf/40)
    GJ2cS   = g3**2/4/math.pi*Ms*(N/5  + Nf/40)
    GJ3hfqS = g3**2/4/math.pi*Ms*N/16

    # Decay Widths of Second Resonances
    GssJhfqS  = g3**2/4/math.pi*math.sqrt(2)*Ms*N/24
    GssJ3hfqS = g3**2/4/math.pi*math.sqrt(2)*Ms*19*N/240
    GssJ5hfqS = g3**2/4/math.pi*math.sqrt(2)*Ms*N/60

    # Definition of the seven functions corresponding to seven subprocesses
    # Each event is specified by (M, Y, y). The ID of the first and second incoming partons are determined by FstpartonID and ScndpartonID, respectively.

    # gg->gg
    def MonteCarlogggg(parameters, *args):

        Y, y                           = parameters
        M, FstpartonID, ScndpartonID   = args
        
        tau = M**2/s

        xa  = math.sqrt(tau)*math.exp( Y)
        xb  = math.sqrt(tau)*math.exp(-Y)

        shat = M**2
        that = -0.5*M**2*math.exp(-y)/math.cosh(y)
        uhat = -0.5*M**2*math.exp( y)/math.cosh(y)

        # Production of the first string resonance
        MSquareString = StringCoeff11*(8/N**2*g3**4/Ms**4*((N**2-4)**2/4/(N**2-1)*(Ms**8/((shat-Ms**2)**2+(Ms*GJ0gS)**2) + (uhat**4+that**4)/((shat-Ms**2)**2 + (Ms*GJ2gS)**2)) + Ms**8/((shat-Ms**2)**2+(Ms*GJ0cS)**2) + (uhat**4+that**4)/((shat-Ms**2)**2 + (Ms*GJ2cS)**2)))

        # Production of the QCD diparton
        MSquareQCD    = QCDCoeff11*(g3**4*(1/shat**2+1/that**2+1/uhat**2)*(2*N**2/(N**2-1)*(shat**2+that**2+uhat**2)+4*(3-N**2)/N**2/(N**2-1)*(shat+that+uhat)**2))

        # Total scattering amplitude
        MSquareTotal  = MSquareString + MSquareQCD

        #Convolution of the scattering amplitudes with parton distribution function
        return(gg2gg11*DistFunc.xfxQ(FstpartonID,xa,PDFScale)*DistFunc.xfxQ(ScndpartonID,xb,PDFScale)*MSquareTotal*M/(math.cosh(y)**2*16*math.pi*shat**2))

    #gg->qqbar
    def MonteCarloggqqbar(parameters, *args):
        
        Y, y                           = parameters
        M, FstpartonID, ScndpartonID   = args
        
        tau = M**2/s

        xa  = math.sqrt(tau)*math.exp( Y)
        xb  = math.sqrt(tau)*math.exp(-Y)

        shat = M**2
        that = -0.5*M**2*math.exp(-y)/math.cosh(y)
        uhat = -0.5*M**2*math.exp( y)/math.cosh(y)

        # Production of the first string resonance
        MSquareString = StringCoeff11*(2/N/(N**2-1)*Nf*g3**4/Ms**4*((N**2-4)/2*uhat*that*(uhat**2+that**2)/((shat-Ms**2)**2+(Ms*GJ2gS)**2) + uhat*that*(uhat**2+that**2)/((shat-Ms**2)**2+(Ms*GJ2cS)**2)))

        # Production of the QCD diparton
        MSquareQCD    = QCDCoeff11*(2*g3**4*Nf*(that**2+uhat**2)/shat**2*(1/2/N/uhat/that*(that+uhat)**2-N/(N**2-1)))

        # Total scattering amplitude
        MSquareTotal  = MSquareString + MSquareQCD

        #Convolution of the scattering amplitudes with parton distribution function
        return(gg2qqbar11*DistFunc.xfxQ(FstpartonID,xa,PDFScale)*DistFunc.xfxQ(ScndpartonID,xb,PDFScale)*MSquareTotal*M/(math.cosh(y)**2*16*math.pi*shat**2))

    #gq->gq
    def MonteCarlogqgq(parameters, *args):
        
        Y, y                           = parameters
        M, FstpartonID, ScndpartonID   = args
        
        tau = M**2/s

        xa  = math.sqrt(tau)*math.exp( Y)
        xb  = math.sqrt(tau)*math.exp(-Y)

        shat = M**2
        that = -0.5*M**2*math.exp(-y)/math.cosh(y)
        uhat = -0.5*M**2*math.exp( y)/math.cosh(y)

        # Production of the first string resonance
        MSquareString       = StringCoeff11*(0.5*(N**2-1)/2/N**2*g3**4/Ms**2*(-Ms**4*that/((shat-Ms**2)**2+(Ms*GJhfqS)**2) - that**3/((shat-Ms**2)**2+(Ms*GJ3hfqS)**2) - Ms**4*uhat/((shat-Ms**2)**2+(Ms*GJhfqS)**2) - uhat**3/((shat-Ms**2)**2+(Ms*GJ3hfqS)**2)))

        # Production of the QCD diparton
        MSquareQCD          = QCDCoeff11*(g3**4*(shat**2+uhat**2)/that**2*(1-(N**2-1)/2/N**2/uhat/shat*(shat+uhat)**2) + g3**4*(shat**2+that**2)/uhat**2*(1-(N**2-1)/2/N**2/that/shat*(shat+that)**2))

        # Production of the second string resonance
        MSquareSecondString = SecondStringCoeff11*(2*(N**2-1)/N**2*(g3**4/2/Ms**2*(1/9*Ms**4*(-uhat)/((shat-2*Ms**2)**2 + (math.sqrt(2)*Ms*GssJhfqS)**2) + (-1/9)*uhat*(3*that+shat)**2/((shat-2*Ms**2)**2 + (math.sqrt(2)*Ms*GssJ3hfqS)**2)) + g3**4/8/Ms**6*(9/25*Ms**4*(-uhat)**3/((shat-2*Ms**2)**2 + (math.sqrt(2)*Ms*GssJ3hfqS)**2) + (-1/25)*uhat**3*(5*that+shat)**2/((shat-2*Ms**2)**2 + (math.sqrt(2)*Ms*GssJ5hfqS)**2))))

        #Total scattering amplitude
        MSquareTotal        = MSquareString + MSquareQCD + MSquareSecondString

        #Convolution of the scattering amplitudes with parton distribution function
        return(gq2gq11*(DistFunc.xfxQ(FstpartonID,xa,PDFScale)*DistFunc.xfxQ(ScndpartonID,xb,PDFScale) + DistFunc.xfxQ(FstpartonID,xb,PDFScale)*DistFunc.xfxQ(ScndpartonID,xa,PDFScale))*MSquareTotal*M/(math.cosh(y)**2*16*math.pi*shat**2))

    #gqbar->gqbar
    def MonteCarlogqbargqbar(parameters, *args):
        
        Y, y                           = parameters
        M, FstpartonID, ScndpartonID   = args
        
        tau = M**2/s

        xa  = math.sqrt(tau)*math.exp( Y)
        xb  = math.sqrt(tau)*math.exp(-Y)

        shat = M**2
        that = -0.5*M**2*math.exp(-y)/math.cosh(y)
        uhat = -0.5*M**2*math.exp( y)/math.cosh(y)

        # Production of the first string resonance
        MSquareString       = StringCoeff11*(0.5*(N**2-1)/2/N**2*g3**4/Ms**2*(-Ms**4*that/((shat-Ms**2)**2+(Ms*GJhfqS)**2) - that**3/((shat-Ms**2)**2+(Ms*GJ3hfqS)**2) - Ms**4*uhat/((shat-Ms**2)**2+(Ms*GJhfqS)**2) - uhat**3/((shat-Ms**2)**2+(Ms*GJ3hfqS)**2)))

        # Production of the QCD diparton
        MSquareQCD          = QCDCoeff11*(g3**4*(shat**2+uhat**2)/that**2*(1-(N**2-1)/2/N**2/uhat/shat*(shat+uhat)**2) + g3**4*(shat**2+that**2)/uhat**2*(1-(N**2-1)/2/N**2/that/shat*(shat+that)**2))

        # Production of the second string resonance
        MSquareSecondString = SecondStringCoeff11*(2*(N**2-1)/N**2*(g3**4/2/Ms**2*(1/9*Ms**4*(-that)/((shat-2*Ms**2)**2 + (math.sqrt(2)*Ms*GssJhfqS)**2) + (-1/9)*that*(3*uhat+shat)**2/((shat-2*Ms**2)**2 + (math.sqrt(2)*Ms*GssJ3hfqS)**2)) + g3**4/8/Ms**6*(9/25*Ms**4*(-that)**3/((shat-2*Ms**2)**2 + (math.sqrt(2)*Ms*GssJ3hfqS)**2) + (-1/25)*that**3*(5*uhat+shat)**2/((shat-2*Ms**2)**2 + (math.sqrt(2)*Ms*GssJ5hfqS)**2))))

        # Total scattering amplitude
        MSquareTotal        = MSquareString + MSquareQCD + MSquareSecondString

        
        #Convolution of the scattering amplitudes with parton distribution function
        return(gqbar2gqbar11*(DistFunc.xfxQ(FstpartonID,xa,PDFScale)*DistFunc.xfxQ(ScndpartonID,xb,PDFScale) + DistFunc.xfxQ(FstpartonID,xb,PDFScale)*DistFunc.xfxQ(ScndpartonID,xa,PDFScale))*MSquareTotal*M/(math.cosh(y)**2*16*math.pi*shat**2))

    #qqbar->gg
    def MonteCarloqqbargg(parameters, *args):

        Y, y                           = parameters
        M, FstpartonID, ScndpartonID   = args
        
        tau = M**2/s
        
        xa  = math.sqrt(tau)*math.exp( Y)
        xb  = math.sqrt(tau)*math.exp(-Y)

        shat = M**2
        that = -0.5*M**2*math.exp(-y)/math.cosh(y)
        uhat = -0.5*M**2*math.exp( y)/math.cosh(y)

        # Production of the first string resonance
        MSquareString = StringCoeff11*(2*(N**2-1)/N**3*g3**4/Ms**4*((N**2-4)/2*uhat*that*(uhat**2+that**2)/((shat-Ms**2)**2+(Ms*GJ2gS)**2) + uhat*that*(uhat**2+that**2)/((shat-Ms**2)**2+(Ms*GJ2cS)**2)))

        # Production of the QCD diparton
        MSquareQCD    = QCDCoeff11*(2*g3**4*(that**2+uhat**2)/shat**2*((N**2-1)**2/2/N**3/uhat/that*(that+uhat)**2-(N**2-1)/N))

        # Total scattering amplitude
        MSquareTotal  = MSquareString + MSquareQCD

        #Convolution of the scattering amplitudes with parton distribution function
        return(qqbar2gg11*(DistFunc.xfxQ(FstpartonID,xa,PDFScale)*DistFunc.xfxQ(ScndpartonID,xb,PDFScale) + DistFunc.xfxQ(FstpartonID,xb,PDFScale)*DistFunc.xfxQ(ScndpartonID,xa,PDFScale))*MSquareTotal*M/(math.cosh(y)**2*16*math.pi*shat**2))

    #gg->gGamma
    def MonteCarlogggGamma(parameters, *args):

        Y, y                           = parameters
        M, FstpartonID, ScndpartonID   = args
        
        tau = M**2/s
        
        xa  = math.sqrt(tau)*math.exp( Y)
        xb  = math.sqrt(tau)*math.exp(-Y)

        shat = M**2
        that = -0.5*M**2*math.exp(-y)/math.cosh(y)
        uhat = -0.5*M**2*math.exp( y)/math.cosh(y)

        # Production of the first string resonance
        MSquareTotal  = StringCoeff11*5*g3**4*Q**2/3/Ms**4*(Ms**8/((shat-Ms**2)**2 + (GJ0gS*Ms)**2) + (that**4 + uhat**4)/((shat-Ms**2)**2 + (GJ2gS*Ms)**2))

        #Convolution of the scattering amplitudes with parton distribution function
        return(2*gg2gGamma11*DistFunc.xfxQ(FstpartonID,xa,PDFScale)*DistFunc.xfxQ(ScndpartonID,xb,PDFScale)*MSquareTotal*M/(math.cosh(y)**2*16*math.pi*shat**2))

    #gq->qGamma
    def MonteCarlogqqGamma(parameters, *args):

        Y, y                           = parameters
        M, FstpartonID, ScndpartonID   = args
        
        tau = M**2/s
        
        xa  = math.sqrt(tau)*math.exp( Y)
        xb  = math.sqrt(tau)*math.exp(-Y)

        shat = M**2
        that = -0.5*M**2*math.exp(-y)/math.cosh(y)
        uhat = -0.5*M**2*math.exp( y)/math.cosh(y)

        # Production of the first string resonance
        MSquareTotal  = -StringCoeff11*g3**4*Q**2/3/Ms**2*(Ms**4*uhat/((shat-Ms**2)**2 + (GJhfqS*Ms)**2) + uhat**3/((shat-Ms**2)**2 + (GJ3hfqS*Ms)**2))

        #Convolution of the scattering amplitudes with parton distribution function
        return(gq2qGamma11*(DistFunc.xfxQ(FstpartonID,xa,PDFScale)*DistFunc.xfxQ(ScndpartonID,xb,PDFScale) + DistFunc.xfxQ(FstpartonID,xb,PDFScale)*DistFunc.xfxQ(ScndpartonID,xa,PDFScale))*MSquareTotal*M/(math.cosh(y)**2*16*math.pi*shat**2))

    # Function to numerically integrate
    def Integrate(Func, args, N, a, b, x):
        value = 0
        for i in range(1, N+1):
            Y = a+((i-(1/2))*((b-a)/N))
            c = -(x - math.fabs(Y))
            d = x - math.fabs(Y)
            for j in range(1, N+1):
                y = c+((j-(1/2))*((d-c)/N))
                params = [Y, y]
                value += ((b-a)/N)*((d-c)/N)*Func(params, *args)
        return(value)
    
    # Number of integration slices
    MC = 5
    
    # Mass weighting
    DeltaMass = (MaxMass - MinMass)/Number
    
    # Assigning the parameters that are used in the LHE file
    IDBMUP = 2212              # Proton beams
    EBMUP  = COME/2            # Energy of each proton beam
    PDFGUP = 0
    PDFSUP = DistFunc.lhapdfID # ID of the PDF set
    IDWTUP = 3                 # Unweighted events
    XWGTUP = 1                 # Unweighted events
    NUP = 4                    # Number of particles
    
    # Finding the maximum cross sections
    # Max and min parameters
    tauMin = MinMass**2/s
    YmaxMin = min([math.log(1/math.sqrt(tauMin)), yMax])
    
    if(Ms < MinMass or Ms > MaxMass):
        Msss = MinMass
    else:
        Msss = Ms
       
    tauMax = Msss**2/s
    YmaxMax = min([math.log(1/math.sqrt(tauMax)), yMax])

    # Finding the minimum and maximum of the functions
    sumggggMin      = Integrate(MonteCarlogggg, (MinMass, 21, 21), MC, -YmaxMin, YmaxMin, yMax)

    sumggqqbarMin   = Integrate(MonteCarloggqqbar, (MinMass, 21, 21), MC, -YmaxMin, YmaxMin, yMax)

    sumgdgdMin = Integrate(MonteCarlogqgq, (MinMass, 21, 1), MC, -YmaxMin, YmaxMin, yMax)
    sumguguMin = Integrate(MonteCarlogqgq, (MinMass, 21, 2), MC, -YmaxMin, YmaxMin, yMax)
    sumgsgsMin = Integrate(MonteCarlogqgq, (MinMass, 21, 3), MC, -YmaxMin, YmaxMin, yMax)
    sumgcgcMin = Integrate(MonteCarlogqgq, (MinMass, 21, 4), MC, -YmaxMin, YmaxMin, yMax)
    sumgbgbMin = Integrate(MonteCarlogqgq, (MinMass, 21, 5), MC, -YmaxMin, YmaxMin, yMax)
    sumgtgtMin = Integrate(MonteCarlogqgq, (MinMass, 21, 6), MC, -YmaxMin, YmaxMin, yMax)

    sumgdbargdbarMin = Integrate(MonteCarlogqbargqbar, (MinMass, 21, -1), MC, -YmaxMin, YmaxMin, yMax)
    sumgubargubarMin = Integrate(MonteCarlogqbargqbar, (MinMass, 21, -2), MC, -YmaxMin, YmaxMin, yMax)
    sumgsbargsbarMin = Integrate(MonteCarlogqbargqbar, (MinMass, 21, -3), MC, -YmaxMin, YmaxMin, yMax)
    sumgcbargcbarMin = Integrate(MonteCarlogqbargqbar, (MinMass, 21, -4), MC, -YmaxMin, YmaxMin, yMax)
    sumgbbargbbarMin = Integrate(MonteCarlogqbargqbar, (MinMass, 21, -5), MC, -YmaxMin, YmaxMin, yMax)
    sumgtbargtbarMin = Integrate(MonteCarlogqbargqbar, (MinMass, 21, -6), MC, -YmaxMin, YmaxMin, yMax)

    sumddbarggMin = Integrate(MonteCarloqqbargg, (MinMass, 1, -1), MC, -YmaxMin, YmaxMin, yMax)
    sumuubarggMin = Integrate(MonteCarloqqbargg, (MinMass, 2, -2), MC, -YmaxMin, YmaxMin, yMax)
    sumssbarggMin = Integrate(MonteCarloqqbargg, (MinMass, 3, -3), MC, -YmaxMin, YmaxMin, yMax)
    sumccbarggMin = Integrate(MonteCarloqqbargg, (MinMass, 4, -4), MC, -YmaxMin, YmaxMin, yMax)
    sumbbbarggMin = Integrate(MonteCarloqqbargg, (MinMass, 5, -5), MC, -YmaxMin, YmaxMin, yMax)
    sumttbarggMin = Integrate(MonteCarloqqbargg, (MinMass, 6, -6), MC, -YmaxMin, YmaxMin, yMax)

    sumgggGammaMin   = Integrate(MonteCarlogggGamma, (MinMass, 21, 21), MC, -YmaxMin, YmaxMin, yMax)

    sumgdGammadMin  = Integrate(MonteCarlogqqGamma, (MinMass, 21, 1), MC, -YmaxMin, YmaxMin, yMax)
    sumguGammauMin  = Integrate(MonteCarlogqqGamma, (MinMass, 21, 2), MC, -YmaxMin, YmaxMin, yMax)
    sumgsGammasMin  = Integrate(MonteCarlogqqGamma, (MinMass, 21, 3), MC, -YmaxMin, YmaxMin, yMax)
    sumgcGammacMin  = Integrate(MonteCarlogqqGamma, (MinMass, 21, 4), MC, -YmaxMin, YmaxMin, yMax)
    sumgbGammabMin  = Integrate(MonteCarlogqqGamma, (MinMass, 21, 5), MC, -YmaxMin, YmaxMin, yMax)
    sumgtGammatMin  = Integrate(MonteCarlogqqGamma, (MinMass, 21, 6), MC, -YmaxMin, YmaxMin, yMax)

    sumggggMax      = Integrate(MonteCarlogggg, (Msss, 21, 21), MC, -YmaxMax, YmaxMax, yMax)

    sumggqqbarMax   = Integrate(MonteCarloggqqbar, (Msss, 21, 21), MC, -YmaxMax, YmaxMax, yMax)

    sumgdgdMax = Integrate(MonteCarlogqgq, (Msss, 21, 1), MC, -YmaxMax, YmaxMax, yMax)
    sumguguMax = Integrate(MonteCarlogqgq, (Msss, 21, 2), MC, -YmaxMax, YmaxMax, yMax)
    sumgsgsMax = Integrate(MonteCarlogqgq, (Msss, 21, 3), MC, -YmaxMax, YmaxMax, yMax)
    sumgcgcMax = Integrate(MonteCarlogqgq, (Msss, 21, 4), MC, -YmaxMax, YmaxMax, yMax)
    sumgbgbMax = Integrate(MonteCarlogqgq, (Msss, 21, 5), MC, -YmaxMax, YmaxMax, yMax)
    sumgtgtMax = Integrate(MonteCarlogqgq, (Msss, 21, 6), MC, -YmaxMax, YmaxMax, yMax)

    sumgdbargdbarMax = Integrate(MonteCarlogqbargqbar, (Msss, 21, -1), MC, -YmaxMax, YmaxMax, yMax)
    sumgubargubarMax = Integrate(MonteCarlogqbargqbar, (Msss, 21, -2), MC, -YmaxMax, YmaxMax, yMax)
    sumgsbargsbarMax = Integrate(MonteCarlogqbargqbar, (Msss, 21, -3), MC, -YmaxMax, YmaxMax, yMax)
    sumgcbargcbarMax = Integrate(MonteCarlogqbargqbar, (Msss, 21, -4), MC, -YmaxMax, YmaxMax, yMax)
    sumgbbargbbarMax = Integrate(MonteCarlogqbargqbar, (Msss, 21, -5), MC, -YmaxMax, YmaxMax, yMax)
    sumgtbargtbarMax = Integrate(MonteCarlogqbargqbar, (Msss, 21, -6), MC, -YmaxMax, YmaxMax, yMax)

    sumddbarggMax = Integrate(MonteCarloqqbargg, (Msss, 1, -1), MC, -YmaxMax, YmaxMax, yMax)
    sumuubarggMax = Integrate(MonteCarloqqbargg, (Msss, 2, -2), MC, -YmaxMax, YmaxMax, yMax)
    sumssbarggMax = Integrate(MonteCarloqqbargg, (Msss, 3, -3), MC, -YmaxMax, YmaxMax, yMax)
    sumccbarggMax = Integrate(MonteCarloqqbargg, (Msss, 4, -4), MC, -YmaxMax, YmaxMax, yMax)
    sumbbbarggMax = Integrate(MonteCarloqqbargg, (Msss, 5, -5), MC, -YmaxMax, YmaxMax, yMax)
    sumttbarggMax = Integrate(MonteCarloqqbargg, (Msss, 6, -6), MC, -YmaxMax, YmaxMax, yMax)

    sumgggGammaMax   = Integrate(MonteCarlogggGamma, (Msss, 21, 21), MC, -YmaxMax, YmaxMax, yMax)

    sumgdGammadMax  = Integrate(MonteCarlogqqGamma, (Msss, 21, 1), MC, -YmaxMax, YmaxMax, yMax)
    sumguGammauMax  = Integrate(MonteCarlogqqGamma, (Msss, 21, 2), MC, -YmaxMax, YmaxMax, yMax)
    sumgsGammasMax  = Integrate(MonteCarlogqqGamma, (Msss, 21, 3), MC, -YmaxMax, YmaxMax, yMax)
    sumgcGammacMax  = Integrate(MonteCarlogqqGamma, (Msss, 21, 4), MC, -YmaxMax, YmaxMax, yMax)
    sumgbGammabMax  = Integrate(MonteCarlogqqGamma, (Msss, 21, 5), MC, -YmaxMax, YmaxMax, yMax)
    sumgtGammatMax  = Integrate(MonteCarlogqqGamma, (Msss, 21, 6), MC, -YmaxMax, YmaxMax, yMax)

    CrossSectionMaxes = [max(sumggggMin, sumggggMax), max(sumggqqbarMin, sumggqqbarMax), max(sumgdgdMin, sumgdgdMax), max(sumguguMin, sumguguMax), max(sumgsgsMin, sumgsgsMax), max(sumgcgcMin, sumgcgcMax), max(sumgbgbMin, sumgbgbMax), max(sumgtgtMin, sumgtgtMax), max(sumgdbargdbarMin, sumgdbargdbarMax), max(sumgubargubarMin, sumgubargubarMax), max(sumgsbargsbarMin, sumgsbargsbarMax), max(sumgcbargcbarMin, sumgcbargcbarMax), max(sumgbbargbbarMin, sumgbbargbbarMax), max(sumgtbargtbarMin, sumgtbargtbarMax), max(sumddbarggMin, sumddbarggMax), max(sumuubarggMin, sumuubarggMax), max(sumssbarggMin, sumssbarggMax), max(sumccbarggMin, sumccbarggMax), max(sumbbbarggMin, sumbbbarggMax) ,max(sumttbarggMin, sumttbarggMax), max(sumgggGammaMin, sumgggGammaMax), max(sumgdGammadMin, sumgdGammadMax), max(sumguGammauMin, sumguGammauMax), max(sumgsGammasMin, sumgsGammasMax), max(sumgcGammacMin, sumgcGammacMax), max(sumgbGammabMin, sumgbGammabMax), max(sumgtGammatMin, sumgtGammatMax)]
        
    # Weights of the individual subprocesses for error calculation
    Weightgggg = 0
    Errorgggg  = 0

    Weightggqqbar = 0
    Errorggqqbar  = 0

    Weightgqgq = 0
    Errorgqgq  = 0

    Weightgqbargqbar = 0
    Errorgqbargqbar  = 0

    Weightqqbargg = 0
    Errorqqbargg  = 0

    WeightgggGamma = 0
    ErrorgggGamma  = 0

    WeightgqqGamma = 0
    ErrorgqqGamma  = 0
    
    # Total cross section
    TotalCrossSection = 0
 
    # Creating the LHE file for saving the events
    fh = open("events.lhe", "w")

    # Counting number of events total and of each type
    numberofevents = 0
    Ngggg = 0
    Nggqqbar = 0
    Ngqgq = 0
    Ngqbargqbar = 0
    Nqqbargg = 0
    NgggGamma = 0
    NgqqGamma = 0

    # Event generation loop
    while(numberofevents < Number):

        # A list that saves the weight of each subprocess at a random invariant mass. This is used to specify the type of subprocess
        CrossSections = []

        bol = 1

        while(bol == 1):

            # Random invariant mass in the specified interval
            M = random.uniform(MinMass, MaxMass)

            if(M == COME):
                break
            
            tau = M**2/s
            Ymax = min([math.log(1/math.sqrt(tau)), yMax])

            # Initial values for the calculation of the cross-sections of the subprocesses
            sumgggg      = Integrate(MonteCarlogggg, (M, 21, 21), MC, -Ymax, Ymax, yMax)

            sumggqqbar   = Integrate(MonteCarloggqqbar, (M, 21, 21), MC, -Ymax, Ymax, yMax)

            sumgdgd = Integrate(MonteCarlogqgq, (M, 21, 1), MC, -Ymax, Ymax, yMax)
            sumgugu = Integrate(MonteCarlogqgq, (M, 21, 2), MC, -Ymax, Ymax, yMax)
            sumgsgs = Integrate(MonteCarlogqgq, (M, 21, 3), MC, -Ymax, Ymax, yMax)
            sumgcgc = Integrate(MonteCarlogqgq, (M, 21, 4), MC, -Ymax, Ymax, yMax)
            sumgbgb = Integrate(MonteCarlogqgq, (M, 21, 5), MC, -Ymax, Ymax, yMax)
            sumgtgt = Integrate(MonteCarlogqgq, (M, 21, 6), MC, -Ymax, Ymax, yMax)

            sumgdbargdbar = Integrate(MonteCarlogqbargqbar, (M, 21, -1), MC, -Ymax, Ymax, yMax)
            sumgubargubar = Integrate(MonteCarlogqbargqbar, (M, 21, -2), MC, -Ymax, Ymax, yMax)
            sumgsbargsbar = Integrate(MonteCarlogqbargqbar, (M, 21, -3), MC, -Ymax, Ymax, yMax)
            sumgcbargcbar = Integrate(MonteCarlogqbargqbar, (M, 21, -4), MC, -Ymax, Ymax, yMax)
            sumgbbargbbar = Integrate(MonteCarlogqbargqbar, (M, 21, -5), MC, -Ymax, Ymax, yMax)
            sumgtbargtbar = Integrate(MonteCarlogqbargqbar, (M, 21, -6), MC, -Ymax, Ymax, yMax)

            sumddbargg = Integrate(MonteCarloqqbargg, (M, 1, -1), MC, -Ymax, Ymax, yMax)
            sumuubargg = Integrate(MonteCarloqqbargg, (M, 2, -2), MC, -Ymax, Ymax, yMax)
            sumssbargg = Integrate(MonteCarloqqbargg, (M, 3, -3), MC, -Ymax, Ymax, yMax)
            sumccbargg = Integrate(MonteCarloqqbargg, (M, 4, -4), MC, -Ymax, Ymax, yMax)
            sumbbbargg = Integrate(MonteCarloqqbargg, (M, 5, -5), MC, -Ymax, Ymax, yMax)
            sumttbargg = Integrate(MonteCarloqqbargg, (M, 6, -6), MC, -Ymax, Ymax, yMax)

            sumgggGamma   = Integrate(MonteCarlogggGamma, (M, 21, 21), MC, -Ymax, Ymax, yMax)

            sumgdGammad  = Integrate(MonteCarlogqqGamma, (M, 21, 1), MC, -Ymax, Ymax, yMax)
            sumguGammau  = Integrate(MonteCarlogqqGamma, (M, 21, 2), MC, -Ymax, Ymax, yMax)
            sumgsGammas  = Integrate(MonteCarlogqqGamma, (M, 21, 3), MC, -Ymax, Ymax, yMax)
            sumgcGammac  = Integrate(MonteCarlogqqGamma, (M, 21, 4), MC, -Ymax, Ymax, yMax)
            sumgbGammab  = Integrate(MonteCarlogqqGamma, (M, 21, 5), MC, -Ymax, Ymax, yMax)
            sumgtGammat  = Integrate(MonteCarlogqqGamma, (M, 21, 6), MC, -Ymax, Ymax, yMax)

            CrossSections = [sumgggg, sumggqqbar, sumgdgd, sumgugu, sumgsgs, sumgcgc, sumgbgb, sumgtgt, sumgdbargdbar, sumgubargubar, sumgsbargsbar, sumgcbargcbar, sumgbbargbbar, sumgtbargtbar, sumddbargg, sumuubargg, sumssbargg, sumccbargg, sumbbbargg, sumttbargg, sumgggGamma, sumgdGammad, sumguGammau, sumgsGammas, sumgcGammac, sumgbGammab, sumgtGammat]
            
            # Determination of the subprocess type
            CrossSectionsSum = [sum(CrossSections[:i+1]) for i in range(len(CrossSections))]
            
            RSig = random.uniform(0, CrossSectionsSum[-1])
            
            for i in range(len(CrossSections)):
                if(RSig < CrossSectionsSum[i]):
                    InteractionIndex = i
                    break
            
            RCrossSection = random.uniform(0, CrossSectionMaxes[InteractionIndex])
            if(RCrossSection > CrossSections[InteractionIndex]):
                break

            RandomY = random.uniform(-Ymax+10**-9, Ymax-10**-9)
            Randomy = random.uniform(-(yMax-math.fabs(RandomY)), (yMax-math.fabs(RandomY)))
            
            # Seven if statements for calculating the kinematic variables and filling the LHE files, corresponding to seven different subprocesses
            if(InteractionIndex == 0):
                
                MaximumAmplitude = MonteCarlogggg([0, 0], *(M, 21, 21))
                RAmplitude = random.uniform(0, MaximumAmplitude)
                ActualAmplitude = MonteCarlogggg([RandomY, Randomy], *(M, 21, 21))
                if(RAmplitude > ActualAmplitude):
                    break

                # Calculation of the kinematic variables of outgoing particles
                # ma = mb = 0
                # m1 = m2 = 0
                xa = math.sqrt(tau)*math.exp( RandomY)
                xb = math.sqrt(tau)*math.exp(-RandomY)
                Ea = xa*EBMUP
                Eb = xb*EBMUP
                y1 = RandomY + Randomy
                y2 = RandomY - Randomy
                pt = 0.5*M/math.cosh(Randomy)
                E1 = pt*math.cosh(y1)
                E2 = pt*math.cosh(y2)
                phi = random.uniform(0, 2*math.pi)
                px1 = pt*math.cos(phi)
                py1 = pt*math.sin(phi)
                px2 = -px1
                py2 = -py1
                pz1 = E1*math.tanh(y1)
                pz2 = E2*math.tanh(y2)
            
                # Cross section calculation
                Ngggg += 1
                weight = CrossSections[InteractionIndex]*(10**9)*0.389379*DeltaMass
                Weightgggg += weight
                Errorgggg += weight**2
                TotalCrossSection += weight
                
                # Filling the LHE file
                fh.write("<event>\n")
                fh.write("{}  {}  {}  {}  {} {}\n".format(NUP, 1, XWGTUP, PDFScale, QED, alpha3))
                fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,101,102,0,0,Ea,Ea,0,0,9))
                fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,102,103,0,0,-Eb,Eb,0,0,9))
                fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,101,104,px1,py1,pz1,E1,0,0,9))
                fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,104,103,px2,py2,pz2,E2,0,0,9))
                fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(21,21,xa,xb,PDFScale,DistFunc.xfxQ(21,xa,PDFScale),DistFunc.xfxQ(21,xb,PDFScale)))
                fh.write("</event>\n")
                
                numberofevents += 1
                if(numberofevents%50   == 0): print(".")
                if(numberofevents%1000 == 0): print("\n{} Events are Generated\n".format(numberofevents))
                break
            
            elif(InteractionIndex == 1):
                IDQ = random.randint(1,6)
                Qmass = QuarkMasses[IDQ - 1]
            
                MaximumAmplitude = MonteCarloggqqbar([0, 0], *(M, 21, 21))
                RAmplitude = random.uniform(0, MaximumAmplitude)
                ActualAmplitude = MonteCarloggqqbar([RandomY, Randomy], *(M, 21, 21))
                if(RAmplitude > ActualAmplitude):
                    break

                # Calculation of the kinematic variables of outgoing particles
                # ma = mb = 0
                # m1 = m2 = Qmass
                xa = math.sqrt(tau)*math.exp( RandomY)
                xb = math.sqrt(tau)*math.exp(-RandomY)
                Ea = xa*EBMUP
                Eb = xb*EBMUP
                y1 = RandomY + Randomy
                y2 = RandomY - Randomy
                phi = random.uniform(0, 2*math.pi)
                pt = 0.5/math.cosh(Randomy)*math.sqrt(M**2-4*Qmass**2*math.cosh(Randomy)**2)
                E1 = math.sqrt(Qmass**2+pt**2)*math.cosh(y1)
                E2 = math.sqrt(Qmass**2+pt**2)*math.cosh(y2)
                px1 = pt*math.cos(phi)
                py1 = pt*math.sin(phi)
                px2 = -px1
                py2 = -py1
                pz1 = E1*math.tanh(y1)
                pz2 = E2*math.tanh(y2)
            
                # Cross section calculation
                Nggqqbar += 1
                weight = CrossSections[InteractionIndex]*(10**9)*0.389379*DeltaMass
                Weightggqqbar += weight
                Errorggqqbar += weight**2
                TotalCrossSection += weight

                # Filling the LHE file
                X = random.uniform(0, 1)
                fh.write("<event>\n")
                fh.write("{}  {}  {}  {}  {} {}\n".format(NUP, 2, XWGTUP, PDFScale, QED, alpha3))
                if(X <= 0.5):
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,101,102,0,0,Ea,Ea,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,102,103,0,0,-Eb,Eb,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,1,1,2,101,0,px1,py1,pz1,E1,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,1,1,2,0,103,px2,py2,pz2,E2,Qmass,0,9))
                else:
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,102,101,0,0,Ea,Ea,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,103,102,0,0,-Eb,Eb,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,1,1,2,0,101,px1,py1,pz1,E1,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,1,1,2,103,0,px2,py2,pz2,E2,Qmass,0,9))
                fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(21,21,xa,xb,PDFScale,DistFunc.xfxQ(21,xa,PDFScale),DistFunc.xfxQ(21,xb,PDFScale)))
                fh.write("</event>\n")
            
                numberofevents += 1
                if(numberofevents%50   == 0): print(".")
                if(numberofevents%1000 == 0): print("\n{} Events are Generated\n".format(numberofevents))
                break
            
            elif(InteractionIndex == 2 or InteractionIndex == 3 or InteractionIndex == 4 or InteractionIndex == 5 or InteractionIndex == 6 or InteractionIndex == 7):
                IDQ = InteractionIndex - 1
                Qmass = QuarkMasses[IDQ - 1]
            
                MaximumAmplitude = MonteCarlogqgq([0, 0], *(M, 21, IDQ))
                RAmplitude = random.uniform(0, MaximumAmplitude)
                ActualAmplitude = MonteCarlogqgq([RandomY, Randomy], *(M, 21, IDQ))
                if(RAmplitude > ActualAmplitude):
                    break
                
                # Calculation of the kinematic variables of outgoing particles
                # ma = 0, mb = Qmass or ma = Qmass, mb = 0
                # m1 = 0, m2 = Qmass or m1 = Qmass, m2 = 0
                that = -0.5*M**2*math.exp(-Randomy)/math.cosh(Randomy)
                uhat = -0.5*M**2*math.exp( Randomy)/math.cosh(Randomy)
                xi31 = math.sqrt(uhat/that)                             # ma = 0, mb = Qmass
                xi41 = math.sqrt((that - Qmass**2)/(uhat - Qmass**2))
                xa1 = math.exp(RandomY)*math.sqrt(tau/(xi31*xi41))
                xb1 = math.exp(-RandomY)*math.sqrt(tau*xi31*xi41)
                Ea1 = xa1*EBMUP
                Eb1 = xb1*EBMUP
                y1 = RandomY + Randomy
                y2 = RandomY - Randomy
                d = ((2*(M**2))/((math.cosh(2*Randomy)**2)-1))
                c = ((2*(Qmass**2))/((math.cosh(2*Randomy)**2)-1))
                b = ((2*(Qmass**2)*((math.cosh(2*Randomy))**2))/((math.cosh(2*Randomy)**2)-1))
                a = (math.sqrt(2)*math.sqrt((math.cosh(2*Randomy)**2)*((Qmass**4)*math.cosh(4*Randomy)-(Qmass**4)+2*(M**4))))/((math.cosh(2*Randomy)**2)-1)
                pt = 0.5*math.sqrt(a-b+c-d)
                E11 = pt*math.cosh(y1)                                  # m1 = 0, m2 = Qmass
                E21 = math.sqrt(Qmass**2+pt**2)*math.cosh(y2)
                phi = random.uniform(0, 2*math.pi)
                px1 = pt*math.cos(phi)
                py1 = pt*math.sin(phi)
                px2 = -px1
                py2 = -py1
                pz11 = E11*math.tanh(y1)
                pz21 = E21*math.tanh(y2)
            
                xi32 = math.sqrt((uhat - Qmass**2)/(that - Qmass**2))   # ma = Qmass, mb = 0
                xi42 = math.sqrt(that/uhat)
                xa2 = math.exp(RandomY)*math.sqrt(tau/(xi32*xi42))
                xb2 = math.exp(-RandomY)*math.sqrt(tau*xi32*xi42)
                Ea2 = xa2*EBMUP
                Eb2 = xb2*EBMUP
                E12 = math.sqrt(Qmass**2+pt**2)*math.cosh(y1)           # m1 = Qmass, m2 = 0
                E22 = pt*math.cosh(y2)
                pz12 = E12*math.tanh(y1)
                pz22 = E22*math.tanh(y2)
            
                # Cross section calculation
                Ngqgq += 1
                weight = CrossSections[InteractionIndex]*(10**9)*0.389379*DeltaMass
                Weightgqgq += weight
                Errorgqgq += weight**2
                TotalCrossSection += weight

                # Filling the LHE file
                X = random.uniform(0, 1)
                fh.write("<event>\n")
                fh.write("{}  {}  {}  {}  {} {}\n".format(NUP, 3, XWGTUP, PDFScale, QED, alpha3))
                if(X <= 0.25):
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,102,101,0,0,Ea1,Ea1,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,-1,0,0,101,0,0,0,-Eb1,Eb1,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,102,103,px1,py1,pz11,E11,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,1,1,2,103,0,px2,py2,pz21,E21,Qmass,0,9))
                    fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(21,IDQ,xa1,xb1,PDFScale,DistFunc.xfxQ(21,xa1,PDFScale),DistFunc.xfxQ(IDQ,xb1,PDFScale)))
                elif(X <= 0.5):
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,102,101,0,0,Ea1,Ea1,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,-1,0,0,101,0,0,0,-Eb1,Eb1,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,102,103,px2,py2,pz22,E22,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,1,1,2,103,0,px1,py1,pz12,E12,Qmass,0,9))
                    fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(21,IDQ,xa1,xb1,PDFScale,DistFunc.xfxQ(21,xa1,PDFScale),DistFunc.xfxQ(IDQ,xb1,PDFScale)))
                elif(X <= 0.75):
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,-1,0,0,101,0,0,0,Ea2,Ea2,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,104,101,0,0,-Eb2,Eb2,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,1,1,2,103,0,px2,py2,pz21,E21,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,104,103,px1,py1,pz11,E11,0,0,9))
                    fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,21,xa2,xb2,PDFScale,DistFunc.xfxQ(IDQ,xa2,PDFScale),DistFunc.xfxQ(21,xb2,PDFScale)))
                else:
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,-1,0,0,101,0,0,0,Ea2,Ea2,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,104,101,0,0,-Eb2,Eb2,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,1,1,2,103,0,px1,py1,pz12,E12,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,104,103,px2,py2,pz22,E22,0,0,9))
                    fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,21,xa2,xb2,PDFScale,DistFunc.xfxQ(IDQ,xa2,PDFScale),DistFunc.xfxQ(21,xb2,PDFScale)))
		fh.write("</event>\n")
            
                numberofevents += 1
                if(numberofevents%50   == 0): print(".")
                if(numberofevents%1000 == 0): print("\n{} Events are Generated\n".format(numberofevents))
                break
            
            elif(InteractionIndex == 8 or InteractionIndex == 9 or InteractionIndex == 10 or InteractionIndex == 11 or InteractionIndex == 12 or InteractionIndex == 13):
                IDQ = InteractionIndex - 7
                Qmass = QuarkMasses[IDQ - 1]
            
                MaximumAmplitude = MonteCarlogqbargqbar([0, 0], *(M, 21, -IDQ))
                RAmplitude = random.uniform(0, MaximumAmplitude)
                ActualAmplitude = MonteCarlogqbargqbar([RandomY, Randomy], *(M, 21, -IDQ))
                if(RAmplitude > ActualAmplitude):
                    break
            
                # Calculation of the kinematic variables of outgoing particles
                # ma = 0, mb = Qmass or ma = Qmass, mb = 0
                # m1 = 0, m2 = Qmass or m1 = Qmass, m2 = 0
                that = -0.5*M**2*math.exp(-Randomy)/math.cosh(Randomy)
                uhat = -0.5*M**2*math.exp( Randomy)/math.cosh(Randomy)
                xi31 = math.sqrt(uhat/that)                             # ma = 0, mb = Qmass
                xi41 = math.sqrt((that - Qmass**2)/(uhat - Qmass**2))
                xa1 = math.exp(RandomY)*math.sqrt(tau/(xi31*xi41))
                xb1 = math.exp(-RandomY)*math.sqrt(tau*xi31*xi41)
                Ea1 = xa1*EBMUP
                Eb1 = xb1*EBMUP
                y1 = RandomY + Randomy
                y2 = RandomY - Randomy
                d = ((2*(M**2))/((math.cosh(2*Randomy)**2)-1))
                c = ((2*(Qmass**2))/((math.cosh(2*Randomy)**2)-1))
                b = ((2*(Qmass**2)*((math.cosh(2*Randomy))**2))/((math.cosh(2*Randomy)**2)-1))
                a = (math.sqrt(2)*math.sqrt((math.cosh(2*Randomy)**2)*((Qmass**4)*math.cosh(4*Randomy)-(Qmass**4)+2*(M**4))))/((math.cosh(2*Randomy)**2)-1)
                pt = 0.5*math.sqrt(a-b+c-d)
                E11 = pt*math.cosh(y1)                                  # m1 = 0, m2 = Qmass
                E21 = math.sqrt(Qmass**2+pt**2)*math.cosh(y2)
                phi = random.uniform(0, 2*math.pi)
                px1 = pt*math.cos(phi)
                py1 = pt*math.sin(phi)
                px2 = -px1
                py2 = -py1
                pz11 = E11*math.tanh(y1)
                pz21 = E21*math.tanh(y2)
            
                xi32 = math.sqrt((uhat - Qmass**2)/(that - Qmass**2))   # ma = Qmass, mb = 0
                xi42 = math.sqrt(that/uhat)
                xa2 = math.exp(RandomY)*math.sqrt(tau/(xi32*xi42))
                xb2 = math.exp(-RandomY)*math.sqrt(tau*xi32*xi42)
                Ea2 = xa2*EBMUP
                Eb2 = xb2*EBMUP
                E12 = math.sqrt(Qmass**2+pt**2)*math.cosh(y1)           # m1 = Qmass, m2 = 0
                E22 = pt*math.cosh(y2)
                pz12 = E12*math.tanh(y1)
                pz22 = E22*math.tanh(y2)
            
                # Cross section calculation
                Ngqbargqbar += 1
                weight = CrossSections[InteractionIndex]*(10**9)*0.389379*DeltaMass
                Weightgqbargqbar += weight
                Errorgqbargqbar += weight**2
                TotalCrossSection += weight

                # Filling the LHE file
                X = random.uniform(0, 1)
                fh.write("<event>\n")
                fh.write("{}  {}  {}  {}  {} {}\n".format(NUP, 4, XWGTUP, PDFScale, QED, alpha3))
                if(X <= 0.25):
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,102,101,0,0,Ea1,Ea1,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,-1,0,0,0,102,0,0,-Eb1,Eb1,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,103,101,px1,py1,pz11,E11,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,1,1,2,0,103,px2,py2,pz21,E21,Qmass,0,9))
                    fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(21,-IDQ,xa1,xb1,PDFScale,DistFunc.xfxQ(21,xa1,PDFScale),DistFunc.xfxQ(-IDQ,xb1,PDFScale)))
                elif(X <= 0.5):
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,102,101,0,0,Ea1,Ea1,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,-1,0,0,0,102,0,0,-Eb1,Eb1,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,103,101,px2,py2,pz22,E22,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,1,1,2,0,103,px1,py1,pz12,E12,Qmass,0,9))
                    fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(21,-IDQ,xa1,xb1,PDFScale,DistFunc.xfxQ(21,xa1,PDFScale),DistFunc.xfxQ(-IDQ,xb1,PDFScale)))
                elif(X <= 0.75):
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,-1,0,0,0,102,0,0,Ea2,Ea2,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,102,103,0,0,-Eb2,Eb2,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,1,1,2,0,104,px2,py2,pz21,E21,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,104,103,px1,py1,pz11,E11,0,0,9))
                    fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,21,xa2,xb2,PDFScale,DistFunc.xfxQ(-IDQ,xa2,PDFScale),DistFunc.xfxQ(21,xb2,PDFScale)))
                else:
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,-1,0,0,0,102,0,0,Ea2,Ea2,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,102,103,0,0,-Eb2,Eb2,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,1,1,2,0,104,px1,py1,pz12,E12,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,104,103,px2,py2,pz22,E22,0,0,9))
                    fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,21,xa2,xb2,PDFScale,DistFunc.xfxQ(-IDQ,xa2,PDFScale),DistFunc.xfxQ(21,xb2,PDFScale)))
		fh.write("</event>\n")
            
                numberofevents += 1
                if(numberofevents%50   == 0): print(".")
                if(numberofevents%1000 == 0): print("\n{} Events are Generated\n".format(numberofevents))
                break

            elif(InteractionIndex == 14 or InteractionIndex == 15 or InteractionIndex == 16 or InteractionIndex == 17 or InteractionIndex == 18 or InteractionIndex == 19):
                IDQ = InteractionIndex - 13
                Qmass = QuarkMasses[IDQ - 1]
            
                MaximumAmplitude = MonteCarloqqbargg([0, 0], *(M, IDQ, -IDQ))
                RAmplitude = random.uniform(0, MaximumAmplitude)
                ActualAmplitude = MonteCarloqqbargg([RandomY, Randomy], *(M, IDQ, -IDQ))
                if(RAmplitude > ActualAmplitude):
                    break
            
                # Calculation of the kinematic variables of outgoing particles
                # ma = mb = Qmass
                # m1 = m2 = 0
                xa = math.sqrt(tau)*math.exp( RandomY)
                xb = math.sqrt(tau)*math.exp(-RandomY)
                Ea = xa*EBMUP
                Eb = xb*EBMUP
                y1 = RandomY + Randomy
                y2 = RandomY - Randomy
                pt = 0.5*M/math.cosh(Randomy)
                E1 = pt*math.cosh(y1)
                E2 = pt*math.cosh(y2)
                phi = random.uniform(0, 2*math.pi)
                px1 = pt*math.cos(phi)
                py1 = pt*math.sin(phi)
                px2 = -px1
                py2 = -py1
                pz1 = E1*math.tanh(y1)
                pz2 = E2*math.tanh(y2)
            
                # Cross section calculation
                Nqqbargg += 1
                weight = CrossSections[InteractionIndex]*(10**9)*0.389379*DeltaMass
                Weightqqbargg += weight
                Errorqqbargg += weight**2
                TotalCrossSection += weight

                # Filling the LHE file
                X = random.uniform(0, 1)
                fh.write("<event>\n")
                fh.write("{}  {}  {}  {}  {} {}\n".format(NUP, 5, XWGTUP, PDFScale, QED, alpha3))
                if(X >= 0.5):
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,-1,0,0,101,0,0,0,Ea,Ea,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,-1,0,0,0,103,0,0,-Eb,Eb,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,101,104,px1,py1,pz1,E1,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,104,103,px2,py2,pz2,E2,0,0,9))
                    fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,-IDQ,xa,xb,PDFScale,DistFunc.xfxQ(IDQ,xa,PDFScale),DistFunc.xfxQ(-IDQ,xb,PDFScale)))
                else:
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,-1,0,0,0,101,0,0,Ea,Ea,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,-1,0,0,103,0,0,0,-Eb,Eb,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,104,101,px1,py1,pz1,E1,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,103,104,px2,py2,pz2,E2,0,0,9))
                    fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(-IDQ,IDQ,xa,xb,PDFScale,DistFunc.xfxQ(-IDQ,xa,PDFScale),DistFunc.xfxQ(IDQ,xb,PDFScale)))
                fh.write("</event>\n")
            
                numberofevents += 1
                if(numberofevents%50   == 0): print(".")
                if(numberofevents%1000 == 0): print("\n{} Events are Generated\n".format(numberofevents))
                break

            elif(InteractionIndex == 20):
                MaximumAmplitude = MonteCarlogggGamma([0, 0], *(M, 21, 21))
                RAmplitude = random.uniform(0, MaximumAmplitude)
                ActualAmplitude = MonteCarlogggGamma([RandomY, Randomy], *(M, 21, 21))
                if(RAmplitude > ActualAmplitude):
                    break
            
                # Calculation of the kinematic variables of outgoing particles
                # ma = mb = 0
                # m1 = m2 = 0
                xa = math.sqrt(tau)*math.exp( RandomY)
                xb = math.sqrt(tau)*math.exp(-RandomY)
                Ea = xa*EBMUP
                Eb = xb*EBMUP
                y1 = RandomY + Randomy
                y2 = RandomY - Randomy
                pt = 0.5*M/math.cosh(Randomy)
                E1 = pt*math.cosh(y1)
                E2 = pt*math.cosh(y2)
                phi = random.uniform(0, 2*math.pi)
                px1 = pt*math.cos(phi)
                py1 = pt*math.sin(phi)
                px2 = -px1
                py2 = -py1
                pz1 = E1*math.tanh(y1)
                pz2 = E2*math.tanh(y2)
                
                # Cross section calculation
                NgggGamma += 1
                weight = CrossSections[InteractionIndex]*(10**9)*0.389379*DeltaMass
                WeightgggGamma += weight
                ErrorgggGamma += weight**2
                TotalCrossSection += weight

                # Filling the LHE file
                X = random.uniform(0, 1)
                fh.write("<event>\n")
                fh.write("{}  {}  {}  {}  {} {}\n".format(NUP, 6, XWGTUP, PDFScale, QED, alpha3))
                if(X <= 0.5):
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,102,101,0,0,Ea,Ea,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,103,102,0,0,-Eb,Eb,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,103,101,px1,py1,pz1,E1,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(22,1,1,2,0,0,px2,py2,pz2,E2,0,0,9))
                else:
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,102,101,0,0,Ea,Ea,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,103,102,0,0,-Eb,Eb,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(22,1,1,2,0,0,px1,py1,pz1,E1,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,1,1,2,103,101,px2,py2,pz2,E2,0,0,9))
                fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(21,21,xa,xb,PDFScale,DistFunc.xfxQ(21,xa,PDFScale),DistFunc.xfxQ(21,xb,PDFScale)))
                fh.write("</event>\n")
            
                numberofevents += 1
                if(numberofevents%50   == 0): print(".")
                if(numberofevents%1000 == 0): print("\n{} Events are Generated\n".format(numberofevents))
                break

            elif(InteractionIndex < 27):
                IDQ = InteractionIndex - 20
                Qmass = QuarkMasses[IDQ - 1]
                
                MaximumAmplitude = MonteCarlogqqGamma([0, 0], *(M, 21, IDQ))
                RAmplitude = random.uniform(0, MaximumAmplitude)
                ActualAmplitude = MonteCarlogqqGamma([RandomY, Randomy], *(M, 21, IDQ))
                if(RAmplitude > ActualAmplitude):
                    break
                
                # Calculation of the kinematic variables of outgoing particles
                # ma = 0, mb = Qmass or ma = Qmass, mb = 0
                # m1 = 0, m2 = Qmass or m1 = Qmass, m2 = 0
                that = -0.5*M**2*math.exp(-Randomy)/math.cosh(Randomy)
                uhat = -0.5*M**2*math.exp( Randomy)/math.cosh(Randomy)
                xi31 = math.sqrt(uhat/that)                             # ma = 0, mb = Qmass
                xi41 = math.sqrt((that - Qmass**2)/(uhat - Qmass**2))
                xa1 = math.exp(RandomY)*math.sqrt(tau/(xi31*xi41))
                xb1 = math.exp(-RandomY)*math.sqrt(tau*xi31*xi41)
                Ea1 = xa1*EBMUP
                Eb1 = xb1*EBMUP
                y1 = RandomY + Randomy
                y2 = RandomY - Randomy
                d = ((2*(M**2))/((math.cosh(2*Randomy)**2)-1))
                c = ((2*(Qmass**2))/((math.cosh(2*Randomy)**2)-1))
                b = ((2*(Qmass**2)*((math.cosh(2*Randomy))**2))/((math.cosh(2*Randomy)**2)-1))
                a = (math.sqrt(2)*math.sqrt((math.cosh(2*Randomy)**2)*((Qmass**4)*math.cosh(4*Randomy)-(Qmass**4)+2*(M**4))))/((math.cosh(2*Randomy)**2)-1)
                pt = 0.5*math.sqrt(a-b+c-d)
                E11 = pt*math.cosh(y1)                                  # m1 = 0, m2 = Qmass
                E21 = math.sqrt(Qmass**2+pt**2)*math.cosh(y2)
                phi = random.uniform(0, 2*math.pi)
                px1 = pt*math.cos(phi)
                py1 = pt*math.sin(phi)
                px2 = -px1
                py2 = -py1
                pz11 = E11*math.tanh(y1)
                pz21 = E21*math.tanh(y2)
            
                xi32 = math.sqrt((uhat - Qmass**2)/(that - Qmass**2))   # ma = Qmass, mb = 0
                xi42 = math.sqrt(that/uhat)
                xa2 = math.exp(RandomY)*math.sqrt(tau/(xi32*xi42))
                xb2 = math.exp(-RandomY)*math.sqrt(tau*xi32*xi42)
                Ea2 = xa2*EBMUP
                Eb2 = xb2*EBMUP
                E12 = math.sqrt(Qmass**2+pt**2)*math.cosh(y1)           # m1 = Qmass, m2 = 0
                E22 = pt*math.cosh(y2)
                pz12 = E12*math.tanh(y1)
                pz22 = E22*math.tanh(y2)
            
                # Cross section calculation
                NgqqGamma += 1
                weight = CrossSections[InteractionIndex]*(10**9)*0.389379*DeltaMass
                WeightgqqGamma += weight
                ErrorgqqGamma += weight**2
                TotalCrossSection += weight

                # Filling the LHE file
                X = random.uniform(0, 1)
                fh.write("<event>\n")
                fh.write("{}  {}  {}  {}  {} {}\n".format(NUP, 7, XWGTUP, PDFScale, QED, alpha3))
                if(X <= 0.5):
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,101,102,0,0,Ea2,Ea2,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,-1,0,0,102,0,0,0,-Eb2,Eb2,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,1,1,2,101,0,px1,py1,pz12,E12,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(22,1,1,2,0,0,px2,py2,pz22,E22,0,0,9))
                    fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(21,IDQ,xa1,xb1,PDFScale,DistFunc.xfxQ(21,xa1,PDFScale),DistFunc.xfxQ(IDQ,xb1,PDFScale)))
                else:
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,-1,0,0,102,0,0,0,Ea1,Ea1,Qmass,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(21,-1,0,0,103,102,0,0,-Eb1,Eb1,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(22,1,1,2,0,0,px1,py1,pz11,E11,0,0,9))
                    fh.write("{}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,1,1,2,103,0,px2,py2,pz21,E21,Qmass,0,9))
                    fh.write("#pdf  {}  {}  {}  {}  {}  {}  {}\n".format(IDQ,21,xa2,xb2,PDFScale,DistFunc.xfxQ(IDQ,xa2,PDFScale),DistFunc.xfxQ(21,xb2,PDFScale)))
                fh.write("<event>\n")
            
                numberofevents += 1
                if(numberofevents%50   == 0): print(".")
                if(numberofevents%1000 == 0): print("\n{} Events are Generated\n".format(numberofevents))
                break

    fh.write("</LesHouchesEvents>")
    fh.close()

    print("\nFinalizing...\n")
    
    # Calculating cross sections
    CrossSectiongggg = TotalCrossSection*Ngggg/Number
    CrossSectionggqqbar = TotalCrossSection*Nggqqbar/Number
    CrossSectiongqgq = TotalCrossSection*Ngqgq/Number
    CrossSectiongqbargqbar = TotalCrossSection*Ngqbargqbar/Number
    CrossSectionqqbargg = TotalCrossSection*Nqqbargg/Number
    CrossSectiongggGamma = TotalCrossSection*NgggGamma/Number
    CrossSectiongqqGamma = TotalCrossSection*NgqqGamma/Number
    
    # Calculating the error in the cross sections
    ggggStandardError           = math.sqrt(math.fabs(Number*Errorgggg - Weightgggg**2))/math.sqrt(Number)
    gqgqStandardError           = math.sqrt(math.fabs(Number*Errorgqgq - Weightgqgq**2))/math.sqrt(Number)
    ggqqbarStandardError        = math.sqrt(math.fabs(Number*Errorggqqbar - Weightggqqbar**2))/math.sqrt(Number)
    gqbargqbarStandardError     = math.sqrt(math.fabs(Number*Errorgqbargqbar - Weightgqbargqbar**2))/math.sqrt(Number)
    qqbarggStandardError        = math.sqrt(math.fabs(Number*Errorqqbargg - Weightqqbargg**2))/math.sqrt(Number)
    ggGammaStandardError        = math.sqrt(math.fabs(Number*ErrorgggGamma - WeightgggGamma**2))/math.sqrt(Number)
    gqGammaStandardError        = math.sqrt(math.fabs(Number*ErrorgqqGamma - WeightgqqGamma**2))/math.sqrt(Number)
        
    # Printing the Calculated cross-sections on the screen
    print("{0:<20}{1:<25}{2:<30}".format('SubProcess', 'ID', 'Cross-Section (pb)'))
    if(gg2gg11 == 1):
        print("{0:<20}{1:<25}{2:<30}".format('gg2gg', '1', CrossSectiongggg))
    if(gg2qqbar11 == 1):
        print("{0:<20}{1:<25}{2:<30}".format('gg2qqbar', '2', CrossSectionggqqbar))
    if(gq2gq11 == 1):
        print("{0:<20}{1:<25}{2:<30}".format('gq2gq', '3', CrossSectiongqgq))
    if(gqbar2gqbar11 == 1):
        print("{0:<20}{1:<25}{2:<30}".format('gqbar2gqbar', '4', CrossSectiongqbargqbar))
    if(qqbar2gg11 == 1):
        print("{0:<20}{1:<25}{2:<30}".format('qqbar2gg', '5', CrossSectionqqbargg))
    if(gg2gGamma11 == 1):
        print("{0:<20}{1:<25}{2:<30}".format('gg2gGamma', '6', CrossSectiongggGamma))
    if(gq2qGamma11 == 1):
        print("{0:<20}{1:<25}{2:<30}".format('gq2qGamma', '7', CrossSectiongqqGamma))

    print("\n")
    print("{0:<45}{1:<65}".format('Total Cross-Section (pb)', TotalCrossSection))
    
    # Writing the input parameters to the LHE file
    fh = open("begin.lhe", "w")
        
    fh.write("<LesHouchesEvents version=\"%.1f\">\n" % 1.0)
    fh.write("<!--\n")
    fh.write("  File Written by STRINGS - Version 2.00, May 2020\n")
    fh.write("  Generator by Fairhurst Lyons, Pourya Vakilipourtakalou, and Douglas M. Gingrich\n")
    fh.write("  Parameters:\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(RandGenSEED, 'RandGenSEED', 'Seed for the the Random Number Generator'))
    fh.write("\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(COME, 'COME', 'Centre of Mass Energy (GeV)'))
    fh.write("\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(Number, 'Number', 'Number of Events'))
    fh.write("\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(Ms, 'Ms', 'String Scale (GeV)'))
    fh.write("\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(MinMass, 'MinMass', 'Minimum Invariant Mass (GeV)'))
    fh.write("\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(MaxMass, 'MaxMass', 'Maximum Invariant Mass (GeV)'))
    fh.write("\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(yMax, 'yMax', 'Upper Bound for the Rapidity of the Outgoing Partons'))
    fh.write("\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(PDFSet, 'PDFSet', 'PDF Set of the LHAPDF'))
    fh.write("\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(PDFScale, 'PDFScale', 'Scale at Which the PDF Set is Evaluated (GeV)'))
    fh.write("\n")
    if(Coupling == -1):
        fh.write("  {0:<10}{1:<22}{2:<30}".format(Coupling, 'Coupling', 'Running Coupling Constant (alpha_s without 4*pi Factor)'))
        fh.write("\n")
        fh.write("  {0:<10}{1:<22}{2:<30}".format(CouplingScale, 'CouplingScale', 'Scale at Which the Running Coupling is Calculated (GeV)'))
        fh.write("\n")
    else:
        fh.write("  {0:<10}{1:<22}{2:<30}".format(Coupling, 'Coupling', 'Coupling Constant (alpha_s without 4*pi Factor)'))
        fh.write("\n")
    
        fh.write("  {0:<10}{1:<22}{2:<30}".format(dMass, 'dMass', 'Mass of the Down Quark (GeV)'))
    fh.write("\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(uMass, 'uMass', 'Mass of the Up Quark (GeV)'))
    fh.write("\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(sMass, 'sMass', 'Mass of the Strange Quark (GeV)'))
    fh.write("\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(cMass, 'cMass', 'Mass of the Charm Quark (GeV)'))
    fh.write("\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(bMass, 'bMass', 'Mass of the Bottom Quark (GeV)'))
    fh.write("\n")
    fh.write("  {0:<10}{1:<22}{2:<30}".format(tMass, 'tMass', 'Mass of the Top Quark (GeV)'))
    fh.write("\n")
    
    if(QCDCoeff11 == 1):
        fh.write("  {0:<10}{1:<22}{2:<30}".format(QCDCoeff, 'QCDCoeff', '(Enabled)  Production of QCD tree-level diparton'))
        fh.write("\n")
    else:
        fh.write("  {0:<10}{1:<22}{2:<30}".format(QCDCoeff, 'QCDCoeff', '(Disabled) Production of QCD tree-level diparton'))
        fh.write("\n")
    if(StringCoeff11 == 1):
        fh.write("  {0:<10}{1:<22}{2:<30}".format(StringCoeff, 'FirstStringCoeff', '(Enabled)  Production of First  String Resonance ( 2 --> 2 Partonic Scattering and 2-Parton --> Parton-Gamma Scattering )'))
        fh.write("\n")
    else:
        fh.write("  {0:<10}{1:<22}{2:<30}".format(StringCoeff, 'FirstStringCoeff', '(Disabled) Production of First  String Resonance  ( 2 --> 2 Partonic Scattering and 2-Parton --> Parton-Gamma Scattering )'))
        fh.write("\n")
    if(SecondStringCoeff11 == 1):
        fh.write("  {0:<10}{1:<22}{2:<30}".format(SecondStringCoeff, 'SecondStringCoeff', '(Enabled)  Production of Second String Resonance ( 2 --> 2 Partonic Scattering )'))
        fh.write("\n")
    else:
        fh.write("  {0:<10}{1:<22}{2:<30}".format(SecondStringCoeff, 'SecondStringCoeff', '(Disabled) Production of Second String Resonance ( 2 --> 2 Partonic Scattering )'))
        fh.write("\n")
    if(gg2gg11 == 1):
        fh.write("  {0:<10}{1:<22}{2:<30}".format(gg2gg, 'gg2gg', '(Enabled)  gg --> gg Subprocess       (ID = 1)'))
        fh.write("\n")
    else:
        fh.write("  {0:<10}{1:<22}{2:<30}".format(gg2gg, 'gg2gg', '(Disabled) gg --> gg Subprocess       (ID = 1)'))
        fh.write("\n")
    if(gg2qqbar11 == 1):
        fh.write("  {0:<10}{1:<22}{2:<30}".format(gg2qqbar, 'gg2qqbar', '(Enabled)  gg --> qqbar Subprocess    (ID = 2)'))
        fh.write("\n")
    else:
        fh.write("  {0:<10}{1:<22}{2:<30}".format(gg2qqbar, 'gg2qqbar', '(Disabled) gg --> qqbar Subprocess    (ID = 2)'))
        fh.write("\n")
    if(gq2gq11 == 1):
        fh.write("  {0:<10}{1:<22}{2:<30}".format(gq2gq, 'gq2gq', '(Enabled)  gq --> gq Subprocess       (ID = 3)'))
        fh.write("\n")
    else:
        fh.write("  {0:<10}{1:<22}{2:<30}".format(gq2gq, 'gq2gq', '(Disabled) gq --> gq Subprocess       (ID = 3)'))
        fh.write("\n")
    if(gqbar2gqbar11 == 1):
        fh.write("  {0:<10}{1:<22}{2:<30}".format(gqbar2gqbar, 'gqbar2gqbar', '(Enabled)  gqbar --> gqbar Subprocess (ID = 4)'))
        fh.write("\n")
    else:
        fh.write("  {0:<10}{1:<22}{2:<30}".format(gqbar2gqbar, 'gqbar2gqbar', '(Disabled) gqbar --> gqbar Subprocess (ID = 4)'))
        fh.write("\n")
    if(qqbar2gg11 == 1):
        fh.write("  {0:<10}{1:<22}{2:<30}".format(qqbar2gg, 'qqbar2gg', '(Enabled)  qqbar --> gg Subprocess    (ID = 5)'))
        fh.write("\n")
    else:
        fh.write("  {0:<10}{1:<22}{2:<30}".format(qqbar2gg, 'qqbar2gg', '(Disabled) qqbar --> gg Subprocess    (ID = 5)'))
        fh.write("\n")
    if(gg2gGamma11 == 1):
        fh.write("  {0:<10}{1:<22}{2:<30}".format(gg2gGamma, 'gg2gGamma', '(Enabled)  gg --> gGamma Subprocess   (ID = 6)'))
        fh.write("\n")
    else:
        fh.write("  {0:<10}{1:<22}{2:<30}".format(gg2gGamma, 'gg2gGamma', '(Disabled) gg --> gGamma Subprocess   (ID = 6)'))
        fh.write("\n")
    if(gq2qGamma11 == 1):
        fh.write("  {0:<10}{1:<22}{2:<30}".format(gq2qGamma, 'gq2qGamma', '(Enabled)  gq --> qGamma Subprocess   (ID = 7)'))
        fh.write("\n")
    else:
        fh.write("  {0:<10}{1:<22}{2:<30}".format(gq2qGamma, 'gq2qGamma', '(Disabled) gq --> qGamma Subprocess   (ID = 7)'))
        fh.write("\n")

    print("\nSuccessfully Generated {} Events".format(numberofevents))
    print("Events are saved in STRINGSfile.lhe\n")
    print("Thanks for using STRINGS-2.00\n")

    # Updating the LHE file with the calculated cross-sections
    fh.write("-->\n")
    fh.write("<init>\n")
    fh.write("  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(IDBMUP, IDBMUP, EBMUP, EBMUP, PDFGUP, PDFGUP, PDFSUP, PDFSUP, IDWTUP, NPRUP))
    if(gg2gg11 == 1):
        fh.write("  {}  {}  {}  {}\n".format(CrossSectiongggg, ggggStandardError, 1, 1))
    if(gg2qqbar11 == 1):
        fh.write("  {}  {}  {}  {}\n".format(CrossSectionggqqbar, ggqqbarStandardError, 1, 2))
    if(gq2gq11 == 1):
        fh.write("  {}  {}  {}  {}\n".format(CrossSectiongqgq, gqgqStandardError, 1, 3))
    if(gqbar2gqbar11 == 1):
        fh.write("  {}  {}  {}  {}\n".format(CrossSectiongqbargqbar, gqbargqbarStandardError, 1, 4))
    if(qqbar2gg11 == 1):
        fh.write("  {}  {}  {}  {}\n".format(CrossSectionqqbargg, qqbarggStandardError, 1, 5))
    if(gg2gGamma11 == 1):
        fh.write("  {}  {}  {}  {}\n".format(CrossSectiongggGamma, gggGammaStandardError, 1, 6))
    if(gq2qGamma11 == 1):
        fh.write("  {}  {}  {}  {}\n".format(CrossSectiongqqGamma, gqqGammaStandardError, 1, 7))
    fh.write("</init>\n")
    fh.close()
    
    call("cat events.lhe >> begin.lhe",shell=True)
    call("rm events.lhe",shell=True)
    call("mv begin.lhe STRINGSfile.lhe",shell=True)

# Definition of the input parameters with their default values.
# Two versions of the arguments are assigned for each input that can be used to change the parameter.
parser = argparse.ArgumentParser(description='Parameters Passed to the STRINGS Generator')
parser.add_argument('-v', '--version', action='version', version='STRINGS-2.00')
parser.add_argument('-RandGenSEED', '--RandGenSEEDvalue', default=123456, help='Seed for Random Number Generator',type=float)
parser.add_argument('-Number', '--Numbervalue', default=10000, help='Number of Events',type=int)
parser.add_argument('-Ms', '--Msvalue', default=7000, help='String Scale of the String Theory (GeV)',type=float)
parser.add_argument('-COME', '--COMEvalue', default=13000, help='Centre of Mass Energy (GeV)',type=float)
parser.add_argument('-MinMass', '--MinMassvalue', default=6000, help='Lower Bound of the Invariant Mass (GeV)',type=float)
parser.add_argument('-MaxMass', '--MaxMassvalue', default=8000, help='Upper Bound of the Invariant Mass (GeV)',type=float)
parser.add_argument('-yMax', '--yMaxvalue', default=2.5, help='Upper Limit for the Rapidity of the Outgoing Partons',type=float)
parser.add_argument('-PDFSet', '--PDFSetvalue', default="cteq6l1", help='Parton Distribution Function Set of the LHAPDF',type=str)
parser.add_argument('-PDFScale', '--PDFScalevalue', default=-22, help='Scale at which the Parton Distribution Function is Evaluated (GeV)',type=float)
parser.add_argument('-Coupling', '--Couplingvalue', default=-1, help='Coupling Constant',type=float)
parser.add_argument('-CouplingScale', '--CouplingScalevalue', default=-22, help='Scale at Which the Running Coupling Constant is Calculated(GeV)',type=float)
parser.add_argument('-FirstStringCoeff', '--FirstStringCoeffvalue', default="true", help='First String Resonance',type=str)
parser.add_argument('-SecondStringCoeff', '--SecondStringCoeffvalue', default="false", help='Second String Resonance',type=str)
parser.add_argument('-QCDCoeff', '--QCDCoeffvalue', default="false", help='QCD Tree-Level',type=str)
parser.add_argument('-dMass', '--dMassvalue', default=5e-3, help='Mass of the Down Quark (GeV)',type=float)
parser.add_argument('-uMass', '--uMassvalue', default=2e-3, help='Mass of the Up Quark (GeV)',type=float)
parser.add_argument('-sMass', '--sMassvalue', default=1e-3, help='Mass of the Strange Quark (GeV)',type=float)
parser.add_argument('-cMass', '--cMassvalue', default=1.25, help='Mass of the Charm Quark (GeV)',type=float)
parser.add_argument('-bMass', '--bMassvalue', default=4.2, help='Mass of the Bottom Quark (GeV)',type=float)
parser.add_argument('-tMass', '--tMassvalue', default=172.5, help='Mass of the Top Quark (GeV)',type=float)
parser.add_argument('-gg2gg', '--gg2ggvalue', default="true", help='gg -> gg Subprocess',type=str)
parser.add_argument('-gg2qqbar', '--gg2qqbarvalue', default="true", help='gg -> qqbar Subprocess',type=str)
parser.add_argument('-gq2gq', '--gq2gqvalue', default="true", help='gq -> gq Subprocess',type=str)
parser.add_argument('-gqbar2gqbar', '--gqbar2gqbarvalue', default="true", help='gqbar -> gqbar Subprocess',type=str)
parser.add_argument('-qqbar2gg', '--qqbar2ggvalue', default="true", help='qqbar -> gg Subprocess',type=str)
parser.add_argument('-gg2gGamma', '--gg2gGammavalue', default="false", help='gg -> gGamma Subprocess',type=str)
parser.add_argument('-gq2qGamma', '--gq2qGammavalue', default="false", help='gq -> qGamma Subprocess',type=str)

args = parser.parse_args()

print("########################################################")
print("################# STRINGS-VERSION 2.00 #################")
print("########################################################")
print("####                                                ####")
print("#### Oct 2020                                       ####")
print("####                                                ####")
print("#### Authors:                                       ####")
print("####                                                ####")
print("####\t Fairhurst Lyons                            ####")
print("####\t Email:                                     ####")
print("####\t \t rflyons@ualberta.ca                ####")
print("####\t \t ruth.fairhurst.lyons@cern.ch       ####")
print("####                                                ####")
print("####\t Pourya Vakilipourtakalou                   ####")
print("####\t Email:                                     ####")
print("####\t \t vakilipo@ualberta.ca               ####")
print("####\t \t pourya.vakilipourtakalou@cern.ch   ####")
print("####                                                ####")
print("####\t Douglas M. Gingrich                        ####")
print("####\t Email:                                     ####")
print("####\t \t gingrich@ualberta.ca               ####")
print("####                                                ####")
print("########################################################")
print("########################################################")

# A checker is set to make sure all of the input variables are correctly assigned
checker = 0

if(args.Numbervalue <= 0):
    print("Error: Invalid Value for the Number of Generated Events\nIt Should be Positive\n")
    checker = 1
if(args.Msvalue <= 0):
    print("Error: Invalid Value for the String Scale\nIt Should be Positive\n")
    checker = 1
if(args.COMEvalue <= 0):
    print("Error: Invalid Value for Centre of Mass Energy\nIt Should be Positive\n")
    checker = 1
if(args.MinMassvalue <= 0):
    print("Error: Invalid Value for the Lower Bound of the Invariant Mass\nIt Should be Positive\n")
    checker = 1
if(args.MaxMassvalue <= 0):
    print("Error: Invalid Value for the Upper Bound of the Invariant Mass\nIt Should be Positive\n")
    checker = 1
if(args.MaxMassvalue > args.COMEvalue):
    print("Error: Invalid Value for the Upper Bound of the Invariant Mass\nIt Should Not be larger than the Centre of Mass Energy\n")
    checker=1
elif(args.MaxMassvalue <= args.MinMassvalue):
    print("Error: Invalid Value for the Upper Bound of the Invariant Mass\nIt Should be greater than the Lower Bound of the Invariant Mass\n")
    checker = 1
elif(args.MaxMassvalue > args.COMEvalue):
    print("Error: Invalid Value for the Upper Bound of the Invariant Mass\nIt Should not be greater than the Centre of Mass Energy\n")
    checker = 1
if(args.yMaxvalue == -1):
    args.yMaxvalue = float("inf")
elif(args.yMaxvalue < 0):
    print("Error: Invalid Value for the Upper Bound of the Rapidity\nIt Should be Positive or for the Upper Bound to be Infinity, Use -1\n")
    checker = 1
if(args.PDFScalevalue <= 0 and args.PDFScalevalue != -22):
    print("Error: Invalid Value for the Scale at Which PDFs are Determined\nIt Should be Positive\n")
    checker = 1
if(args.Couplingvalue == -1):
    args.Couplingvalue = -1
elif(args.Couplingvalue < 0):
    print("Error: Invalid Value for the Coupling Constant\nIt Should be positive or for running coupling use -1\n")
    checker = 1
if(args.CouplingScalevalue <= 0 and args.CouplingScalevalue != -22):
    print("Error: Invalid Value for the Scale at Which Running Coupling is Measured\nIt Should be Positive\n")
    checker = 1
if(args.QCDCoeffvalue == 'false' or args.QCDCoeffvalue == 'False'):
    if(args.FirstStringCoeffvalue == 'false' or args.FirstStringCoeffvalue == 'False'):
        if(args.SecondStringCoeffvalue == 'false' or args.SecondStringCoeffvalue == 'False'):
            checker = 1
            print("Error: Type of Event Generation is not Specified\n")
if(args.gg2ggvalue == 'false' or args.gg2ggvalue == 'False'):
    if(args.gg2qqbarvalue == 'false' or args.gg2qqbarvalue == 'False'):
        if(args.gq2gqvalue == 'false' or args.gq2gqvalue == 'False'):
            if(args.gqbar2gqbarvalue == 'false' or args.gqbar2gqbarvalue == 'False'):
                if(args.qqbar2ggvalue == 'false' or args.qqbar2ggvalue == 'False'):
                    if(args.gg2gGammavalue == 'false' or args.gg2gGammavalue == 'False'):
                        if(args.gq2qGammavalue == 'false' or args.gq2qGammavalue == 'False'):
                            checker = 1
                            print("Error: No Subprocess is Turned On\n")
if(args.gg2ggvalue == 'false' or args.gg2ggvalue == 'False'):
    if(args.gg2qqbarvalue == 'false' or args.gg2qqbarvalue == 'False'):
        if(args.gq2gqvalue == 'false' or args.gq2gqvalue == 'False'):
            if(args.gqbar2gqbarvalue == 'false' or args.gqbar2gqbarvalue == 'False'):
                if(args.qqbar2ggvalue == 'false' or args.qqbar2ggvalue == 'False'):
                    if(args.gg2gGammavalue == 'true' or args.gg2gGammavalue == 'True'):
                        if(args.QCDCoeffvalue == 'true' or args.QCDCoeffvalue == 'True'):
                            checker = 1
                            print("Error: QCD Diparton Cannot be Produced Through gg->gGamma Scattering\nPlease Turn On Either of the 2->2 Partonic Scatterings")
                        if(args.SecondStringCoeffvalue == 'true' or args.SecondStringCoeffvalue == 'True'):
                            checker = 1
                            print("Error: Second string cannot be produced through gg->gGamma scattering\nPlease Turn On Either of the 2->2 Partonic Scatterings")
                    if(args.gq2qGammavalue == 'true' or args.gq2qGammavalue == 'True'):
                        if(args.QCDCoeffvalue == 'true' or args.QCDCoeffvalue == 'True'):
                            checker = 1
                            print("Error: QCD Diparton Cannot be Produced Through gq->qGamma Scattering\nPlease Turn On Either of the 2->2 Partonic Scatterings")
                        if(args.SecondStringCoeffvalue == 'true' or args.SecondStringCoeffvalue == 'True'):
                            checker = 1
                            print("Error: Second string cannot be produced through gq->qGamma scattering\nPlease Turn On Either of the 2->2 Partonic Scatterings")
if(args.dMassvalue < 0):
    print("Error: Invalid Value for the Mass of the Down Quark\nIt Should be Positive\n")
    checker = 1
if(args.uMassvalue < 0):
    print("Error: Invalid Value for the Mass of the UP Quark\nIt Should be Positive\n")
    checker = 1
if(args.sMassvalue < 0):
    print("Error: Invalid Value for the Mass of the Strange Quark\nIt Should be Positive\n")
    checker = 1
if(args.cMassvalue < 0):
    print("Error: Invalid Value for the Mass of the Charm Quark\nIt Should be Positive\n")
    checker = 1
if(args.bMassvalue < 0):
    print("Error: Invalid Value for the Mass of the Bottom Quark\nIt Should be Positive\n")
    checker = 1
if(args.tMassvalue < 0):
    print("Error: Invalid Value for the Mass of the Top Quark\nIt Should be Positive\n")
    checker = 1
if(args.gg2ggvalue != "True" and args.gg2ggvalue != "true" and args.gg2ggvalue != "False" and args.gg2ggvalue != "false"):
    print("Error: Invalid Value; In order to enable or disable gg --> gg subprocess, set gg2gg to true or false, respectively.\n")
    checker = 1
if(args.gg2qqbarvalue != "True" and args.gg2qqbarvalue != "true" and args.gg2qqbarvalue != "False" and args.gg2qqbarvalue != "false"):
    print("Error: Invalid Value; In order to enable or disable gg --> qqbar subprocess, set gg2qqbar to true or false, respectively.\n")
    checker = 1
if(args.gq2gqvalue != "True" and args.gq2gqvalue != "true" and args.gq2gqvalue != "False" and args.gq2gqvalue != "false"):
    print("Error: Invalid Value; In order to enable or disable gq --> gq subprocess, set gq2gq to true or false, respectively.\n")
    checker = 1
if(args.gqbar2gqbarvalue != "True" and args.gqbar2gqbarvalue != "true" and args.gqbar2gqbarvalue != "False" and args.gqbar2gqbarvalue != "false"):
    print("Error: Invalid Value; In order to enable or disable gqbar --> gqbar subprocess, set gqbar2gqbar to true or false, respectively.\n")
    checker = 1
if(args.qqbar2ggvalue != "True" and args.qqbar2ggvalue != "true" and args.qqbar2ggvalue != "false" and args.qqbar2ggvalue != "False"):
    print("Error: Invalid Value; In order to enable or disable qqbar --> gg subprocess, set qqbar2gg to true or false, respectively.\n")
    checker = 1
if(args.gg2gGammavalue != "True" and args.gg2gGammavalue != "true" and args.gg2gGammavalue != "False" and args.gg2gGammavalue != "false"):
    print("Error: Invalid Value; In order to enable or disable gg --> gGamma subprocess, set gg2gGamma to true or false, respectively.\n")
    checker = 1
if(args.gq2qGammavalue != "True" and args.gq2qGammavalue != "true" and args.gq2qGammavalue != "false" and args.gq2qGammavalue != "False"):
    print("Error: Invalid Value; In order to enable or disable gq --> qGamma subprocess, set gq2qGamma to true or false, respectively.\n")
    checker = 1

# If all of the input parameters are properly defined, the main function is called
if(checker == 0):
    main(args.RandGenSEEDvalue, args.Numbervalue, args.Msvalue, args.COMEvalue, args.MinMassvalue, args.MaxMassvalue, args.yMaxvalue, args.PDFSetvalue, args.PDFScalevalue, args.Couplingvalue, args.CouplingScalevalue, args.FirstStringCoeffvalue, args.SecondStringCoeffvalue, args.QCDCoeffvalue, args.dMassvalue, args.uMassvalue, args.sMassvalue, args.cMassvalue, args.bMassvalue, args.tMassvalue, args.gg2ggvalue, args.gg2qqbarvalue, args.gq2gqvalue, args.gqbar2gqbarvalue, args.qqbar2ggvalue, args.gg2gGammavalue, args.gq2qGammavalue)
