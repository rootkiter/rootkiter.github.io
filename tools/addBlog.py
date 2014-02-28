import time
import os

def addhead():
	layout  = 'post'
	mytitle = raw_input("Please input the title now :")
	while(len(mytitle)<=0):
		mytitle = raw_input("The title con't be null,you need input it:")
	nowdate = time.strftime("%Y-%m-%d")
	nowtime = time.strftime("%H:%M:%S")
	mymusic = raw_input("Input a music name ( 'name' / 0 / nil ):")
	if (len(mymusic)<=0):
		mymusic = "nil"
	elif (mymusic == '0'):
		mymusic = "backmusic.mp3"
	mytags  = raw_input("Input tags (nil) :")
	if(len(mytags)<=0):
		mytags='nil'
	filename = 'new_'+nowdate+'-'+mytitle

	newfile = open(filename ,'w')
	newfile.write('---')
	newfile.write("\nlayout: " + layout)
	newfile.write("\ntitle:  \"" + mytitle +"\"")
	newfile.write("\ndate:   " + nowdate)
	newfile.write("\ntime:   " + nowtime)
	newfile.write("\ntags:   ")
	newfile.write("\n     - " +mytags )
	newfile.write("\nmusic:  " + mymusic)
	newfile.write("\n---")
	newfile.close()
	print "The file name is ["+ filename
	return filename

def vimedit(filename):
	os.system("vim "+ filename)

def replaceCmd(filename):
	oldfile = open(filename,"r")
	newfilename = filename.replace('new_','')
	newfile = open("../_posts/"+newfilename+".markdown","w")
	line = oldfile.readline()
	i = 0
	while line:
		if line.startswith("add_img:"):
## Add Image
			imgname = line.replace("add_img:","")
			imgname = imgname.replace(" ","")
			imgname = imgname.replace("\n","")
			newfile.write("<img \nsrc=\"http://rootkiter.{{ site.domain }}/music/"+ imgname+"\" title=\""+imgname+"\" align=\"center\">\n")
		elif line.startswith("add_liebiao:"):
			resu = "<ul>\n"
			line = oldfile.readline()
			while(not "end_liebiao:" in line):
				line = line.replace("\n","")
				liebiao = line.split(' ')
				for item in liebiao :
					resu += "<li>"+item+"</li>\n"
				line = oldfile.readline()
			resu += "</ul>\n"
			newfile.write( resu )
		elif line.startswith("add_table:"):
			resu = "<table>\n"
			line = oldfile.readline()
			while(not "end_table" in line):
				line = line.replace("\n","")
				resu += "<tr>\n"
				buf = line.split(" ")
				for item in buf:
					resu += "<th>"+item+"</th>\n"
				resu += "</tr>\n"
				line = oldfile.readline()
			resu += "</table>\n"
			newfile.write( resu )
		else:
			newfile.write( line )
		line = oldfile.readline()
		i += 1
		print "Translating line: "+ i
	oldfile.close()
	newfile.close()
	return newfilename

#addhead()
#newfilename = "new_2014_02_28_test"
newfilename = addhead()
vimedit(newfilename)
print "::::::::" + replaceCmd(newfilename)

