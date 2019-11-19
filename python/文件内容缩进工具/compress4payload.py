import getopt
import sys
import os


# 把代码压缩成Payload
def execute(file, list1, encoding='utf-8'):
	if not os.path.exists(file):
		print("所选文件不存在！")
		sys.exit(0)
	with open("%s.min" % file, 'a', encoding=encoding) as f:
		for line in open(file, 'r', encoding=encoding):
			if line.endswith('\r\n'):
				line = line[:len(line) - 2]
			elif line.endswith('\n'):
				line = line[:len(line) - 1]
			if line.strip().startswith("#") or line.strip().startswith("//"):
				continue
			if "-p" in list1:
				if line.strip().startswith("print"):
					continue
			line = check_note(line)
			# 规则字符串转换
			if "-z" in list1:
				line = line.replace("+", "%2b")
			if "-x" in list1:
				line = line.replace("\\", "\\\\")
			if "-c" in list1:
				line = line.replace("\"", "\\\"")
			f.write("%s " % line)
		print("生成文件：%s" % "%s.min" % file)


def check_note(line):
	return check_note_e(check_note_e(line, "//"), "#")


def check_note_e(line, reg, start=None):
	if not start:
		start = 0
	if line.find(reg, start, len(line)) != -1:
		tmp_line = line.replace('\\"', '')
		tmp_line = tmp_line.replace('\\\'', '')
		n = tmp_line.count("\"", 0, line.find(reg, start, len(line)))
		if (n % 2) == 0:
			n = tmp_line.count("'", 0, line.find(reg, start, len(line)))
			if (n % 2) == 0:
				line = line[:line.find(reg, start, len(line))]
			else:
				start = line.find(reg, start, len(line)) + 1
				line = check_note_e(line, reg, start)
		else:
			start = line.find(reg, start, len(line)) + 1
			line = check_note_e(line, reg, start)

	return line


if __name__ == '__main__':
	help_ = "参数：'-f' 或 '--file=' 指定文件，'-e' 或 '--encoding=' 指定编码方式，默认编码为utf-8。\r\n-p 将print为首的行去掉， -z 将+转换成%2b， -x 将\\转换成\\\\， -c 将\"转换为\\\"。"
	file = None
	encoding = "utf-8"

	try:
		options, args = getopt.getopt(sys.argv[1:], 'hf:e:pzxc', ["help", "file=", "encoding="])
	except getopt.GetoptError:
		sys.exit(0)
	list1 = []
	for name, value in options:
		if name in ("-h", "--help"):
			print(help_)
			sys.exit(0)
		if name in ("-f", "--file"):
			file = value
		if name in ("-e", "--encoding"):
			encoding = value
		if name in ("-p", "-z", "-x", "-c"):
			list1.append(name)

	# 校验参数
	if file is None or file.strip() == '':
		print("请指定需要缩进的文件")
		print(help_)
	else:
		if file.endswith(".py") or file.endswith(".sh"):
			print("python和shell的文件目前搞不了！  (｡ŏ_ŏ)")
		else:
			execute(file, list1, encoding)
