from botobot_api.models import Message

def test_menu_resource(client):   
    url = '/'

    # Bad request - incorrect method.
    response = client.get(url)
    assert response.status_code == 405

    # Bad request - no data provided.
    response = client.post(url)
    assert response.status_code == 400

    # Check the service.
    response = client.post(url, data={'client':'telegram', 'version':'1.0', 'chat_id':'pytest_test'})
    assert response.status_code == 200

    # Two messages expected: 'general.hello' and the api list.
    messages = response.json["messages"]
    assert len(messages) == 2
    assert messages[0] == Message.get('general.hello').fulltext

def test_statictext_resource(client):
    url = "/statictext/about"

    # Bad request - incorrect method.
    response = client.get(url)
    assert response.status_code == 405

    # Check the service.
    response = client.post(url, data={'client':'telegram', 'version':'1.0', 'chat_id':'pytest_test'})
    assert response.status_code == 200

    # StaticText always returns one message.
    assert len(response.json["messages"]) == 1

def test_weather_resource(client, requests_mock):
    url = "/weather"

    # Bad request - incorrect method.
    response = client.get(url)
    assert response.status_code == 405

    # Mock the call to third part API.
    mock_result = { "dataseries" : [ { "date" : 20220219, "temp2m" : { "max" : 29, "min" : 15 } }, { "date" : 20220219, "temp2m" : { "max" : 29, "min" : 15  } } ] }
    requests_mock.get('https://www.7timer.info/bin/api.pl', json=mock_result)
    
    response = client.post(url, data={'client':'telegram', 'version':'1.0', 'chat_id':'pytest_test'})
    assert response.status_code == 200

    # It should receive 3 messages.
    assert len(response.json["messages"]) == 3

def test_stocks_resource(client, mocker):
    url = "/stocks"

    # Bad request - incorrect method.
    response = client.get(url)
    assert response.status_code == 405

    response = client.post(url, data={'client':'telegram', 'version':'1.0', 'chat_id':'pytest_test'})
    assert response.status_code == 200

    # Message asking for the ticker.
    assert len(response.json["messages"]) == 1

    # Mocks the call to yfinance module.   
    return_object = lambda: None
    return_object.info = {'info':{'longName':'Coca-cola', 'sector':'Food', 'country':'US', 'currentPrice':1.99, 'currency':'USD'}}
    mocker.patch('yfinance.Ticker', return_value=return_object)
    response = client.post(url, data={'client':'telegram', 'version':'1.0', 'chat_id':'pytest_test', 'message':'KO'})
    assert response.status_code == 200

    # Ticker information.
    assert len(response.json["messages"]) == 2
