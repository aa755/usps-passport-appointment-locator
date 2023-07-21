# usps-passport-appointment-locator

quick start: 
- get the poetry environment going, using `poetry install` and `poetry shell`
- example usage
```
(passport-appointment-locator-py3.9) ➜  passport-appointment-locator git:(main) ✗ python  passport_appt.py --zip-code 94086 --polling-interval 100 --max-date 20230820 
checking in 5 locations near zip code 94086 upto date: 20230820
found date 20230817 at ('209 E JAVA DR', 'SUNNYVALE')
found date 20230818 at ('209 E JAVA DR', 'SUNNYVALE')
found date 20230817 at ('211 HOPE ST', 'MOUNTAIN VIEW')
found date 20230818 at ('211 HOPE ST', 'MOUNTAIN VIEW')
found date 20230817 at ('1525 MIRAMONTE AVE', 'LOS ALTOS')
found date 20230818 at ('1525 MIRAMONTE AVE', 'LOS ALTOS')
found date 20230818 at ('1050 KIELY BLVD', 'SANTA CLARA')
found date 20230817 at ('21701 STEVENS CREEK BLVD', 'CUPERTINO')
found date 20230818 at ('21701 STEVENS CREEK BLVD', 'CUPERTINO')
will check again in 100s

```
