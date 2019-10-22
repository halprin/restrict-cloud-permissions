from bs4 import BeautifulSoup
import requests
import re
import traceback
import iterator_chain


def get_nth_item_in_list_or_default(list, index, default):
    return list[index] if -len(list) <= index < len(list) else default


def download_url(url):
    response = requests.get(url)
    return response.text


def find_first_table(parser):
    return get_nth_item_in_list_or_default(parser.find_all('div', 'table'), 0, None)


def find_a_tags_to_http(parser):
    return parser.find_all('a', href=re.compile('^http'))


def get_title(parser):
    h1 = parser.h1
    if h1 is not None:
        return h1.string
    else:
        return ''


def keep_non_blank_and_differences(conversion_tuple):
    return conversion_tuple[1] != '' and conversion_tuple[0] != conversion_tuple[1]


alpha_numeric = re.compile('^[a-zA-Z0-9]+$')


def keep_alpha_numeric_and_warn_on_others(conversion_tuple):
    try:
        if alpha_numeric.match(conversion_tuple[1]) is None:
            print(f"{conversion_tuple} seems fishy, throwing out")
            return False
        else:
            return True
    except Exception:
        print(f"{conversion_tuple} seems fishy, throwing out")
        return False


def cumulate_conversion_tuple_to_dictionary(cumulator, conversion_tuple):
    cumulator[conversion_tuple[1]] = conversion_tuple[0]
    return cumulator


def get_service_conversion(url):
    print(f'Generating conversion for {url}')
    try:
        html = download_url(url)
        parser = BeautifulSoup(html, 'html.parser')
        service_prefix = parser.code.string
        first_table = find_first_table(parser)
        if first_table is not None:
            http_links = find_a_tags_to_http(first_table)
        else:
            http_links = []

        conversion = iterator_chain.from_iterable(http_links) \
            .map(lambda a_tag: (a_tag.string.strip(), a_tag['href'])) \
            .map(lambda link_tuples: (link_tuples[0], download_url(link_tuples[1]))) \
            .map(lambda link_tuples: (link_tuples[0], BeautifulSoup(link_tuples[1], 'html.parser'))) \
            .map(lambda link_tuples: (link_tuples[0], get_title(link_tuples[1]))) \
            .filter(keep_non_blank_and_differences) \
            .filter(keep_alpha_numeric_and_warn_on_others) \
            .map(lambda conversion_tuple: (f'{service_prefix}:{conversion_tuple[0]}', f'{service_prefix}:{conversion_tuple[1]}')) \
            .reduce(cumulate_conversion_tuple_to_dictionary, initial={})
    except Exception:
        print(f'There was an issue getting the conversion from {url}')
        traceback.print_exc()
        conversion = {}

    return conversion


def get_list_of_services_links(parser):
    return parser.find(string='Topics').parent.parent.parent.find_all('a')


def cumulate_service_conversion_dictionaries(cumulator, conversion):
    return {**cumulator, **conversion}


def get_all_service_conversions():
    base_url = 'https://docs.aws.amazon.com/IAM/latest/UserGuide/'
    html = download_url(f'{base_url}reference_policies_actions-resources-contextkeys.html')
    parser = BeautifulSoup(html, 'html.parser')
    service_links = get_list_of_services_links(parser)

    service_urls = iterator_chain.from_iterable(service_links) \
        .map(lambda a_tag: a_tag['href']) \
        .map(lambda href: f'{base_url}{href}') \
        .list()

    all_service_conversion = iterator_chain.from_iterable(service_urls) \
        .map(get_service_conversion) \
        .reduce(cumulate_service_conversion_dictionaries, initial={})

    print(len(all_service_conversion.values()))
    print(all_service_conversion)


if __name__ == '__main__':
    get_all_service_conversions()
