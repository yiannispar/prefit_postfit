#########################
# author: I. Paraskevas #
# created: 28 Nov, 2023 #
#########################

from turtle import ht
import ROOT
import config
import os

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLegendBorderSize(0)

config_file = config.Config()

## load settings from config
file = config_file.input_file
samples = config_file.samples
prefit_dir = config_file.prefit_dir
postfit_dir = config_file.postfit_dir
plots_dir = config_file.output_plots_dir
input_file_mode = config_file.input_file_mode

infile = ROOT.TFile(file, "READ")
categories = infile.GetListOfKeys()

print(f"Input file {file}")
print(f"Samples {samples}")

for category in categories:
    
    category = category.GetName()
    c = ROOT.TCanvas("c","c",800,800)
    c.SetTicks()
    hs = ROOT.THStack("hs",";;Events")

    if config_file.set_logy: 
        c.SetLogy()
        hs.SetMinimum(config_file.stack_ymin)
        hs.SetMaximum(config_file.stack_ymax)

    leg = ROOT.TLegend(0.12,0.65,0.89,0.87)
    leg.SetTextSize(0.05)

    for sample in samples:
        h_temp = infile.Get(category + "/" + sample)
        h_temp.SetLineColor(config_file.colors[sample])
        h_temp.SetFillColor(config_file.colors[sample])
        hs.Add(h_temp)
        leg.AddEntry(h_temp, sample, "f")

    data_hist = infile.Get(category + "/data_obs")
    data_hist.SetMarkerStyle(20)
    data_hist.SetMarkerColor(ROOT.kBlack)
    data_hist.SetLineColor(ROOT.kBlack)
    data_hist.GetXaxis().SetRangeUser(0,200)
    leg.AddEntry(data_hist, "Data", "lep")

    #relative bkg uncertainty in ratio plot
    unc = ROOT.TGraphAsymmErrors(infile.Get(category + "/TotalProcs"))
    unc.SetFillColor(4)
    unc.SetFillStyle(3013)
    unc.SetLineStyle(0)
    unc.SetLineWidth(0)
    unc.SetMarkerSize(0)
    unc.Draw("E2same")

    hRelUnc = unc.Clone()
    for i in range(hRelUnc.GetN()):
        val = hRelUnc.GetY()[i]
        errUp = hRelUnc.GetErrorYhigh(i)
        errLow = hRelUnc.GetErrorYlow(i)
        if val==0:
            continue
        hRelUnc.SetPointEYhigh(i, errUp/val)
        hRelUnc.SetPointEYlow(i, errLow/val)
        hRelUnc.SetPoint(i, hRelUnc.GetX()[i], 1 )
    hRelUnc.SetFillColor(4)
    hRelUnc.SetFillStyle(3013)
    hRelUnc.SetLineStyle(0)
    hRelUnc.SetLineWidth(0)
    hRelUnc.SetMarkerSize(0)
    leg.AddEntry(hRelUnc, "BKG. unc", "f")

    ## ratio plot
    rp = ROOT.TRatioPlot(hs,data_hist)
    rp.Draw()
    rp.GetLowYaxis().SetNdivisions(4,1,1)
    rp.GetLowerRefYaxis().SetTitle("MC / Data")
    rp.GetLowerRefYaxis().SetTitleOffset(1.55)
    rp.SetGridlines([0.8,1,1.2])
    rp.SetSeparationMargin(0)
    rp.GetLowerRefGraph().SetMarkerStyle(20)
    rp.GetLowerRefGraph().SetMinimum(0.6)
    rp.GetLowerRefGraph().SetMaximum(1.4)
    rp.GetLowerPad().cd()
    hRelUnc.Draw("E2same")
    rp.GetUpperPad().cd()
    data_hist.SetMarkerStyle(20)
    data_hist.Draw("same")
    leg.SetNColumns(4)
    leg.Draw()

    # ## test to see if total processes histo matches stack
    # h_tot_Procs = infile.Get(category + "/TotalProcs")
    # h_tot_Procs.SetMarkerStyle(5)
    # h_tot_Procs.SetMarkerColor(ROOT.kRed)
    # h_tot_Procs.Draw("same ep")

    latex = ROOT.TLatex()
    latex.SetTextSize(0.05)
    latex.DrawLatexNDC(0.1, 0.915, "#bf{ #font[22]{CMS Preliminary}}")
    latex.SetTextSize(0.05)
    latex.DrawLatexNDC(0.40, 0.915, category )

    prefit_or_postfix = "prefit" if "prefit" in category else "postfit"
    output_dir = plots_dir + "/" + prefit_or_postfix + "/"
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    
    c.SaveAs(output_dir + category + "." + config_file.plot_format)
    del c