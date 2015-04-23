# racingpost
Scrapy+www.racingpost.com

Install:
. bootstrap.sh

Start spider:
cd racingpost
../env/bin/scrapy crawl racingpost -a date=2015-04-09
../env/bin/scrapy crawl hkjc -a date=20150412 -a racecoursecode=ST
../env/bin/scrapy crawl scmp -a year=2007