#!/usr/bin/env python
import os,sys
import math
import urllib2
import codecs, binascii
import pylab as pl

def main():
	pass
	test_txt()
	
	
def test_txt():
	q=txt() # object from class
	#print q.Txt2List("01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz")
	q.txt="Attack at dawn."
	print q.txt
	print q.lst
	print q.hex
	print q.bin
	k = txt()
	k.txt="Secret"
	q.hex = k.hex
	print q.txt
	print q.lst
	print q.hex
	print q.bin
	k.txt="qweasd"	
	q.lst = k.lst
	print q.txt
	print q.lst
	print q.hex
	print q.bin
	k.txt="Secret"
	q.bin = k.bin
	print q.txt
	print q.lst
	print q.hex
	print q.bin
	q.txt = q.GetBinReverse()
	print q.bin
	

class txt(object):
	"""
		txt Class: for Geocaching usage and beyond
		Code-style: We are all consenting adults here who can RTFC
	"""
	def __init__(self,inTXT=""):
		self._txt = str(inTXT)

	def __str__(self):
		return self._txt

	@property
	def txt(self):
		"""Get TXT as string."""
		return self._txt
	@txt.setter
	def txt(self,inTXT):
		self._txt = str(inTXT)

	@property
	def lst(self):
		"""Get TXT as list of decimal numbers."""
		return [ ord(c)%256 for c in self._txt ]
	@lst.setter
	def lst(self,inLIST):
		self._txt = "".join([chr(i) for i in inLIST])

	@property
	def hex(self):
		"""Get TXT as hexadecimal string (ASCII)."""
		#for c in range(2-len(CH)):
		#CH += "0"
		#for L in self.lst:
			#print L
		return "".join([ (format(i, '#04X'))[2:] for i in self.lst ])
	@hex.setter
	def hex(self,inHEX):
		#self.lst = [int(inHEX[step*2:step*2+2],16) for step in range(len(inHEX)/2)]
		self.lst = [int(inHEX[step:step+2],16) for step in range(0,len(inHEX),2)]
		
	@property
	def bin(self):
		"""Get TXT as binary string 8bit (ASCII)."""
		return "".join([ (format(i, '#010b'))[2:] for i in self.lst ])
	@bin.setter
	def bin(self,inBIN):
		self.lst = [int(inBIN[step:step+8],2) for step in range(0,len(inBIN),8)]

	def guess(self,inANY):
		tmpTXT = txt()		
		if all([C in "01" for C in inANY]):
			tmpTXT.bin = inANY
			self.txt = tmpTXT.txt
			return True
		elif all([C in "0123456789ABCDEF" for C in inANY]):
			tmpTXT.hex = inANY
			self.txt = tmpTXT.txt
			return True
		elif all([C in txt.ASCII() for C in inANY]):
			tmpTXT.hex = inANY
			self.txt = tmpTXT.txt
			return True
		elif all([C>=0 and C<255 for C in inANY]):
			tmpTXT.lst = inANY
			self.txt = tmpTXT.txt
			return True
		else:
			self.txt = ""
			return False
	
	def GetXOR(self,inTXT):
		"""return Exclusive OR of the TXT and inTXT"""
		OUT = ""
		KEY = txt.Txt2Hex(inTXT)
		for l in range(len(self.hex)/2):
			L=int(self.hex[ l*2 : (l+1)*2 ],16)
			R=-1
			if (l*2+2)%len(KEY) == 0:
				R=int(KEY[len(KEY)-2:len(KEY)],16)
			else:
				R=int(KEY[ (l*2)%(len(KEY)) : (l*2+2)%(len(KEY)) ],16)
			CH = (format(L ^ R, '#04X'))[2:4]
			OUT += CH
		return self.Hex2Txt(OUT)
		
	def XOR(self,inTXT):
		"""apply Exclusive OR of the TXT and inTXT"""
		self.txt = self.GetXOR(inTXT)

	def GetInvert(self):
		"""return inverted Bitwise of the TXT (0->1, 1->0; done by XOR with 0xFF)"""
		return self.GetXOR(chr(255))

	def Invert(self):
		"""invert Bitwise of the TXT"""
		self.txt = self.GetInvert()

	def GetBitReverse(self):
		"""Reverse (Mirror) the bits of TXT (Big <--> Little Endieness)"""
		BIN = self.bin
		RevBIN = "".join([ BIN[i] for i in range(len(BIN)-1,-1,-1) ])
		tmpTXT = txt()
		tmpTXT.bin = RevBIN
		return tmpTXT.txt #self.Bin2Txt(RevBIN)

	def BitReverse(self):
		"""invert Bitwise of the TXT"""
		self.txt = self.BitReverse()
	
	
	@staticmethod
	def Txt2List(TXT):
		tmpTXT = txt(TXT)
		return tmpTXT.lst
		#return [ ord(c) for c in TXT ]

	@staticmethod
	def Hex2List(HEX):
		tmpTXT = txt()
		tmpTXT.hex = HEX
		return tmpTXT.lst
		#return [int(HEX[step*2:step*2+2],16) for step in range(len(HEX)/2)]
		#print "".join([  binascii.a2b_hex(HEX[i:i+2]) for i in xrange(0, len(HEX), 2) ]),

	@staticmethod
	def Hex2Txt(HEX):
		tmpTXT = txt()
		tmpTXT.hex = HEX
		return tmpTXT.txt
		#return "".join([chr(i) for i in txt.Hex2List(HEX)])

	@staticmethod
	def Txt2Hex(TXT):
		tmpTXT = txt(TXT)
		return tmpTXT.hex
		#return "".join([  "{0:02X}".format(i) for i in txt.Txt2List(TXT) ])

	@staticmethod
	def Bin2Txt(BIN):
		tmpTXT = txt()
		tmpTXT.bin = BIN
		return tmpTXT.txt
		#return "".join([chr(i) for i in txt.Hex2List(HEX)])

	@staticmethod
	def Txt2Bin(TXT):
		tmpTXT = txt(TXT)
		return tmpTXT.bin
		#return "".join([ (format(i, '#04X'))[2:4] for i in txt.Txt2List(TXT) ])

	@staticmethod
	def ZeroTxt(len):
		return "".join([ chr(0) for i in range(len)])
	
	@staticmethod
	def ALPH():
		return "".join([ chr(i) for i in range(65,65+26) ])

	@staticmethod
	def ALPHnum():
		return "".join([ chr(i) for i in range(65,65+26) ]+[ chr(i) for i in range(48,48+10) ])

	@staticmethod
	def ASCII():
		return "".join(chr(c) if chr(c).isspace() or chr(c).isalnum() else '_' for c in range(256))

	@staticmethod
	def GetCesar(TXT,shft):
		AL=txt.ALPH()
		ROTTXT=""
		ROTL=''
		for L in TXT:
			#print AL.find(L.upper())
			if AL.find(L.upper())>=0 :
				ROTL=AL[(AL.find(L.upper())+shft)%26 ]
				if not L.isupper():
					ROTL=ROTL.lower()
			else:
				ROTL=L
			#print ROTL
			ROTTXT+=ROTL
		return ROTTXT

	@staticmethod
	def GetROT13(TXT):
		return txt.GetCesar(TXT,13)

	@staticmethod
	def KeyScheduling(KEY):
		"""RC4 Key Scheduling. Source: Wiki"""
		S=[i for i in range(256)]
		#print S 
		j=0
		for i in range(256):
			j=( j + S[i]+ord(KEY[i%len(KEY)]) ) % 256
			S[i],S[j] = S[j],S[i]
		#print S
		return S

	@staticmethod
	def PseudoRandomGeneration(INP,Sin=[],iin=0,jin=0):
		"""RC4 Algorothm. Source: Wiki"""
	#def PseudoRandomGeneration(INP,Sin,iin=0,jin=0,filterAlnum=False):
		i=iin%256
		j=jin%256
		S=Sin[:]
		OUT=""
		for step in range(len(INP)):
			L=ord(INP[step])	
			#print L
			i = (i + 1) % 256
			j = (j + S[i]) % 256
			S[i],S[j] = S[j],S[i]
			K = S[(S[i] + S[j]) % 256]
			#print format(K, '#02X'),
			#print K,L,format(K ^ L, '#04X'),
			C=chr(K ^ L % 256)
			#if filterAlnum==True:
				#if C.isalnum() or C.isspace():
					#OUT += C
			#else:
				#OUT += C
			OUT += C	
		return OUT


