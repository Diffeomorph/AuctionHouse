
import unittest
import auction_program as ap

class TestAuctionProgram(unittest.TestCase):
    """
    A class to test auction_program.py
    """
    
    def test_auction_creation(self):
        test_auction = ap.Auction(10, 1.0, 'SELL', 'toaster_1', 10.0, 20.0)
        
        self.assertEqual(test_auction.timestamp, 10)
        self.assertEqual(test_auction.user_id, 1.0)
        self.assertEqual(test_auction.action, 'SELL')
        self.assertEqual(test_auction.item, 'toaster_1')
        self.assertEqual(test_auction.reserve_price, 10.0)
        self.assertEqual(test_auction.close_time, 20.0)
        
    def test_update_lowest_bid(self):
        test_auction = ap.Auction(10, 1.0, 'SELL', 'toaster_1', 10.0, 20.0)
        test_auction.lowest_bid = 25
        test_auction.update_lowest_bid(15)
    
        self.assertEqual(test_auction.lowest_bid, 15)
    
    def test_update_high_bids(self):
        test_auction = ap.Auction(10, 1.0, 'SELL', 'toaster_1', 10.0, 20.0)
        test_auction.highest_bid_user = [50,6]
        test_auction.second_highest_bid_user = [40,5]
        
        #higher than highest
        test_auction.update_high_bids(60,7)
        self.assertEqual(test_auction.highest_bid_user, [60,7])
        
        #higher than second, lowest than highest
        test_auction.update_high_bids(55,8)
        self.assertEqual(test_auction.highest_bid_user, [60,7])
        self.assertEqual(test_auction.second_highest_bid_user, [55,8])
        
     
    def test_auction_house_creation(self):
        ath = ap.AuctionHouse()
        test_auction1 = ap.Auction(10, 1.0, 'SELL', 'toaster_1', 10.0, 20.0)
        test_auction2 = ap.Auction(15, 8.0, 'SELL', 'tv_1', 250.00, 20)
        ath.add_auction(test_auction1)
        ath.add_auction(test_auction2)
        
        self.assertEqual(ath.auctions[test_auction1.item],test_auction1)
        self.assertEqual(ath.auctions[test_auction2.item],test_auction2)
        
    def test_get_auction_house_results(self):
        ath = ap.AuctionHouse()
        ath.auctions['toaster_1'] = ap.Auction(10, 1.0, 'SELL', 'toaster_1', 10.0, 20.0)
        ath.auctions['toaster_1'].highest_bid_user = [20.0, 8.0]
        ath.auctions['toaster_1'].second_highest_bid_user = [12.5, 5.0]
        ath.auctions['toaster_1'].bid_count = 3
        ath.auctions['toaster_1'].lowest_bid = 7.5
        
        ath.auctions['tv_1'] = ap.Auction(15, 8.0, 'SELL', 'tv_1', 250.0, 20.0)
        ath.auctions['tv_1'].highest_bid_user = [200.0, 3.0]
        ath.auctions['tv_1'].second_highest_bid_user = [150.0, 1.0]
        ath.auctions['tv_1'].bid_count = 2
        ath.auctions['tv_1'].lowest_bid = 150.0
        
        ans = ['20 | toaster_1 | 8 | SOLD | 12.50 | 3 | 20.00 | 7.50',
 '20 | tv_1 | UNSOLD | 0.00 | 2 | 200.00 | 150.00']
        
        self.assertEqual(ath.get_results_of_all_auctions(),ans)
                
    
if __name__ == '__main__':
    unittest.main()