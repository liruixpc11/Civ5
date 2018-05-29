# coding=utf-8
import os
import sys
import re

PART_PATTERN = re.compile(ur'^(第[一二三四五六七八九十]+部分)，(.*)')
SECTION_PATTERN = re.compile(ur'^([一二三四五六七八九十]+)，(.*)')
SUBSEC_PATTERN = re.compile(ur'^(\d+\.\d+)(.*)')

PATTERNS = (
	(PART_PATTERN, u"# {} {}"),
	(SECTION_PATTERN, u"## {}、{}"),
	(SUBSEC_PATTERN, u"### {} {}"),
)

if len(sys.argv) != 2:
	print("USAGE: {} MD_FILE".format(sys.argv[0]))
	sys.exit(1)

origin_file = sys.argv[1]
if not os.path.exists(origin_file):
	raise Exception("file {} not exists".format(origin_file))

bak_file = origin_file + ".bak"
if os.path.exists(bak_file):
	os.remove(bak_file)
os.rename(origin_file, bak_file)

out_lines = []
with open(bak_file, 'r') as in_file:
	lines = in_file.readlines()
	for i, line in enumerate(lines):
		line = line.decode('utf-8')
		if not len(line.strip()):
			if len(lines) > i + 1 and not len(lines[i + 1].strip()):
				pass
			else:
				out_lines.append(line)
			continue

		if line.startswith('#') or not line.strip():
			out_lines.append(line)
		else:
			matched = False
			for pattern, format_s in PATTERNS:
				m = pattern.match(line)
				if m:
					out_lines.append(format_s.format(m.group(1), m.group(2)))
					matched = True
					break
			if not matched:
				if (not line.startswith('![') and
					not line.endswith(u"。\n") and
					not line.endswith(u"！\n")):
					out_lines.append(line[:-1] + u"。\n")
				else:
					out_lines.append(line)

		if len(lines) > i + 1 and len(lines[i + 1].strip()):
			out_lines.append(u"\n")

with open(origin_file, 'wb') as out_file:
	for line in out_lines:
		out_file.write(line.encode('utf-8'))