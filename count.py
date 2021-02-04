import os

def count_images():
	dirs = list(os.walk("."))[0][1][1:]
	print(f"Number of classes: {len(dirs)}")
	for each in dirs:
		print(f"{each} => {len(os.listdir(each))}")
		
		# Generate for markdown
		# print(f"|{each}|{len(os.listdir(each))}|")		 

if __name__ == '__main__':
	count_images()
	