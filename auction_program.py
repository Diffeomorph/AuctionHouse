
import pandas as pd
import collections
import sys

class AuctionHouse:
    """
    AuctionHouse is a class which holds all the auctions.
    
    auctions: hashmap/dictionary from auction item to instance of the Auction class
    
    get_results_of_all_auctions: a function which loops through all the auctions in the Auction House, gathering output data for each auction
    """
    
    def __init__(self,):
        self.auctions = collections.defaultdict(Auction)
        
    def add_auction(self, auction):
        self.auctions[auction.item] = auction
        
    def get_results_of_all_auctions(self,):
        # loop through all the auctions and record the answer                     
        ans = []
        for auct_item, auct in self.auctions.items():

            res = ''
            res += str(int(auct.close_time)) + ' | ' + auct.item +  ' | '
            
            if auct.bid_count == 0 or auct.highest_bid_user[0] < auct.reserve_price:
                res += 'UNSOLD' + ' | ' + '0.00' + ' | ' + str(auct.bid_count)
            elif auct.bid_count > 1:
                res += str(int(auct.highest_bid_user[1]))  + ' | ' + 'SOLD' + ' | ' + str("{:.2f}".format(auct.second_highest_bid_user[0])) + ' | ' + str(auct.bid_count)
            elif auct.bid_count == 1:
                res += str(int(auct.highest_bid_user[1])) + ' | ' + 'SOLD' + ' | ' + str("{:.2f}".format(auct.reserve_price)) + ' | ' + str(auct.bid_count)
            
            res +=  ' | ' + str("{:.2f}".format(auct.highest_bid_user[0])) + ' | ' + str("{:.2f}".format(auct.lowest_bid))
            ans.append(res)
            
        return ans
        

class Auction:
    """
    This is a class to record how a particular auction unfolds.
    
    timestamp: time when the auction opened
    user_id: id of the user in question
    action: always SELL, as setting up auction for the item
    item: unique string describing the item being auctioned
    reserve_price: lowest price the seller will sell the item
    close_item: end time of the auction
    highest_bid_user: records the price and user_id of the highest bidder
    second_highest_bid_user: records the price and user_id of the second highest bidder
    bid_count: counts number of bids in auction (before or equal to close time)
    lowest_bid: records the lowest bid received (can be less than reserve_price)
    
    update_lowest_bid: function to update the lowest bid
    update_high_bids: function which updates the highest bid and user and the second highest bid and user for a new bid
    """
    
    def __init__(self, timestamp, user_id, action, item, reserve_price, close_time):
        self.timestamp = timestamp 
        self.user_id = user_id
        self.action = action
        self.item = item
        self.reserve_price = reserve_price
        self.close_time = close_time
        self.highest_bid_user = [-1,None]  
        self.second_highest_bid_user = [-1,None]
        self.bid_count = 0
        self.lowest_bid = None
        
    def update_lowest_bid(self, amount):
        if self.lowest_bid == None:
            self.lowest_bid = amount
        else:
            if self.lowest_bid > amount:
                self.lowest_bid = amount
        return
    
    def update_high_bids(self, amount, user_id):
        if amount > self.highest_bid_user[0]:
            tmp = self.highest_bid_user
            self.highest_bid_user = [amount, user_id]
            if tmp[0] > self.second_highest_bid_user[0]:
                self.second_highest_bid_user = tmp
        elif amount > self.second_highest_bid_user[0]:
            self.second_highest_bid_user = [amount, user_id]
        return 
        
        
if __name__ == "__main__":
    # get file name which holds data
    file = str(sys.argv[1])
    
    # read in the required data
    input_file = pd.read_csv(file, header=None, sep = '|')
    input_file.columns = ['timestamp', 'user_id', 'action', 'item', 'amount', 'close_time'] 
    
    auction_house = AuctionHouse()
    
    # iterate through the rows of the dataframe/input file
    for index, row in input_file.iterrows():
        # case: creating a new auction
        if not pd.isnull(row['close_time']):
            new_auction = Auction(row['timestamp'], row['user_id'], row['action'], row['item'], row['amount'], row['close_time'])
            auction_house.add_auction(new_auction)
        
        # case: adding bids to the required auction
        elif pd.isnull(row['close_time']) and not pd.isnull(row['user_id']):
            particular_auction = auction_house.auctions[row['item']]
            
            # if auction has already closed then continue
            if particular_auction.close_time < row['timestamp']: 
                continue
            
            # do updates on various quantities
            particular_auction.bid_count += 1
            particular_auction.update_lowest_bid(row['amount'])
            particular_auction.update_high_bids(row['amount'], row['user_id'])
            
    #print out the answer, line by line
    print(*auction_house.get_results_of_all_auctions(), sep='\n')
    