def bitDisassembleImage(imgpath):
	"""
	disassemble image into Red, Green, Blue, Value, RGB-Mix for all 8bits
	usefull 
	"""
	 
	import os,sys
	import Image
	#imgpath = sys.argv[1]  

	img = Image.open(imgpath).convert('RGB')

	imgr = [Image.new( 'RGB', img.size, "black") for i in range(8)]
	imgg = [Image.new( 'RGB', img.size, "black") for i in range(8)]
	imgb = [Image.new( 'RGB', img.size, "black") for i in range(8)]
	imga = [Image.new( 'RGB', img.size, "black") for i in range(8)]
	imgv = [Image.new( 'RGB', img.size, "black") for i in range(8)]
	
	pxr  = [i.load() for i in imgr]
	pxg  = [i.load() for i in imgg]
	pxb  = [i.load() for i in imgb]
	pxa  = [i.load() for i in imga]
	pxv  = [i.load() for i in imgv]

	
	for x in range(img.size[0]): 
		for y in range(img.size[1]):
			r,g,b = img.getpixel((x,y))
			for bit in range(8):
				pxr[bit][x,y] = ( (((r>>bit)&0x1)<<8)  ,0 ,0) 
				pxg[bit][x,y] = ( 0, (((g>>bit)&0x1)<<8)  ,0) 
				pxb[bit][x,y] = ( 0, 0, (((b>>bit)&0x1)<<8) )
				rl= (((r>>bit)&0x1)<<8)
				gl= (((g>>bit)&0x1)<<8)
				bl= (((b>>bit)&0x1)<<8)
				vl = (rl&gl&bl)
				pxa[bit][x,y] = ( rl, gl, bl) 
				pxv[bit][x,y] = ( vl, vl, vl) 
