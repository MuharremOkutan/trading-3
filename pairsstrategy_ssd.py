#!/usr/bin/env python
"""
This module implements a pairs trading algorithm. The trading
algrorithm is based on Sum of Squared Distance (SSD) method.
"""
import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt
pd.options.display.mpl_style = 'default'
from itertools import combinations

window          = 261 #251
fw_start        = 1
fw_end          = window
tw_start        = 0 #fw_end
tw_end          = 0 #131
window_trade    = 130 #125 #132
industries      = 0
portfolio       = pd.DataFrame()
industry        = 0

def get_df( ser1, ser2,):
    pairs       = pd.DataFrame(index=ser2.index)
    pairs['y']  = ser1
    pairs['x']  = ser2
 
    return pairs

def formation_trading(pairs): #window=261
    print('formation_trading            ..... >')
    global fw_start, fw_end, tw_start, tw_end, window_trade

    closeness           = []
    pairs['long']       = np.nan
    pairs['short']      = np.nan
    pairs['exit']       = np.nan
    
    # Pairs formation period of 12 months, everytime we get into a
    # new formation window, determine the newly closely moving
    # pairs.
    print('Formation window %d == %d' % ((fw_end - fw_start), window-1))

    print('Formation window %d :  %d' % (fw_start, fw_end))
    print('Trade window     %d :  %d' % (tw_start, tw_end))
    y = pairs['y'][fw_start:fw_end]
    x = pairs['x'][fw_start:fw_end]
    
    y_comp      = y.pct_change() + 1
    y_comp_cum  = y_comp.cumprod()
    x_comp      = x.pct_change() + 1
    x_comp_cum  = x_comp.cumprod()
    
    distance    = y_comp_cum  - x_comp_cum
    distance_std    = distance.std()

    # Generate market signals over the next 6 months
    entry_threshold     = 2 * distance_std      # 2 standard deviations
    exit_threshold      = distance.mean() #The next crossing of the prices
    
    y_tp = pairs['y'][tw_start:tw_end]
    x_tp = pairs['x'][tw_start:tw_end]
    y_tp_comp      = y_tp.pct_change() + 1
    y_tp_comp_cum  = y_tp_comp.cumprod()
    x_tp_comp      = x_tp.pct_change() + 1
    x_tp_comp_cum  = x_tp_comp.cumprod()
    tp_distance    = y_tp_comp_cum  - x_tp_comp_cum

    pairs.ix[tw_start:tw_end, 'distance'] = tp_distance
    pairs.ix[tw_start:tw_end, 'long']      = (pairs[tw_start:tw_end]['distance'] <= -entry_threshold) * 1.0
    pairs.ix[tw_start:tw_end, 'short']     = (pairs[tw_start:tw_end]['distance'] >= entry_threshold) * 1.0
    pairs.ix[tw_start:tw_end, 'exit']      = (np.abs(pairs[tw_start:tw_end]['distance']) <= np.abs(exit_threshold)) * 1.0
            
    print('formation_trading            ..... <')

    return pairs[tw_start:tw_end]

def market_position(pairs):
    print('market_positions:            ... >')
    pairs['long_mkt']   = 0
    pairs['short_mkt']  = 0

    
    pairs.ix[:]['long_mkt'][pairs['long']==1] = 1
    pairs.ix[:]['short_mkt'][pairs['short']==1] = 1
    pairs.ix[:]['long_mkt'][pairs['exit']==1] = 0
    pairs.ix[:]['short_mkt'][pairs['exit']==1] = 0
    print('market_positions:            ... <')
    return pairs

def trading_pair_returns(pairs): # Perhaps this functions and others do not need to know the real indexing
    print('trading_pair_returns         ... >')
    pairs['positions']  = pairs['long_mkt'] - pairs['short_mkt']
    ret_y               = pairs['y'].pct_change()
    ret_x               = pairs['x'].pct_change()
    spread              = ret_x - ret_y
    ret_xy              = pairs['positions'] * spread
    pairs['returns']    = ret_xy
    return pairs['returns']

def trade(ser1, ser2):
    print('trade >')
    trading_pairs       = get_df(ser1, ser2)
    results             = formation_trading(trading_pairs)
    market_df           = market_position(results)
    returns             = trading_pair_returns(market_df)
    print('The length of returns: %d' % (len(returns)))

    return returns

#===========================================================#
#                       Portfolio                           #
#===========================================================#

# Pick the stocks pairs from an industry
def loadfile():
    """
    This function loads the file/sheet containing the pairs to be
    traded per industry. Change the location and sheetname parameters
    when necessary to point to the desired files. The data is
    preloaded into the environment and what is passed in this function
    is an excel file describing the data.
    """
    print('loadfile: >')
#    dir         = '../Data_EuroStoxx/dataset_description.xlsx'
#    sheetname   = 'pd_data_desc_ICBsectnames'
    dir         = '../Data_EuroStoxx/dataset_description.xlsx'
    sheetname   = 'pd_data_desc_L2sectnames'

    xls_file    = pd.ExcelFile(dir)
    pairs       = xls_file.parse(sheetname, index_col=0, header=0, parse_cols=[0, 1, 2])
    pairs       = pairs.sort(columns=['Industry'])
    return pairs

