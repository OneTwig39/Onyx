// This file is compiled for each target os and placed under src/boot/<osName>

package main

import "encoding/binary"
import "io"
import "os"
import "os/exec"
import "path/filepath"
import "strings"

func main() {
	self, _ := os.Executable()
	file, _ := os.Open(self)
	defer file.Close()

	file.Seek(-2, io.SeekEnd)

	var length uint16
	binary.Read(file, binary.BigEndian, &length)

	file.Seek(-int64(2+length), io.SeekEnd)

	data := make([]byte, length)
	io.ReadFull(file, data)

	args := strings.Fields(string(data))
	argv := []string{}

	for _, a := range args {
		if strings.HasPrefix(a, "%PATH%") {
			argv = append(argv, filepath.Join(filepath.Dir(self), "bin", a[6:]))
		} else {
			argv = append(argv, a)
		}
	}

	argv = append(argv, os.Args[1:]...)
	cmd := exec.Command(argv[0], argv[1:]...)

	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	exit := cmd.Run()

	if exit == nil {
		os.Exit(0)
	}

	os.Exit(exit.(*exec.ExitError).ExitCode())
}
