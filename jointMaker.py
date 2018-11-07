import maya.cmds as mc



### Defaulet Value ###

alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
slArm = list(range(0))
slLwArm = list(range(0))
slwrist = list(range(0))
slwristEd = list(range(0))
slupLeg = list(range(0))
slLwLeg = list(range(0))
slAnkle = list(range(0))
slgpArm	= list(range(0))
slgpLeg	= list(range(0))

i = 0
x = 0
y = 0
z = 0
r = 0
alX = 0
alY = 0



def createArmLoc():
	global slArm, slLwArm, slwrist, slwristEd
	global alpha, i

	# create Locator #
	lg = mc.group(em=True, n='ArmLocator_{}'.format(alpha[i]))
	la = mc.spaceLocator( n='upArmPosition_{}'.format(alpha[i]), a=True )
	ll = mc.spaceLocator( n='lowArmPosition_{}'.format(alpha[i]), a=True )
	lw = mc.spaceLocator( n='wristPosition_{}'.format(alpha[i]), a=True )
	le = mc.spaceLocator( n='wristEndPosition_{}'.format(alpha[i]), a=True )

	print alpha[i]
	print lg
	print la
	print ll
	print lw
	print le
	print 'i={}'.format(i)

	slgpArm.append(lg)
	slArm.append(la[0])
	slLwArm.append(ll[0])
	slwrist.append(lw[0])
	slwristEd.append(le[0])

	# Set Position #
	mc.setAttr('{}.t'.format(slArm[i]), 6,30,0)
	mc.setAttr('{}.t'.format(slLwArm[i]), 11,30,0)
	mc.setAttr('{}.t'.format(slwrist[i]), 16,30,0)
	mc.setAttr('{}.t'.format(slwristEd[i]), 21,30,0)

	print slwrist

	# Parent Locator #
	mc.parent(slwristEd[i], slwrist[i])
	mc.parent(slwrist[i], slLwArm[i])
	mc.parent(slLwArm[i], slArm[i])
	mc.parent(slArm[i], lg)

	mc.select(clear=True)

	i = i + 1

def createLegLoc():
	global slgpLeg, slupLeg, slLwLeg, slAnkle
	global alpha, x

	# create Locator #
	lg = mc.group(em=True, n='LegLocator_{}'.format(alpha[x]))
	lu = mc.spaceLocator( n='upLegPosition_{}'.format(alpha[x]), a=True )
	ll = mc.spaceLocator( n='lowLegPosition_{}'.format(alpha[x]), a=True )
	la = mc.spaceLocator( n='anklePosition_{}'.format(alpha[x]), a=True )

	slgpLeg.append(lg)
	slupLeg.append(lu[0])
	slLwLeg.append(ll[0])
	slAnkle.append(la[0])

	print x
	print slAnkle


	# Set Position #
	mc.setAttr('{}.t'.format(slupLeg[x]), 5,14,0)
	mc.setAttr('{}.t'.format(slLwLeg[x]), 5,7,0)
	mc.setAttr('{}.t'.format(slAnkle[x]), 5,0,0)

	# Parent Locator #
	mc.parent(slAnkle[x], slLwLeg[x])
	mc.parent(slLwLeg[x], slupLeg[x])
	mc.parent(slupLeg[x], lg)

	mc.select(clear=True)

	x = x + 1


def delArmLoc():
	global i, slgpArm, slArm, slLwArm, slwrist, slwristEd

	for d in range(i):
		sec = mc.select(slgpArm[d])
		mc.delete(at=sec)

	slgpArm = list(range(0))
	slArm = list(range(0))
	slLwArm = list(range(0))
	slwrist = list(range(0))
	slwristEd = list(range(0))

	i = 0


def delLegLoc():
	global x, slgpLeg, slupLeg, slLwLeg, slAnkle

	for d in range(x):
		sec = mc.select(slgpLeg[d])
		mc.delete(at=sec)

	slgpLeg	= list(range(0))
	slupLeg	= list(range(0))
	slLwLeg	= list(range(0))
	slAnkle	= list(range(0))

	x = 0

