import xlrd
import re
import os



XLSDIR = '../xls/'

listing = os.listdir(XLSDIR)
files = []
for infile in listing:
    if infile[-3:].upper() == 'XLS' and not infile == 'Blank2.xls':
	files.append(infile)

for filename in files:
    print filename
    match = re.search(r"(?P<districtname>.*?)\s+(?P<provinceno>\d)-(?P<districtno>\d+)-(?P<barriono>\d+)", filename, re.DOTALL)
    if not match:
	raise ValueError("Failed to parse filename: %s" % filename)
    
    districtname = match.group("districtname")
    provinceno = int(match.group("provinceno"))
    districtno = int(match.group("districtno"))
    barriono = int(match.group("barriono"))
    
    wb = xlrd.open_workbook(XLSDIR + filename)
    colranges = [[0,10], [12,22]]
    
    for sheetname in wb.sheet_names() :
	sh = wb.sheet_by_name(sheetname)
	# is there data on this sheet?
	if not sh.nrows:
	    continue
	
	match = re.search(r"(?P<territoryno>\d+)", sh.row_values(0)[0], re.DOTALL)
	if not match:
	    # is this sheet empty of houses?
	    if sh.nrows < 5 or not sh.row_values(4)[0]:
		continue
	    
	    # There are house but no territory number
	    raise ValueError("Failed to extract territory number from: %s" % (filename + ":" + sheetname))
    
	territoryno = int(match.group("territoryno"))
	for colrange in colranges:
	    for rownum in range(sh.nrows)[4:]:
		cols = sh.row_values(rownum)[colrange[0]:colrange[1]]
		if not cols[0]:
		    continue
		
		blockno = cols[0] if type(cols[0]) == unicode else unicode(int(cols[0]))
		if ':' in blockno:
		    continue
		
		house = {}
		house['territoryno'] = territoryno
		house['districtname'] = districtname
		house['provinceno'] = provinceno
		house['districtno'] = districtno
		house['barriono'] = barriono
		
		if type(cols[1]) == float:
		    if unicode(cols[1])[-2:] == '.0':
			house['houseno'] = unicode(int(cols[1]))
		    else:
			house['houseno'] = unicode(cols[1])
		else:
		    house['houseno'] = cols[1]
		    
		
		house['directions'] = cols[2] if type(cols[2]) == unicode else unicode(cols[2])
		house['notes'] = cols[3] if type(cols[3]) == unicode else unicode(cols[3])
		
		if blockno.isnumeric():
		    house['blockno'] = int(blockno)
		    print house
		else:
		    print house
		    print '--------------', blockno
		    print
    print '---------------------'