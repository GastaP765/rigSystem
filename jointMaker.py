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


### Bend Twist & Twist Bend ###
def TtoB():

	#create joint
	jnt = mc.ls(sl=True)
	tar = mc.listRelatives('{}'.format(jnt[0]))
	par = mc.listRelatives('{}'.format(jnt[0]), p=True)
	twi_trs = mc.getAttr('{}.translateX'.format(jnt[0]))
	jnt_trs = mc.getAttr('{}.worldMatrix[0]'.format(jnt[0]))
	par_trs = mc.getAttr('{}.worldMatrix[0]'.format(par[0]))
	jnt_orix = mc.getAttr('{}.jointOrientX'.format(jnt[0]))
	jnt_oriy = mc.getAttr('{}.jointOrientY'.format(jnt[0]))
	jnt_oriz = mc.getAttr('{}.jointOrientZ'.format(jnt[0]))
	twi_trs = twi_trs / 2
	jnt_rot = [-1 * jnt_orix, -1 * jnt_oriy, -1 * jnt_oriz]

	twi = mc.joint(n='{}_twist'.format(jnt[0]), rad=0.3, p=(par_trs[12],par_trs[13],par_trs[14]))
	ben = mc.joint(n='{}_bend'.format(jnt[0]), rad=0.3, p=(jnt_trs[12],jnt_trs[13],jnt_trs[14]))
	mc.parent('{}'.format(twi), '{}'.format(par[0]))
	mc.joint('{}'.format(twi), e=True, oj='xyz', sao='yup')
	mc.setAttr('{}.translateX'.format(twi), twi_trs)
	mc.setAttr('{}.translateX'.format(ben), twi_trs)
	mc.setAttr('{}.jointOrientX'.format(ben), jnt_orix)
	mc.setAttr('{}.jointOrientY'.format(ben), jnt_oriy)
	mc.setAttr('{}.jointOrientZ'.format(ben), jnt_oriz)


	#vectorCalculation
	co1 = mc.createNode('composeMatrix')
	co2 = mc.createNode('composeMatrix')
	inv = mc.createNode('inverseMatrix')
	mlt = mc.createNode('multMatrix')
	dec = mc.createNode('decomposeMatrix')
	trs = mc.createNode('transform')

	mc.connectAttr('{}.translate'.format(tar[0]), '{}.inputTranslate'.format(co1))
	mc.connectAttr('{}.scale'.format(tar[0]), '{}.inputScale'.format(co1))
	mc.connectAttr('{}.rotate'.format(tar[0]), '{}.inputRotate'.format(co1))
	mc.connectAttr('{}.shear'.format(tar[0]), '{}.inputShear'.format(co1))
	mc.connectAttr('{}.scale'.format(jnt[0]), '{}.inputScale'.format(co2))
	mc.connectAttr('{}.jointOrient'.format(jnt[0]), '{}.inputRotate'.format(co2))
	mc.connectAttr('{}.shear'.format(jnt[0]), '{}.inputShear'.format(co2))
	mc.connectAttr('{}.outputMatrix'.format(co2), '{}.inputMatrix'.format(inv))
	mc.connectAttr('{}.outputMatrix'.format(co1), '{}.matrixIn[0]'.format(mlt))
	mc.connectAttr('{}.outputMatrix'.format(inv), '{}.matrixIn[1]'.format(mlt))
	mc.connectAttr('{}.matrixSum'.format(mlt), '{}.inputMatrix'.format(dec))
	mc.connectAttr('{}.outputRotate'.format(dec), '{}.rotate'.format(trs))
	mc.connectAttr('{}.outputTranslate'.format(dec), '{}.translate'.format(trs))
	mc.connectAttr('{}.outputScale'.format(dec), '{}.scale'.format(trs))
	mc.connectAttr('{}.outputShear'.format(dec), '{}.shear'.format(trs))
	mc.parent('{}'.format(trs), '{}'.format(jnt[0]))
	mat = mc.getAttr('{}.matrix'.format(trs))
	mc.delete('{}'.format(co2), '{}'.format(inv), '{}'.format(mlt), '{}'.format(dec), '{}'.format(trs))


	#createNode
	aim = mc.createNode('aimConstraint', n='{}_beforeSplitTwistDriver'.format(tar[0]))
	mc.addAttr(ln='bend', nc=3, at='double3')
	mc.addAttr(ln='twist', nc=3, at='double3')
	for i in range(3):
		mc.addAttr(ln='bend{}'.format(xyz[i]), at='doubleAngle', p='bend')
		mc.addAttr(ln='twist{}'.format(xyz[i]), at='doubleAngle', p='twist')

	oc1 = mc.createNode('orientConstraint', n='{}_beforeSplitTwist'.format(jnt[0]))
	oc2 = mc.createNode('orientConstraint', n='{}_bendRot'.format(jnt[0]))
	oc3 = mc.createNode('orientConstraint', n='{}_twistRot'.format(jnt[0]))
	pb1 = mc.createNode('pairBlend', n='{}_weightedTwist'.format(jnt[0]))
	pb2 = mc.createNode('pairBlend', n='{}_bendRotSafeRot'.format(jnt[0]))
	pb3 = mc.createNode('pairBlend', n='{}_twistRotSafeRot'.format(jnt[0]))

	mc.parent('{}'.format(aim), '{}'.format(jnt[0]))
	mc.parent('{}'.format(oc1), '{}'.format(jnt[0]))
	mc.parent('{}'.format(oc2), '{}'.format(ben))
	mc.parent('{}'.format(oc3), '{}'.format(twi))


	#setAttr
	mc.setAttr('{}.worldUpType'.format(aim), 4)
	mc.setAttr('{}.rotateMode'.format(pb2), 2)
	mc.setAttr('{}.rotateMode'.format(pb3), 2)
	mc.setAttr('{}.rotInterpolation'.format(pb2), 1)
	mc.setAttr('{}.rotInterpolation'.format(pb3), 1)
	mc.setAttr('{}.scaleCompensate'.format(aim), False)
	for i in range(3):
		mc.setAttr('{0}.aimVector{1}'.format(aim, xyz[i]), mat[i])
		mc.setAttr('{0}.target[0].targetTranslate{1}'.format(aim, xyz[i]), mat[i])
		mc.setAttr('{0}.translate{1}'.format(aim, xyz[i]), 0)
		mc.setAttr('{0}.translate{1}'.format(oc1, xyz[i]), 0)
		mc.setAttr('{0}.translate{1}'.format(oc2, xyz[i]), 0)
		mc.setAttr('{0}.translate{1}'.format(oc3, xyz[i]), 0)
		mc.setAttr('{0}.target[0].targetRotate{1}'.format(oc3, xyz[i]), jnt_rot[i])
		mc.setAttr('{0}.constraintJointOrient{1}'.format(oc3, xyz[i]), jnt_rot[i])


	#connectAttr
	mc.connectAttr('{}.constraintRotate'.format(aim), '{}.bend'.format(aim))
	mc.connectAttr('{}.constraintRotate'.format(aim), '{}.constraintJointOrient'.format(oc1))
	mc.connectAttr('{}.matrix'.format(aim), '{}.target[0].targetParentMatrix'.format(aim))
	mc.connectAttr('{}.matrix'.format(aim), '{}.target[0].targetParentMatrix'.format(oc1))
	mc.connectAttr('{}.twist'.format(aim), '{}.inRotate2'.format(pb1))
	mc.connectAttr('{}.constraintRotate'.format(oc1), '{}.twist'.format(aim))
	mc.connectAttr('{}.constraintRotate'.format(oc2), '{}.inRotate2'.format(pb2))
	mc.connectAttr('{}.constraintRotate'.format(oc3), '{}.inRotate2'.format(pb3))
	mc.connectAttr('{}.outRotate'.format(pb1), '{}.constraintJointOrient'.format(oc2))
	mc.connectAttr('{}.outRotate'.format(pb1), '{}.target[0].targetJointOrient'.format(oc3))
	for i in range(3):
		mc.connectAttr('{0}.scale{1}'.format(jnt[0], xyz[i]), '{0}.scale{1}'.format(ben, xyz[i]))
		mc.connectAttr('{0}.shear{1}'.format(jnt[0], she[i]), '{0}.shear{1}'.format(ben, she[i]))
		mc.connectAttr('{0}.scale{1}'.format(par[0], xyz[i]), '{0}.scale{1}'.format(twi, xyz[i]))
		mc.connectAttr('{0}.shear{1}'.format(par[0], she[i]), '{0}.shear{1}'.format(twi, she[i]))
		mc.connectAttr('{0}.rotate{1}'.format(jnt[0], xyz[i]), '{0}.rotate{1}'.format(aim, xyz[i]))
		mc.connectAttr('{0}.rotate{1}'.format(jnt[0], xyz[i]), '{0}.target[0].targetRotate{1}'.format(oc2, xyz[i]))
		mc.connectAttr('{0}.outRotate{1}'.format(pb2, xyz[i]), '{0}.rotate{1}'.format(ben, xyz[i]))
		mc.connectAttr('{0}.outRotate{1}'.format(pb3, xyz[i]), '{0}.rotate{1}'.format(twi, xyz[i]))


