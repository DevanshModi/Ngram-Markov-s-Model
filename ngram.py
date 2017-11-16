############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import re
import random
import math
import operator
#from decimal import *

############################################################
# Markov Models
############################################################

#TODO: laplace smoothing n other checks
def product(iterable):
    return reduce(operator.mul, iterable, 1)

def tokenize(text):
    return re.findall(r"[\w]+|[^\s\w]", text)

def ngrams(n, tokens):
    if n == 1:
        tokens.append("<END>")
        return [((), x) for x in tokens]
    else:
        for i in range(n-1):
            tokens.insert(0, "<START>")

        tokens.append("<END>")
        nglist = zip(*[tokens[i:] for i in range(n)])
        nglist = [(x[:-1], x[-1]) for x in nglist]

        return nglist

#t = tokenize("a b a b")
#print ngrams(1, t)

class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.count = dict()
        self.countTotal = dict()

    def update(self, sentence):
        tokens = tokenize(sentence)
        data = ngrams(self.n, tokens)

        for val in data:
            #Lower case for each token
            #lowval = tuple(map(lambda x:x.lower(), val[0]))
            if val[0] in self.countTotal:
                self.countTotal[val[0]] += 1
            else:
                self.countTotal[val[0]] = 1

            if (val[0], val[1]) in self.count:
                self.count[(val[0], val[1])] += 1
            else:
                self.count[(val[0], val[1])] = 1

    def prob(self, context, token):
        #lowval = tuple(map(lambda x: x.lower(), context))

        count1 = self.countTotal[context] if context in self.countTotal else 0
        #lowercase conversion
        count2 = self.count[(context, token)] if (context, token) in self.count else 0

        if count1 != 0:
            return float(count2)/float(count1)
        else:
            return 0.0

    #TODO: verify how tokens are added, from context or existing ones
    def random_token(self, context):
        toks = []

        for t in self.count.keys():
            if t[0] == context:
                toks.append(t[1])

        toks = sorted(toks)

        #print toks

        sum = 0

        r = random.random()

        res = ""
        #print r
        for x in toks:
            sum += self.prob(context, x)
            # print r
            # print sum
            # print "\n"
            if r < sum:
                return x
        return res

    def random_text(self, token_count):
        n = self.n
        start = tuple(["<START>" for i in range(n-1)])
        #print start
        if n == 1:
            context = ()
            start = ()
        else:
            context = start

        #Let's eat the main dish

        maindish = []

        count = 0
        while count < token_count:
            #print context
            t = self.random_token(context)
            #print t
            if t == "<END>":
                context = start
                #print "YEHH"
            if n!=1 and t != "<END>":
                #temp = context[-1]
                #print tem
                context = context[1:] + (t,)
                #print context
                #context += (t,) #more appetizers coz they r too good.
            #print t

            #print context
            maindish+=[t]
            count+=1

        #print maindish
        return ' '.join(maindish)

    def perplexity(self, sentence):
        tokens = tokenize(sentence)
        ngdata = ngrams(self.n,tokens)
        #getcontext().prec = 6

        psum = [-1.0*math.log(self.prob(i[0], i[1])) for i in ngdata]
        #m = math.log(self.n)

        psum = float(sum(psum))
        return math.exp(psum/len(ngdata))

# random.seed(1)
# print m.random_text(100)

def create_ngram_model(n, path):
    model = NgramModel(n)

    with open(path) as fileng:
        lines = fileng.readlines()
    lines = [x.strip() for x in lines]

    #print lines

    for l in lines:
        model.update(l)

    return  model
