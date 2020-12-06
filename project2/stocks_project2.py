import json
quotes =  {
  "AAPL": {
    "name": "Apple", 
    "quotes": {
      "20201031-083000": [ "110.5", "111.17", "110.64", "110.64", "5684400"], 
      "20201031-083500": [ "111.5", "111.17", "111.64", "111.64", "1473400"], 
      "20201031-084000": [ "112.5", "112.17", "112.64", "112.64", "2987600"]
    }
  }, 
  "AMZN": {
    "name": "Amazon", "quotes": {}
  }
}

def get_tickers(event, context):
    empty_dic = {}
    for key in quotes.keys():
        print (key + ": "+  quotes[key]['name'])
        empty_dic [key]= quotes[key]['name']

    return empty_dic  

def get_ticker(event, context):
    ticker = event['pathParameters']["ticker"]
    empty_dic = {}
    empty_dic[tickr] = quotes[tickr]['name']

    return empty_dic  

def create_ticker(event, context):

    ticker = event['pathParameters']["ticker"]
    name = event['pathParameters']["name"]
    this_dic = {
        ticker: {'name': name, 'quotes': {}}
    }
    quotes.update(this_dic)   

def delete_ticker(event, context):
        del quotes[tickr]
        print(tickr)

def get_quotes(event, context):
    ticker = event['pathParameters']["ticker"]
    empty_dic = {}
    empty_dic[tickr] = quotes[tickr]['quotes']
    return empty_dic
        
def get_quote(event, context):
    tickr = event['pathParameters']["ticker"]
    datetime = event['pathParameters']["datetime"]
    quote1 = (quotes[tickr]['quotes'][datetime])
    quote1 = ' '.join([str(elem) for elem in quote1]) 
    print(quote1 + "\n")
    return quote1

def add_quote(event, context):
    datetime = date1+"-"+time1
    this_dict = {
        datetime: [ open1, high1, low1, close1, vol1]
    }
    for key, value in this_dict.items():
        print(key, value)
    
    quotes[name]["quotes"].update(this_dict)
    
def avg(event, context):
    empty_list = []
    store_avg = 0.0
    tickr = event['pathParameters']["ticker"]
    datetime = event['pathParameters']["ticker"]
    period = int(event['[pathParameters']["period"])
 
    for quote, value in quotes[tickr]['quotes'].items():
        empty_list.append(value[3])
        if quote == datetime:
            break

    for i in empty_list:
        if len(empty_list) <= 20:
            break
        del empty_list[0]
    
    for i in empty_list:
        print(i)
        store_avg = store_avg + float(i)
        
    store_avg = store_avg/len(empty_list)

    print ("store_avg",store_avg)
    print (empty_list)
    return  store_avg

def atr(event, context):
    empty_list = []
    store_avg = 0.0
    tickr = event['pathParameters']["ticker"]
    datatime = event['pathParameters']["datetime"]
    period = int(event['pathParameters']["period"])
 
    for quote, value in quotes[tickr]['quotes'].items():
        result = float(value[1])- float(value[2])
        empty_list.append(result)
        if quote == datetime:
            break

    for i in empty_list:
        if len(empty_list) <= 20:
            break
        del empty_list[0]
    
    for i in empty_list:
        print(i)
        store_avg = store_avg + float(i)
        
    store_avg = store_avg/len(empty_list)

    print ("store_avg",store_avg)
    print (empty_list)   

    return  store_avg


def uploader(event, context):
    name_file = event['pathParameters']["name_file"]
    print(name_file)
    f = open(file, "r")
    f.readline()
    input_data = f.readlines() 

    for i in input_data:
        if i.rstrip():
            j = i.split(",")
            name = j[0].split(".")
            name = name[0]
            date_time = j[2] + "-" +j[3]
            open1 = j[4]
            high = j[5]
            low = j[6]
            close1 = j[7]
            vol = j[8]


# Debug interface: return internal data structures
# ---
@app.route('/debug/dump')
def dump():
    return jsonify(quotes)   















