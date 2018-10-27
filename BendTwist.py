import maya.cmds as mc

xyz = 'XYZ'
she = 'XY', 'XZ', 'YZ'

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
	mc.addAttr('{}'.format(twi), ln='twistWeight', min=0, max=1, dv=1, k=True)
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
		mc.addAttr(ln='bend{}'.format(xyz[i]), at='doubleAngle', p='bend', k=True)
		mc.addAttr(ln='twist{}'.format(xyz[i]), at='doubleAngle', p='twist', k=True)

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


win = mc.window(t='BtoTtest', widthHeight=(200,30))
mc.columnLayout()
mc.button(l='BtoT', c='BtoT()')
mc.showWindow(win)