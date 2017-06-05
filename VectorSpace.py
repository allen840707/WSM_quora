# -*- encoding:utf-8 -*-
from pprint import pprint
from Parser import Parser
import util
#import tfidf
import numpy as np
import math
class VectorSpace:
    """ A algebraic model for representing text documents as vectors of identifiers. 
    A document is represented as a vector. Each dimension of the vector corresponds to a 
    separate term. If a term occurs in the document, then the value in the vector is non-zero.
    """

    #Collection of document term vectors
    documentVectors = []

    #Mapping of vector index to keyword
    vectorKeywordIndex=[]

    #Tidies terms
    parser=None

    #new add
    
    docutfidf = []
    freq  = []
    checkfreq = []
    def __init__(self, documents=[]):
        self.documentVectors=[]
        self.parser = Parser()
        if(len(documents)>0):
            self.build(documents)

    def build(self,documents):
        """ Create the vector space for the passed document strings """
        self.vectorKeywordIndex = self.getVectorKeywordIndex(documents)
        self.freq = [0] * len(self.vectorKeywordIndex)
        self.checkfreq = [0] * len(self.vectorKeywordIndex)
        self.documentVectors = [self.makeVector(document) for document in documents]
        self.docutfidf = [self.fortfidf(document) for document in documents]   
        
        #print self.vectorKeywordIndex
        #print self.documentVectors


    def getVectorKeywordIndex(self, documentList):
        """ create the keyword associated to the position of the elements within the document vectors """

        #Mapped documents into a single word string	
        vocabularyString = " ".join(documentList)

        vocabularyList = self.parser.tokenise(vocabularyString)
        #Remove common words which have no search value
        vocabularyList = self.parser.removeStopWords(vocabularyList)
        uniqueVocabularyList = util.removeDuplicates(vocabularyList)
        vectorIndex={}
        offset=0
        #Associate a position with the keywords which maps to the dimension on the vector used to represent this word
        for word in uniqueVocabularyList:
            vectorIndex[word]=offset
            offset+=1
        return vectorIndex  #(keyword:position)


    def makeVector(self, wordString):
        """ @pre: unique(vectorIndex) """

        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex) 
        self.checkfreq = [0] * len(self.vectorKeywordIndex)
        wordList = self.parser.tokenise(wordString)
        wordList = self.parser.removeStopWords(wordList)
        for word in wordList:
            if word in self.vectorKeywordIndex:
                vector[self.vectorKeywordIndex[word]] += 1; #Use simple Term Count Model
                if self.checkfreq[self.vectorKeywordIndex[word]] == 0 :
                    self.freq[self.vectorKeywordIndex[word]] += 1;
                    self.checkfreq[self.vectorKeywordIndex[word]] = 1 ;
       

        return vector


    
    def buildQueryVector(self, termList):
        """ convert query string into a term vector """
        query = self.makeVector(" ".join(termList))
        return query


    def related(self,documentId):
        """ find documents that are related to the document indexed by passed Id within the document Vectors"""
        ratings = [util.cosine(self.documentVectors[documentId], documentVector) for documentVector in self.documentVectors]
        #ratings.sort(reverse=True)
        return ratings


    def search(self,searchList):
        """ search for documents that match based on a list of terms """
        queryVector = self.buildQueryVector(searchList)

        ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
         
        #ratings.sort(reverse=True)
        return ratings
    
    def search_one(self,searchlist,fil):
        
        queryVector = self.buildQueryVector(searchlist)
        #splitlist = searchlist[0].split()
        ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
        result = {k : v for k , v in zip(fil , ratings)} #威德版
        #result = {fil[i] : ratings[i] for i in range(len(fil))} #俊翔版
        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        print("Term Frequency (TF) Weighting + Cosine Similarity")
        print("DocID    Score")
        for word, score in sorted_result[:5]:
            print word[:word.rfind('.product')] ," " ,round(score, 6)
        #tfidf(searchlist, blob, bloblist)
        #return sorted_result

    def search_two(self , searchlist , fil):
        queryVector = self.buildQueryVector(searchlist)
        ratings = [self.jaccard(queryVector, documentVector ) for documentVector in self.documentVectors]
        result = {k : v for k , v in zip(fil , ratings)}
        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        print("Term Frequency (TF) Weighting + Jaccard Similarity")
        print("DocID    Score")
        for word, score in sorted_result[:5]:
            print word[:word.rfind('.product')] ," " , '{:06f}'.format(round(score, 6))
  
    def jaccard(self,x,y):
        x = np.asarray(x, np.bool) # Not necessary, if you keep your data
        y = np.asarray(y, np.bool) # in a boolean array already!
        return  np.double(np.bitwise_and(x, y).sum()) / np.double(np.bitwise_or(x, y).sum()) 

    
    def fortfidf (self,document):
        #vocabularyString = " ".join(document)     
        vocabularyString = document
        document = self.parser.tokenise(vocabularyString)
        #Remove common words which have no search value
        document = self.parser.removeStopWords(document)
        #document = list (util.removeDuplicates(document) )
        return document

    def maketfidf_vector (self ,wordlist ,total ):

        vector = [0] * len(self.vectorKeywordIndex)
        result = [0] * len(self.vectorKeywordIndex)
        r = len(wordlist) 
        wordlist = " ".join(wordlist)
        wordList = self.parser.tokenise(wordlist)
        wordList = self.parser.removeStopWords(wordList)

        for word in wordList:
            if word in self.vectorKeywordIndex:

                vector[self.vectorKeywordIndex[word]] += 1; #Use simple Term Count Model
        
        
        for word in wordList:
            if word in self.vectorKeywordIndex:
        

                result[self.vectorKeywordIndex[word]] =   vector[self.vectorKeywordIndex[word]]  * math.log (  total / (1.0 + self.freq[self.vectorKeywordIndex[word]] ) )  
                result[self.vectorKeywordIndex[word]] =   (result[self.vectorKeywordIndex[word]] / r )



        return result




if  __name__ == '__main__':
    #test data
    documents = ["The cat in the hat disabled",
                 "A cat is a fine pet ponies.",
                 "Dogs and cats make good pets.",
                 "I haven't got a hat."]
    print (documents)
    vectorSpace = VectorSpace(documents)
    #aa  = vectorSpace.getVectorKeywordIndex(cat)
    print (vectorSpace.vectorKeywordIndex)

#    aa = vectorSpace.vectorKeywordIndex['make']
#    print aa
#    bb = vectorSpace.documentVectors
#    print bb 
#    print (vectorSpace.vectorKeywordIndex)
    print (vectorSpace.documentVectors)
    print (  '3' in vectorSpace.vectorKeywordIndex )
    #pprint(vectorSpace.related(1))

    #pprint(vectorSpace.search(["cat is"]))
    
 #   print (vectorSpace.freq)
#    print(vectorSpace.docutfidf)
#    print (vectorSpace.maketfidf_vector (["asd","cat","dog"],1)) 

###################################################
