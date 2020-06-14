import email
import smtplib
from datetime import datetime

import pandas as pd
import sys
import os
import re

PARAMS = {'SERVER': 'smtp.gmail.com:587',
          'EMAIL': 'username@gmail.com', 'PASSWORD': 'app-password'}
PATH = 'C:/.../Amazon-Bot'
PYTHON_PATH = 'C:/.../python.exe'


def check_query_errors(pages, limit, sort_column):
    error_msg = ''
    if pages < 1:
        error_msg += 'Error: The number of pages must be positive.\n'
    if limit < 0:
        error_msg += 'Error: The item limit must be non-negative.\n'
    if sort_column not in ['LIST_PRICE', 'PRICE', 'RATING',
                           'REVIEWS', 'STOCK', 'NONE']:
        error_msg += 'Error: Sort column must be either list_price, ' \
                     'price, rating, reviews, or stock.\n'
    if error_msg != '':
        print(error_msg)
        sys.exit()


def check_track_errors(low, high, change, discount, stock):
    error_msg = ''
    if low < 0 or high < 0 or change < 0 \
            or discount < 0 or stock < 0:
        error_msg += 'Error: All triggers must be non-negative.\n'
    if low >= high > 0:
        error_msg += 'Error: The lower price trigger must be less than the upper price trigger.\n'
    if discount > 100:
        error_msg += 'Error: Discount must be between 0-100.\n'
    if error_msg != '':
        print(error_msg)
        sys.exit()


def create_df(data, columns):
    return pd.DataFrame(data, columns=columns)


def clean_df(df, sort, ascending):
    df.dropna(subset=['NAME'], inplace=True)
    df.drop_duplicates(keep=False, inplace=True)
    if sort != 'NONE':
        df.sort_values(by=sort, ascending=ascending,
                       na_position='last', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def save_df(df, file_name, directory):
    path = f'{PATH}/{directory}/{file_name}.csv'
    df.to_csv(path, index=False)
    print(f'Successfully saved file in {path}')
    return path


def generate_script(directory, args):
    script_id = get_size(directory) + 1
    name = directory[-5:]
    path = f'{PATH}/{directory}/{name}-{script_id}.bat'
    with open(path, 'w') as file:
        file.write(f'{PYTHON_PATH} {PATH}/src/{name}.py '
                   f'\"{args[0]}\" $false {args[1]} {args[2]} {args[3]} {args[4]} {args[5]}')
    print(f'Successfully generated script in {path}')


def send_email(subject, body, path, file_name):
    message = email.message.EmailMessage()
    message['From'] = PARAMS['EMAIL']
    message['To'] = PARAMS['EMAIL']
    message['Subject'] = subject
    message.set_content(body)
    message.add_attachment(open(path, 'r', encoding='utf8').read(),
                           filename=f'{file_name}.csv')

    with smtplib.SMTP(PARAMS['SERVER']) as server:
        server.starttls()
        try:
            server.login(PARAMS['EMAIL'], PARAMS['PASSWORD'])
        except smtplib.SMTPException:
            print('Error: Unable to send email.\n'
                  'Check your connection and verify that your email credentials are correct')
            return
        server.send_message(message)
        server.quit()
    print('Successfully sent email')


def clean_str(string):
    string = re.sub('[<>:"/|\\\\?*.]', '', string)
    return string.replace(' ', '_')


def open_csv(path):
    return pd.read_csv(f'{PATH}/{path}.csv')


def is_file(path):
    return os.path.isfile(f'{PATH}/{path}.csv')


def get_size(directory):
    return len(os.listdir(f'{PATH}/{directory}'))


def get_time():
    return datetime.today()
