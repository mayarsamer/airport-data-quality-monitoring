
    # Analysis Report

    ## Missing Values Summary
    | Column                   |   MissingPercentage | MissingPercentage_Display   |
|:-------------------------|--------------------:|:----------------------------|
| Airport Code             |                 2   | 2.00%                       |
| Airport GPS Code         |                26   | 🚨 higher than 10% missing   |
| Airport Region Code      |                11.8 | 🚨 higher than 10% missing   |
| Flight Arrival Country   |                 3.5 | 3.50%                       |
| Flight Arrival City      |                30.3 | 🚨 higher than 10% missing   |
| Flight Duration          |                 0   | 0.00%                       |
| Flight Number            |                16   | 🚨 higher than 10% missing   |
| Flight Departure Airport |                 5.9 | 5.90%                       |
| Flight Airline Code      |                 0   | 0.00%                       |
  
    
  
    



    ## Flight Duration Outliers
    | Column          |   OutlierCount |   OutlierPercentage | OutlierPercentage_Display   |
|:----------------|---------------:|--------------------:|:----------------------------|
| Flight Duration |            139 |                13.9 | 🚨 **13.90%**                |

    

    



    ## Flight Duration Outliers (Detailed)
    | Airport Code   | Airport GPS Code   | Airport Region Code   | Flight Arrival Country   | Flight Arrival City   |   Flight Duration | Flight Number   | Flight Departure Airport      | Flight Airline Code   | OutlierReason           |
|:---------------|:-------------------|:----------------------|:-------------------------|:----------------------|------------------:|:----------------|:------------------------------|:----------------------|:------------------------|
| NHT            | EGWU               | GB-ENG                | France                   | Paris                 |                12 | AA7566          | John F. Kennedy International | AA                    | Unusual flight duration |
| NYN            | YNYN               | AU-NSW                | Austria                  | Vienna                |                12 | AC9723          | Toronto Pearson               | AC                    | Unusual flight duration |
| CFT            | KCFT               | US-AZ                 | UK                       | London                |                11 | AA7764          | John F. Kennedy International | AA                    | Unusual flight duration |
| KGG            |                    | SN-TC                 | USA                      | Denver                |                21 |                 | Incheon International         | KE                    | Unusual flight duration |
| BNV            |                    | PG-MPL                | USA                      | Atlanta               |                12 | IB1137          | Adolfo Suárez Madrid–Barajas  | IB                    | Unusual flight duration |

    

    



    ## Exact Duplicate Rows
    | Airport Code   | Airport GPS Code   | Airport Region Code   | Flight Arrival Country   | Flight Arrival City   | Flight Duration   | Flight Number   | Flight Departure Airport   | Flight Airline Code   |
|----------------|--------------------|-----------------------|--------------------------|-----------------------|-------------------|-----------------|----------------------------|-----------------------|

    





       ## Duplicate Flight Numbers
    | Flight Number   |   Count |
|:----------------|--------:|
| AA4031          |       2 |
| AA6628          |       2 |
| AC9149          |       2 |
| AI1813          |       2 |
| AI8375          |       2 |
| AM1251          |       2 |
| AM4416          |       2 |
| AM6125          |       2 |
| AV4168          |       3 |
| AV4922          |       2 |
| BA8735          |       2 |
| CX3624          |       2 |
| CX5062          |       2 |
| DL4434          |       2 |
| EK6800          |       2 |
| IB9630          |       2 |
| KE1298          |       2 |
| KE5277          |       2 |
| KE9760          |       2 |
| KL5197          |       2 |





    