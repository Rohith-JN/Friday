# Friday
> A simple Personal-Assistant made to automate Windows and other simple tasks

## Features

2. Answer different type of questions
3. Send messages to groups and personal chat in telegram # Telegram credentials required
4. Get stock prices # YahoofinanceApi required
5. Access native windows controls like brightness, volume, shutdown, sleep and restart

# Technologies Used

1. Python
2. Telegram API
4. Yahoo finance API
5. Wolframalpha API

## Meta

1. Twitter – [@RohithNambiar4](https://twitter.com/dbader_org)<br>
2. Stackoverflow - [Rohith Nambiar](https://stackoverflow.com/users/15747757/rohith-nambiar)
3. Check out my other repositories - [Other projects](https://github.com/Rohith-JN)

## Contributing

1. Fork it (<https://github.com/Rohith-JN/Personal-assistant/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
6. Add new intents in the intents.json

<!-- Markdown link & img dfn's -->
[Stackoverflow]: https://stackoverflow.com/users/15747757/rohith-nambiar

## Trying out the project

1. To open apps using Friday you need to first create a file called paths.py and then add the app's name and their paths 

```
studio = ("android-studio", "android studio", "Android studio")

paths = {
    studio: r"C:\Program Files\Android\Android Studio\bin\studio64.exe",
}
```

2. Make a file called API_keys.py then add these credentials

```
api_id = xxxx # telegram api key
api_hash = xxxx # telegram api hash
token = xxxx # telegram token
phone = xxxx # telegram phone number

#API keys
yfinance_api_key = xxxx
wolframalphaApIKey = xxxx
OpenWeather_API_Key = xxxx
```
