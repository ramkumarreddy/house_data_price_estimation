print "Id,SalePrice"
with open('out3.csv', 'r') as content_file:
    content = content_file.read()
content = content.split('\n')
for i in range(0,len(content)):
	if ',' in content[i]:
		x = 0.45
		y = 0.5
		z = 0.05
		a = float(content[i].split(',')[0])
		b = float(content[i].split(',')[1])
		c = float(content[i].split(',')[2])
		if abs(c-a)<2000:
			x = 0.2
			y = 0.2
			z = 0.6
		elif abs(c-a)<6100:
			x = 0.25
			y = 0.25
			z = 0.5
		elif abs(c-a)<16000:
			x = 0.3
			y = 0.3
			z = 0.4
		elif abs(c-a)<20000:
			x = 0.35
			y = 0.45
			z = 0.2
		elif abs(c-a)<33000:
			x = 0.45
			y = 0.45
			z = 0.1
		ans = (a*x)+(b*y)+(c*z)
		print "%d,%f" %(i+1461,ans)