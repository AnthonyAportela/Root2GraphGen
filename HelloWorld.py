#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import ROOT
import uproot as ur

### Comments are verbose because I have no idea what I'm doing

## Make global style changes
ROOT.gStyle.SetOptStat(0) # Disable the statistics box

## managing file names for signal and background, as well as name of output pdf of plots
outFileName = 'MCplts.pdf'
filedir  = "root://cmsxrootd.fnal.gov//store/group/lpclonglived/analyses/muonShowerMET/v135/"
signalFilename = "ggH_HToSSTobbbb_MH-125_MS-15_ctau-100000_137000pb_weighted.root"
#filename = "ggH_HToSSTobbbb_MH-125_MS-15_ctau-100000_TuneCP5_13TeV-powheg-pythia8_41530pb_weighted.root"
backgroundFilename = "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_1pb_weighted.root"
treename = "MuonSystem"


## creates list of variables we want to look at. Kinda gross but less gross than typing out all the variables by hand
# the files are accessed here using uproot ad a quick and dirty way of listing the variable names. 
tree = ur.open(filedir + signalFilename + ':' + treename)
# actual filtering process
variables = ['Flag2_all', 'Flag_all', 'HT']
variables.extend(tree.keys(filter_name = 'Z*')) #faster than +
variables.extend(tree.keys(filter_name = 
                           lambda s: ('RechitCluster' in s) 
                              and s.startswith(('csc', 'dt')) 
                              and s.endswith('Spread')
                ))
variables.extend(tree.keys(filter_name = 
                           lambda s: s.startswith(('csc', 'dt')) 
                              and s.endswith(('ClusterNChamber', 'ClusterTime', 'ClusterSize',
                                              'ClusterEta', 'ClusterPhi',
                                              'RechitsEta', 'RechitsPhi',
                                              'X', 'Y', 'Z'))
                ))
variables.extend(tree.keys(filter_name = 
                           lambda s: s.startswith(('jet','gHiggs'))
                              and s.endswith(('Pt','E','Eta','Phi','Time'))
                ))
variables.extend(tree.keys(filter_name = 
                           lambda s: s.startswith(('nCsc', 'nDt')) 
                              and s.endswith(('RechitClusters','Rechits'))
                ))



## accesses root files using pyroot because it's easier to plot using built-in root stuff
signalFile = ROOT.TFile.Open(filedir + signalFilename, "READ")
signaltree = signalFile.Get("MuonSystem") #overwrites tree above
#signaltree.SetDirectory(0)
#signalFile.Close()
backgroundFile = ROOT.TFile.Open(filedir + backgroundFilename, "READ")
backgroundtree = backgroundFile.Get("MuonSystem") #overwrites tree above
#backgroundtree.SetDirectory(0)
#backgroundFile.Close()

## This part is the actually drawing of the hists
# make canvas
canvas = ROOT.TCanvas("canvas")
canvas.cd()

# opens/creates pdf to write into
canvas.Print(outFileName + "[")



# loops over variable names to draw them onto seperate plots
for variable in variables:

    signaltree.Draw(variable, "", "HIST") # WHY IS PYROOT SO POORLY DOCUMENTED
    backgroundtree.Draw(variable, "","HIST same")# this was a minor nightmare to figure out
    
    signalHist = signaltree.GetHistogram()
    backgroundHist = backgroundtree.GetHistogram()
    
    signalArea = signalHist.Integral()
    backgroundArea = backgroundHist.Integral()
    
    if(signalArea > 0):
        signalHist.Scale(1/signalArea) # no one can hear me scream
    if(backgroundArea > 0):
        backgroundHist.Scale(1/backgroundArea)
        
    backgroundHist.SetLineColor(ROOT.kRed)
    
    signalHist.GetXaxis().SetTitle("TODO")
    signalHist.GetYaxis().SetTitle("Number of events (Arbitrary units)")
    
    legend = ROOT.TLegend()
    legend.AddEntry(signaltree, signalFilename[:signalFilename.index("_")])
    legend.AddEntry(backgroundtree, backgroundFilename[:backgroundFilename.index("_")])
    
    legend.Draw()   

    canvas.SetLogy(True)
    canvas.Print(outFileName)
    canvas.Clear()
    
    '''TODO
    ratio = signalHist.Clone()
    ratio.Divide(backgroundHist)
    ratio.SetLineColor(ROOT.kBlack)
        
    pad1 = ROOT.TPad("pad1", "pad1",0 ,0.3 ,1 ,1)
    pad1.SetLogy(True)
    pad1.Draw()
    pad1.cd()
    signalHist.Draw(variable)
    backgroundHist.Draw(variable + ",same")

    canvas.cd()
    pad2 = ROOT.TPad ("pad2" ,"pad2" ,0 ,0.05 ,1 ,0.3)
    pad2.Draw()
    pad2.cd()
    ratio.Draw(variable)
    canvas.Print(outFileName)
    canvas.Clear()
    '''

canvas.Print(outFileName + "]") #closes pdf
canvas.Close() #closes canvas

del variables #artifact of using jupyter



