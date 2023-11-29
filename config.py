import ROOT

class Config:
  
  def __init__(self):  
    self.input_file_mode = 2
    self.samples = ["tt_bb", "tt_bj", "tt_cc", "tt_cj", "tt_lf", "ttZ_Zbb","ttZ_Zcc","ttZ_Zother","ttH_hbb", "ttH_hcc", "ttbarW", "singlet","ttH_hww","ttH_htt"]
    #only used in mode 1
    self.prefit_dir = "shapes_prefit"
    self.postfit_dir = "shapes_fit_b"
    self.output_plots_dir = "plots/"
    self.input_file = "/eos/user/i/iparaske/temp/puppi_branch/CMSSW_11_3_4/src/PlotToolsTTH/ttH/cards/scripts/runs/val_midscore_data_nominal/shapes.root"
    self.plot_format = "png"
    self.dataset_legend = "59.8 fb^{-1} (13 TeV)"
    self.plot_type = "#bf{ #font[22]{CMS} #font[72]{Preliminary} } "
    self.stack_ymin = 1e1
    self.stack_ymax = 1e4
    self.set_logy = True
    
    ## plot legend
    self.legend = {
      "tt_bb":"t#bar{t}+bb",
      "tt_bj":"t#bar{t}+bj",
      "tt_cc":"t#bar{t}+cc",
      "tt_cj":"t#bar{t}+cj",
      "tt_lf":"t#bar{t}+lf",
      "ttH_hcc": "t#bar{t}(H #rightarrow #bar{c}c)",
      "ttH_hbb": "t#bar{t}(H #rightarrow #bar{b}b)",
      "ttH_htt": "t#bar{t}(H #rightarrow #tau#tau)",
      "ttZ": "t#bar{t}Z",
      "ttbarW": "t#bar{t}W",
      "singlet": "ST",
      "diboson": "VV",
      "qcd-mg": "QCD",
      "wjets": "W+Jets",
      "zjets": "Z+Jets",
      "ttH_hww": "t#bar{t}(H #rightarrow WW)",
      "ttZ_Zbb": "t#bar{t}Z(Z #rightarrow #bar{b}b)",
      "ttZ_Zcc": "t#bar{t}Z(Z #rightarrow #bar{c}c)",
      "ttZ_Zother": "t#bar{t}Z(Z #rightarrow #bar{q}q)",
    }
    
    ## plot colors
    self.colors = {
      "tt_bb": 607,
      "tt_bj": 608,
      "tt_cc": 623,
      "tt_cj": 624,
      "tt_lf": 866,
      "ttH_hcc": 898,
      "ttH_hbb": 880,
      "ttH_htt": ROOT.kGray,
      "ttZ": 829,
      "ttbarW": 801,
      "singlet": 859,
      "diboson": 7,
      "qcd-mg": 811,
      "wjets": 821,
      "zjets": 821,
      "ttH_hww": 43,
      "ttZ_Zbb": 30,
      "ttZ_Zcc": 38,
      "ttZ_Zother": 829,
    }  