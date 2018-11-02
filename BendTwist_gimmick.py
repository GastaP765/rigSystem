import maya.cmds as mc

xyz = 'XYZ'
she = 'XY', 'XZ', 'YZ'

def cntBendJnt():
	global many, j, get, jcnt, jnt

	jnt = list(range(0))
	many = list(range(0))
	j = 0
	
	get = mc.ls(typ='joint')
	for i in get:
		if 'twist' in '{}'.format(i):
			get2 = mc.listRelatives(i, p=True)
			if 'bend' in '{}'.format(get2):
				many.append(get2[0])

	jcnt = len(many)
	BtoT()

def BtoT():
	global jnt

	ben = many[j]
	tjo = mc.listRelatives(ben)
	twi = tjo[0]
	jmat = mc.getAttr('{}.worldMatrix'.format(many[j]))
	jnt_mat = list(map(round, jmat, [3]*len(jmat)))
	for i in get:
		pmat = mc.getAttr('{}.worldMatrix'.format(i))
		par_mat = list(map(round, pmat, [3]*len(pmat)))
		if jnt_mat == par_mat:
			if i != many[j]:
				jnt.append(i)


	#create node
	aim = mc.createNode('aimConstraint', n='{}_afterSplitTwistDriver'.format(jnt[j]))
	mc.select('{}'.format(aim), r=True)
	mc.addAttr(ln='bend', nc=3, at='double3')
	mc.addAttr(ln='twist', nc=3, at='double3')
	for i in range(3):
		mc.addAttr(ln='bend{}'.format(xyz[i]), at='doubleAngle', p='bend', k=True)
		mc.addAttr(ln='twist{}'.format(xyz[i]), at='doubleAngle', p='twist', k=True)

	oc1 = mc.createNode('orientConstraint', n='{}_afterSplitTwist'.format(jnt[j]))
	oc2 = mc.createNode('orientConstraint', n='{}_rot'.format(jnt[j]))
	oc3 = mc.createNode('orientConstraint', n='{}_twistRot'.format(jnt[j]))
	pb1 = mc.createNode('pairBlend', n='{}_weightedTwist'.format(jnt[j]))
	mc.addAttr(ln='inRot2', nc=3, at='double3', w=False)
	for i in range(3):
		mc.addAttr(ln='inRot2{}'.format(xyz[0]), at='doubleAngle', p='inRot2', w=False)

	pb2 = mc.createNode('pairBlend', n='{}_rotSafeRot'.format(jnt[j]))
	pb3 = mc.createNode('pairBlend', n='{}_twistRotSafeRot'.format(jnt[j]))

	grp = mc.group('{}'.format(oc1),'{}'.format(oc2),'{}'.format(oc3), n='{}_Bend->Twist'.format(jnt[j]))
	mc.parent('{}'.format(aim), '{}'.format(jnt[j]))
	mc.parent('{}'.format(grp), '{}'.format(jnt[j]))
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
	mc.connectAttr('{}.rotate'.format(jnt[j]), '{}.target[0].targetRotate'.format(oc3))
	mc.connectAttr('{}.constraintRotate'.format(oc3), '{}.inRotate2'.format(pb3))
	mc.connectAttr('{}.twistWeight'.format(twi), '{}.weight'.format(pb1))
	for i in range(3):
		mc.connectAttr('{0}.rotate{1}'.format(jnt[j], xyz[i]), '{0}.rotate{1}'.format(aim, xyz[i]))
		mc.connectAttr('{0}.translate{1}'.format(jnt[j], xyz[i]), '{0}.translate{1}'.format(ben, xyz[i]))
		mc.connectAttr('{0}.scale{1}'.format(jnt[j], xyz[i]), '{0}.scale{1}'.format(ben, xyz[i]))
		mc.connectAttr('{0}.shear{1}'.format(jnt[j], she[i]), '{0}.shear{1}'.format(ben, she[i]))
		mc.connectAttr('{0}.scale{1}'.format(ben, xyz[i]), '{0}.scale{1}'.format(twi, xyz[i]))
		mc.connectAttr('{0}.outRotate{1}'.format(pb2, xyz[i]), '{0}.rotate{1}'.format(ben, xyz[i]))
		mc.connectAttr('{0}.outRotate{1}'.format(pb3, xyz[i]), '{0}.rotate{1}'.format(twi, xyz[i]))

	roop()

def roop():
	global j, jnt

	if j == jcnt - 1:
		return
	else:
		j+=1
		BtoT()


win = mc.window(t='BtoTtest', widthHeight=(200,30))
mc.columnLayout()
mc.button(l='BtoT', c='cntBendJnt()')
mc.showWindow(win)