def createArmJnt():
	global z

	for t in range(i):
		## get Position Locator ##
		mc.select(clear=True)
		upArmPositX = mc.getAttr('{}.tx'.format(slArm[t]))
		upArmPositY = mc.getAttr('{}.ty'.format(slArm[t]))
		upArmPositZ = mc.getAttr('{}.tz'.format(slArm[t]))
		lowArmPositX = mc.getAttr('{}.tx'.format(slLwArm[t]))
		lowArmPositY = mc.getAttr('{}.ty'.format(slLwArm[t]))
		lowArmPositZ = mc.getAttr('{}.tz'.format(slLwArm[t]))
		wristPositX = mc.getAttr('{}.tx'.format(slwrist[t]))
		wristPositY = mc.getAttr('{}.ty'.format(slwrist[t]))
		wristPositZ = mc.getAttr('{}.tz'.format(slwrist[t]))
		wristEndPositX = mc.getAttr('{}.tx'.format(slwristEd[t]))
		wristEndPositY = mc.getAttr('{}.ty'.format(slwristEd[t]))
		wristEndPositZ = mc.getAttr('{}.tz'.format(slwristEd[t]))

		print upArmPositY

		## create Joint ##
		mc.joint( n='upArm_{}'.format(alpha[t+z]), p=(0,0,0), a=True)
		mc.joint( n='lowArm_{}'.format(alpha[t+z]), p=(3,0,0), a=True )
		mc.joint( n='wrist_{}'.format(alpha[t+z]), p=(6,0,0), a=True )
		mc.joint( n='wristEnd_{}'.format(alpha[t+z]), p=(9,0,0), a=True )

		# ## Joint Set Position ##
		mc.setAttr( 'upArm_{}.tx'.format(alpha[t+z]), upArmPositX )
		mc.setAttr( 'upArm_{}.ty'.format(alpha[t+z]), upArmPositY )
		mc.setAttr( 'upArm_{}.tz'.format(alpha[t+z]), upArmPositZ )
		mc.setAttr( 'lowArm_{}.tx'.format(alpha[t+z]), lowArmPositX )
		mc.setAttr( 'lowArm_{}.ty'.format(alpha[t+z]), lowArmPositY )
		mc.setAttr( 'lowArm_{}.tz'.format(alpha[t+z]), lowArmPositZ )
		mc.setAttr( 'wrist_{}.tx'.format(alpha[t+z]), wristPositX )
		mc.setAttr( 'wrist_{}.ty'.format(alpha[t+z]), wristPositY )
		mc.setAttr( 'wrist_{}.tz'.format(alpha[t+z]), wristPositZ )
		mc.setAttr( 'wristEnd_{}.tx'.format(alpha[t+z]), wristEndPositX )
		mc.setAttr( 'wristEnd_{}.ty'.format(alpha[t+z]), wristEndPositY )
		mc.setAttr( 'wristEnd_{}.tz'.format(alpha[t+z]), wristEndPositZ )

		# ## jointOrient Set ##
		mc.joint( 'upArm_{}'.format(alpha[t+z]), e=True, oj='xyz', sao='yup' )
		mc.joint( 'lowArm_{}'.format(alpha[t+z]), e=True, oj='xyz', sao='yup' )
		mc.joint( 'wrist_{}'.format(alpha[t+z]), e=True, oj='xyz', sao='yup' )
		mc.setAttr( 'wristEnd_{}.jointOrient'.format(alpha[t+z]), 0,0,0 )

		agp = mc.group(n='armGrp_{}'.format(alpha[t+z]), em=True)
		mc.parent('upArm_{}'.format(alpha[t+z]), 'armGrp_{}'.format(alpha[t+z]))

	z = z + t + 1
	print t
	delArmLoc()


