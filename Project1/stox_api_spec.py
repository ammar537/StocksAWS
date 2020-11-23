import flask
from flask import abort, jsonify, request

app = flask.Flask(__name__)

# Suggested internal data structure (example)

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

# quotes = {
#     'AAPL': {'name': 'Apple', 'quotes': {}}, 
#     'GOOG': {'name': 'Alphabet', 'quotes':{}},
#     'AMZN': {'name': 'Amazon', 'quotes': {}},
#     'NFLX': {'name': 'Netflix', 'quotes': {}},
#     'MSFT': {'name': 'Microsoft', 'quotes': {}}
# }
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


# Return a list of all tickers and their name. E.g.:
# {
#     'AAPL': 'Apple', 
#     'GOOG': 'Alphabet',
# }
@app.route('/tickers', methods=['GET'])
def get_tickers():
    empty_dic = {}
    for key in quotes.keys():
        print (key + ": "+  quotes[key]['name'])
        empty_dic [key]= quotes[key]['name']

    return empty_dic  

# Return a ticker and it name. E.g.:
# {
#     'AAPL': 'Apple', 
# }  
@app.route('/ticker/<tickr>', methods=['GET'])
def get_ticker(tickr):
    empty_dic = {}
    empty_dic[tickr] = quotes[tickr]['name']
    return empty_dic  

# Create a new ticker. E.g.:
# curl -i -X POST -d http://localhost:5000/ticker "ticker=CSCO&name=Cisco"
# ---
@app.route('/ticker', methods=['PUT','POST'])
def create_ticker():
    data = request.get_data().decode("utf8")
    res = data.split('&')
    res1 = res[0].split('=')
    name = res[1].split('=')
    name = name[1]
    print('name', name)
    ticker = res1[1]
    print("ticker", ticker)
    this_dic = {
        ticker: {'name': name, 'quotes': {}}
    }
    quotes.update(this_dic)
    # qoutes update this_dic
    return request.url   

# Delete a ticker, along with all quote information. E.g.:
# curl -i  -X DELETE http://localhost:5000/ticker/MSFT
# ---
@app.route('/ticker/<tickr>', methods=['DELETE'])
def delete_ticker(tickr):
    if request.url in "http://localhost:5000/ticker":
        del quotes[tickr]
        print(tickr)
        return request.url   

# Get all quotes for a ticker. E.g.:
# {
#    "20201031-083000": [ "110.5", "111.17","110.64", "110.64", "5684400"], 
#    "20201031-083500": [ "111.5", "112.17", "111.64", "111.64", "5684400"], 
#    "20201031-084000": [ "112.5", "112.17", "112.64", "112.64", "5684400"]
# }
@app.route('/quotes/<tickr>',methods=['GET'])
def get_quotes(tickr):
    empty_dic = {}
    empty_dic[tickr] = quotes[tickr]['quotes']
    return empty_dic
        
# Return a specific quote per ticker/datetime
# curl http://localhost:5000/quote/AAPL/20201031-083000
# ---
@app.route('/quote/<tickr>/<datetime>')
def get_quote(tickr,datetime):
    quote1 = (quotes[tickr]['quotes'][datetime])
    quote1 = ' '.join([str(elem) for elem in quote1]) 
    print(quote1 + "\n")
    return quote1+ "\n"

# Create a new quote
# curl -i -X POST http://localhost:5000/quote \ 
#      -d "ticker=AAPL&date=20201031&time=084000&open=110.5&high=111.17&low=110.64&close=110.64&vol=5684400" \
#       
# ---
@app.route('/quote',methods=['POST'])
def add_quote():
    data = request.get_data().decode("utf8")
    res = data.split('&')
    res1 = res[0].split('=')
    name = res[0].split('=')
    name = name[1]
    res2 = res[1].split('=')
    date1 = res[1].split('=')
    date1 = date1[1]
    res3 = res[2].split('=')
    time1 = res[2].split('=')
    time1 = time1[1]
    res4 = res[3].split('=')
    open1 = res[3].split('=')
    open1 = open1[1]
    res5 = res[4].split('=')
    high1 = res[4].split('=')
    high1 = high1[1]
    res6 = res[5].split('=')
    low1 = res[5].split('=')
    low1 = low1[1]
    res7 = res[6].split('=')
    close1 = res[6].split('=')
    close1 = close1[1]
    res8 = res[7].split('=')
    vol1 = res[7].split('=')
    vol1 = vol1[1]
    print (name, date1, time1, open1, high1, low1, close1, vol1)
    datetime = date1+"-"+time1
    print(datetime)
    this_dict = {
        datetime: [ open1, high1, low1, close1, vol1]
    }
    for key, value in this_dict.items():
        print(key, value)
    
    quotes[name]["quotes"].update(this_dict)
    
    return request.url
    
# --- average computation ---
# curl -i http://localhost:5000/stat/avg/AAPL/20201031-083000/20
# ---
@app.route('/stat/avg/<tickr>/<datetime>/<int:period>')
def avg(tickr, datetime, period):
    empty_list = []
    store_avg = 0.0

    print(quotes[tickr]['quotes'][datetime][3]) 
    for quote, value in quotes[tickr]['quotes'].items():
        # print(quote, value[3])
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
    return request.url   


# --- average computation ---
# curl -i http://localhost:5000/stat/atr/AAPL/20201031-083000/20
# ---
@app.route('/stat/atr/<tickr>/<datetime>/<int:period>')
def atr(tickr, datetime, period):
    empty_list = []
    store_avg = 0.0

    print(quotes[tickr]['quotes'][datetime][1]) 
    for quote, value in quotes[tickr]['quotes'].items():
       #print(quote, value[1], value[2])
        # print(quote, value[3])
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
    return request.url   

# curl http://localhost:5000/uploader/amzn.us.txt
# ---
@app.route('/uploader/<file>')
def uploader(file):
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

            if name not in quotes:
                this_dict =  {
                    name: {'name': name, 'quotes':{
                            date_time: [ open1, high, low, close1, vol]}
                            }
                        }
                quotes.update(this_dict)
            else:
                this_dict = {
                    date_time: [ open1, high, low, close1, vol]
                  }
                quotes[name]['quotes'].update(this_dict)


            # print(name, date_time, open1, high, low, close1, vol)
    return request.url

# Debug interface: return internal data structures
# ---
@app.route('/debug/dump')
def dump():
    return jsonify(quotes)   















