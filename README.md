![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

![Emoji](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/emoji-faller.yml/badge.svg)

![Event](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/event-logger.yml/badge.svg)

![Website](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/website.yml/badge.svg)

# Containerized App Exercise
## Overview
The Hand-Tracking Emoji Generator application utilizes hand tracking technology powered by MediaPipe to generate emojis based on users' hand gestures. With this application, users can express themselves using a range of emojis without the need for traditional input methods. Additionally, the application incorporates a database to track the history of previously generated emojis, providing users with a convenient way to revisit their favorite expressions.

## Features
- **Hand Tracking**: Utilizes MediaPipe's hand tracking technology to accurately detect and interpret users' hand gestures.
- **Emoji Generation**: Generates emojis based on recognized hand gestures, allowing users to express themselves visually.
- **User-Friendly Interface**: Designed with an intuitive and easy-to-use interface for seamless interaction and expression.

## How to Run
- Make sure docker is running on your machine before entering this command:
```
docker-compose up --build
```
- After successful build, you can access the website at http://localhost:5001


## Contributors
* [Bonny](https://github.com/BonnyCChavarria) 
* [Christina](https://github.com/crb623)
* [Damla](https://github.com/damlaonder)
* [Yura](https://github.com/yurawu27)
