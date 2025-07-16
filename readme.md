# Reddit Persona Generator

This project is a tool that takes a Reddit username, pulls their posts and comments, analyzes them to create a detailed user persona, and saves or displays the result. It’s built to help understand someone’s online personality based on their Reddit activity, using Python and a few handy libraries.

## How It Works

The application follows a straightforward flow:

1. **Takes a Username**: You input a Reddit username when you run the program.
2. **Scrapes Posts and Comments**: It visits the user’s Reddit profile, grabs their posts and comments, and organizes the data.
3. **Generates a Persona**: Using the scraped data, it creates a detailed persona (like age, interests, personality traits) with the help of Google’s Gemini API.
4. **Saves or Logs the Persona**: The persona is either saved to a JSON file or printed to the console for you to see.

The program prints status updates (like “Scraping Data” or “Persona Generated Successfully”) so you know what’s happening at each step.

## Architecture
Below is the architecture diagram showing how the components interact:
![Architecture Diagram]<img width="1186" height="598" alt="Architecture" src="https://github.com/user-attachments/assets/40adf5e2-8160-485b-9fa0-6941b1b90c75" />

## Setup

Here’s how to get this running on your own machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Apx-Monstr/personify.git
   cd personify
   ```

2. **Install Python**:
   Make sure you have Python 3.8 or higher installed. You can check by running:
   ```bash
   python --version
   ```

3. **Install Dependencies**:
   Create a virtual environment (optional but recommended) and install the required libraries from `requirements.txt`:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the project root and add your Gemini API key:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```
   You can get a Gemini API key from [Google’s AI Studio](https://ai.google.dev/).

5. **Install a Web Driver**:
   The scraper uses Selenium to browse Reddit. You’ll need a web driver for your browser (Chrome is recommended):
   - Download the ChromeDriver from [here](https://chromedriver.chromium.org/downloads) matching your Chrome version.
   - Add the ChromeDriver executable to your system’s PATH or place it in the project directory.
   - Alternatively, you can use Firefox or Edge by changing the browser setting in `main.py`.

6. **Run the Application**:
   Run the main script and enter a Reddit username when prompted:
   ```bash
   python main.py
   ```

   The program will scrape data, generate a persona, and save it to a JSON file in the project directory.

## Files and Their Purpose

Here’s a breakdown of each file, what it does, and the key methods inside it.

### `main.py`
This is the entry point of the application. It ties everything together, asks for a username, and runs the scraping, generation, and output processes.

- **Class: `Application`**
  - `__init__()`: Sets up the application, defaults to using Chrome as the browser.
  - `run(username)`: Takes a Reddit username, runs the scraper, generates the persona, and saves/logs the result. Prints status messages along the way.
- **Function: `main()`**
  - Prompts for a username and starts the `Application` class.

### `scraper.py`
This file handles scraping Reddit for user posts and comments using Selenium and BeautifulSoup.

- **Class: `Scraper`**
  - `__init__(browser)`: Sets up the scraper with a browser (Chrome, Firefox, or Edge).
  - `start()`: Initializes the browser driver.
  - `stop()`: Closes the browser driver.
- **Class: `RedditScraper` (inherits from `Scraper`)
  - `__init__(browser)`: Initializes the scraper with empty lists for posts and comments, and a username.
  - `start(username)`: Starts the browser and scrapes posts and comments for the given username.
  - `scrapePosts()`: Pulls the user’s Reddit posts, grabbing titles, descriptions, and links.
  - `scrapeComments()`: Pulls the user’s Reddit comments, including the comment text, subreddit, and related page.
  - `getPosts()`: Returns the scraped posts.
  - `getComments()`: Returns the scraped comments.
  - `data()`: Returns both posts and comments as a tuple.

### `generator.py`
This file analyzes the scraped data and uses the Gemini API to create a detailed user persona.

- **Class: `Generator`**
  - `__init__(inputData)`: Takes a dictionary of posts and comments, sets up the Gemini API.
  - `analyseRawInput()`: Processes the input data, summarizing posts, comments, or other data types.
  - `analyzePosts(posts)`: Analyzes post data, extracting topics, post lengths, and subreddits.
  - `analyzeComments(comments)`: Analyzes comment data, including lengths, subreddits, and engagement frequency.
  - `analyzeGenericData(data)`: Handles any other data types, summarizing their structure.
  - `createPrompt()`: Builds a prompt for the Gemini API based on the analyzed data.
  - `generatePersona()`: Sends the prompt to Gemini and returns a JSON persona.
  - `getPersona()`: Returns the generated persona.
  - `getRawAnalysis()`: Returns the raw data analysis.
  - `getProcessedAnalysis()`: Returns the processed data analysis (currently unused).

### `output.py`
This file handles saving or displaying the generated persona.

- **Class: `Output`**
  - `__init__(output)`: Takes the persona data.
  - `writeFile(filename)`: Saves the persona to a JSON file (uses a random filename if none provided).
  - `logFile()`: Prints the persona to the console in a formatted way.

## Notes
- Make sure your Gemini API key is valid and has sufficient quota.
- The scraper might fail if Reddit’s layout changes or if the username doesn’t exist. Check the console for error messages.
- The persona is saved as a JSON file in the project directory, named after the persona’s generated name plus a random string.

Feel free to tweak the code or add more features! If you run into issues, check the console output for clues or ensure your dependencies are correctly installed.
