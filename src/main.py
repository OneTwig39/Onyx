import os
import platform
import re
import shutil
import subprocess
import sys

target = {
	"system": "linux",
	"arch": "amd64",
	"type": "exe"
}

for argument in sys.argv[1:]:
	if argument == "linux":
		target["system"] = "linux"
	if argument == "amd64":
		target["arch"] = "amd64"
	if argument == "shell":
		target["type"] = "shell"

srcModule = os.path.join(os.path.dirname(os.path.dirname(__file__)), "module",
	"linux" if platform.system() == "Linux" else None,
	"amd" if platform.machine() == "AMD64" or platform.machine() == "x86_64" else None,
	"64"
)
dstModule = os.path.join(os.path.dirname(os.path.dirname(__file__)), "module",
	target["system"],
	"amd" if target["arch"] == "amd64" else None,
	"64"
)

if os.path.isdir("dst"):
	shutil.rmtree("dst")
if os.path.isdir("tmp"):
	shutil.rmtree("tmp")
os.mkdir("dst")
shutil.copytree("src", os.path.join("tmp", "scripts"))

requirements = []
scripts = []

with open("app", "r") as f:
	for line in f.read().splitlines():
		if not line:
			continue

		path = ""
		modules = []
		versions = []

		splits = sorted([line.index("/")] + [m.start() for m in re.finditer("\\?", line)] + [len(line)])
		prev = 0
		for split in splits:
			if line[prev] == "/":
				path = line[prev+1:split]
			elif line[prev] == "?":
				modules.append(line[prev+1:split].split("@")[0])
				if "@" in line[prev+1:split]:
					versions.append(line[prev+1:split].split("@")[1])
				else:
					versions.append("")
			else:
				name = line[:split]

			prev = split

		if len(modules) == 0:
			if os.path.splitext(path)[1] == ".go":
				modules = ["go"]
				versions = [""]
			if os.path.splitext(path)[1] == ".py":
				modules = ["python"]
				versions = [""]
		for index, version in enumerate(versions):
			if version:
				continue

			if modules[index] == "go":
				versions[index] = "1.25.12"
			if modules[index] == "python":
				versions[index] = "2026.7.18.3.14.6"

		for index, module in enumerate(modules):
			if module == "python":
				if not os.path.isdir(os.path.join("tmp", module, versions[index])):
					shutil.copytree(os.path.join(dstModule, module, versions[index]), os.path.join("tmp", module, versions[index]))
					requirements.append(module)

		scripts.append({"name": name, "path": path, "modules": modules, "versions": versions})

for script in scripts:
	if script["modules"][-1] == "go":
		bootstrap = ["%PATH%" + os.path.join("scripts", os.path.splitext(script["path"])[0])]
	if script["modules"][-1] == "python":
		bootstrap = ["%PATH%" + os.path.join("python", script["versions"][-1], "bin", "python"), "%PATH%" + os.path.join("scripts", os.path.splitext(script["path"])[0] + ".pyc")]

	if script["name"] == "main":
		if target["system"] == "linux" and target["type"] == "exe":
			shutil.copy(os.path.join(os.path.dirname(__file__), "boot", "linux"), os.path.join("dst", "app"))
			with open(os.path.join("dst", "app"), "ab") as f:
				data = b" ".join([cmd.encode() for cmd in bootstrap])
				f.write(data + len(data).to_bytes(2, byteorder="big"))
	else:
		if "python" in requirements:
			for version in os.listdir(os.path.join("tmp", "python")):
				with open(os.path.join("tmp", "python", version, "lib", sorted(os.listdir(os.path.join("tmp", "python", version, "lib")))[7], script["name"] + ".py"), "w") as f:
					f.write(f"""\
import os
import subprocess
import sys

def call(argv):
	return subprocess.Popen([{", ".join([f'os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), "{cmd[6:]}")' if cmd.startswith("%PATH%") else f'"{cmd}"' for cmd in bootstrap])}] + argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

class _module(sys.modules[__name__].__class__):
	def __call__(self, argv=[]):
		return call(argv)

sys.modules[__name__].__class__ = _module\
""")
for script in scripts:
	file = os.path.join("tmp", "scripts", script["path"])

	for index, module in enumerate(script["modules"]):
		if module == "go":
			subprocess.run([os.path.join(srcModule, "go", script["versions"][index], "bin", "go"), "build", "-o", os.path.splitext(file)[0], file])
			os.remove(file)
			file = os.path.splitext(file)[0]
		if module == "python":
			subprocess.run([os.path.join(dstModule, "python", script["versions"][index], "bin", "python"), "-m", "py_compile", file])
			shutil.copyfile(os.path.join(os.path.dirname(file), "__pycache__", os.listdir(os.path.join(os.path.dirname(file), "__pycache__"))[0]), os.path.splitext(file)[0] + ".pyc")
			os.remove(file)
			shutil.rmtree(os.path.join(os.path.dirname(file), "__pycache__"))
			file = os.path.splitext(file)[0] + ".pyc"

shutil.copytree("tmp", os.path.join("dst", "bin"))
if os.path.isdir("tmp"):
	shutil.rmtree("tmp")
