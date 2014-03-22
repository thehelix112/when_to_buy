#!/usr/bin/python

import sys
import urllib2
import argparse
from bs4 import BeautifulSoup
from bs4 import element


class car:
    def __init__(self):
        self.make = None
        self.model = None
        self.trim = None
        self.colour = None
        self.mileage = None
        self.year = None
        self.price = None

    def __str__(self):
        return "%s %s %s %s - %s %s mi $%s" % (self.year,
                                               self.make, 
                                               self.model, 
                                               self.trim, 
                                               self.colour,
                                               self.mileage,
                                               self.price)
class cars_parser:

    # /// \brief return a list of cars
    def load(self, price_max=85000, price_min=0):

        cars = []

        # this is the hardcoded query for nissan, gtr, yr 2013-2015, $0-85000, order by miles/price
        url = "http://www.cars.com/for-sale/searchresults.action?PMmt=1-1-0&crSrtFlds=stkTypId-feedSegId-mkId-mdId-pseudoPrice-yrId&feedSegId=28705&isDealerGrouping=false&mdId=21204&mkId=20077&prMn=%s&prMx=%s&rd=100000&rpp=50&sf1Dir=ASC&sf1Nm=miles&sf2Dir=DESC&sf2Nm=price&stkTypId=28881&zc=90034&yrId=51683&yrId=47272&searchSource=GN_REFINEMENT" % (price_min, price_max)

        result = urllib2.urlopen(url)
        html_doc = result.read()
        if 'move along, nothing to see here' in html_doc:
            print "The provided query does not exist"
            return None

        soup = BeautifulSoup(html_doc)
        table = soup.find_all('div', {"class": "col20 vehicle-info"})

        for i_vehicle_info in table:
            l_car = car()
            l_car.make = i_vehicle_info.find('span', {'class': 'mmtSort'}).string.split()[0]
            l_car.model = i_vehicle_info.find('span', {'class': 'mmtSort'}).string.split()[1]
            l_car.trim = " ".join(i_vehicle_info.find('span', {'class': 'mmtSort'}).string.split()[2:])
            l_car.year =  i_vehicle_info.find('span', {'class': 'modelYearSort'}).string
            l_car.colour =  i_vehicle_info.find('span', {'class': 'exteriorColorSort'}).contents[0]
            price_and_mileage = i_vehicle_info.findNextSibling('div', {'class': 'col8 align-right'})
            l_car.price = str(price_and_mileage.find('span', {'class': 'priceSort'}).string).translate(None, '$, ')
            l_car.mileage = str(price_and_mileage.find('span', {'class': 'milesSort'}).string).translate(None, ', mi.')
            cars.append(l_car)

        return cars


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dave's When to Buy Tool")
    parser.add_argument('--price-min', type=str, default='0',
            help='The minimum price (default 0)')
    parser.add_argument('--price-max', type=str, default='85000',
            help='The maximum price (default 85000)')
    args = parser.parse_args()

    l_cars_parser = cars_parser()
    cars = l_cars_parser.load(price_min=args.price_min,
                              price_max=args.price_max)
    for car in cars:
        print car

    # DA TODO:
    # get the VIN from queries like this:  http://www.cars.com/go/search/detail.jsp?listingId=125768592&listingRecNum=0
    # where the listing id comes from:
    #    
    # <div class="col8 align-right">
    #   <h4 class="price">
    #     <span class="priceSort">$42,300</span>
    #   </h4>
    #   <div class="mileage">
    #     <span class="milesSort">5 mi.</span>
    #   </div>
    #
    # </div>
    # <div class="clearfix">
    #   <span></span>
    # </div>
    #
    # <div class="listing-options-row">
    #   <div class="col8 js-save-vehicle-wrap row"
    #     id="saved-anchor-601639777">
    #
    #       <label class="float-left"> <input type="checkbox"
    #         class="js-save-vehicle" data-js="save-vehicle"
    #         data-listing-id="601639777"

    # work out how to make a scatter plot of the entries:
    #   y axis: price
    #   x axis: miles travelled
    #   color coded based on year and trim?
    #   NEW full price values as well (pull from gtrlife)

