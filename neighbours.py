from sklearn.neighbors import NearestNeighbors
import numpy as np

UNSEEN_CLASSES = [3,8,11,16,51]

#TODO: Normalize the vectors to be unit vectors.

def get_nn(classnames, Full_data, one_example):
	nbrs = NearestNeighbors(n_neighbors=4, algorithm='auto', metric='cosine').fit(Full_data) 
	distances, nn_indices = nbrs.kneighbors(one_example)
	print('nearest neighbours:')
	for i, index in enumerate(nn_indices[0][1:]):
		print(classnames[index], distances[0][i])
	print('\n')
	return nn_indices[0], distances[0] # nn_indices is a 2D array
	#print classnames[nn_indices]


def generate_embeddings():
	# Use fasttext api to print sentence vectors to console + split labels out
	# read embedding strings as numpy floats

	embeddings = np.zeros((60,600), dtype=float)
	with open("original_embeddings_no_labels.txt") as input_file:
		for i, line in enumerate(input_file):
			line = line.strip()
			for j, number in enumerate(line.split()):
				embeddings[i][j]=float(number)
				
	np.save('class_embeddings', embeddings)
	
	# strip labels out 
	classnames_length = []
	with open('action_classes_original.txt', 'r') as f:
	    classnames = f.read().split('\n')
	    for c in classnames:
		l = len(c.split(' '))
		#print(c, l)
		classnames_length.append(l)
	
	# generate bigram embeddings from output file (with label names)
	bigram_embeddings = np.zeros((60,700), dtype=float)
	with open("output_embeddings.txt") as input_file:
	    for i, line in enumerate(input_file):
		line = line.strip()
		line_array = line.split()
		line_em = line_array[classnames_length[i]:]
		for j, number in enumerate(line_em):
		    bigram_embeddings[i][j]=float(number)

	# save as a numpy array
	np.save('bigram_embeddings', bigram_embeddings)


def main():

	# read the class name text file 
	classnames = []
	with open('action_classes_original.txt', 'r') as f:
		classnames = f.read().split('\n')
		for i in f:
			classnames.append(i)

	x = np.load('class_embeddings.npy')

	for u in UNSEEN_CLASSES:
		print('original_class', classnames[u])
		get_nn(classnames, x, np.reshape(x[u], (1, 600)))




if __name__ == '__main__':
	main()
