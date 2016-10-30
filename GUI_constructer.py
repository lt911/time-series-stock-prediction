__author__ = 'ktc312'

from Tkinter import *
import tkMessageBox
import ttk as ttk
from calendar import *
from datetime import *
from dateutil.relativedelta import relativedelta
from other_functions import *
from analysis import *
from PIL import Image, ImageTk


# The main window
class Master:
    def __init__(self, master):

        # configures of main window
        master.title('Final Project')
        master.resizable(False, False)
        master.configure(background='light gray')

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 15, 'bold'))

        # the first frame, content header and some other text to explain what the program do
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()

        # two label in the first frame
        ttk.Label(self.frame_header, wraplength=440, text='Forecasting Stock Price Using ARIMA Model',
                  background='Gray', font=('PHOSPHATE', 20, 'bold')
                  ).grid(row=0, column=0, padx=10, pady=15)
        ttk.Label(self.frame_header, wraplength=440, background='Gray',
                  text="Please input the ticker of the stock you are interested in, then input the start date and "
                       "end date (for example: 2010-10-30). The end date can be TODAY since we will import the most"
                       " updated data from Yahoo Finance API. (Please enter the start date first, then enter "
                       "the end date)", font=('Arial', 12), foreground="black"
                  ).grid(row=1, column=0, padx=10, pady=15)

        # the second frame, content three input ask user for ticker name, start date ,and end date
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        ttk.Label(self.frame_content, text='Ticker Name:', wraplength=300
                  ).grid(row=0, column=0, padx=5, pady=10)
        ttk.Label(self.frame_content, text='Start Date:', wraplength=100
                  ).grid(row=0, column=1, padx=5, pady=10)
        ttk.Label(self.frame_content, text='End Date:', wraplength=100
                  ).grid(row=0, column=2, padx=5, pady=10)

        # create tkinter.StringVar variables for default values in the input widgets
        self.ticker_example = StringVar()
        self.df_start_date = StringVar()
        self.date_of_today = StringVar()

        self.ticker_example.set('ticker symbol')
        self.df_start_date.set('yyyy-mm-dd')
        # self.ticker_example.set('yhoo')
        # self.df_start_date.set('2011-11-11')
        self.date_of_today.set(get_today())

        self.ticker_example.trace("w", self.determine_function)
        self.df_start_date.trace("w", self.determine_function)
        self.date_of_today.trace("w", self.determine_function)

        sdv = master.register(self.start_date_validate)
        edv = master.register(self.end_date_validate)
        tnv = master.register(self.ticker_validate)


        # create three tkinter.Entry input widgets
        self.entry_name = ttk.Entry(self.frame_content, textvariable=self.ticker_example,
                                    validate='key', validatecommand=(tnv, '%P'),
                                    width=24, foreground="gray")
        self.entry_start_date = ttk.Entry(self.frame_content, textvariable=self.df_start_date,
                                          validate='key', validatecommand=(sdv, '%P'),
                                          width=10, foreground="gray")
        self.entry_end_date = ttk.Entry(self.frame_content, textvariable=self.date_of_today,
                                        validate='key', validatecommand=(edv, '%P'),
                                        width=10, foreground="black")

        # put these three Entry widgets onto the frame
        self.entry_name.grid(row=1, column=0, padx=5)
        self.entry_start_date.grid(row=1, column=1, padx=5)
        self.entry_end_date.grid(row=1, column=2, padx=5)

        # create the notification about entry data
        self.input_validate = StringVar()
        # the test will change depends on what user entry
        self.input_validate.set('Please Enter Ticker Symbol, Start Date, and End Date')
        self.validate_label = ttk.Label(self.frame_content, textvariable=self.input_validate, wraplength=300
                  , foreground = 'black')
        self.validate_label.grid(row=2, column=0, columnspan=3, padx=5, pady=10)

        # create the clear and submit button
        self.clear_button = ttk.Button(self.frame_content, text='Clear', command=self.clear)
        self.submit_button = ttk.Button(self.frame_content, text='Submit', command=self.submit, state=DISABLED)

        # put these two button onto the frame
        self.clear_button.grid(row=3, column=0, padx=5, pady=5, sticky=E)
        self.submit_button.grid(row=3, column=1, padx=5, pady=5)

        # set default values for keys of tkinter's validate command
        self.ticker_pass = False
        self.start_date_pass = False
        self.end_date_pass = True

    def submit(self):
        # function of submit button, open new window when click
        # No loading information when opening the new window,
        # disable the submit button to prevent user open multiple windows
        global Entry_name
        global Start_date
        global End_date
        # enable to pass these variables to other classes(windows)
        Entry_name = self.entry_name.get()
        Start_date = self.entry_start_date.get()
        End_date = self.entry_end_date.get()
        # open Toplevel window
        self.newWindow = Toplevel()
        self.submit_button.configure(state=DISABLED)
        self.app = ResultWindow(self.newWindow)

    def clear(self):
        # function of clear button, turn values in Entry widgets back to default
        self.ticker_example.set('ticker symbol')
        self.df_start_date.set('yyyy-mm-dd')
        self.date_of_today.set(get_today())
        self.ticker_pass = False
        self.start_date_pass = False
        self.end_date_pass = True
        # disable the submit button, only allow open one top level window at a time
        self.submit_button.configure(state=DISABLED)

    def start_date_validate(self, input_date):
        """ Method to Validate Entry text input size, Author: S.Prasanna """
        TEXT_MAXINPUTSIZE = 10
        if (self.entry_start_date.index(END) >= TEXT_MAXINPUTSIZE - 1):
            self.entry_start_date.delete(TEXT_MAXINPUTSIZE - 1)

        # check if start date input is valid
        two_month = relativedelta(months=2)

        try:
            end_date = datetime.strptime(self.entry_end_date.get(), '%Y-%m-%d')
            date = datetime.strptime(input_date, '%Y-%m-%d')
        except ValueError:
            self.start_date_pass = False
            self.entry_start_date.configure(foreground= 'black')
            return True
        else:
            # must at least have two months time period
            if date + two_month < end_date:
                self.start_date_pass = True
                self.entry_start_date.configure(foreground= 'black')
                return True
            else:
                self.start_date_pass = False
                self.entry_start_date.configure(foreground= 'black')
                return True

    def end_date_validate(self, input_date):
        TEXT_MAXINPUTSIZE = 10
        if (self.entry_end_date.index(END) >= TEXT_MAXINPUTSIZE - 1):
            self.entry_end_date.delete(TEXT_MAXINPUTSIZE - 1)
        # check if end date input is valid
        two_month = relativedelta(months=2)

        try:
            start_date = datetime.strptime(self.entry_start_date.get(), '%Y-%m-%d')
            date = datetime.strptime(input_date, '%Y-%m-%d')
        except ValueError:
            self.end_date_pass = False
            self.entry_end_date.configure(foreground= 'black')
            return True

        else:
            if date <= datetime.now():
                if start_date + two_month < date:
                    self.end_date_pass = True
                    self.entry_end_date.configure(foreground= 'black')
                    return True
                else:
                    self.end_date_pass = False
                    self.entry_end_date.configure(foreground= 'black')
                    return True
            else:
                self.end_date_pass = False
                self.entry_end_date.configure(foreground= 'black')
                return True

    def ticker_validate(self, input_name):
        TEXT_MAXINPUTSIZE = 10
        if (self.entry_name.index(END) >= TEXT_MAXINPUTSIZE - 1):
            self.entry_name.delete(TEXT_MAXINPUTSIZE - 1)
        # check if ticker name input is valid (in the ticker symbols list)
        ticker_list = get_ticker_list()
        try:
            input_name = input_name.upper()
        except:
            pass
        if input_name in ticker_list:
            self.ticker_pass = True
            self.entry_name.configure(foreground= 'black')
            return True
        else:
            self.ticker_pass = False
            self.entry_name.configure(foreground= 'black')
            return True

    def determine_function(self, ticker, start, end):
        # validate function, if all three Entry widget have valid input, then enable the submit button
        if self.start_date_pass and self.end_date_pass and self.ticker_pass:
            self.input_validate.set('Ready to Submit!')
            self.validate_label.configure(foreground = 'dark green')
            self.submit_button.configure(state=NORMAL)
        elif self.start_date_pass and self.end_date_pass:
            self.input_validate.set('Invalid Ticker Symbol')
            self.validate_label.configure(foreground = 'red')
            self.submit_button.configure(state=DISABLED)
        elif self.end_date_pass and self.ticker_pass:
            self.input_validate.set('Invalid Start Date')
            self.validate_label.configure(foreground = 'red')
            self.submit_button.configure(state=DISABLED)
        else:
            self.input_validate.set('Invalid End Date')
            self.validate_label.configure(foreground = 'red')
            self.submit_button.configure(state=DISABLED)