def BtoT():

	#create joint
	jnt = mc.ls(sl=True)
	tar = mc.listRelatives('{}'.format(jnt[0]))
	par = mc.listRelatives('{}'.format(jnt[0]), p=True)
	jnt_trs = mc.getAttr('{}.worldMatrix[0]'.format(jnt[0]))
	tar_trs = mc.getAttr('{}.worldMatrix[0]'.format(tar[0]))

	ben = mc.joint(n='{}_bend'.format(jnt[0]), rad=0.3, p=(jnt_trs[12],jnt_trs[13],jnt_trs[14]))
	twi = mc.joint(n='{}_twist'.format(jnt[0]), rad=0.3, p=(tar_trs[12],tar_trs[13],tar_trs[14]))
	mc.joint('{}'.format(ben), e=True, oj='xyz', sao='yup')
	for i in range(3):
		mc.setAttr('{0}.jointOrient{1}'.format(twi, xyz[i]), 0)

	twi_trs = mc.getAttr('{}.translateX'.format(twi))
	twi_trs = twi_trs / 2
	mc.setAttr('{}.translateX'.format(twi), twi_trs)
	mc.addAttr('{}'.format(twi), ln='twistWeight', min=0, max=1, dv=1)
	if par is not None:
		mc.parent('{}'.format(ben), '{}'.format(par[0]))
	elif par is None:
		mc.parent('{}'.format(ben), w=True)


	#create node
	aim = mc.createNode('aimConstraint', n='{}_afterSplitTwistDriver'.format(jnt[0]))
	mc.select('{}'.format(aim), r=True)
	mc.addAttr(ln='bend', nc=3, at='double3')
	mc.addAttr(ln='twist', nc=3, at='double3')
	for i in range(3):
		mc.addAttr(ln='bend{}'.format(xyz[i]), at='doubleAngle', p='bend')
		mc.addAttr(ln='twist{}'.format(xyz[i]), at='doubleAngle', p='twist')

	oc1 = mc.createNode('orientConstraint', n='{}_afterSplitTwist'.format(jnt[0]))
	oc2 = mc.createNode('orientConstraint', n='{}_rot'.format(jnt[0]))
	oc3 = mc.createNode('orientConstraint', n='{}_twistRot'.format(jnt[0]))
	pb1 = mc.createNode('pairBlend', n='{}_weightedTwist'.format(jnt[0]))
	mc.addAttr(ln='inRot2', nc=3, at='double3', w=False)
	for i in range(3):
		mc.addAttr(ln='inRot2{}'.format(xyz[0]), at='doubleAngle', p='inRot2', w=False)

	pb2 = mc.createNode('pairBlend', n='{}_rotSafeRot'.format(jnt[0]))
	pb3 = mc.createNode('pairBlend', n='{}_twistRotSafeRot'.format(jnt[0]))

	grp = mc.group('{}'.format(oc1),'{}'.format(oc2),'{}'.format(oc3), n='{}_Bend->Twist'.format(jnt[0]))
	mc.parent('{}'.format(aim), '{}'.format(jnt[0]))
	mc.parent('{}'.format(grp), '{}'.format(jnt[0]))
	mc.setAttr('{}.visibility'.format(grp), 0)


	#setAttr
	mc.setAttr('{}.target[0].targetTranslateX'.format(aim), 1)
	mc.setAttr('{}.worldUpType'.format(aim), 4)
	mc.setAttr('{}.interpType'.format(oc2), 2)
	mc.setAttr('{}.interpType'.format(oc3), 2)
	mc.setAttr('{}.rotateMode'.format(pb2), 2)
	mc.setAttr('{}.rotateMode'.format(pb3), 2)
	mc.setAttr('{}.rotInterpolation'.format(pb2), 1)
	mc.setAttr('{}.rotInterpolation'.format(pb3), 1)
	for i in range(3):
		mc.setAttr('{0}.translate{1}'.format(aim, xyz[i]), 0)


	#connectAttr
	mc.connectAttr('{}.constraintRotate'.format(aim), '{}.bend'.format(aim))
	mc.connectAttr('{}.constraintRotate'.format(aim), '{}.constraintJointOrient'.format(oc1))
	mc.connectAttr('{}.constraintRotate'.format(oc1), '{}.twist'.format(aim))
	mc.connectAttr('{}.matrix'.format(aim), '{}.target[0].targetParentMatrix'.format(aim))
	mc.connectAttr('{}.matrix'.format(aim), '{}.target[0].targetParentMatrix'.format(oc1))
	mc.connectAttr('{}.bend'.format(aim), '{}.target[0].targetJointOrient'.format(oc2))
	mc.connectAttr('{}.twist'.format(aim), '{}.inRotate1'.format(pb1))
	mc.connectAttr('{}.inRot2'.format(pb1), '{}.inRotate2'.format(pb1))
	mc.connectAttr('{}.outRotate'.format(pb1), '{}.target[0].targetRotate'.format(oc2))
	mc.connectAttr('{}.constraintRotate'.format(oc2), '{}.inRotate2'.format(pb2))
	mc.connectAttr('{}.constraintRotate'.format(oc2), '{}.constraintJointOrient'.format(oc3))
	mc.connectAttr('{}.rotate'.format(jnt[0]), '{}.target[0].targetRotate'.format(oc3))
	mc.connectAttr('{}.constraintRotate'.format(oc3), '{}.inRotate2'.format(pb3))
	mc.connectAttr('{}.twistWeight'.format(twi), '{}.weight'.format(pb1))
	for i in range(3):
		mc.connectAttr('{0}.rotate{1}'.format(jnt[0], xyz[i]), '{0}.rotate{1}'.format(aim, xyz[i]))
		mc.connectAttr('{0}.translate{1}'.format(jnt[0], xyz[i]), '{0}.translate{1}'.format(ben, xyz[i]))
		mc.connectAttr('{0}.scale{1}'.format(jnt[0], xyz[i]), '{0}.scale{1}'.format(ben, xyz[i]))
		mc.connectAttr('{0}.shear{1}'.format(jnt[0], she[i]), '{0}.shear{1}'.format(ben, she[i]))
		mc.connectAttr('{0}.scale{1}'.format(ben, xyz[i]), '{0}.scale{1}'.format(twi, xyz[i]))
		mc.connectAttr('{0}.outRotate{1}'.format(pb2, xyz[i]), '{0}.rotate{1}'.format(ben, xyz[i]))
		mc.connectAttr('{0}.outRotate{1}'.format(pb3, xyz[i]), '{0}.rotate{1}'.format(twi, xyz[i]))