def createLegJnt():
	global y

	for t in range(x):
		print x
		print t
		## get Position Locator ##
		mc.select(clear=True)
		upLegX = mc.getAttr('{}.tx'.format(slupLeg[t]))
		upLegY = mc.getAttr('{}.ty'.format(slupLeg[t]))
		upLegZ = mc.getAttr('{}.tz'.format(slupLeg[t]))
		lowLegX = mc.getAttr('{}.tx'.format(slLwLeg[t]))
		lowLegY = mc.getAttr('{}.ty'.format(slLwLeg[t]))
		lowLegZ = mc.getAttr('{}.tz'.format(slLwLeg[t]))
		ankleX = mc.getAttr('{}.tx'.format(slAnkle[t]))
		ankleY = mc.getAttr('{}.ty'.format(slAnkle[t]))
		ankleZ = mc.getAttr('{}.tz'.format(slAnkle[t]))

		## create Joint ##
		mc.joint( n='upLeg_{}'.format(alpha[t+y]), p=(5,10,0), a=True )
		mc.joint( n='lowLeg_{}'.format(alpha[t+y]), p=(5,5,0), a=True )
		mc.joint( n='ankle_{}'.format(alpha[t+y]), p=(5,0,0), a=True )

		## Joint Set Position ##
		mc.setAttr( 'upLeg_{}.tx'.format(alpha[t+y]), upLegX )
		mc.setAttr( 'upLeg_{}.ty'.format(alpha[t+y]), upLegY )
		mc.setAttr( 'upLeg_{}.tz'.format(alpha[t+y]), upLegZ )
		mc.setAttr( 'lowLeg_{}.tx'.format(alpha[t+y]), lowLegX )
		mc.setAttr( 'lowLeg_{}.ty'.format(alpha[t+y]), lowLegY )
		mc.setAttr( 'lowLeg_{}.tz'.format(alpha[t+y]), lowLegZ )
		mc.setAttr( 'ankle_{}.tx'.format(alpha[t+y]), ankleX )
		mc.setAttr( 'ankle_{}.ty'.format(alpha[t+y]), ankleY )
		mc.setAttr( 'ankle_{}.tz'.format(alpha[t+y]), ankleZ )


		## jointOrient Set ##
		mc.joint( 'upLeg_{}'.format(alpha[t+y]), e=True, oj='xyz', sao='yup' )
		mc.joint( 'lowLeg_{}'.format(alpha[t+y]), e=True, oj='xyz', sao='yup' )
		mc.setAttr( 'ankle_{}.jointOrient'.format(alpha[t+y]), 0,0,0 )

		bgp = mc.group(n='legGrp_{}'.format(alpha[t+y]), em=True)
		mc.parent('upLeg_{}'.format(alpha[t+y]), 'legGrp_{}'.format(alpha[t+y]))

	y = y + t + 1

	delLegLoc()


############################
def jointMakeWin():
	##== Create Main Window ==##

	if mc.window('jointMake', exists=True):
		mc.deleteUI('jointMake')

	createWin = mc.window('jointMake', t='jointMake', w=250, h=150)
	mc.columnLayout(adj=True)

	mc.separator( h=5 )
	mc.text('Arm Joint')
	mc.separator( h=5 )
	mc.rowLayout(nc=2)
	mc.button(l='Set Arm Position', w=150, h=50, c='createArmLoc()' )
	mc.button(l='Create Arm Joint', w=150, h=50, c='createArmJnt()' )
	mc.setParent('..')

	mc.separator( h=5 )
	mc.text('Leg Joint')
	mc.separator( h=5 )
	mc.rowLayout(nc=2)
	mc.button(l='Set Leg Position', w=150, h=50, c='createLegLoc()' )
	mc.button(l='Create Leg Joint', w=150, h=50, c='createLegJnt()' )
	mc.setParent('..')

	mc.menuBarLayout()
	mc.menu(label='Edit', to=False)
	mc.menuItem(label='Twist -> Bend', c='TtoB()')
	mc.menuItem(label='Bend -> Twist', c='BtoT()')
	mc.menuItem(label='Angle Diver', c='AngleD()')

	mc.showWindow(createWin)

jointMakeWin()
