# SageBot

A Telegram bot that provides concise, slightly ironic, philosophical responses from a "sage" powered by Llama 3.1 8B model.

## Features

- Responds to any text message with a short, philosophical answer
- Uses Llama 3.1 8B model via OpenRouter
- Designed for deployment on Railway
- Rate limiting to prevent abuse

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/sagebot.git
   cd sagebot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   TELEGRAM_TOKEN=your_telegram_token_here
   OPENROUTER_KEY=your_openrouter_key_here
   RAILWAY_ENV=development
   ```

## Usage

### Local Development

Run the bot locally:
```
./scripts/dev.sh
```

Format code with black and ruff:
```
./scripts/format.sh
```

### Deployment

The bot is configured for deployment on Railway:

1. Push your code to GitHub
2. Connect your GitHub repository to Railway
3. Add the required environment variables in Railway:
   - `TELEGRAM_TOKEN`: Your Telegram bot token
   - `OPENROUTER_KEY`: Your OpenRouter API key
   - `RAILWAY_ENV`: Set to "production"
   - `WEBHOOK_URL`: Your Railway app URL (optional, for webhook mode)

## Running Tests

```
pytest tests/
```

## License

MIT 