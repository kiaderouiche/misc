#!/bin/bash
########################################################
################   STRINGS-VERSION 2.00 ################
########################################################
#####################################################################################################
#### Authors:
####          Fairhurst Lyons,          Email: rflyons@ualberta.ca,
####          Pourya Vakilipourtakalou, Email: vakilipo@ualberta.ca, pourya.vakilipourtakalou@cern.ch
####          Douglas M. Gingrich,      Email: gingrich@ualberta.ca
#####################################################################################################
######################################## INPUT VARIABLES ############################################
#####################################################################################################

RandGenSEED=123456    #### A Seed for the Random Number Generator
COME=13000            #### Centre of Mass Energy of the Proton-Proton Collision (GeV).
Ms=1000               #### String Scale (GeV) ==> This is the Same Scale for QCD.
MinMass=6000          #### Lower Bound for the Invariant Mass (GeV).
MaxMass=8000          #### Upper Bound for the Invariant Mass (GeV). The Maximum Value for this Variable is COME. The Default Value is the COME
ymax=2.5              #### Upper Bound for the Rapidity of the Outgoing Partons  |y1|,|y2| < ymax.
Number=10000          #### Number of Events to be Generated.
PDFSet=cteq6l1        #### Parton Distribution Function (PDF) Set. Other PDF Sets that Can be Set Here: "CT14lo", "CT10"
Coupling=-1           #### The Running Coupling Constant, alpha_s (= g^2/4*pi). In Order to Use a Fixed Coupling Constant, Simply Use the Intended Value.
CouplingScale=$Ms     #### Scale at Which Coupling Constant is Calculated (Only if the Running Coupling is Being Used). The Default Value for this Variable is the String Scale Ms.
PDFScale=$Ms          #### Scale at which PDFs are Determined. The Default Value for this Variable is the QCD Scale "CouplingScale".

################### SubProcessess #################

gg2gg=true       #### gg -> gg       Subprocess (ID = 1)
gg2qqbar=true    #### gg -> qqbar    Subprocess (ID = 2)
gq2gq=true       #### gq -> gq       Subprocess (ID = 3)
gqbar2gqbar=true #### gqbar -> gqbar Subprocess (ID = 4)
qqbar2gg=true    #### qqbar -> gg    Subprocess (ID = 5)
gg2gGamma=false  #### gg -> gGamma   Subprocess (ID = 6)
gq2qGamma=false  #### gq -> qGamma   Subprocess (ID = 7)

###################################################

QCDCoeff=false           #### Production of QCD tree-level diparton
FirstStringCoeff=true    #### Production of First  String Resonance ( 2 --> 2 Partonic Scattering and 2-Parton --> Parton-Gamma Scattering )
SecondStringCoeff=false  #### Production of Second String Resonance ( 2 --> 2 Partonic Scattering )

################## Qurak Masses ###################

dMass=5e-3    #### GeV
uMass=2e-3    #### GeV
sMass=1e-3    #### GeV
cMass=1.25    #### GeV
bMass=4.2     #### GeV
tMass=172.5   #### GeV

####################################################

python3.9 STRINGS.py -RandGenSEED $RandGenSEED \
                  -Number $Number \
                  -Ms $Ms \
                  -COME $COME \
                  -MinMass $MinMass \
                  -MaxMass $MaxMass \
                  -yMax $yMax \
                  -PDFSet $PDFSet \
                  -PDFScale $PDFScale \
                  -Coupling $Coupling \
                  -CouplingScale $CouplingScale \
                  -FirstStringCoeff $FirstStringCoeff  \
                  -SecondStringCoeff $SecondStringCoeff \
                  -QCDCoeff $QCDCoeff \
                  -dMass $dMass \
                  -uMass $uMass \
                  -sMass $sMass \
                  -cMass $cMass \
                  -bMass $bMass \
                  -tMass $tMass \
                  -gg2gg $gg2gg \
                  -gg2qqbar $gg2qqbar \
                  -gq2gq $gq2gq \
                  -gqbar2gqbar $gqbar2gqbar \
                  -qqbar2gg $qqbar2gg \
                  -gg2gGamma $gg2gGamma \
                  -gq2qGamma $gq2qGamma
