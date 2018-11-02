import maya.cmds as mc

xyz = 'XYZ'
she = 'XY', 'XZ', 'YZ'

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


win = mc.window(t='TtoBtest', widthHeight=(200,30))
mc.columnLayout()
mc.button(l='TtoB', c='TtoB()')
mc.showWindow(win)