def portfolios(pairs_df, data_df):
    """
    This function first identifies the trading pairs in each industry
    so as to form a portfolio. The pairs are traded and the returns
    aggregated. The traded pairs that constitute the portfolio are
    equally weighted.
    """
    global window, fw_end, fw_start, industries, portfolio, industry, tw_start, tw_end, window_trade # name1, name2
    print('portfolios >')
    portfolio_returns   = pd.DataFrame(index=data_df.index)     # Collect pairs returns
    portfolios_ret_df   = pd.DataFrame(index=data_df.index)     # Collect all portfolio returns
    industries  = pairs_df['Industry'].unique()
    for i in industries:
        industry = i
        fw_start  = 1
        fw_end    = window
        tw_start  = (fw_end + 1)
        tw_end    = tw_start + window_trade            # Next six months
        trading_counter = 0

        print('Industry:                                        ... %s' % industry)
        portfolio       = pairs_df[pairs_df['Industry'] == industry]
        if len(portfolio) <= 2: continue        # We skip portfolios made of 1 stock only
        portfolio       = formportfoliopairs(portfolio, industry)
        portfolio       = rebalanceportfolio(portfolio, data_df)
        portfolio_top   = portfolio.sort(columns=['distance'])[0:20]   # Pick top 20 portfolios
        print('Portfolio size: %d' % len(portfolio_top.index))
        print(portfolio)
        print(portfolio_top)
        while (len(data_df[fw_start:fw_end]) == (window-1)) and (len(data_df[tw_start: tw_end]) == window_trade):
            print('Formation window %d == %d' % ((fw_end - fw_start), window-1))
            for i in range(len(portfolio_top.index)):
                stock1_name = portfolio_top.ix[portfolio_top.index[i]]['Stock1']
                stock2_name = portfolio_top.ix[portfolio_top.index[i]]['Stock2']
#                 name1 = stock1_name # Remove after testing
#                 name2 = stock2_name

                # Select pairs from the data and trade
                stock1      = data_df[stock1_name][industry]                      # Series
                stock2      = data_df[stock2_name][industry]                      # Series
                
                returns     = trade(stock1, stock2)                               # Call trader
                name        = str('pair_%d' % i)
                if(returns.name != name): 
                    returns.name=name
                print('****Returns name: %s*****' % returns.name)
                print('Formation window %d :  %d' % (fw_start, fw_end))
                print('Trade window     %d :  %d' % (tw_start, tw_end))
                portfolio_returns.ix[tw_start:tw_end, name] = returns

            ind_port_returns        = portfolio_returns.sum(axis=1)             # portfolio returns, add all the pairs' returns
            ind_port_returns        = ind_port_returns / len(portfolio.index)   # returns scaled by port size
            if not ind_port_returns.name: ind_port_returns.name = industry      # If no name give name
            portfolios_ret_df.ix[tw_start:tw_end, industry] = ind_port_returns
            fw_start      = fw_end - window_trade #tw_start #tw_end + 1
            fw_end        = fw_start + window - 1
            tw_start  = (fw_end + 1)
            tw_end    = tw_start + window_trade                                 # Next six months
            trading_counter += 1
            portfolio                   = rebalanceportfolio(portfolio, data_df)
            portfolio_top   = portfolio.sort(columns=['distance'])[0:20]        # Take the top closest pairs, note they are sorted
            print(portfolio_top)
            print('Number of trading times %d' % trading_counter)

    return portfolios_ret_df


def rebalanceportfolio(portfolio, data_df):
    """
    Take the existing industry portfolio and create new pairs over the
    new estimation period and return the top X portfolios
    """
    print('rebalanceportfolio           ...... >')
    global industry
    df          = pd.DataFrame(portfolio.index)
    closeness   = []

    for i in portfolio.index:
        stock1_name     = portfolio.ix[i]['Stock1']
        stock2_name     = portfolio.ix[i]['Stock2']
        stock1          = data_df[fw_start:fw_end][stock1_name][industry]       # Series
        stock2          = data_df[fw_start:fw_end][stock2_name][industry]       # Series
        
        stock1_comp     = stock1.pct_change() + 1     
        stock1_comp_cum = stock1_comp.cumprod()
        stock2_comp     = stock2.pct_change() + 1
        stock2_comp_cum  = stock2_comp.cumprod()
        
        distance    = stock1_comp_cum  - stock2_comp_cum
        distance_sq = np.square(distance)
        closeness.append( (distance_sq.sum(), stock1_name, stock2_name)) 
    df = pd.DataFrame(closeness, columns=['distance', 'Stock1', 'Stock2'])
    print('rebalanceportfolio           ...... <')
    return df

def runtest(data):
    pairs_df    = loadfile()
    results     = portfolios(pairs_df, data)
    return results

def formportfoliopairs(indpairs, industry):
    names       = list(indpairs['Name'])
    names       = pd.Series(names).unique()
    pairs       = list(combinations(names, 2))     # Different combinations of series
    portfolio   = pd.DataFrame(pairs, columns=['Stock1', 'Stock2'])
    portfolio['industry'] = industry
    
    return portfolio

