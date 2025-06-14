# Project Chimera: A Journey into Building a Real-Time Phishing Proxy

Hi there! My name is Kittipat, and I'm a final-year Computer Engineering and Cyber Security student at SIIT.

I've always been fascinated by how modern, secure websites defend themselves. I wanted to go beyond theory and actually build the tools used in penetration testing to truly understand how these defenses work from the inside out. This project is the result of that journey.

## What is This Project?

At its core, Project Chimera is a standalone web server I wrote in Python using the Flask framework. When you give it a target website (like a login page), it doesn't just make a static copy. It acts as a live, invisible middleman—a reverse proxy.

It fetches the real website's content on the fly, intelligently rewrites the page's links and forms to point back to itself, and then serves that modified page to a user. The goal is to do this so seamlessly that even dynamic, JavaScript-heavy sites continue to function, all while allowing me to intercept the data submitted in login forms for security research.

## The Journey: From a Simple Script to a Full-Fledged Proxy

This project was a huge learning experience, and it evolved a lot as I hit the same defensive walls that real-world attackers face.

* **It started with a simple idea:** Could I clone a login page with a basic Python script? I first tried using the `requests` and `BeautifulSoup` libraries. This worked on simple, old websites, but I quickly hit my first major roadblock: modern applications like Steam or GitHub are built with JavaScript. My script just saw a blank, empty shell because it couldn't render the page like a real browser.

* **Discovering Real-World Defenses:** This failure led me down a rabbit hole of research. To solve the JavaScript problem, I learned how to use professional-grade tools like `mitmproxy` to intercept live HTTPS traffic. This was a breakthrough! But it immediately exposed me to the next layer of security. I ran into:
    * **HSTS (HTTP Strict Transport Security):** A browser security policy that completely blocks you from ignoring certificate warnings. I had to learn the specific bypasses that security testers use to get around this in a controlled lab environment.
    * **Server-Side Anti-Bot Systems:** When I targeted major platforms like Facebook, I discovered my tool was being trapped in endless redirect loops. I learned that their servers are smart enough to detect non-human requests and send them on a wild goose chase.

* **The Final Architecture:** All these challenges forced me to abandon simple cloning and build the final version of this tool: a standalone reverse proxy. It's smarter, handles redirects, and is a much more realistic simulation of a sophisticated phishing tool.

## Core Features

-   **Standalone Server:** Runs as a single Python/Flask application.
-   **Live Reverse Proxy:** Fetches and serves content from a live target in real-time.
-   **Dynamic Content Rewriting:** Intelligently rewrites HTML links and form actions to keep the user within the proxy.
-   **Credential Capture:** Intercepts form submissions and logs the data to a local text file.
-   **Publicly Deployable:** Can be easily exposed to the internet for realistic testing using `ngrok`.

## Tech Stack

Python | Flask | Requests | BeautifulSoup4 | ngrok | mitmproxy (for research)

## Getting Started

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-folder>
    ```

2.  **Set up Virtual Environment & Install Dependencies:**
    ```bash
    # Create and activate a virtual environment
    python -m venv venv
    .\venv\Scripts\activate

    # Install required libraries from requirements.txt
    pip install -r requirements.txt
    ```

3.  **Configure and Run the Server:**
    * Open `app.py` and set the `TARGET_HOST` to the test site you want to clone.
    * In your terminal, run the application:
    ```bash
    python app.py
    ```

4.  **Make it Live (Optional):**
    * In a second terminal, use `ngrok` to get a public URL.
    ```bash
    ngrok http 5000
    ```

## A Quick But Important Note on Ethics

I built this tool to learn about and understand security systems, not to cause harm. It is intended for educational use on systems you have explicit permission to test (like a virtual machine or a test website like `testphp.vulnweb.com`).

Please, do not use this tool or its concepts for any malicious purpose. Let's use our skills to build and protect.
