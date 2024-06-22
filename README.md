# Text to Speech Converter

## Overview

The Text to Speech Converter is a web application that allows users to convert text into speech using various voice and language options. The application interacts with an API to generate and retrieve audio files. The project has been enhanced to provide a modern, user-friendly interface.

## Features

- Select from a variety of voices to convert text into speech.
- Display the generated Post ID with an option to copy it to the clipboard.
- Retrieve and play generated audio files based on the Post ID.

## Technologies Used

- HTML
- CSS
- JavaScript
- jQuery
- Font Awesome
- Google Fonts

1. **Clone the repository:**
    ```bash
    git clone https://github.com/amirmalaeb/text-to-speech-converter.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd text-to-speech-converter
    ```

3. **Open `index.html` in your preferred web browser.**

## Usage

1. **Select a voice:**
    - Choose from the dropdown menu of available voices.

2. **Enter text:**
    - Type the text you want to convert into speech in the provided textarea.

3. **Generate speech:**
    - Click the "Text to Speech!" button to generate the speech. The Post ID will be displayed with an option to copy it.

4. **Retrieve and play audio:**
    - Enter the Post ID in the provided input field and click "Retrieve" to retrieve and play the generated audio file.
  


![text-to-speech](https://github.com/AmirMalaeb/Text-to-Speech-Converter/assets/162432988/9b6930fd-fb2a-4e71-a98e-92346d869798)



Steps Documentation:

Step 1: Set Up Your AWS Environment

 1.	Create an S3 Bucket:
	•	Create an S3 bucket to store the generated MP3 files.
	•	Enable public access to this bucket so the MP3 files can be accessed via URL.
	
 2.	Create a DynamoDB Table:
	•	Create a DynamoDB table named posts with a primary key id (string).
	
 3.	Create an SNS Topic:
	•	Create an SNS topic named new_posts to handle notifications for new posts.
	
 4	Create IAM Roles:
	•	Create an IAM role for your Lambda functions with the necessary permissions

 Step 2: Create Lambda Functions

 1.	Lambda Function 1: new_post
	•	Please find code in the files (post function)
    •	Environment Variables:
    •	DB_TABLE_NAME: Name of the DynamoDB table (posts).
	•	SNS_TOPIC: ARN of the SNS topic (new_posts).

 2.	Lambda Function 2: convert_to_speech
	•	Please find code in the files (text-to-speech function)
    •	Environment Variables:
	•	DB_TABLE_NAME: Name of the DynamoDB table (posts).
	•	BUCKET_NAME: Name of the S3 bucket.

 3. •	Lambda Function 3: get_post
    •   Please find code in the files (get function)
    •	Environment Variables:
	•	DB_TABLE_NAME: Name of the DynamoDB table (posts).

  Step 3: Create API Gateway

  1.	Create a REST API:
	•	Create a new REST API.
  
  2.	Create Resources and Methods:
	•	Resource: /new_post
	•	Method: POST
	•	Integration: Lambda Function (new_post)
	•	Method: Triggered by SNS Topic (new_posts)
	•	Method: GET
	•	Integration: Lambda Function (get_post)
	
  3.	Enable CORS:
	•	Enable CORS for all resources and methods in your API Gateway.
  
  4.	Deploy the API:
	•	Deploy the API to a stage (e.g., dev).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or feedback, please contact Amir at amir.malaeb@gmail.com.