# the second window, shows results
class ResultWindow:
    def __init__(self, master):

        # configures of second window
        self.master = master
        master.title('Results')
        master.resizable(False, False)

        # get the input values from the main window class
        global Entry_name
        global Start_date
        global End_date

        # #thees assignment is just for testing
        # Entry_name = 'goog'
        # Start_date = '2014-12-01'
        # End_date = '2015-12-10'

        if not test_ticker(Entry_name):
            print "Can't get the data"
            tkMessageBox.showinfo(title='Feedback', message="Can't get the data")
            try:
                self.master.destroy()
            except TclError:
                print 'TclError, Result window closed, however.'
                pass
        else:
            self.analysis = Analysis(Start_date, End_date, Entry_name)

            # this variable is for MoreWindow
            global param_df
            param_df = str(self.analysis.param_df())

            # set all the variables to have correct values
            self.stock = Share(Entry_name)
            self.company_name = get_company_name(Entry_name)
            self.predict_values = self.analysis.predict_val().values
            self.descriptive_stat = self.analysis.descriptive_stat()

            self.company = StringVar()
            self.symbol = StringVar()
            self.start_date = StringVar()
            self.end_date = StringVar()

            self.company.set(self.company_name)
            self.symbol.set(Entry_name.upper())
            self.start_date.set(Start_date)
            self.end_date.set(End_date)

            self.prev_close = StringVar()
            self.highest_price = StringVar()
            self.lowest_price = StringVar()
            self.ave_price = StringVar()
            self.trade_days = StringVar()

            self.prev_close.set(str(self.stock.get_price()))
            self.highest_price.set(str(self.descriptive_stat[7]).replace('[', '').replace(']', ''))
            self.lowest_price.set(str(self.descriptive_stat[3]).replace('[', '').replace(']', ''))
            self.ave_price.set(str(self.descriptive_stat[1]).replace('[', '').replace(']', ''))
            self.trade_days.set(str(self.descriptive_stat[0]).replace('[', '').replace(']', ''))

            self.first_price = StringVar()
            self.second_price = StringVar()
            self.third_price = StringVar()
            self.fourth_price = StringVar()
            self.fifth_price = StringVar()
            self.sixth_price = StringVar()
            self.seventh_price = StringVar()

            self.first_price.set(str(self.predict_values[0]).replace('[', '').replace(']', ''))
            self.second_price.set(str(self.predict_values[1]).replace('[', '').replace(']', ''))
            self.third_price.set(str(self.predict_values[2]).replace('[', '').replace(']', ''))
            self.fourth_price.set(str(self.predict_values[3]).replace('[', '').replace(']', ''))
            self.fifth_price.set(str(self.predict_values[4]).replace('[', '').replace(']', ''))
            self.sixth_price.set(str(self.predict_values[5]).replace('[', '').replace(']', ''))
            self.seventh_price.set(str(self.predict_values[6]).replace('[', '').replace(']', ''))

            # Create all the frames in this window
            self.frame_header = ttk.Frame(self.master, width=600, height=100)# ,relief = RIDGE)
            self.frame_info = ttk.Frame(self.master, width=200, height=500 ,  relief = RIDGE)
            self.frame_plot = ttk.Frame(self.master, width=400, height=400)  # , relief = RIDGE)
            self.frame_other = ttk.Frame(self.master, width=400, height=100)#  ,  relief = RIDGE)
            self.frame_button = ttk.Frame(self.master, width=600, height=100)  # ,  relief = RIDGE)
            self.frame_header.grid(row=0, column=0, columnspan=2)
            self.frame_info.grid(row=1, column=0, rowspan=2, sticky="nsew")
            self.frame_plot.grid(row=1, column=1, sticky="nsew")
            self.frame_other.grid(row=2, column=1, sticky="nsew")
            self.frame_button.grid(row=3, column=0, columnspan=2)

            # create the header label needed in the results window
            ttk.Label(self.frame_header, wraplength=800, text='Financial Time Series Data Forecasting'
                      , background='Gray', font=('PHOSPHATE', 30, 'bold')
                      ).pack(padx=200)
            ttk.Label(self.frame_header, wraplength=800, text='This results include: '
                                                              '(1) The basic information of the stock; (2) The statistical '
                                                              'summary of the time series data (the stock historical prices);'
                                                              ' (3) The plot of the original data and the predicted data.'
                      ).pack(pady=5)

            # create a notebook widget to show the plots
            self.plot_notebook = ttk.Notebook(self.master, width=400, height=400)
            self.f1 = ttk.Frame(self.plot_notebook)  # first page, which would get widgets gridded into it
            self.f2 = ttk.Frame(self.plot_notebook)  # second page
            self.plot_notebook.add(self.f1, text='Compare')
            self.plot_notebook.add(self.f2, text='Predict')
            self.plot_notebook.grid(row=1, column=1, sticky="nsew")

            # create plots and open the plots
            self.analysis.compare_plot()
            self.compare_plot = ImageTk.PhotoImage(Image.open('Predicted_vs_historical_data.jpg'
                                                              ).resize((400, 400), Image.ANTIALIAS))
            self.analysis.predict_plot()
            self.predict_plot = ImageTk.PhotoImage(Image.open('Predicted_plots.jpg'
                                                              ).resize((400, 400), Image.ANTIALIAS))
            # put plots onto the Notebook widget
            compare_plot_label = Label(self.f1, image=self.compare_plot)
            predict_plot_label = Label(self.f2, image=self.predict_plot)
            compare_plot_label.pack()
            predict_plot_label.pack()

            # create all the content labels needed
            ttk.Label(self.frame_info, text='Stock Information:',
                      wraplength=200, anchor=NW, justify=LEFT, font=('Arial', 15, 'bold')
                      ).grid(row=0, column=0, columnspan=2, pady=5, padx=5)
            ttk.Label(self.frame_info, text='Company Name:', wraplength=200, justify=LEFT
                      ).grid(row=1, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_info, textvariable=self.company, wraplength=200, justify=LEFT
                      ).grid(row=1, column=1, sticky=W, padx=5)
            ttk.Label(self.frame_info, text='Ticker Symbol:', wraplength=200, justify=LEFT
                      ).grid(row=2, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_info, textvariable=self.symbol, wraplength=200, justify=LEFT
                      ).grid(row=2, column=1, sticky=W, padx=5)
            ttk.Label(self.frame_info, text='Start Date:', wraplength=200, justify=LEFT
                      ).grid(row=3, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_info, textvariable=self.start_date, wraplength=200, justify=LEFT
                      ).grid(row=3, column=1, sticky=W, padx=5)
            ttk.Label(self.frame_info, text='End Date:', wraplength=200, justify=LEFT
                      ).grid(row=4, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_info, textvariable=self.end_date, wraplength=200, justify=LEFT
                      ).grid(row=4, column=1, sticky=W, padx=5)
            ttk.Label(self.frame_info, text=' ', wraplength=200, justify=LEFT
                      ).grid(row=5, column=0, sticky=W, padx=5)

            ttk.Label(self.frame_info, text='Descriptive Statistics:',
                      wraplength=200, anchor=NW, justify=LEFT, font= ('Arial', 15, 'bold')
                      ).grid(row=6, column=0, columnspan=2, pady=5, padx=5)
            ttk.Label(self.frame_info, text='Prev Close: ', wraplength=200, justify=LEFT
                      ).grid(row=7, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_info, textvariable=self.prev_close, wraplength=200, justify=LEFT
                      ).grid(row=7, column=1, sticky=W, padx=5)
            ttk.Label(self.frame_info, text='Highest Price:', wraplength=200, justify=LEFT
                      ).grid(row=8, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_info, textvariable=self.highest_price, wraplength=200, justify=LEFT
                      ).grid(row=8, column=1, sticky=W, padx=5)
            ttk.Label(self.frame_info, text='Lowest Price:', wraplength=200, justify=LEFT
                      ).grid(row=9, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_info, textvariable=self.lowest_price, wraplength=200, justify=LEFT
                      ).grid(row=9, column=1, sticky=W, padx=5)
            ttk.Label(self.frame_info, text='Average Price:', wraplength=200, justify=LEFT
                      ).grid(row=10, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_info, textvariable=self.ave_price, wraplength=200, justify=LEFT
                      ).grid(row=10, column=1, sticky=W, padx=5)
            ttk.Label(self.frame_info, text='Trade days:', wraplength=200, justify=LEFT
                      ).grid(row=11, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_info, textvariable=self.trade_days, wraplength=200, justify=LEFT
                      ).grid(row=11, column=1, sticky=W, padx=5)
            ttk.Label(self.frame_info, text=' ', wraplength=200, justify=LEFT
                      ).grid(row=12, column=0, sticky=W, padx=5)

            ttk.Label(self.frame_info, text='Conclusion:',
                      wraplength=200, anchor=NW, justify=LEFT, font=('Arial', 15, 'bold')
                      ).grid(row=13, column=0, columnspan=2, pady=5, padx=5)
            ttk.Label(self.frame_info, text=' ', wraplength=200, justify=LEFT
                      ).grid(row=14, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_info, text='(1) in the first graph, the blue line is the actual prices and the green '
                                            'line is the predicted prices using ARIMA model based on the historical '
                                            'prices. You can see the comparison of the real prices and the predicted '
                                            'prices. '
                      , wraplength=250
                      ).grid(row=15, column=0, columnspan=2, sticky=W, padx=5)
            ttk.Label(self.frame_info, text='(2) in the second graph, the blue line represents the historical prices'
                                            ' and the red line is the predicted prices forecast by ARIMA model.'
                      , wraplength=250
                      ).grid(row=16, column=0, columnspan=2, sticky=W, padx=5)

            ttk.Label(self.frame_other, text='Predict Price: Seven Days Price Forecast',
                      wraplength=400, anchor=NW, justify=LEFT, font= ('Arial', 15, 'bold')
                      ).grid(row=0, column=0, columnspan=4, pady=5, padx=5)
            ttk.Label(self.frame_other, text='1st: ', wraplength=200, justify=LEFT
                      ).grid(row=1, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_other, textvariable=self.first_price, wraplength=200, justify=LEFT
                      ).grid(row=1, column=1, sticky=W, padx=5)
            ttk.Label(self.frame_other, text='2nd: ', wraplength=200, justify=LEFT
                      ).grid(row=2, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_other, textvariable=self.second_price, wraplength=200, justify=LEFT
                      ).grid(row=2, column=1, sticky=W, padx=5)
            ttk.Label(self.frame_other, text='3rd: ', wraplength=200, justify=LEFT
                      ).grid(row=3, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_other, textvariable=self.third_price, wraplength=200, justify=LEFT
                      ).grid(row=3, column=1, sticky=W, padx=5)
            ttk.Label(self.frame_other, text='4th: ', wraplength=200, justify=LEFT
                      ).grid(row=4, column=0, sticky=W, padx=5)
            ttk.Label(self.frame_other, textvariable=self.fourth_price, wraplength=200, justify=LEFT
                      ).grid(row=4, column=1, sticky=W, padx=5)

            ttk.Label(self.frame_other, text='5th: ', wraplength=200, justify=LEFT
                      ).grid(row=1, column=2, sticky=W, padx=5)
            ttk.Label(self.frame_other, textvariable=self.fifth_price, wraplength=200, justify=LEFT
                      ).grid(row=1, column=3, sticky=W, padx=5)
            ttk.Label(self.frame_other, text='6th: ', wraplength=200, justify=LEFT
                      ).grid(row=2, column=2, sticky=W, padx=5)
            ttk.Label(self.frame_other, textvariable=self.sixth_price, wraplength=200, justify=LEFT
                      ).grid(row=2, column=3, sticky=W, padx=5)
            ttk.Label(self.frame_other, text='7th: ', wraplength=200, justify=LEFT
                      ).grid(row=3, column=2, sticky=W, padx=5)
            ttk.Label(self.frame_other, textvariable=self.seventh_price, wraplength=200, justify=LEFT
                      ).grid(row=3, column=3, sticky=W, padx=5)

            # create quit button, will close the second window
            self.quitButton = ttk.Button(self.frame_button, text='Quit', width=25, command=self.close_windows)
            self.moreButton = ttk.Button(self.frame_button, text='More', width=25, command=self.more)
            ttk.Label(self.frame_button, text='   ', width=11).grid(row=0, column=0, padx=5)
            ttk.Label(self.frame_button, text='   ', width=11).grid(row=0, column=3, padx=5)
            self.quitButton.grid(row=0, column=1, padx=5, pady=5, sticky=S)
            self.moreButton.grid(row=0, column=2, padx=5, pady=5, sticky=S)

    def close_windows(self):
        # the function to close the second window
        self.master.destroy()

    def more(self):
        # function of more button, open new window when click
        self.newWindow = Toplevel()
        self.app = MoreWindow(self.newWindow)


