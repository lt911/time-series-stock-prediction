'''
GUI ask ticker name, start date, and end date in the following form
ticker_symbol = 'XXXXX'
start_date = 'YYYY-MM-DD'
end_date = 'YYYY-MM-DD'

pass these three variables into main program

df = read_data(ticker_symbol, start_date, end_date)

analysis(df) (this is a class)
df.descriptive will give all the descriptive statistics AS A
df.arma_model will give a forecast price(float or int) AS B
df.plot will give all the plots we need AS C

print A, B, C in 'nice format' in GUI
'''

from GUI_constructer import *

def main():

    root = Tk()
    Master(root)
    root.mainloop()


if __name__ == "__main__":
    main()