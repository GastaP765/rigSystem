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

win = mc.window(t='BtoTtest', widthHeight=(200,30))
mc.columnLayout()
mc.button(l='BtoT', c='BtoT()')
mc.showWindow(win)