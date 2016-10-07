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
		ans = (a*x)+(b*y)+(c*z)
		print "%d,%f" %(i+1461,ans)