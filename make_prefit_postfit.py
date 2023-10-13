#########################
# author: I. Paraskevas #
# created: June 8, 2023 #
#########################

import ROOT
from array import array
from configparser import ConfigParser
import json

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLegendBorderSize(0)

config_object = ConfigParser()
config_object.read("config.ini")

## load settings from config
file = config_object["SETTINGS"]["file"]
samples = json.loads(config_object.get("SETTINGS","samples"))
colors = json.loads(config_object.get("SETTINGS","colors"))
data_hist_name = config_object["SETTINGS"]["data_hist_name"]
prefit_dir = config_object["SETTINGS"]["prefit_dir"]
postfit_dir = config_object["SETTINGS"]["postfit_dir"]
output_dir = config_object["SETTINGS"]["output_dir"]
input_file_mode = int(config_object["SETTINGS"]["input_file_mode"])

file = ROOT.TFile(file, "READ")

## modes
## 1: one dir for prefit distributions and one dir for postfit distributions
if input_file_mode == 1:
    print("Using mode 1")
    bins_prefit = file.Get(prefit_dir).GetListOfKeys()
    bins_postfit = file.Get(postfit_dir).GetListOfKeys()

    ## prefit
    for bin_prefit in bins_prefit:
        
        c = ROOT.TCanvas("c","c",800,800)
        hs_prefit = ROOT.THStack("hs_prefit",";;Events")

        for index, sample in enumerate(samples):
            h_temp = file.Get(prefit_dir + "/" + bin_prefit.GetName() + "/" + sample)
            h_temp.SetLineColor(colors[index])
            h_temp.SetFillColor(colors[index])
            hs_prefit.Add(h_temp)

        hs_prefit.Draw()
        hs_prefit.SetMaximum(int(hs_prefit.GetMaximum())+10)

        data_hist = file.Get(prefit_dir + "/" + bin_prefit.GetName() + "/" + data_hist_name)

        rp = ROOT.TRatioPlot(hs_prefit,data_hist)
        rp.Draw()
        rp.GetLowerRefYaxis().SetTitle("Data/MC")
        rp.GetLowerRefYaxis().SetTitleOffset(1.55)
        rp.SetGridlines([0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8])
        rp.SetSeparationMargin(0)
        rp.GetLowerRefGraph().SetLineColor(0)
        rp.GetLowerRefGraph().SetMinimum(0.6)
        rp.GetLowerRefGraph().SetMaximum(1.4)
        rp.GetLowerPad().cd()
        rp.GetUpperPad().cd()
        data_hist.SetMarkerStyle(20)
        data_hist.Draw("same")

        c.SaveAs(output_dir + "/prefit/" + bin_prefit.GetName() + ".png")
        del c

    ## postfit
    for bin_postfit in bins_postfit:
        
        c = ROOT.TCanvas("c","c",800,800)
        hs_postfit = ROOT.THStack("hs_postfit",";;Events")

        for index, sample in enumerate(samples):
            h_temp = file.Get(postfit_dir + "/" + bin_postfit.GetName() + "/" + sample)
            h_temp.SetLineColor(colors[index])
            h_temp.SetFillColor(colors[index])
            hs_postfit.Add(h_temp)

        hs_postfit.Draw()
        hs_postfit.SetMaximum(int(hs_postfit.GetMaximum())+10)

        data_hist = file.Get(postfit_dir + "/" + bin_postfit.GetName() + "/" + data_hist_name)
        data_hist.SetMarkerStyle(20)
        data_hist.Draw("same ep")

        c.SaveAs(output_dir + "/postfit/" + bin_postfit.GetName() + ".png")
        del c

## 2: one dir for each bin (prefit + postfit)
if input_file_mode == 2:
    print("Using mode 2")
    bins = file.GetListOfKeys()

    for bin_ in bins:
        
        c = ROOT.TCanvas("c","c",800,800)
        hs = ROOT.THStack("hs",";;Events")

        leg = ROOT.TLegend(0.35,0.55,0.89,0.89)
        leg.SetTextSize(0.06)

        for index, sample in enumerate(samples):
            h_temp = file.Get(bin_.GetName() + "/" + sample)
            h_temp.SetLineColor(colors[index])
            h_temp.SetFillColor(colors[index])
            hs.Add(h_temp)
            leg.AddEntry(h_temp, sample, "f")

        data_hist = file.Get(bin_.GetName() + "/" + data_hist_name)
        data_hist.SetMarkerStyle(20)
        data_hist.SetMarkerColor(ROOT.kBlack)
        data_hist.SetLineColor(ROOT.kBlack)
        data_hist.GetXaxis().SetRangeUser(0,200)

        hs_max = round(hs.GetMaximum())
        if hs_max < 10:  set_max = hs_max+5
        if 10 <= hs_max < 30:  set_max = hs_max+15
        if 30 <= hs_max < 50:  set_max = hs_max+30
        if 50 <= hs_max < 80:  set_max = hs_max+50
        if hs_max > 100:  set_max = hs_max+200
        hs.SetMaximum(set_max)

        #relative bkg uncertainty in ratio plot
        unc_postfit = ROOT.TGraphAsymmErrors(file.Get(bin_.GetName() + "/TotalProcs"))
        unc_postfit.SetFillColor(4)
        unc_postfit.SetFillStyle(3013)
        unc_postfit.SetLineStyle(0)
        unc_postfit.SetLineWidth(0)
        unc_postfit.SetMarkerSize(0)
        unc_postfit.Draw("E2same")

        hRelUnc = unc_postfit.Clone()
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

        rp = ROOT.TRatioPlot(hs,data_hist)
        rp.Draw()
        rp.GetLowerRefYaxis().SetTitle("MC / Data")
        rp.GetLowerRefYaxis().SetTitleOffset(1.55)
        rp.SetGridlines([0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8])
        rp.SetSeparationMargin(0)
        rp.GetLowerRefGraph().SetMarkerStyle(20)
        rp.GetLowerRefGraph().SetMinimum(0.6)
        rp.GetLowerRefGraph().SetMaximum(1.4)
        rp.GetLowerPad().cd()
        hRelUnc.Draw("E2same")
        rp.GetUpperPad().cd()
        data_hist.SetMarkerStyle(20)
        data_hist.Draw("same")
        leg.SetNColumns(3)
        leg.Draw()

        latex = ROOT.TLatex()
        latex.SetTextSize(0.05)
        latex.DrawLatexNDC(0.1, 0.915, "#bf{ #font[22]{CMS Preliminary}}")
        latex.SetTextSize(0.05)
        latex.DrawLatexNDC(0.44, 0.915, bin_.GetName() )

        plot_dir = "prefit" if "prefit" in bin_ else "postfit"
        c.SaveAs(output_dir + "/" + plot_dir + "/" + bin_.GetName() + ".png")
        del c