class MoreWindow:
    def __init__(self, master):
        self.master = master
        # configures of the third window
        master.title('More')
        master.resizable(False, False)

        # get the values of param_df
        global param_df

        # the label of the header
        Label(self.master, text="By looking these plots, we can determine 'd'", wraplength=400, justify=LEFT
              ).pack()

        # create the notebook widget to show plots
        self.plot_notebook = ttk.Notebook(self.master, width=400, height=400)
        self.f1 = ttk.Frame(self.plot_notebook)  # first page, which would get widgets gridded into it
        self.f2 = ttk.Frame(self.plot_notebook)  # second page
        self.f3 = ttk.Frame(self.plot_notebook)
        self.plot_notebook.add(self.f1, text='ACF vs PACF')
        self.plot_notebook.add(self.f2, text='diff 1')
        self.plot_notebook.add(self.f3, text='diff 2')
        self.plot_notebook.pack()

        # plots may not be created, so use 'try' to open .jpg file, put the plots onto the notebook widget
        # if it can open
        try:
            self.ACF_plot = ImageTk.PhotoImage(Image.open('ACF_vs_PACF.jpg'
                                                          ).resize((400, 400), Image.ANTIALIAS))
            Label(self.f1, image=self.ACF_plot).pack()
        except:
            Label(self.f3, text="Can't find the plot of ACF vs PACF").pack()
        try:
            self.diff1_plot = ImageTk.PhotoImage(Image.open('ACF_vs_PACF_diff1.jpg'
                                                            ).resize((400, 400), Image.ANTIALIAS))
            Label(self.f2, image=self.diff1_plot).pack()
        except:
            Label(self.f3, text='diff1 test is not needed since we already have the optimal d.').pack()
        try:
            self.diff2_plot = ImageTk.PhotoImage(Image.open('ACF_vs_PACF_diff2.jpg'
                                                            ).resize((400, 400), Image.ANTIALIAS))
            Label(self.f3, image=self.diff2_plot).pack()
        except:
            Label(self.f3, text='diff2 test is not needed since diff1 has already achieved the optimal d.').pack()

        # get the param_df and put it into the label, will appears under the notebook widget
        self.param_df = StringVar()
        self.param_df.set(param_df)
        Label(self.master, textvariable=self.param_df).pack()
        Label(self.master, text='We use these parameter to fit an ARIMA model for prediction, '
                                'which provides the results in "result window"', wraplength=400, justify=LEFT
              ).pack()

        # create the quit button
        self.quitButton = Button(self.master, text='Quit', width=25, command=self.close_windows)
        self.quitButton.pack()

    def close_windows(self):
        # the function to close the second window
        self.master.destroy()
