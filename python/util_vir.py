import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def insertChar(mystring, position, chartoinsert):
    '''
    :param mystring: Gene string
    :param position: Insert position to the gene
    :param chartoinsert: Character to insert
    :return:
    '''
    mystring = mystring[:position] + chartoinsert + mystring[position:]
    return mystring

def process_gene(s):
    '''
    :param s: Gene string
    :return: Gene string for split
    '''
    pos = [i for i in range(1,50)]
    for i in range (len(pos)):
        p = pos[i]+i
        s = insertChar(s, p, '-')
    return s

def merge_parent(n):
    '''
    # May need to change the file_path for the original data
    :param n: number of generation to process
    :return: pandas dataframe for analysis also save as CSV file
    '''
    pieces = {}
    for i in range (n):
        a = "%sparent.txt" % str(i)
        data = pd.read_csv(a, sep='/n',header=None)
        data.columns = ['Gene']
        data.reset_index()
        df = data.Gene.str.split(' score=',expand=True)
        df.columns = ['Gene','Score']
        pieces[i] = df
    df = pd.concat(pieces)
    df.reset_index(inplace = True)
    df.reset_index(inplace = True)
    df.drop("index",inplace = True, axis = 1)
    df.drop("level_1",inplace = True, axis = 1)
    df.columns= ['Generation','Gene','Score']
    df_2 = df.Gene.apply(lambda x: process_gene(x))
    df.drop('Gene',inplace = True,axis = 1)
    df = df.join(df_2,how = 'left')
    df_s = df.Gene.str.split('-',expand = True)
    df = df.join(df_s,how = 'left')
    df.drop('Gene',inplace = True, axis =1 )
    column_name = ['Generation','Score'] + ['Spot_%i' %i for i in range (1,51)]
    df.columns = column_name
    df.to_csv (r'Merge_parent.csv', index = False, header=True)
    for column in df.columns:
        df[column] = df[column].astype(int)
    return df

def data_generation_single (df,n):
    '''
    :param df: dataframe from the merge_parent function
    :param n: num index of generation
    :return: dataframe for lot the data
    '''
    df_p = df[df['Generation'] == n]
    data = {}
    for i in range (1,50):
        col = "Spot_%d" %i
        index = df_p[col].value_counts().index
        list_count = df_p[col].value_counts()
        res = []
        for i in range (4):
            if i in index:
                res.append(list_count[i])
            else:
                res.append(0)
        data[col] = res
    df = pd.DataFrame(data)
    plotdata = df_test.T
    plotdata.index = [i for i in range (1,50)]
    return plotdata

def plot_single(df,n):
    '''
    :param df: dataframe from the data_generation_single
    :param n: number index of the generation
    :return: none save the figure in the current folder
    '''
    plotdata = data_plot
    stacked_data = plotdata.apply(lambda x: x*100/sum(x), axis=1)
    stacked_data.plot(kind="bar", stacked=True)
    plt.title("Generation_%d" % n)
    plt.xlabel("Spot")
    plt.ylabel("Percentage(%)")
    plt.savefig('books_read.png')