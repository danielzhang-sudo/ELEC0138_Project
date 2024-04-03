import pandas as pd
from data import clean_data
import argparse

def main(args):
	df = clean_data(args)
	print(df.head())
	print(df.info)

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--path', type=str, default='data.csv', help='path to dataset')

	args = parser.parse_args()
	main(args)
