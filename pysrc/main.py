import time

while True:
	try:
		# Check hashsum of main.py. If different, machine reset
		import init
		print("init code found. Executing...")
		init.main()
	except Exception as e:
		print("Exception occurred: " + str(e))
	print("Waiting 10 seconds for init code...")
	time.sleep(10)
