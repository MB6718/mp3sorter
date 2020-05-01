import os
import click
import eyed3

@click.command()
@click.option('-s', '--src-dir',
			  type=click.Path(),
			  help='Source directory.',
			  default=os.getcwd())
@click.option('-d', '--dst-dir',
			  type=click.Path(),
			  help='Destination directory.',
			  default=os.getcwd())
def main(src_dir, dst_dir):

	"""Final task "Sorter of *.mp3 files by ID3 tags" [Author: Max Bee]"""

	# Проверяем, что путь 'src_dir' существует в ФС
	source_path_exists = os.path.exists(src_dir)
	if source_path_exists:
		files_list = get_files_list(src_dir)
		if files_list:
			for file_name in files_list:
				file_handler(dst_dir, src_dir, file_name)
			print('Done')
		else:
			print('ERROR: There are no *.mp3 files on the specified path')
	else:
		print('ERROR: Source directory not exist')
		
def file_handler(destination_dir, source_dir, file_name):
	# соединяем пути с учетом правил ОС и получаем сведения об аудио файле
	artist, title, album = get_file_tags(os.path.join(source_dir, file_name))
	if artist == None or album == None:
		#print(f'{artist} | {title} | {album}\n>>> PASS')
		pass
	else:		
		new_file_name = file_name
		if title != None:
			new_file_name = f'{title} - {artist} - {album}.mp3'
		
		destination_path = os.path.join(destination_dir, artist, album)
		# Создаём цепь директорий по указанному пути
		destination_dir_maked = make_dest_dir(destination_path)
		if destination_dir_maked:
			# если цепь создана, перемещаем файл по пути
			move_file(source_dir, destination_path, file_name, new_file_name)
		else:
			print('ERROR: ')

def move_file(source_path, destination_path, file_name, new_file_name):
	file_from = os.path.join(source_path, file_name)
	file_to = os.path.join(destination_path, new_file_name)
	show_info(file_from, file_to)

def show_info(file_from, file_to):
	file_from = file_from.replace(os.getcwd(), '')
	file_to = file_to.replace(os.getcwd(), '')
	print(f'{file_from} > {file_to}')
		
def make_dest_dir(destination_path):
	# проверяем, существует ли указанный путь
	destination_path_exists = os.path.exists(destination_path)
	if destination_path_exists:
		# Проверим, что у текущего пользователя есть права на запись по пути
		write_permission = os.access(destination_path, mode=os.W_OK)
		if not write_permission:
			return False
	else:
		# Создаём каталоги по указанному пути
		os.makedirs(destination_path, mode=0o777, exist_ok=True)
	return True
	
def get_file_tags(file_name):
	# получаем из файла ID3 тэги
	mp3_file = eyed3.load(file_name)
	try:
		return mp3_file.tag.artist, mp3_file.tag.title, mp3_file.tag.album
	except AttributeError:
		return None, None, None

def get_files_list(directory):
	# Получаем список файлов в переменную files
	files = os.listdir(directory)

	# Фильтруем список
	mp3_files = list(filter(lambda x: x.endswith('.mp3'), files))

	return mp3_files

# точка входа в программу
if __name__ == '__main__':
	main()
