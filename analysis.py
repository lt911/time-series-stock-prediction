__author__ = 'liz'

from yahoo_finance import Share
import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
from scipy import stats
import matplotlib.pyplot as plt
import scikits.statsmodels.api as sm
import scikits.statsmodels.tsa.arima_process as tsp
import scikits.statsmodels.tsa.stattools as tss
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima_model import ARIMA

import warnings
warnings.filterwarnings("ignore")

class Analysis:
    '''class which deals with all the analytical procedures'''

    def __init__(self, start_date, end_date, ticker):
        '''clean data and store class attributes'''
        stock = Share(ticker)
        df = pd.DataFrame(stock.get_historical(start_date,end_date))[['Date','Adj_Close']]
        df['Adj_Close'] = df['Adj_Close'].astype(float)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_index(by = 'Date', ascending = True)
        df.index = range(len(df))
        df.columns = ['Date', 'Price']
        self.df = df
        self.ts = df.set_index('Date')
        self.date = df['Date']
        self.val = df['Price']
        self.start = self.ts.index[0]
        self.end = self.ts.index[-1]

        # following Series are used for finding the optimal parameter d by comparing the acf's and
        # pacf's for the timeseries at different diff stage.
        self.diff1_val = pd.Series(np.diff(self.val))
        self.diff1_val_na = pd.Series(np.concatenate(([np.nan], self.diff1_val.values)))
        self.diff2_val = pd.Series(np.diff(self.diff1_val_na))
        self.diff2_val_na = pd.Series(np.concatenate(([np.nan], self.diff2_val.values)))

    def descriptive_stat(self):
        '''function shows basic decriptive stats about the timeseries data, returns statistics in an array'''
        print "========================"
        print "Descriptive Statistics"
        print self.df.describe()
        print "======================== \n"
        return self.df.describe().values

    def d_param(self, diff):
        '''function takes different values for difference step, and returns true or false flag if acf and pacf values
        lie into the threshold area'''
        THRESHOLD = 0.08
        if diff == 0:
            acf = tss.acf(self.val)
            pacf = tss.pacf(self.val)
            # acf and pacf plots
            fig = plt.figure(figsize = (12,8))
            ax1 = fig.add_subplot(121)
            fig = plot_acf(self.val,lags =40 ,ax=ax1)
            ax2 = fig.add_subplot(122, sharey=ax1)
            fig= plot_pacf(self.val, lags = 40, ax =ax2)
            plt.savefig('ACF_vs_PACF.jpg')
            plt.close()
            # check if most acf and pacf are lie in the accepted region for diff0
            acf_percent = len(acf[np.abs(acf) <= THRESHOLD])/float(len(acf))
            pacf_percent = len(pacf[np.abs(pacf) <= THRESHOLD])/float(len(pacf))
            return (acf_percent >= .65) and (pacf_percent >= 0.65)

        elif diff == 1:
            diff1_acf = tss.acf(self.diff1_val.dropna())
            diff1_pacf = tss.pacf(self.diff1_val.dropna())
            # for acf and pacf plots
            fig = plt.figure(figsize = (12,8))
            ax1 = fig.add_subplot(121)
            fig = plot_acf(self.diff1_val.dropna(),lags =40 ,ax=ax1)
            ax2 = fig.add_subplot(122, sharey=ax1)
            fig= plot_pacf(self.diff1_val.dropna(), lags = 40, ax =ax2)
            plt.savefig('ACF_vs_PACF_diff1.jpg')
            plt.close()
            # check if most acf and pacf are lie in the accepted region for diff1
            acf_percent = len(diff1_acf[np.abs(diff1_acf) <= THRESHOLD])/float(len(diff1_acf))
            pacf_percent = len(diff1_pacf[np.abs(diff1_pacf) <= THRESHOLD])/float(len(diff1_pacf))
            return (acf_percent >= .65) and (pacf_percent >= 0.65)

        elif diff == 2:
            diff2_acf = tss.acf(self.diff2_val.dropna())
            diff2_pacf = tss.pacf(self.diff2_val.dropna())
            # check save fig for acf and pacf plots
            fig = plt.figure(figsize = (12,8))
            ax1 = fig.add_subplot(121)
            fig = plot_acf(self.diff2_val.dropna(),lags =40 ,ax=ax1)
            ax2 = fig.add_subplot(122, sharey=ax1)
            fig = plot_pacf(self.diff2_val.dropna(), lags = 40, ax =ax2)
            plt.savefig('ACF_vs_PACF_diff2.jpg')
            plt.close()
            # check if most acf and pacf are lie in the accepted region for diff2
            acf_percent = len(diff2_acf[np.abs(diff2_acf) <= THRESHOLD])/float(len(diff2_acf))
            pacf_percent = len(diff2_pacf[np.abs(diff2_pacf) <= THRESHOLD])/float(len(diff2_pacf))
            return (acf_percent >= .65) and (pacf_percent >= 0.65)

        else:
            raise InvalidParamError

    def d_determination(self):
        '''fuction which determines the value for d (distancing)'''
        if self.d_param(0):
            return 0
        elif self.d_param(1):
            return 1
        elif self.d_param(2):
            return 2
        else:
            # print "Couldn't get a best diff model, so we use diff1 model"
            return 1

    def param_dict(self):
        '''build a dictionary to map param orders to aics'''
        d = self.d_determination()
        if d == 0:
            ts = self.ts
        elif d == 1:
            dic = {'Date' :self.date, 'diff1_val': self.diff1_val_na}
            df_new =pd.DataFrame(dic)
            ts = df_new.set_index('Date')
        else:
            dic = {'Date' :self.date, 'diff2_val': self.diff2_val_na}
            df_new =pd.DataFrame(dic)
            ts = df_new.set_index('Date')
        arima_mod_aics = {}

        # create a nested loop for getting parameters p and q into account. return the parameters in
        # a right order of (p, d, q) when achieves the minimun aic.
        for p in range(3):
            for q in range(3):
                try:
                    order = (p, 0, q)
                    params = (p, d, q)
                    arima_mod = ARIMA(ts.dropna(), order).fit(method = 'css-mle', disp = 0)
                    arima_mod_aics[params] = arima_mod.aic
                except:
#                    arima_mod = ARIMA(ts.dropna(), order).fit(method = 'css', disp = 0 )
#                    print "error raised due to mle method warrning"
                    pass
        return arima_mod_aics

    def param_df(self):
        '''return a dataframe built from the arima_mod_aics'''
        self.aic_df = pd.DataFrame(self.param_dict().items(), columns = ['param order', 'aic'])
        print "========================================"
        print "Parameter order with AICs"
        print self.aic_df
        print "We choose the parameter order with the \n smallest corresponding AIC"
        print "=========================================\n"
        return self.aic_df

    def param_determination(self):
        '''funtion which determines values for parameter's p (autoregressive) and q (moving average)
        based on value of d, returns final parameter order in a tuple'''
        arima_mod_aics = self.param_dict()
        for param, aic in arima_mod_aics.items():
            if aic == min(arima_mod_aics.values()):
                return param

    def arima_model(self):
        ''' uses parameter order determined in param_determination() to fit an ARIMA model, returns model results'''
        order = self.param_determination()
	try:
            self.results = ARIMA(self.ts, order).fit(method = 'css-mle', disp = 0 )
            return self.results
        except:
            self.results = ARIMA(self.ts, order).fit(method = 'css', disp = 0 )
            return self.results

    def predict_val(self):
        '''using arima model to forecast the stock values in the next 7 days'''
        self.pred_val = self.arima_model().forecast(7)[0]
        base = self.end
        self.time_period = [base + timedelta(days = x) for x in range(1,8)]
        pred_df =  pd.DataFrame(self.pred_val, index = self.time_period)
        pred_df.columns = ['Price']
        print "========================================"
        print "Predict Price: Seven-Day Forecast"
        print pred_df
        print "========================================\n"        
        return pred_df

    def compare_plot(self):
        '''generate comparison plot'''
        result = self.arima_model()
        fig = result.plot_predict()
        plt.savefig('Predicted_vs_historical_data.jpg')
        print "Please check the save 'Predicted_vs_historical_data.jpg' for the comarison of \n historical data and the predicted plot.\n"

    def predict_plot(self):
        '''generate prediction plot'''
        pred_df =  self.predict_val()
        pred_time = pred_df.index.astype(datetime)
        pred_vals = pred_df['Price']
        scale1 = np.mean(self.val)
        scale2 = np.mean(self.val[-40:])

        fig = plt.figure(figsize = (12, 8))
        ax1 = fig.add_subplot(211)
        ax1.plot_date(self.date.astype(datetime), self.val, '-b', label = 'original data')
        ax1.plot_date(pred_time, pred_vals, '-r', label = 'predicted values')
        ax1.annotate("Forecast",
            xy=(pred_time[0], pred_vals[0]), xycoords='data',
            xytext=(pred_time[-1] + timedelta(1), scale1), textcoords='data',
            arrowprops=dict(arrowstyle="fancy",
                            connectionstyle="arc3"),
            )
        ax1.set_title('Full plot')
        plt.legend(loc = 'upper left',fancybox = True)

        ax2 = fig.add_subplot(212)
        ax2.plot_date(self.ts.index[-40:].astype(datetime), self.ts.Price[-40:], '-b', label = 'original data')
        ax2.plot_date(pred_time, pred_vals,'+r',label = 'predicted values' )
        plt.xticks(rotation = 45)
        ax2.annotate("Forecast",
            xy=(pred_time[0], pred_vals[0]), xycoords='data',
            xytext=(pred_time[-1] + timedelta(1), scale2), textcoords='data',
            arrowprops=dict(arrowstyle="fancy",
                            connectionstyle="arc3"),
            )
        ax2.set_title('Close-up plot')
        plt.legend(loc = 'upper left',fancybox = True)
        plt.savefig('Predicted_plots.jpg')
        print "Please check the save 'Predicted_plot.jpg' for the predicted plots.\n"


class InvalidParamError(Exception):
    def __str__(self):
        # user exception when enter invalid input
        return 'Parameter only takes [0,1,2]'

