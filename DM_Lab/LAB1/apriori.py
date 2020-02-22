
from collections import defaultdict
import csv
from optparse import OptionParser    # parse command-line parameters

class Apriori(object):
    def __init__(self, minSupp, minConf):
        """ Parameters setting
        """
        self.minSupp = minSupp  # min support (used for mining frequent sets)
        self.minConf = minConf  # min confidence (used for mining association rules)

    def fit(self, filePath):
        """ Run the apriori algorithm, return the frequent *-term sets. 
        """
        # Initialize some variables to hold the tmp result
        transListSet  = self.getTransListSet(filePath)   # get transactions (list that contain sets)
        itemSet       = self.getOneItemSet(transListSet) # get 1-item set
        itemCountDict = defaultdict(int)         # key=candiate k-item(k=1/2/...), value=count
        freqSet       = dict()                   # a dict store all frequent *-items set
        
        self.transLength = len(transListSet)     # number of transactions
        self.itemSet     = itemSet
        
        # Get the frequent 1-term set
        freqOneTermSet = self.getItemsWithMinSupp(transListSet, itemSet, 
                                             itemCountDict, self.minSupp)

        # Main loop
        k = 1
        currFreqTermSet = freqOneTermSet
        while currFreqTermSet != set():
            freqSet[k] = currFreqTermSet  
            k += 1
            currCandiItemSet = self.getJoinedItemSet(currFreqTermSet, k) 
            currFreqTermSet  = self.getItemsWithMinSupp(transListSet, currCandiItemSet, 
                                                   itemCountDict, self.minSupp) 
            
            
        #
        self.itemCountDict = itemCountDict 
        self.freqSet       = freqSet       
        return itemCountDict, freqSet
            
            
    def getSpecRules(self, rhs):
        """ Specify a right item, construct rules for it
        """
        if rhs not in self.itemSet:
            print('Please input a term contain in the term-set !')
            return None
        
        rules = dict()
        for key, value in self.freqSet.items():
            for item in value:
                if rhs.issubset(item) and len(item) > 1:
                    item_supp = self.getSupport(item)
                    item = item.difference(rhs)
                    conf = item_supp / self.getSupport(item)
                    if conf >= self.minConf:
                        rules[item] = conf
        return rules
        
    
    def getSupport(self, item):
        """ Get the support of item """
        return self.itemCountDict[item] / self.transLength
        
        
    def getJoinedItemSet(self, termSet, k):
        """ Generate new k-terms candiate itemset"""
        return set([term1.union(term2) for term1 in termSet for term2 in termSet 
                    if len(term1.union(term2))==k])
    
        
    def getOneItemSet(self, transListSet):
        """ Get unique 1-item set in `set` format 
        """
        itemSet = set()
        for line in transListSet:
            for item in line:
                itemSet.add(frozenset([item]))
        return itemSet
        
    
    def getTransListSet(self, filePath):
        """ Get transactions in list format 
        """
        transListSet = []
        with open(filePath, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for line in reader:
                transListSet.append(set(line))
        for i in transListSet:
            i.discard('')                
        return transListSet
                
    
    def getItemsWithMinSupp(self, transListSet, itemSet, freqSet, minSupp):
        """ Get frequent item set using min support
        """
        itemSet_  = set()
        localSet_ = defaultdict(int)
        for item in itemSet:
            freqSet[item]   += sum([1 for trans in transListSet if item.issubset(trans)])
            localSet_[item] += sum([1 for trans in transListSet if item.issubset(trans)])
        
        # Only conserve frequent item-set 
        n = len(transListSet)
        for item, cnt in localSet_.items():
            itemSet_.add(item) if float(cnt)/n >= minSupp else None
        
        return itemSet_


if __name__ == '__main__':
    
    # Parsing command-line parameters
    optParser = OptionParser()
    optParser.add_option('-f', '--file', 
                         dest='filePath',
                         help='Input a csv file',
                         type='string',
                         default=None)  # input a csv file
                         
    optParser.add_option('-s', '--minSupp', 
                         dest='minSupp',
                         help='Mininum support',
                         type='float',
                         default=0.20)  # mininum support value
                         
    optParser.add_option('-c', '--minConf', dest='minConf',
                         help='Mininum confidence',
                         type='float',
                         default=0.60)  # mininum confidence value    
                         
    optParser.add_option('-r', '--rhs', dest='rhs',
                         help='Right destination',
                         type='string',
                         default=None)  # 

    (options, args) = optParser.parse_args()       
        
    # Get two important parameters
    filePath = options.filePath
    minSupp  = options.minSupp
    minConf  = options.minConf
    rhs      = frozenset([options.rhs])
    print("""Parameters: \n - filePath: {} \n - mininum support: {} \n - mininum confidence: {} \n - rhs: {}\n""".\
          format(filePath,minSupp,minConf, rhs))

    # Run and print
    objApriori = Apriori(minSupp, minConf)
    itemCountDict, freqSet = objApriori.fit(filePath)
    for key, value in freqSet.items():
        print('frequent {}-term set:'.format(key))
        print('-'*20)
        for itemset in value:
            print(list(itemset))
        print()

    # Return rules with regard of `rhs`
    rules = objApriori.getSpecRules(rhs)
    print('-'*20)
    print('rules refer to {}'.format(list(rhs)))
    for key, value in rules.items():
        print('{} -> {}: {}'.format(list(key), list(rhs), value))
