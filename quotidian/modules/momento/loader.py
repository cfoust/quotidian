import os, re, datetime, string

def fileNameToDateTime(fn):
	parts = fn.split(' ')

	dateo = datetime.datetime.strptime(parts[0],'%Y.%m.%d')

	return dateo

def dateTimeToFileName(dt):

	fn = dt.strftime('%Y.%m.%d - %a, ')

	d = dt.strftime('%d')
	if d[0] == '0':
		d = d[1]
	fn += d
	fn += dt.strftime(' %b %Y.txt')
	return fn

class Day:
	@staticmethod
	def fromFile(filename):
		if not os.path.exists(filename):
			raise Exception("File does not exist: %s" % filename)
		e = Day()
		with open(filename,'r') as f:
			lines = f.readlines()

		# States
		LookingForDateLine = 0
		LookingForEntry = 1
		ScanningEntry = 2

		state = 0

		state = LookingForDateLine
		entries = []
		entry = {}

		fdate = fileNameToDateTime(filename.split('\\')[-1])

		for i,line in enumerate(lines):
			if state == LookingForDateLine:
				parts = line.split(' ')
				if len(parts) == 4:
					if len(parts[1]) == 1:
						parts[1] = '0' + parts[1]

					try:
						dt = datetime.datetime.strptime(' '.join(parts),'%A %d %B %Y\n')
					except:
						continue
					if dt == fdate:
						state = LookingForEntry
			elif state == LookingForEntry:
				parts = line.split(' ')

				if len(parts) >= 2:
					parts = parts[:2]

					if 'AM' in ' '.join(parts) or 'PM' in ' '.join(parts): 
						subparts = parts[0].split(':')

						if len(subparts[0]) == 1:
							subparts[0] = '0' + subparts[0]

						parts[0] = ':'.join(subparts)

						try:
							dt = datetime.datetime.strptime(' '.join(parts),'%I:%M %p')
						except:
							dt = None
							entry['timestamp'] = ' '.join(parts)

						entry['time'] = dt
						entry['text'] = ' '.join(line.split(' ')[2:])
						entry['extras'] = {}

						state = ScanningEntry
			elif state == ScanningEntry:
				
				printl = True
				if re.match(r'([A-Z][a-z]+):',line):
					tagType = re.match(r'([A-Z][a-z]+):',line).group(1)
					line = line[len(tagType) + 1:]
					entry['extras'][tagType] = line.split(',')
					printl = False

				if line == '---\n' or i == (len(lines) - 1):
					state = LookingForEntry
					entry['text'] = entry['text'].rstrip()

					for type in entry['extras']:
						entry['extras'][type] = [x.strip() for x in entry['extras'][type]]

					entries.append(entry)
					entry = {}
					continue

				if printl:
					entry['text'] += line

		if state == LookingForDateLine:
			raise Exception("Failed to find valid date line in %s." % (filename))

		e.entries = entries
		e.date = fdate
		e.name = filename.split('/')[-1]
		return e

	def toFile(self,filename):
		with open(filename,'w') as f:
			f.write('\n')
			dateString = self.date.strftime('%A %d %B %Y')
			f.write(dateString + '\n')
			for i in range(len(dateString)):
				f.write('=')
			f.write('\n\n')

			sorted_entries = sorted(self.entries, key=lambda entry: entry['time'])
			for i, entry in enumerate(sorted_entries):

				timestamp = entry['time'].strftime('%I:%M %p')

				if timestamp[0] == '0':
					timestamp = timestamp[1:]

				f.write(timestamp + ' ' + entry['text'] + '\n\n')

				for type in entry['extras']:
					entry['extras'][type] = [x.strip() for x in entry['extras'][type]]
					f.write(type + ': ' + ', '.join(entry['extras'][type]) + '\n')

				if i != (len(self.entries) - 1):
					f.write('\n---\n\n')
	def __init__(self):
		self.entries = []
		self.extras = {}
		self.date = None

class Diary:
	def __init__(self,folder,debug = False):
		if not os.path.isdir(folder):
			raise Exception('Not a folder: %s' % folder)

		def log(s):
			if debug == True:
				print s

		log("Scanning full_entries/ for compatible entries.")

		files = []
		# for subdir, dirs, filez in os.walk(os.getcwd() + "\\full_entries\\"):
		for subdir, dirs, filez in os.walk("full_entries/"):
		    for file in filez:
				if not (re.search("Attachments", subdir)):
					ftable = {}
					ftable['name'] = file
					f=open(os.getcwd() + "\\full_entries\\" + file, 'r')
					ftable['path'] = os.getcwd() + "\\full_entries\\" + file
					ftable['lines'] = f.readlines()
					files.append(ftable)


		log("%d total files." % len(files))

		log("Ensuring sanity of file names.")
		oldfiles = files
		files = []

		for file in oldfiles:
			name = file['name']
			try:
				dt = fileNameToDateTime(name)
				file['date'] = dt
				files.append(file)
			except:
				log("Parsing file failed, skipping: \"%s\"." % name)

		log("%d total valid files." % (len(files)))

		log("Beginning parse.")
		oldfiles = files
		files = []
		
		for file in oldfiles:
			try:
				files.append(Day.fromFile(file['path']))
			except:
				log("Parsing of file %s failed." % file['path'])

		log("Finished parsing. %d files contained entries." % len(files))

		self.files = files