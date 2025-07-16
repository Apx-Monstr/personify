from scraper import RedditScraper as RScraper
from generator import Generator
from output import Output
from constants import DEFAULT_BROWSER
class Application:
    def __init__(self):
        self.browser = DEFAULT_BROWSER
        
    def run(self, username):
        print("Starting application...")
        try:
            print("Scraping Data...")
            rscraper = RScraper(browser=self.browser)
            rscraper.start(username=username)
            print("Scraping Successful")
            posts, comments = rscraper.data()
            print("Data retrieved successfully")
            print("Generating Persona...")
            gen = Generator(inputData={
                "posts": posts,
                "comments": comments
            })
            persona = gen.generatePersona()
            print("Persona Generated Successfully")
            print("Saving Persona...")
            file = Output(persona)
            file.logFile()
            file.writeFile()
            print("Persona Saved Successfully")
        except Exception as e:
            print(f"Error occurred: {str(e)}")
        finally:
            print("Prgram Executed Successfully")

def main():
    username = input("Enter Reddit username: ").strip()
    app = Application()
    app.run(username)

if __name__ == "__main__":
    main()