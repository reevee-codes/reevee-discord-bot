# Discord Bot

This is old project and its still work in progess, but will be updated.
A Discord bot that provides various utilities including air pollution data and New York Times articles.

## Setup

1. **Prerequisites**
   - Java 17 or higher
   - Maven
   - Discord Bot Token
   - AirVisual API Key
   - New York Times API Key

2. **Configuration**
   Create `application.properties` in `src/main/resources/`:
   ```properties
   airvisual.api.key=your_airvisual_api_key
   nyt.api.key=your_nyt_api_key
   ```

3. **Getting API Keys**
   - **Discord Bot Token**: 
     1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
     2. Create New Application or select existing
     3. Go to "Bot" section
     4. Click "Reset Token" to get your bot token
   
   - **AirVisual API Key**: Sign up at [AirVisual](https://www.iqair.com/air-pollution-data-api)
   - **NYT API Key**: Sign up at [NYT Developer Portal](https://developer.nytimes.com/)

## Running the Bot

### Command Line

Run with token
`java -jar bot.jar -t YOUR_DISCORD_TOKEN`
Or use long format
`java -jar bot.jar --token YOUR_DISCORD_TOKEN`
Show help menu
`java -jar bot.jar -h`


### IDE Setup
1. Open project in your IDE
2. Edit Run Configuration
3. Add Program Arguments: `-t YOUR_DISCORD_TOKEN`

## Available Commands

- `!air` - Get air pollution data for nearest city
- `!world <number>` - Get most popular NYT articles (specify number of articles to display)

## Building from Source
 bash
 mvn clean package


The compiled jar will be in the `target` directory.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security Notes

- Never commit your API keys or tokens
- Add `application.properties` to `.gitignore`
- If you suspect your token has been compromised, reset it immediately

- ---------------------------------
<h3>BACKLOG:</h3>
- 1. Fix "!air" and do air quality response formatting: <br>
  "The tempearture in [city] is [current].[weather].[tp] c, and air humidity is  [current].[weather].[hu] %, with [current].[weather].[ws] m/s of wind"<br>
- + adding image to response to 1:  load an image based on [current].[weather].[ic] <br>
- 2. show current day and polish namedays<br>
- 3. hosting <br>
- 4. create in memory todolist for all users<br>
- 5. add to in memory todolist<br>
- 6. add icon from user<br>
- 7. remind about duolingo at 22 CET<br>
- -----------------------------------------------------------
