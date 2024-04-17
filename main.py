from data import clean_dataset, get_database
from model import preprocess, train, predict

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--path', type=str, default='data.csv')
    parser.add_argument('--dates_update', action='store_true', default=True)
    parser.add_argument('--from_dataset', action='store_true', default='')
    parser.add_argument('--database', type=str, default='database.db')
    parser.add_argument("-f", "--file", required=False)
    args = parser.parse_args()

    if args.from_dataset:
        df = clean_dataset(args)
    else:
        df = get_database(args)
