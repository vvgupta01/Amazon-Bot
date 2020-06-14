from AmazonBot import AmazonBot
import Utils
import sys


def main():
    amazon_bot = AmazonBot()

    url, generate, low, high, change, discount, stock = sys.argv[1:]
    low = float(low)
    high = float(high)
    change = float(change)
    discount = int(discount)
    stock = int(stock)
    Utils.check_track_errors(low, high, change, discount, stock)

    errors = []
    data = amazon_bot.retrieve(url, errors)
    if data is None:
        sys.exit()
    file_name = Utils.clean_str(data[0])
    data.append(Utils.get_time().strftime('%m/%d/%Y %I:%M%p'))

    list_price_str = 'None' if data[1] is None \
        else '${:.2f}'.format(data[1])
    price_str = 'Not Available' if data[2] is None \
        else '${:.2f}'.format(data[2])
    print(f'List Price: {list_price_str} Price: {price_str} '
          f'Availability: {data[3]}')
    if generate == 'True' and (low > 0 or high > 0 or change > 0
                               or discount > 0 or stock > 0):
        args = [url, low, high, change, discount, stock]
        Utils.generate_script('scripts_track', args)

    if not Utils.is_file(f'items/{file_name}'):
        columns = ['LIST_PRICE', 'PRICE', 'AVAILABILITY', 'DATETIME']
        df = Utils.create_df([data[1:]], columns)
        Utils.save_df(df, file_name, 'items')
    else:
        df = Utils.open_csv(f'items/{file_name}')

        body = ''
        if data[2] is None:
            body += f'Price is no longer available.\n'
        else:
            current_change = abs(data[2] - df['PRICE'].iloc[0])
            if data[2] <= low:
                body += f'Price is ${data[2]:.2f} ' \
                        f'(${low:.2f} lower price trigger).\n'
            elif data[2] >= high != 0:
                body += f'Price is ${data[2]:.2f} ' \
                        f'(${high:.2f} upper price trigger).\n '
            if current_change >= change > 0:
                body += f'Price changed by ${current_change:.2f} and is ' \
                        f'${data[2]:.2f} (${change:.2f} price change trigger).\n'
            if discount > 0 and data[1] is not None:
                current_discount = int((data[1] - data[2]) / data[1] * 100)
                if current_discount >= discount:
                    body += f'Item is {current_discount}% off ' \
                            f'({discount}% discount trigger).\n'

            stock_str = 'left in stock'
            if stock > 0 and stock_str in data[3]:
                current_stock = int(data[3][5:-28])
                if current_stock <= stock:
                    body += f'Only {current_stock} left in stock ' \
                            f'({stock} stock trigger)'
            last = df['AVAILABILITY'].iloc[-1]
            is_stock = stock_str in data[3]
            if (not is_stock and data[3] != last) or \
                    ((stock_str in last) != is_stock):
                body += f'Availability: {data[3]}\n'

        df.loc[df.shape[0]] = data[1:]
        path = Utils.save_df(df, file_name, 'items')

        if body != '':
            date = Utils.get_time().strftime('%m/%d/%Y')
            time = Utils.get_time().strftime('%I:%M %p')
            body = f'The following are updates for \'{data[0]}\' ' \
                   f'on {date} at {time}:\n{body}\n{url}'
            Utils.send_email('Amazon Bot: Tracked Item Update', body, path, 'item')


if __name__ == '__main__':
    main()
