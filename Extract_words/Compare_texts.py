import matplotlib.pyplot as plt
import numpy as np



plt.rc('xtick', labelsize=9) 
plt.rc('ytick', labelsize=9) 

def get_stopwords():
    file = 'stopwords.txt'
    f = open(file, encoding='utf-8')
    lines = f.readlines()
    sw = {}
    for l in lines:
        l = l.strip(' \n\r').lower()
        sw[l] = True
    return sw

def get_wordcount(sw, filename):
    f = open(filename, encoding='utf-8')
    wc = {}
    while True:
        line = f.readline()
        if not line: # or line_count > 10:
            break
        words = line.split()
        for w in words:            
            w = w.strip("!.,\"(){} _–: ").lower()

            if w in sw:
                continue

            if not w in wc:
                wc[w] = 0

            wc[w] = wc[w] + 1
    return wc


def store_results(wc, out_filename):
    fo = open(out_filename, "w", encoding="utf-8")
    for w, c in sorted(wc.items(), key=lambda item: item[1], reverse=True):
        fo.write(f'{w},{c}\n')





def read_file(csvfilename):
    f = open(csvfilename, encoding ='utf-8')
    top_lines = f.readlines()
    top_pairs = []
    
    for l in top_lines:
        toks = l.split(',')
        try:
            int(float(toks[1]))
            top_pairs.append((toks[0], int(float(toks[1]))))
        except:
            pass
    return top_pairs




def make_plot_single(top_pairs, outfilename, title, number_of_words) :
    n = number_of_words
    labels = [(x[0]) for x in top_pairs[:n]]
    counts = [int(x[1]) for x in top_pairs[:n]]
    lable_position = np.arange(len(labels))
    
    plt.barh(lable_position, counts, align='center', alpha=0.5)
    plt.yticks(lable_position, labels)
    plt.xlabel('count')
    plt.title(title)
    plt.savefig(outfilename)
    plt.close()



def get_sum(nums):
    sum = 0
    for n in nums:
        sum += n
    return sum


def normalize(top_pairs):
    sum = get_sum([tp[1] for tp in top_pairs])
    return [(tp[0],(tp[1]/sum)*100) for tp in top_pairs]

def make_dict(top_pairs):
    dict = {}
    for w,p in top_pairs:
        dict[w] = p
    return dict




def compare_plots(top_pairs1, top_pairs2, title, outfilename, number_of_words):
    n = number_of_words
    norm_top1 = normalize(top_pairs1)
    norm_top2 = normalize(top_pairs2)
    dic_top2 = make_dict(norm_top2)
    x = []
    y = []
    stats = []
    for w, p1 in norm_top1[:n]:
        p2 = 0
        if w in dic_top2:
            p2 = dic_top2[w]

        stats.append(w)
        x.append(p2)
        y.append(p1)

    width = 0.20
    lable_position = np.arange(len(stats))
    plt.bar(lable_position, y, width=width)
    plt.bar(lable_position + width, x, width=width)
    plt.xticks(lable_position, labels=stats)
    plt.xlabel("count")
    plt.ylabel("word percentage rate")
    plt.title(title)
    plt.savefig(outfilename)
    plt.show()
    
def ultimate_chart(top_pairs1, top_pairs2, title, outfilename, number_of_words):
    n = number_of_words
    norm_top1 = normalize(top_pairs1)
    norm_top2 = normalize(top_pairs2)
    dic_top2 = make_dict(norm_top2)
    dicc_top2 = make_dict(top_pairs2)
    x = []
    y = []
    stats = []
    for w, p1 in norm_top1[:n]:
        p2 = 0
        if w in dic_top2:
            p2 = dic_top2[w]

        stats.append(w)
        x.append(p2)
        y.append(p1)   

    xx = []
    yy = []
    for ww , pp1 in top_pairs1[:n]:
        pp2 = 0
        if ww in dicc_top2:
            pp2 = dicc_top2[ww]
        xx.append(pp2)   
        yy.append(pp1)    

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.suptitle(title)
    ax1.plot(stats, xx)
    ax2.plot(stats, yy,)
    ax3.plot(stats, x,)
    ax4.plot(stats, y,)

    for ax in fig.get_axes():
        ax.label_outer()
    plt.savefig(outfilename)


def Create_Stats(filename):
    
    sw = get_stopwords()
    words = get_wordcount(sw, f"{filename}.txt")
    store_results(words, f"{filename}_result.csv")
    return read_file(f"{filename}_result.csv")





trump_stats = Create_Stats("trump")
make_plot_single(trump_stats, "trump.jpg", "trump words", 30)

clinto_stats = Create_Stats("clinton")
make_plot_single(clinto_stats, "clinton.jpg", "clinton words", 30)


compare_plots(trump_stats, clinto_stats, "trump against clinton", "trump_clinton.jpg",20)
compare_plots(clinto_stats, trump_stats, "clinton against trump", "clinton_trump.jpg",20)

ultimate_chart(trump_stats, clinto_stats, " ", "extra_chart.jpg", 16)
