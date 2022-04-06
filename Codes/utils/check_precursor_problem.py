import cobra
from cobra import Model, Reaction, Metabolite
import escher 
from escher import Builder
import numpy as np
import pandas as pd
import glob
def check_precursor_problem(model,list_of_rxns):

    not_produced = []
    for r in list_of_rxns:
        for m in model.reactions.get_by_id(r).metabolites:
            if model.reactions.get_by_id(r).lower_bound == 0:
                n = 0
            else:
                n = 9999999
            if model.reactions.get_by_id(r).metabolites[m] < n: #substrates only\
                new_rxn = Reaction('DM' + m.id)
                new_rxn.add_metabolites({m:-1})
                new_rxn.lower_bound = 0
                model.add_reaction(new_rxn)# added the exchange reaction for this metabolite

                model.objective = model.reactions.get_by_id('DM' + m.id)# ask for the flux of this metabolite
                f = model.optimize().objective_value
                if f < 1e-6:#if the flux lower than 1e-6, it means this metabolite cannot be produced
                    not_produced.append(m.id)
                model.reactions.get_by_id('DM' + m.id).remove_from_model()# remove the reaction that was just added above
            model.objective = model.reactions.NGAM # set the NGAM reaction as objective reaction, otherwise no objective reaction
        not_produced = set(not_produced)# get a unique list of element in list not_produced
                
    return (not_produced) # print the unique list of metabolites not produced
