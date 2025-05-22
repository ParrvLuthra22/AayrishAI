import platform
import subprocess
import webbrowser
import asyncio
import os
import requests
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"

classes = ["zCubwf", "hgKElc", "LTK00 sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
           "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTK00", "vlzY6d",
           "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e",
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

client = Groq(api_key=GroqAPIKey)

messages = []

systemChatBot = [{
    "role": "system",
    "content": f"Hello, I am {os.environ.get('USER', 'JarvisAI')}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."
}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenEditor(file_path):
        subprocess.call(["open", "-a", "TextEdit", file_path])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": prompt})
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.strip().replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)
    os.makedirs("Data", exist_ok=True)
    file_path = f"Data/{Topic.lower().replace(' ', '')}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ContentByAI)
    OpenEditor(file_path)
    return True

def YoutubeSearch(Topic):
    url = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(url)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    try:
        subprocess.run(["open", "-a", app], check=True)
        return True
    except Exception as e:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': "UWcKNb"})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            print("Failed to retrieve search results.")
            return None

        html = search_google(app)
        if html:
            link = extract_links(html)
            if link:
                webopen(link[0])
        return True
def CloseApp(app):
    try:
        subprocess.run(["pkill", "-f", app], check=True)
        return True
    except:
        return False

def System(command):
    def run_applescript(script):
        subprocess.run(["osascript", "-e", script])

    if command == "mute":
        run_applescript("set volume output muted true")
    elif command == "unmute":
        run_applescript("set volume output muted false")
    elif command == "volume up":
        run_applescript("set volume output volume ((output volume of (get volume settings)) + 10)")
    elif command == "volume down":
        run_applescript("set volume output volume ((output volume of (get volume settings)) - 10)")
    return True

async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
            funcs.append(fun)
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No Function Found. For {command}")
    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True
