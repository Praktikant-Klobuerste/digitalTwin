import subprocess

program1 = "./digitalTwin/digitalTwin2022_v22_12.py"
program2 = "./digitalTwin/01_uebung_handshake.py"

p1 = subprocess.Popen(["python", program1])
p2 = subprocess.Popen(["python", program2])

p1.wait()
p2.wait()