###############################################################

def AngleD():
	tar_jo = list(range(3))
	exps = list(range(0))

	jnt = mc.ls(sl=True)
	tar = mc.listRelatives('{}'.format(jnt[0]))
	par = mc.listRelatives('{}'.format(jnt[0]), p=True)
	mc.addAttr(ln='bendH', sn='bh', at='doubleAngle')
	mc.addAttr(ln='bendV', sn='bv', at='doubleAngle')
	mc.addAttr(ln='aimVector', nc=3, at='double3')
	for i in range(3):
		tar_jo[i] = mc.getAttr('{0}.jointOrient{1}'.format(tar[0], xyz[i]))
		mc.addAttr(ln='aimVector{}'.format(xyz[i]), at='double', p='aimVector')


	#createJoint
	jnt_trs = mc.getAttr('{}.worldMatrix[0]'.format(jnt[0]))
	tar_trs = mtr = mc.getAttr('{}.worldMatrix[0]'.format(tar[0]))

	beV = mc.joint(n='{}_bendV'.format(jnt[0]), rad=0.3, p=(jnt_trs[12],jnt_trs[13],jnt_trs[14]))
	bVe = mc.joint(n='{}_bendVend'.format(jnt[0]), rad=0.3, p=(tar_trs[12],tar_trs[13],tar_trs[14]))
	beH = mc.joint(n='{}_bendH'.format(jnt[0]), rad=0.3, p=(jnt_trs[12],jnt_trs[13],jnt_trs[14]))
	bHe = mc.joint(n='{}_bendHend'.format(jnt[0]), rad=0.3, p=(tar_trs[12],tar_trs[13],tar_trs[14]))
	mc.joint('{}'.format(beV), e=True, oj='xyz', sao='yup')
	mc.joint('{}'.format(beH), e=True, oj='xyz', sao='yup')
	mc.parent(beV, par[0])
	mc.parent(beH, par[0])
	for i in range(3):
		mc.setAttr('{0}.jointOrient{1}'.format(bVe, xyz[i]), tar_jo[i])
		mc.setAttr('{0}.jointOrient{1}'.format(bHe, xyz[i]), tar_jo[i])


	#createNode
	vep = mc.createNode('vectorProduct', n='{}_vectorProduct'.format(jnt[0]))
	exp = mc.expression(n='{}_Exp'.format(jnt[0]), o='{}'.format(jnt[0]))
	mc.expression(exp, e=True, uc='none', ae=0)


	#setAttr
	mc.setAttr('{}.input1X'.format(vep), 1.0)
	mc.setAttr('{}.operation'.format(vep), 3)
	mc.setAttr('{}.normalizeOutput'.format(vep), True)

	#connectAttr
	mc.connectAttr('{}.matrix'.format(jnt[0]), '{}.matrix'.format(vep))
	mc.connectAttr('{0}.output[0]'.format(exp), '{}.bendH'.format(jnt[0]))
	mc.connectAttr('{0}.output[1]'.format(exp), '{}.bendV'.format(jnt[0]))
	mc.connectAttr('{}.bendH'.format(jnt[0]), '{}.rotateY'.format(beH))
	mc.connectAttr('{}.bendV'.format(jnt[0]), '{}.rotateZ'.format(beV))
	for i in range(3):
		mc.connectAttr('{0}.output{1}'.format(vep, xyz[i]), '{0}.aimVector{1}'.format(jnt[0], xyz[i]))
		mc.connectAttr('{0}.aimVector{1}'.format(jnt[0], xyz[i]), '{0}.input[{1}]'.format(exp, i))


	#expression
	exps.append('vector $x_vec = <<1., .0, .0>>;')
	exps.append('vector $y_vec = <<.0, 1., .0>>;')
	exps.append('vector $z_vec = <<.0, .0, 1.>>;')
	exps.append('vector $vec = <<' + jnt[0] + '.aimVectorX, ')
	exps.append(jnt[0] + '.aimVectorY, ' + jnt[0] + '.aimVectorZ>>;')
	exps.append('float $aim = dot($x_vec, $vec) + 1;')
	exps.append(jnt[0] + '.bendH = atan2(dot($z_vec, $vec), $aim) * -2.;')
	exps.append(jnt[0] + '.bendV = atan2(dot($y_vec, $vec), $aim) * 2.;')
	imp = ''.join(exps)
	mc.expression(exp, e=True, s='{}'.format(imp))








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
