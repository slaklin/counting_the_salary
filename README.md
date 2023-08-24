# Programming vacancies compare
This project uses the web services api hh.ru and superjob.ru to search for programmer vacancies in various programming languages and identify the average salary for each of them separately. Outputs the result for services in the form of a table.

## How to install
1. Create [api.superjob](https://api.superjob.ru/) Generate API Key for work with API.

#### Requirements

Python3 should be already installed. Then use pip to install dependencies:
```
pip install -r requirements.txt
```
### Create an environment

#### Environment variables

- SECRET_KEY

1. Place the `.env` file in the root folder of your project.
2. `.env` contains text data without quotes.

For example, if you print `.env` content, you will see:

```
$ cat .env
SECRET_KEY=1a5d754733b015ghty67660143c70238efa4esad1taec48
```
## Example of running a script
```
C:\Users\Training\counting_the_salary\counting_the_salary\counting_the_salary.py
```
## Project Goals
This code was written for educational purposes as part of an online course for web developers at [dvmn.org.](https://dvmn.org/)

