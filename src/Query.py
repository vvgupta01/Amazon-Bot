from AmazonBot import AmazonBot
import Utils
import sys


def main():
    now = Utils.get_time()
    amazon_bot = AmazonBot()

    query, generate, pages, limit, sort, ascending, email = sys.argv[1:]
    Utils.check_query_errors(int(pages), int(limit), sort.upper())

    df = amazon_bot.query(query, int(pages), int(limit),
                          sort.upper(), ascending == 'True')

    if df is None:
        sys.exit()

    date_time = now.strftime('%m-%d-%Y-%H%M')
    path = Utils.save_df(df, f'{Utils.clean_str(query)}_{date_time}', 'queries')

    if generate == 'True':
        args = [query, pages, limit, sort, ascending, email]
        Utils.generate_script('scripts_query', args)

    if email == 'True':
        date = now.strftime('%m/%d/%Y')
        time = now.strftime('%I:%M %p')
        order_str = 'ascending' if ascending == 'True' else 'descending'
        body = f'The following is the search query result for ' \
               f'\'{query}\' from Amazon.com on {date} at {time}, ' \
               f'limited to the first {pages} pages and sorted ' \
               f'by {sort} in {order_str} order.'
        Utils.send_email('Amazon Bot: Search Query Results',
                         body, path, query)


if __name__ == '__main__':
    main()
