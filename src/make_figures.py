from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import matplotlib
import pathlib
import pandas as pd
import numpy as np

ROOT_DIR = pathlib.Path(__file__).parent.parent

structured_data_dir = pathlib.Path().joinpath(ROOT_DIR,"data","structured")
figures_dir = pathlib.Path().joinpath(ROOT_DIR,"figures")

def make_word_cloud(freq,title=None,savefile=None,fontsize=20,figsize=(10,10),
                    width = 190,height=130,scale=3,stopwords=STOPWORDS,
                    dpi=100,background_color="white",
                    colormap="viridis"):

    '''make a wordcloud from word frequency data'''
    mask_path = figures_dir.joinpath("house.jpg")
    mask = np.array(Image.open(mask_path))

    word_cloud = WordCloud(width=width*scale, height=height*scale,background_color=background_color,

                                      max_words=100,
                                      max_font_size=90, 
                                      random_state=42,
                                      mask=mask,
                                      colormap=colormap,
                                      stopwords=stopwords).generate_from_frequencies(freq)

    plt.figure(figsize=figsize,dpi=dpi)
    plt.title(title)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title,fontsize=fontsize)
    plt.tight_layout(pad=0)
    if savefile is not None:
        plt.savefig(savefile,dpi=dpi,pad_inches=0)


matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20) 
matplotlib.rc('axes', labelsize=20)
matplotlib.rc('axes', titlesize=25)

def plot_freq(freq,topn=15,title=None,savefig=None):
    '''plot bar char of the most frequent words/bigrams'''
    
    fig, ax = plt.subplots(figsize=(15,7))
    freq[:topn].sort_values().plot.barh(ax=ax)
    
    ax.set_xlabel("word occurrence count")
    ax.set_title(title)
    fig.tight_layout()
    if savefig is not None:
        fig.savefig(savefig,pad_inches=0)

for grams in ("unigrams","bigrams","trigrams"):
    file = structured_data_dir.joinpath(f"{grams}_freq.tsv")
    freq = pd.read_csv(file,index_col=0,sep="\t").iloc[:,0]

    fig_save_path = figures_dir.joinpath(f"{grams}_cloud.jpg")
    make_word_cloud(freq,savefile=fig_save_path,background_color="black",
                    colormap="Pastel2_r",dpi=200,figsize=(20,20))

    fig_save_path = figures_dir.joinpath(f"{grams}_bar.jpg")

    plot_freq(freq,title=f"most common {grams}",savefig=fig_save_path)