#
	for bit in range(8):
		imgr[bit].save(imgpath+"_r"+str(bit)+".png")
		imgg[bit].save(imgpath+"_g"+str(bit)+".png")
		imgb[bit].save(imgpath+"_b"+str(bit)+".png")
		imgv[bit].save(imgpath+"_v"+str(bit)+".png")
		imga[bit].save(imgpath+"_a"+str(bit)+".png")
	if False:
	#print img.size[0],"x",img.size[1]," = ", img.size[1]*img.size[0]
	
		Rxy = img.tostring()[0::3]
		Gxy = img.tostring()[1::3]
		Bxy = img.tostring()[2::3]
		#print R[img.size[0]*0],R[img.size[0]*1],R[img.size[0]*2] 
		
		Ryx,Gyx,Byx=[],[],[]
		for x in xrange(img.size[0]):    # for every pixel:
			for y in xrange(img.size[1]):
				Ryx.append(Rxy[x+y*img.size[0]])
				Gyx.append(Gxy[x+y*img.size[0]])
				Byx.append(Bxy[x+y*img.size[0]])
	
	
def decodeRepeatNumber(numstr):
	"""
	41 => 1111; 14 => 4
	GCHJ89, GCWXWP
	"""
	p=numstr
	print p
	while len(p)%2 == 0:
		p="".join([ int(p[i])*p[i+1] for i in range(0,len(p),2) ]);
		print p

def encodeRepeatNumber(numstr):
	"TODO"
	pass

def GetFreq(LIST):
	hist=[[l,LIST.count(l)] for l in [c for c in range(256)]]
	histnonz=[[l,LIST.count(l)] for l in [c for c in range(256)] if LIST.count(l)>0]
	alph, freq = [v[0] for v in hist], [v[1] for v in hist] 
	return freq

def Get8BitFreq(TXT):
	Lall = Txt2List(TXT)
	L = [0,0,0,0,0,0,0,0]
	L[0] += sum([ C>>0 & 1 for C in Lall ])
	L[1] += sum([ C>>1 & 1 for C in Lall ])
	L[2] += sum([ C>>2 & 1 for C in Lall ])
	L[3] += sum([ C>>3 & 1 for C in Lall ])
	L[4] += sum([ C>>4 & 1 for C in Lall ])
	L[5] += sum([ C>>5 & 1 for C in Lall ])
	L[6] += sum([ C>>6 & 1 for C in Lall ])
	L[7] += sum([ C>>7 & 1 for C in Lall ])
	return L


lorem="""
Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur? At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.
"""

lorem_en="""
But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure? On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains.
"""


if __name__ == '__main__':
	main()
