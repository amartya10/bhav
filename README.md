# bhav

Daily BSE Market Update API

Data Source: https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx)

## Run 
    docker-compose up
 
## End-Points
### GET
  
 

`api/equity`

    query paramters: 
    optional(limit = 100 & page = 0 ) default,
    
    curl -i -H 'Accept: application/json' http://localhost:8000/api/equity/
     
`api/equity/search/?q={query}`

    query parameter:
        query is BSE Script code or name
        optional(limit = 100 & page = 0 ) default,

    curl -i -H 'Accept: application/json' http://localhost:8000/api/equity/search/?q=tata
    

`api/equity/date/{date}`
    
    path paramter:
        {date} required format 'dd-mm-yyyy'
      
    curl -i -H 'Accept: application/json' http://localhost:8000/api/equity/date/25-06-2021
    
`api/equity/date/{date}/search/?q={query}`
    
    path parameter:
        {date} required format 'dd-mm-YYYY'
      
    query parameter: 
         q in equals BSE code or Symbol
         optional(limit = 100 & page = 0 ) default,
      
    curl -i -H 'Accept: application/json' http://localhost:8000/api/equity/date/25-06-2021/search/?q=tata

### POST

`api/equity/export`,`api/equitu/date/{date}/export`
    
    body:
      list of script code
    
    curl -H 'Content-Type: application/json' -X POST -d '[514358,521200]'  http://localhost:8000/api/equity/export
    curl -H 'Content-Type: application/json' -X POST -d '[514358,521200]'  http://localhost:8000/api/date/{date}/equity/export

  
   

