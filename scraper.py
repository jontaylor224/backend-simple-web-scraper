#!/usr/bin/env python

__author__ = 'jontaylor224'

import argparse
import requests
import re
import sys


def get_data(target_url):
    '''Takes target_url and returns the text from a GET request to that URL'''
    raw_data = requests.get(target_url)
    text_data = raw_data.text
    return text_data


def parse_data(data):
    '''takes URL text data and parses for URLs, email addresses, and phone numbers'''
    urls = sorted(set(re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)))
    emails = sorted(set(re.findall(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data)))
    phone_numbers = set(re.findall(
        r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?', data))
    formatted_numbers = sorted(format_phone_numbers(phone_numbers))
    print_data(urls, emails, formatted_numbers)


def format_phone_numbers(numbers):
    '''Takes a list of phone numbers in tuples and returns a list of formatted strings
    Example:
    [(u'234', u'555', u'1134')] returns ['234-555-1134']'''
    new_numbers_list = []
    for number in numbers:
        formatted_num = '{}-{}-{}'.format(
            number[0], number[1], number[2])
        new_numbers_list.append(formatted_num)
    return new_numbers_list


def print_data(urls, emails, phone_numbers):
    '''prints URLS, emails and phone numbers from parsed data in more readable format'''
    print('URLS\n')
    for url in urls:
        print('{}\n'.format(url))
    print('\n\nEmails\n')
    for email in emails:
        print('{}\n'.format(email))
    print('\n\nPhone Numbers\n')
    for phone in phone_numbers:
        print('{}\n'.format(phone))


def create_parser():
    '''create an argument parser object'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help="target url to scrape")
    return parser


def main(args):
    ''' parse args and if URL is given, scrape for URLS, email addresses and phone numbers'''
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    if parsed_args.url:
        site_data = get_data(parsed_args.url)
        parse_data(site_data)
    else:
        print("Please provide a URL to parse")


if __name__ == '__main__':
    main(sys.argv[1:])
