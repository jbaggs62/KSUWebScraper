# importing the module
import json
from statistics import mean
import collections
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import matplotlib.pyplot as plt





def Avglst(lst):
    # returns the average value if not None
    newlst = []
    for x in lst:
        if x != None:
            newlst.append(x)

    #print("newlst len ",len(newlst))
    if len(newlst)>0:
        return mean(newlst)

file = open("email.json", 'r')
json_data = json.load(file)
#print(json_data)
print(type(json_data))

z=0
lst_body = []
lst_emails = []

for i in json_data:
    lst_body.append(i["body"])
    lst_emails.append(i["emails"])

lgth = []

for i in lst_body:
    body_t = i.split()
    lgth.append(len(body_t))

print(Avglst(lgth))

## frequency of webpages with email
emailcnt=0
webpagecnt=0
for i in lst_emails:
    webpagecnt +=1
    if len(i) > 0:
        emailcnt +=1
#print(emailcnt)
#print(webpagecnt)
print("Proportion of web pages with email: ",emailcnt / webpagecnt*100)



flat_ls = []
for i in lst_emails:
    for j in i:
        flat_ls.append(j)
print(flat_ls)

def most_freq_lst(List, N):
    number = collections.Counter(List)
    return number.most_common(N)

print(most_freq_lst(flat_ls,10))

###split words into list
all_words = []
for i in lst_body:
    body_t = i.split()
    for i in body_t:
        all_words.append(i)   

def most_freq_words(List, N):
    number = collections.Counter(List)
    return number.most_common(N)

most_freq_LIST = most_freq_words(all_words,30)



### remove stop words
nltk.download('stopwords')
from nltk.corpus import stopwords

df_before = pd.DataFrame (most_freq_LIST, columns = ['Words', 'Freq'])

df_before['Perc'] = df_before.apply(lambda row: row.Freq/(len(all_words)) , axis = 1)
print("dataframe before removing stop words")
print(df_before)


stop_words = set(stopwords.words('english'))



def remove_stop_words(List):
    nostop = []
    for i in List:
        if i not in stop_words:
            if i not in string.punctuation:
                nostop.append(i)
    return nostop

noStopWords = remove_stop_words(all_words)
noStopWordsFreq = most_freq_words(noStopWords,30)
df_after = pd.DataFrame (noStopWordsFreq, columns = ['Words', 'Freq'])
print("dataframe after stopwords and punc removed")
df_after['Perc'] = df_after.apply(lambda row: row.Freq/(len(noStopWords)) , axis = 1)
print(df_after)


# graphs
print("This is number of unique words in all words:", len(set(all_words)))
all30cnt = most_freq_lst(all_words,len(set(all_words)))

listx=[]
listy=[]
z=0
for i in all30cnt:
    z += 1
    listx.append(z)
    listy.append(i[1])
    #if z<10:
        #print("this is z ",z," this is i ",i," this is y ",i[1])
plt.plot(listx,listy)
plt.xlabel('Rank')
plt.ylabel('Frequency')
plt.title('Word Distribution')
plt.show()

plt.loglog(listx,listy)
plt.xlabel('log(Rank)')
plt.ylabel('log(Frequency)')
plt.title('Word Distribution Log-Log Plot')
plt.show()