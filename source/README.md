# Drishti - The Intelligent Eye

The goal of this project is to create the 'Drishti' voice assistant, which will be available 24X7 to aid visually impaired people in visualizing the world. Drishti helps visually impaired persons obtain access to the most significant resources that will enhance their living situations by using a variety of custom layouts and speech synthesis. She carries out tasks based on the user's input (in the form of voice) and answers in the same manner.

## Methodology used

This project is composed of various of AI technologies that work well together and can assist our notion.

The project is organized into four sections: intent identification, text-to-speech, object identification, and speech-to-text.
These four AI-powered technologies were then merged to create a smart voice assistant that can understand its user's needs.

![image](https://user-images.githubusercontent.com/64425886/174514005-3f4d1078-db8d-4c97-aead-4485c64e9e86.png)

## Technologies used
All four aspects of our project were implemented using Microsoft Azure services. We utilized
1. LUIS (Language Understanding) - cloud based AI service to extract valuable information in conversations and interpret the user's purpose (intents).
2. Speech-to-text from the Speech service, which is part of Azure Cognitive Services, to convert speech to text.
3. Computer Vision Image Analysis service to correctly recognise and name objects in the surrounding. The OCR capability of this service is also utilised to extract text from images.
4. Text-to-Speech capability of the Speech service, which is part of Azure Cognitive Services, to transform text into humanlike synthesised speech.

Code is written in Python3. Other libraries used are OpenCV-python to capture images of the surrounding and mpg123 to play audio in the system.

## Requirements
1. Python3
2. Git
3. Pip

## How to setup?
1. Create a new directory
2. Use the following command to install virtualenv, if already not installed
```
pip install virtualenv
```
3. cd into new directory
4. Create a virtual environment
```
virtualenv env
```
5. Clone this repository
```
git clone https://github.com/SrishtiSingh2001/Drishti_the_Intelligent_Eye.git
```
6. Activate virtual env

   * For Windows users:
     ```
     source env/Scripts/activate
     ```
   * For Ubuntu users:
     ```
     source env/bin/activate
     ```
7. cd into the source folder
```
cd Drishti_the_Intelligent_Eye/source
```
8. Install dependencies
```
pip install -r requirements.txt
```

## File structure

 ### source

* [audio_files/](./source/audio_files) - contains audio files
  * [sound.mp3](./source\audio_files/sound.mp3)
* [modules/](./source/modules) 
  * [detect.py](./source/modules/detect.py) - Functions for object and color detection and text extraction
  * [functions.py](./source/modules/functions.py) - Functions of get time, brightness and play audio
  * [getIntent.py](./source/modules/getIntent.py) - Function to detect intent using LUIS rest API
  * [speech.py](./source/modules/speech.py) - Speech class for speech synthesis and recognition
  * [\_\_init\_\_.py](./source/modules/__init__.py)
* [.gitignore](./source/.gitignore)
* [main.py](./source/main.py) - Main source file
* [README.md](./source/README.md)
* [requirements.txt](./source/requirements.txt) - All the library dependency list


## How to run the code?
1. cd into source folder
```
cd Drishti_the_Intelligent_Eye/source
```
2. Run the file main.py
```
py main.py
```
**Note:** You need to create your own Azure free account to run the script. Create resources in Azure for speech, computer vision and language understanding. Also create a LUIS account to create intents for the features mentioned below with example phrases and get the require prediction keys and endpoint url. *Keys used in this repo are not public.*

## Usage
1. Speak into the microphone to activate Drishti using phrases like 'Hii Drishti', 'Good morning Drishti', 'Help me Drishti', etc.
2. Drishti will start listening to your query. Speak what you need into the mic.
4. Drishti will respond back in sound.
5. Need more help? Speak again what you want Drishti to do for you.
6. You're done? Stop the conversation using phrases like 'Stop the conversation', 'Quit now', etc.

![image](https://user-images.githubusercontent.com/64425886/174523052-6c3b401a-893b-4855-89f3-5dacbb3f8685.png)

## Example phrases to avail implemented features
1. Describe the the scene - 'Please describe the scene', 'Can you please describe the road?', 'Description of the view', etc.
2. Read text - 'Help me read the text', 'Read the book for me', 'Read this form', etc.
3. Play audio - 'Please play the audio', 'Play my favorite song', etc.
4. Time - 'What's the time right now?', 'Tell me the time', ect.
5. Brightness - 'How is the brightness outside?', 'Is it bright ourside?', etc.
6. End conversation - 'Okay quit now!', 'Let's stop this conversation', etc.

## License
[MIT](https://choosealicense.com/licenses/mit/)
