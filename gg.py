from __future__ import division
import nltk
from nltk.tag import pos_tag
import time
import csv
from numpy.linalg import norm
#from __future__ import divion, unicode_literals
import numpy as np
import math
from pprint import pprint
from Parser import Parser
import util
from VectorSpace import VectorSpace
import os
from nltk.tag import pos_tag

if __name__ == '__main__':
#    User_query = raw_input('Enter Your Query Here :')
#    input_list = User_query.split() 
#    User_query = [a for a in input_list] 
#    open('english.stop', 'r').read().split()
#    doc = []
#   for root, dirs, files in os.walk(yourpath, topdown=False):
#        for a in xrange (len(files)):
#            with open(os.path.join(root, files[a])) as fp: 
#                doc.append(fp.readlines()[0])
    
    sss = time.time()
    csv.field_size_limit(500 * 1024 * 1024)
    count = 0
    q1 = []
    q2 = [] 
    '''f = open('DATA.txt', 'r')
    document = f.read().split()
    
    vec = VectorSpace(document)
    #print document 
    print vec.vectorKeywordIndex
    '''
    xx = open ('TF-IDF_result.txt','w')
                        
                        
    with open('train.csv', 'r') as csvfile:
            
        spamreader = csv.DictReader(csvfile)
        for row in spamreader:
            #print (row['question1'],row['question2'])
            result = []
            if (row['question1'] != None):
                q1.append(row['question1'])
            if (row['question2'] != None):
                q1.append(row['question2'])
            #print q1 
            #print q2
            #vectorSpace = VectorSpace(q1)
            #bloblist = []
            #query_list = []
            #bloblist   = vectorSpace.maketfidf_vector ( q1 ,1 ) 
            #query_list = vectorSpace.maketfidf_vector ( q2 ,1 ) 
            #result = util.cosine (query_list , bloblist )
            #print result 
        vectorSpace = VectorSpace (q1)
        print vectorSpace.vectorKeywordIndex
        

        bloblist = []
        query_list = []
        for row in spamreader :
            Q1 = []
            Q2 = []
            #Q1 = ["What is the step by step guide to invest in share market in india? "] 
            #Q2 = ["What is the step by step guide to invest in share market?"]
            Q1.append(row['question1'])
            Q2.append(row['question2'])
            print Q1
            print Q2 
            bloblist   = vectorSpace.maketfidf_vector ( Q1 ,400000 ) 
            query_list = vectorSpace.maketfidf_vector ( Q2 ,400000 ) 
            result = util.cosine (query_list , bloblist )
            print result 
            xx.write(str(result))
            xx.write('\n')

    xx.close()

